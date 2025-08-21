// YouTube video ID extraction regex
const VIDEO_ID_REGEX = /(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;

// DOM elements
const videoUrlInput = document.getElementById('video-url');
const questionInput = document.getElementById('question');
const submitBtn = document.getElementById('submit-btn');
const clearBtn = document.getElementById('clear-btn');
const videoPreview = document.getElementById('video-preview');
const ytPlayer = document.getElementById('yt-player');
const responseSection = document.getElementById('response-section');
const responseContent = document.getElementById('response-content');
const loadingElement = document.getElementById('loading');
const copyResponseBtn = document.getElementById('copy-response');
const errorMessageElement = document.getElementById('error-message');
const errorTextElement = document.getElementById('error-text');

// Event listeners
videoUrlInput.addEventListener('input', handleVideoUrlChange);
submitBtn.addEventListener('click', handleSubmit);
clearBtn.addEventListener('click', handleClear);
copyResponseBtn.addEventListener('click', copyResponseToClipboard);

// API URL (change this to your actual backend URL when deployed)
const API_URL = '/process_video';

// Extract YouTube video ID from URL
function extractVideoId(url) {
    const match = url.match(VIDEO_ID_REGEX);
    return match ? match[1] : url; // Return the ID or the original string if it's already an ID
}

// Update video preview when URL changes
function handleVideoUrlChange() {
    const url = videoUrlInput.value.trim();
    
    if (!url) {
        videoPreview.style.display = 'none';
        return;
    }
    
    const videoId = extractVideoId(url);
    
    // Check if it looks like a valid video ID (11 characters)
    if (videoId && videoId.length === 11) {
        ytPlayer.src = `https://www.youtube.com/embed/${videoId}`;
        videoPreview.style.display = 'block';
    } else {
        videoPreview.style.display = 'none';
    }
}

// Handle form submission
async function handleSubmit() {
    const url = videoUrlInput.value.trim();
    const question = questionInput.value.trim();
    
    if (!url) {
        showError('Please enter a YouTube URL or video ID');
        return;
    }
    
    if (!question) {
        showError('Please enter a question about the video');
        return;
    }
    
    const videoId = extractVideoId(url);
    
    // Show loading indicator
    loadingElement.style.display = 'flex';
    responseSection.style.display = 'none';
    hideError();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_id: videoId,
                question: question
            })
        });
        
        const data = await response.json();
        
        // Hide loading indicator
        loadingElement.style.display = 'none';
        
        // Show response
        responseContent.textContent = data.answer;
        responseSection.style.display = 'block';
        
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred while processing your request. Please try again.');
        loadingElement.style.display = 'none';
    }
}

// Clear all inputs and responses
function handleClear() {
    videoUrlInput.value = '';
    questionInput.value = '';
    videoPreview.style.display = 'none';
    responseSection.style.display = 'none';
    hideError();
}

// Copy response to clipboard
function copyResponseToClipboard() {
    const textToCopy = responseContent.textContent;
    
    if (!textToCopy) return;
    
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            // Change icon temporarily to indicate success
            copyResponseBtn.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                copyResponseBtn.innerHTML = '<i class="far fa-copy"></i>';
            }, 2000);
        })
        .catch(err => {
            console.error('Could not copy text: ', err);
        });
}

// Show error message
function showError(message) {
    errorTextElement.textContent = message;
    errorMessageElement.style.display = 'block';
}

// Hide error message
function hideError() {
    errorMessageElement.style.display = 'none';
}

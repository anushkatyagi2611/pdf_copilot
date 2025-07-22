// Enhanced PDF Chat Application
let pdfDoc = null;
let pdfId = null;
let currentPage = 1;
let totalPages = 0;
let scale = 1.5;
let chatHistory = [];
let firstMessageSent = false; // Track if first message has been sent

// Create PDF container
const pdfContainer = document.createElement("div");
pdfContainer.id = "pdf-container";
pdfContainer.style.overflowY = "scroll";
pdfContainer.style.height = "100%";
pdfContainer.style.padding = "16px";
document.querySelector("#pdf-viewer").appendChild(pdfContainer);

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Hide welcome message initially if no PDF
    updateConnectionStatus('Ready', 'success');
    
    // Add event listeners
    addEventListeners();
    
    // Auto-resize textarea
    setupTextareaAutoResize();
    
    // Initialize drag and drop
    setupDragAndDrop();
    
    // Hide page navigation initially
    document.getElementById("page-navigation").style.display = "none";
}

function addEventListeners() {
    // PDF upload
    document.getElementById("pdf-file-input").addEventListener("change", handlePDFUpload);
    
    // Chat functionality
    document.getElementById("ask-btn").addEventListener("click", handleAskQuestion);
    document.getElementById("question-input").addEventListener("keydown", handleInputKeydown);
    document.getElementById("clear-chat").addEventListener("click", clearChat);
    document.getElementById("export-chat").addEventListener("click", exportChat);
    
    // Suggestion buttons
    document.addEventListener("click", handleSuggestionClick);
    
    // PDF controls
    document.getElementById("zoom-in").addEventListener("click", () => zoomPDF(0.2));
    document.getElementById("zoom-out").addEventListener("click", () => zoomPDF(-0.2));
    document.getElementById("prev-page").addEventListener("click", () => navigatePage(-1));
    document.getElementById("next-page").addEventListener("click", () => navigatePage(1));
}

function setupTextareaAutoResize() {
    const textarea = document.getElementById("question-input");
    textarea.addEventListener("input", function() {
        this.style.height = "auto";
        this.style.height = Math.min(this.scrollHeight, 120) + "px";
    });
}

function setupDragAndDrop() {
    const pdfViewer = document.getElementById("pdf-viewer");
    
    pdfViewer.addEventListener("dragover", (e) => {
        e.preventDefault();
        pdfViewer.style.borderColor = "#667eea";
        pdfViewer.style.backgroundColor = "rgba(102, 126, 234, 0.05)";
    });
    
    pdfViewer.addEventListener("dragleave", (e) => {
        e.preventDefault();
        pdfViewer.style.borderColor = "";
        pdfViewer.style.backgroundColor = "";
    });
    
    pdfViewer.addEventListener("drop", (e) => {
        e.preventDefault();
        pdfViewer.style.borderColor = "";
        pdfViewer.style.backgroundColor = "";
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type === "application/pdf") {
            const input = document.getElementById("pdf-file-input");
            input.files = files;
            handlePDFUpload({ target: input });
        }
    });
}

function updateConnectionStatus(status, type = 'success') {
    const indicator = document.getElementById("connection-status");
    indicator.innerHTML = `<i class="fas fa-circle"></i> ${status}`;

    const colors = {
        success: '#48bb78',
        warning: '#ed8936',
        error: '#f56565',
        info: '#667eea'
    };
    
    indicator.style.background = `rgba(${type === 'success' ? '72, 187, 120' : 
        type === 'warning' ? '237, 137, 54' : 
        type === 'error' ? '245, 101, 101' : '102, 126, 234'}, 0.1)`;
    indicator.style.color = colors[type];
}

// Enhanced PDF upload handler
async function handlePDFUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    updateConnectionStatus('Uploading...', 'info');
    
    try {
        const formData = new FormData();
        formData.append("file", file);
        
        const res = await fetch("http://127.0.0.1:8000/upload_pdf/", {
            method: "POST",
            body: formData
        });
        
        if (!res.ok) throw new Error('Upload failed');
        
        const data = await res.json();
        pdfId = data.pdf_id;
        
        // Render PDF
        const fileReader = new FileReader();
        fileReader.onload = async function () {
            const typedarray = new Uint8Array(this.result);
            pdfDoc = await pdfjsLib.getDocument({ data: typedarray }).promise;
            totalPages = pdfDoc.numPages;
            
            // Hide PDF placeholder FIRST
            hidePDFPlaceholder();
            
            // Clear old content and render all pages
            pdfContainer.innerHTML = "";
            for (let i = 1; i <= totalPages; i++) {
                await renderPage(i);
            }
            
            // Update UI
            updatePageNavigation();
            // DON'T hide welcome message here anymore
            updateConnectionStatus('PDF Loaded', 'success');
            
            // Show page navigation
            document.getElementById("page-navigation").style.display = "flex";
        };
        fileReader.readAsArrayBuffer(file);
        
    } catch (error) {
        console.error('PDF upload error:', error);
        updateConnectionStatus('Upload Error', 'error');
        showMessage('ai', 'Sorry, there was an error uploading your PDF. Please try again.');
    }
}

function hidePDFPlaceholder() {
    const placeholder = document.querySelector(".pdf-placeholder");
    if (placeholder) {
        placeholder.style.display = "none";
    }
}

async function renderPage(num) {
    const page = await pdfDoc.getPage(num);
    const viewport = page.getViewport({ scale });
    
    const canvas = document.createElement("canvas");
    canvas.classList.add("page-canvas");
    canvas.dataset.pageNumber = num;
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    canvas.style.marginBottom = "20px";
    canvas.style.cursor = "pointer";
    
    await page.render({ 
        canvasContext: canvas.getContext("2d"), 
        viewport 
    }).promise;
    
    // Add click handler for page selection
    canvas.addEventListener("click", () => {
        currentPage = num;
        updatePageNavigation();
        highlightCurrentPage();
    });
    
    const pageWrapper = document.createElement("div");
    pageWrapper.style.textAlign = "center";
    pageWrapper.style.marginBottom = "20px";
    
    const pageLabel = document.createElement("div");
    pageLabel.textContent = `Page ${num}`;
    pageLabel.style.fontSize = "0.9rem";
    pageLabel.style.color = "#667eea";
    pageLabel.style.marginBottom = "8px";
    pageLabel.style.fontWeight = "500";
    
    pageWrapper.appendChild(pageLabel);
    pageWrapper.appendChild(canvas);
    pdfContainer.appendChild(pageWrapper);
}

function highlightCurrentPage() {
    document.querySelectorAll(".page-canvas").forEach(canvas => {
        canvas.style.border = "1px solid rgba(255, 255, 255, 0.2)";
    });
    
    const currentCanvas = document.querySelector(`[data-page-number="${currentPage}"]`);
    if (currentCanvas) {
        currentCanvas.style.border = "3px solid #667eea";
        currentCanvas.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function updatePageNavigation() {
    const pageInfo = document.getElementById("page-info");
    const prevBtn = document.getElementById("prev-page");
    const nextBtn = document.getElementById("next-page");
    
    if (pageInfo) {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }
    
    if (prevBtn) {
        prevBtn.disabled = currentPage <= 1;
    }
    
    if (nextBtn) {
        nextBtn.disabled = currentPage >= totalPages;
    }
}

function navigatePage(direction) {
    const newPage = currentPage + direction;
    if (newPage >= 1 && newPage <= totalPages) {
        currentPage = newPage;
        updatePageNavigation();
        highlightCurrentPage();
    }
}

function zoomPDF(delta) {
    scale = Math.max(0.5, Math.min(3.0, scale + delta));
    
    if (pdfDoc) {
        pdfContainer.innerHTML = "";
        for (let i = 1; i <= totalPages; i++) {
            renderPage(i);
        }
    }
}

// Detect scroll to update current page
pdfContainer.addEventListener("scroll", debounce(() => {
    const canvases = document.querySelectorAll(".page-canvas");
    let closest = null;
    let minOffset = Infinity;
    
    canvases.forEach((canvas) => {
        const rect = canvas.getBoundingClientRect();
        const containerRect = pdfContainer.getBoundingClientRect();
        const offset = Math.abs(rect.top - containerRect.top - containerRect.height / 2);
        
        if (offset < minOffset) {
            minOffset = offset;
            closest = canvas;
        }
    });
    
    if (closest) {
        const newPage = parseInt(closest.dataset.pageNumber);
        if (newPage !== currentPage) {
            currentPage = newPage;
            updatePageNavigation();
        }
    }
}, 100));

function hideWelcomeMessage() {
    const welcomeMessage = document.querySelector(".welcome-message");
    if (welcomeMessage) {
        welcomeMessage.style.display = "none";
    }
}

function handleInputKeydown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleAskQuestion();
    }
}

function handleSuggestionClick(e) {
    if (e.target.classList.contains("suggestion-btn")) {
        const suggestion = e.target.textContent;
        document.getElementById("question-input").value = suggestion;
        handleAskQuestion();
    }
}

// Enhanced ask question handler
async function handleAskQuestion() {
    const questionInput = document.getElementById("question-input");
    const question = questionInput.value.trim();
    
    if (!question || !pdfId) {
        if (!pdfId) {
            showMessage('ai', 'Please upload a PDF first before asking questions.');
        }
        return;
    }
    
    // Clear input and show user message
    questionInput.value = "";
    questionInput.style.height = "auto";
    
    showMessage('user', question);
    showTypingIndicator();
    
    updateConnectionStatus('Thinking...', 'info');
    
    try {
        const formData = new FormData();
        formData.append("pdf_id", pdfId);
        formData.append("page_num", (currentPage - 1).toString());
        formData.append("question", question);
        
        const res = await fetch("http://127.0.0.1:8000/ask/", {
            method: "POST",
            body: formData
        });
        
        if (!res.ok) throw new Error('Failed to get AI response');
        
        const data = await res.json();
        
        hideTypingIndicator();
        showMessage('ai', data.answer);
        updateConnectionStatus('Ready', 'success');
        
        // Store in chat history
        chatHistory.push({
            type: 'user',
            message: question,
            timestamp: new Date(),
            page: currentPage
        });
        
        chatHistory.push({
            type: 'ai',
            message: data.answer,
            timestamp: new Date(),
            page: currentPage
        });
        
    } catch (error) {
        console.error('Ask question error:', error);
        hideTypingIndicator();
        showMessage('ai', 'Sorry, I encountered an error while processing your question. Please try again.');
        updateConnectionStatus('Error', 'error');
    }
}

function showMessage(type, message) {
    const chatBox = document.getElementById("chat-box");
    
    // Hide welcome message only when the first user message is shown
    if (type === 'user' && !firstMessageSent) {
        hideWelcomeMessage();
        firstMessageSent = true;
    }
    
    // Create message element
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", `${type}-message`);
    
    const avatar = document.createElement("div");
    avatar.classList.add("message-avatar");
    
    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");
    
    if (type === 'user') {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
        bubble.innerHTML = `
            <div>${escapeHtml(message)}</div>
            <span class="message-time">${formatTime(new Date())}</span>
        `;
    } else {
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        bubble.innerHTML = `
            <div>${formatAIResponse(message)}</div>
            <span class="message-time">${formatTime(new Date())}</span>
        `;
    }
    
    messageElement.appendChild(avatar);
    messageElement.appendChild(bubble);
    
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.getElementById("typing-indicator");
    indicator.style.display = "flex";
    
    const chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideTypingIndicator() {
    const indicator = document.getElementById("typing-indicator");
    indicator.style.display = "none";
}

function formatAIResponse(message) {
    // Basic formatting for AI responses
    let formatted = escapeHtml(message);
    
    // Convert *bold* to <strong>
    formatted = formatted.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
    
    // Convert line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Convert numbered lists
    formatted = formatted.replace(/^\d+\.\s(.+)$/gm, '<div style="margin-left: 16px;">• $1</div>');
    
    return formatted;
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        const chatBox = document.getElementById("chat-box");
        
        // Remove all messages except welcome message
        const messages = chatBox.querySelectorAll('.message');
        messages.forEach(msg => msg.remove());
        
        // Show welcome message again and reset first message flag
        const welcomeMessage = document.querySelector(".welcome-message");
        if (welcomeMessage) {
            welcomeMessage.style.display = "flex";
            firstMessageSent = false; // Reset the flag
        }
        
        // Clear chat history
        chatHistory = [];
        
        updateConnectionStatus('Chat Cleared', 'success');
    }
}

function exportChat() {
    if (chatHistory.length === 0) {
        alert('No chat history to export.');
        return;
    }
    
    let exportText = `PDF Chat Export - ${new Date().toLocaleDateString()}\n`;
    exportText += `${'='.repeat(50)}\n\n`;

    chatHistory.forEach((item, index) => {
        const role = item.type === 'user' ? 'You' : 'AI Assistant';
        exportText += `${role} (Page ${item.page}) - ${formatTime(item.timestamp)}:\n`;
        exportText += `${item.message}\n\n`;
    });
    
    // Create and download file
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pdf-chat-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    updateConnectionStatus('Chat Exported', 'success');
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
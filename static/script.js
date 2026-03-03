document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const terminal = document.getElementById('terminal');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    
    let eventSource = null;

    function appendLog(msg, type = '') {
        const div = document.createElement('div');
        div.className = `log-line ${type}`;
        div.textContent = msg;
        terminal.appendChild(div);
        terminal.scrollTop = terminal.scrollHeight;
    }

    runBtn.addEventListener('click', async () => {
        // Collect inputs
        const apifyToken = document.getElementById('apifyToken').value.trim();
        const geminiKey = document.getElementById('geminiKey').value.trim();
        const handles = document.getElementById('targetHandles').value;
        const videos = document.getElementById('targetVideos').value;
        const minViews = document.getElementById('minViews').value;

        // Basic validation
        if (!apifyToken || !geminiKey) {
            appendLog('ERROR: Both Apify and Gemini API keys are required.', 'error');
            return;
        }

        if (!handles && !videos) {
            appendLog('ERROR: Please provide at least one Target Handle or specific Target Video URL.', 'error');
            return;
        }

        // Set UI State
        runBtn.disabled = true;
        btnText.textContent = 'Mining in Progress...';
        btnLoader.classList.remove('hidden');
        downloadBtn.classList.add('hidden');
        terminal.innerHTML = ''; // Clear terminal

        try {
            // Initiate backend run
            const response = await fetch('/run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    apify_token: apifyToken,
                    gemini_key: geminiKey,
                    handles: handles,
                    videos: videos,
                    min_views: minViews
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                appendLog(`ERROR: ${data.error}`, 'error');
                resetUI();
                return;
            }

            // Start consuming Server-Sent Events (SSE) log stream
            if (eventSource) {
                eventSource.close();
            }

            eventSource = new EventSource('/stream');
            
            eventSource.onmessage = function(event) {
                if (event.data === "___DONE___") {
                    eventSource.close();
                    appendLog('Pipeline finished. Ready for download.', 'success');
                    downloadBtn.classList.remove('hidden');
                    resetUI();
                } else if (event.data.trim() !== '') {
                    // Check if error
                    let type = '';
                    if (event.data.toLowerCase().includes('error') || event.data.includes('failed')) {
                        type = 'error';
                    }
                    appendLog(event.data, type);
                }
            };

            eventSource.onerror = function(err) {
                console.error("EventSource failed:", err);
                // We keep it open just in case, or close it if it's dead
            };

        } catch (error) {
            appendLog(`NETWORK ERROR: ${error.message}`, 'error');
            resetUI();
        }
    });

    function resetUI() {
        runBtn.disabled = false;
        btnText.textContent = 'Start Extraction Pipeline';
        btnLoader.classList.add('hidden');
    }
});

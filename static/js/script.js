function startScan() {
    fetch('/start_scan')
        .then(response => response.json())
        .then(data => {
            document.getElementById('statusText').innerText = "Scanning started...";
        })
        .catch(error => console.error('Error starting scan:', error));
}

function stopScan() {
    fetch('/stop_scan')
        .then(response => response.json())
        .then(data => {
            document.getElementById('statusText').innerText = "Scanning stopped.";
        })
        .catch(error => console.error('Error stopping scan:', error));
}


// Check plastic detection status (call Flask route)
function checkDetection() {
    fetch('/check_detection')
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').innerText = `Status: ${data.status}`;
        })
        .catch(error => console.error('Error checking detection:', error));
}

// ========== Initialize Elements ========== //
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const webcamVideo = document.getElementById('webcam');
const webcamResult = document.getElementById('webcamResult');
let isWebcamActive = false;

// ========== File Upload ========== //
function handleFiles(files) {
    if (!files || files.length === 0) return;
    const file = files[0];
    
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file (JPEG/PNG)');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:3000/predict', {  // Add full URL
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        document.getElementById('uploadResult').textContent = 
            `Predicted: ${data.class} (${(data.confidence * 100).toFixed(1)}%)`;
    })
    .catch(error => {
        console.error('Upload Error:', error);
        document.getElementById('uploadResult').textContent = `Error: ${error.message}`;
    });
}

// Drag & Drop Handlers
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => e.preventDefault());
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

// ========== Webcam ========== //
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcamVideo.srcObject = stream;
        isWebcamActive = true;
        setInterval(classifyWebcam, 1000); // Classify every 1 second
    } catch (err) {
        console.error('Webcam Error:', err);
        webcamResult.textContent = 'Webcam access denied. Please allow camera permissions.';
    }
}

function classifyWebcam() {
    if (!isWebcamActive) return;

    const canvas = document.createElement('canvas');
    canvas.width = webcamVideo.videoWidth;
    canvas.height = webcamVideo.videoHeight;
    canvas.getContext('2d').drawImage(webcamVideo, 0, 0);
    
    canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('file', blob, 'webcam.jpg');

        fetch('http://localhost:3000/predict', {  // Add full URL
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            webcamResult.textContent = 
                `Predicted: ${data.class} (${(data.confidence * 100).toFixed(1)}%)`;
        })
        .catch(error => console.error('Webcam Prediction Error:', error));
    }, 'image/jpeg');
}




let timestamp;  // Declare timestamp variable

document.getElementById('myButton').addEventListener('click', function () {
    timestamp = Date.now();  // Update the timestamp each time the button is clicked
    document.getElementById('pdfInput').click();
});

document.getElementById('pdfInput').addEventListener('change', function () {
    const files = this.files;
    if (files.length > 0) {
        showProcessingMessage();
        let uploadPromises = [];
        for (let i = 0; i < files.length; i++) {
            uploadPromises.push(uploadFile(files[i]));
        }
        Promise.all(uploadPromises).then(() => {
            hideProcessingMessage();
            showDownloadMessage();
        });
    } else {
        alert('Please upload a PDF file!');
    }
});

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    return fetch(`/saturnia/upload?timestamp=${timestamp}`, {  // Append the timestamp to the URL
        method: 'POST',
        body: formData
    });
}

function showProcessingMessage() {
    const processingMessage = document.getElementById('processingMessage');
    processingMessage.style.opacity = 0;
    processingMessage.style.display = 'block';
    setTimeout(() => {
        processingMessage.style.opacity = 1;
    }, 100);
}

function hideProcessingMessage() {
    const processingMessage = document.getElementById('processingMessage');
    processingMessage.style.opacity = 0;
    setTimeout(() => {
        processingMessage.style.display = 'none';
    }, 500);
}

function showDownloadMessage() {
    const downloadMessage = document.getElementById('downloadMessage');
    downloadMessage.style.opacity = 0;
    downloadMessage.style.display = 'block';
    setTimeout(() => {
        downloadMessage.style.opacity = 1;
    }, 100);
    const downloadLink = document.getElementById('downloadLink');
    downloadLink.addEventListener('click', () => {
        downloadCSV();
    });
}

function downloadCSV() {
    fetch(`/saturnia/download?timestamp=${timestamp}`).then(response => {  // Append the timestamp to the URL
        if (response.ok) {
            window.location.href = `/saturnia/download?timestamp=${timestamp}`;  // Append the timestamp to the URL
            setTimeout(() => {
                location.reload(); // Refresh the page after 10 seconds
            }, 10000);
        } else {
            alert('No CSV data found. Please try again.');
        }
    });
}

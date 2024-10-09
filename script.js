document.getElementById('video-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    const link = document.getElementById('link').value;
    const processLog = document.getElementById('process-log');
    const resultsContainer = document.getElementById('results');

    // Clear previous log and results
    processLog.innerHTML = '';
    resultsContainer.style.display = 'none';

    // Simulate processing
    updateProcessLog('Analyzing video: ' + link);
    setTimeout(() => updateProcessLog('Downloading audio...'), 1000);
    setTimeout(() => updateProcessLog('Audio downloaded successfully.'), 2000);
    setTimeout(() => updateProcessLog('Transcribing audio...'), 3000);
    setTimeout(() => updateProcessLog('Audio transcribed successfully.'), 4000);
    setTimeout(() => updateProcessLog('Analyzing comments...'), 5000);
    setTimeout(() => updateProcessLog('Comments analyzed successfully.'), 6000);
    setTimeout(() => showResults(), 7000);
});

function updateProcessLog(message) {
    const processLog = document.getElementById('process-log');
    processLog.innerHTML += message + '<br>';
    processLog.scrollTop = processLog.scrollHeight; // Auto-scroll
}

function showResults() {
    // Simulated data (Replace with actual data from your backend)
    const transcriptionSummary = "This video discusses various programming techniques and their applications in real-world scenarios.";
    const commentsSummary = "Viewers found the content very informative and engaging, with high praise for the clarity of explanations.";

    document.getElementById('transcription-summary').innerText = transcriptionSummary;
    document.getElementById('comments-summary').innerText = commentsSummary;

    // Sample data for charts
    const sentimentData = {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
            label: 'Sentiment Analysis',
            data: [40, 35, 25],
            backgroundColor: ['#007bff', '#ffc107', '#dc3545'],
        }]
    };
    const keywordData = {
        labels: ['video', 'great', 'tutorial', 'content', 'programming'],
        datasets: [{
            label: 'Top Repeated Keywords',
            data: [30, 25, 20, 18, 15],
            backgroundColor: '#ff6200',
        }]
    };

    // Display results
    const resultsContainer = document.getElementById('results');
    resultsContainer.style.display = 'block';

    // Chart.js for Sentiment Analysis
    const sentimentCtx = document.getElementById('sentiment-chart').getContext('2d');
    new Chart(sentimentCtx, {
        type: 'pie',
        data: sentimentData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
            },
        },
    });

    // Chart.js for Top Repeated Keywords
    const keywordCtx = document.getElementById('keywords-chart').getContext('2d');
    new Chart(keywordCtx, {
        type: 'bar',
        data: keywordData,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
            plugins: {
                legend: {
                    display: false,
                },
            },
        },
    });
}

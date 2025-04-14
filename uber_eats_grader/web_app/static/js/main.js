// Main JavaScript for Uber Eats Restaurant Grader

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle search form submission
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = document.getElementById('restaurant-search');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.classList.add('is-invalid');
            } else {
                searchInput.classList.remove('is-invalid');
            }
        });
    }

    // Handle URL validation
    const urlInput = document.getElementById('url');
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const value = urlInput.value.trim();
            if (value && !isValidUrl(value)) {
                urlInput.classList.add('is-invalid');
                document.getElementById('url-feedback').textContent = 'Please enter a valid Uber Eats URL';
            } else {
                urlInput.classList.remove('is-invalid');
            }
        });
    }

    // URL validation helper
    function isValidUrl(url) {
        try {
            const parsedUrl = new URL(url);
            return parsedUrl.protocol === 'http:' || parsedUrl.protocol === 'https:';
        } catch (e) {
            return false;
        }
    }

    // Handle file input validation
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const file = fileInput.files[0];
            if (file) {
                const fileExt = file.name.split('.').pop().toLowerCase();
                if (fileExt !== 'json') {
                    fileInput.classList.add('is-invalid');
                    document.getElementById('file-feedback').textContent = 'Please upload a JSON file';
                } else {
                    fileInput.classList.remove('is-invalid');
                }
            }
        });
    }

    // Handle dark mode toggle
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('light-mode');
            const isDarkMode = !document.body.classList.contains('light-mode');
            localStorage.setItem('darkMode', isDarkMode);
            
            // Update icon
            const icon = darkModeToggle.querySelector('i');
            if (isDarkMode) {
                icon.classList.remove('bi-sun');
                icon.classList.add('bi-moon');
            } else {
                icon.classList.remove('bi-moon');
                icon.classList.add('bi-sun');
            }
        });
        
        // Check saved preference
        const savedDarkMode = localStorage.getItem('darkMode');
        if (savedDarkMode === 'false') {
            document.body.classList.add('light-mode');
            const icon = darkModeToggle.querySelector('i');
            icon.classList.remove('bi-moon');
            icon.classList.add('bi-sun');
        }
    }

    // Initialize charts if Chart.js is available and elements exist
    if (typeof Chart !== 'undefined') {
        // Component scores chart
        const scoresCanvas = document.getElementById('component-scores-chart');
        if (scoresCanvas) {
            initComponentScoresChart(scoresCanvas);
        }
        
        // Radar chart
        const radarCanvas = document.getElementById('radar-chart');
        if (radarCanvas) {
            initRadarChart(radarCanvas);
        }
    }

    // Example chart initialization functions
    function initComponentScoresChart(canvas) {
        // This would be populated with actual data in production
        const data = {
            labels: ['Menu Structure', 'Pricing', 'Sentiment', 'Visual', 'Promotions'],
            datasets: [
                {
                    label: 'Your Score',
                    data: [0.85, 0.72, 0.91, 0.68, 0.77],
                    backgroundColor: '#3498db',
                    borderColor: '#3498db',
                    borderWidth: 1
                },
                {
                    label: 'Benchmark',
                    data: [0.75, 0.70, 0.72, 0.68, 0.65],
                    backgroundColor: '#e74c3c',
                    borderColor: '#e74c3c',
                    borderWidth: 1
                }
            ]
        };
        
        new Chart(canvas, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1
                    }
                }
            }
        });
    }
    
    function initRadarChart(canvas) {
        // This would be populated with actual data in production
        const data = {
            labels: ['Menu Structure', 'Pricing', 'Sentiment', 'Visual', 'Promotions'],
            datasets: [
                {
                    label: 'Your Score',
                    data: [0.85, 0.72, 0.91, 0.68, 0.77],
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    borderColor: '#3498db',
                    pointBackgroundColor: '#3498db',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#3498db'
                },
                {
                    label: 'Benchmark',
                    data: [0.75, 0.70, 0.72, 0.68, 0.65],
                    backgroundColor: 'rgba(231, 76, 60, 0.2)',
                    borderColor: '#e74c3c',
                    pointBackgroundColor: '#e74c3c',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#e74c3c'
                }
            ]
        };
        
        new Chart(canvas, {
            type: 'radar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    r: {
                        min: 0,
                        max: 1
                    }
                }
            }
        });
    }
});

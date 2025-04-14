import os
import sys
import json
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
import threading
import time
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("web_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("WebApp")

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import application modules
from data_extraction_module import UberEatsExtractor
from analysis_engine import AnalysisEngine
from grading_system import GradingSystem

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'spice-uber-eats-grader-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['REPORTS_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
app.config['ALLOWED_EXTENSIONS'] = {'json'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

# Initialize application components
extractor = UberEatsExtractor(output_dir=app.config['UPLOAD_FOLDER'])
analyzer = AnalysisEngine()
grader = GradingSystem(output_dir=app.config['REPORTS_FOLDER'])

# Store background jobs
jobs = {}

def allowed_file(filename):
    """Check if file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_restaurant_url(job_id, url):
    """
    Process a restaurant URL in the background.
    
    Args:
        job_id (str): Unique job identifier
        url (str): Uber Eats restaurant URL
    """
    try:
        logger.info(f"Starting job {job_id} for URL: {url}")
        
        # Update job status
        jobs[job_id]['status'] = 'extracting'
        jobs[job_id]['progress'] = 10
        jobs[job_id]['message'] = 'Extracting data from Uber Eats...'
        
        # Extract data
        restaurant_data = extractor.extract_restaurant_data(url)
        if not restaurant_data:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = 'Failed to extract data from URL'
            return
        
        # Update job status
        jobs[job_id]['status'] = 'analyzing'
        jobs[job_id]['progress'] = 40
        jobs[job_id]['message'] = 'Analyzing restaurant data...'
        
        # Analyze data
        analysis_results = analyzer.analyze_restaurant(restaurant_data)
        
        # Update job status
        jobs[job_id]['status'] = 'grading'
        jobs[job_id]['progress'] = 70
        jobs[job_id]['message'] = 'Generating grades and reports...'
        
        # Grade results
        grading_results = grader.process_analysis_results(analysis_results)
        
        # Generate reports
        pdf_path = grader.generate_pdf_report(grading_results)
        pptx_path = grader.generate_presentation(grading_results)
        viz_paths = grader.generate_visualizations(grading_results)
        
        # Update job status
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['message'] = 'Analysis completed successfully'
        jobs[job_id]['results'] = {
            'grading_results': grading_results,
            'reports': {
                'pdf': os.path.basename(pdf_path) if pdf_path else None,
                'pptx': os.path.basename(pptx_path) if pptx_path else None,
                'visualizations': {k: os.path.basename(v) for k, v in viz_paths.items()}
            }
        }
        
        logger.info(f"Job {job_id} completed successfully")
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = f'Error: {str(e)}'

def process_uploaded_file(job_id, file_path):
    """
    Process an uploaded JSON file in the background.
    
    Args:
        job_id (str): Unique job identifier
        file_path (str): Path to uploaded JSON file
    """
    try:
        logger.info(f"Starting job {job_id} for file: {file_path}")
        
        # Update job status
        jobs[job_id]['status'] = 'loading'
        jobs[job_id]['progress'] = 10
        jobs[job_id]['message'] = 'Loading data from file...'
        
        # Load data from file
        with open(file_path, 'r') as f:
            restaurant_data = json.load(f)
        
        # Update job status
        jobs[job_id]['status'] = 'analyzing'
        jobs[job_id]['progress'] = 40
        jobs[job_id]['message'] = 'Analyzing restaurant data...'
        
        # Analyze data
        analysis_results = analyzer.analyze_restaurant(restaurant_data)
        
        # Update job status
        jobs[job_id]['status'] = 'grading'
        jobs[job_id]['progress'] = 70
        jobs[job_id]['message'] = 'Generating grades and reports...'
        
        # Grade results
        grading_results = grader.process_analysis_results(analysis_results)
        
        # Generate reports
        pdf_path = grader.generate_pdf_report(grading_results)
        pptx_path = grader.generate_presentation(grading_results)
        viz_paths = grader.generate_visualizations(grading_results)
        
        # Update job status
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['message'] = 'Analysis completed successfully'
        jobs[job_id]['results'] = {
            'grading_results': grading_results,
            'reports': {
                'pdf': os.path.basename(pdf_path) if pdf_path else None,
                'pptx': os.path.basename(pptx_path) if pptx_path else None,
                'visualizations': {k: os.path.basename(v) for k, v in viz_paths.items()}
            }
        }
        
        logger.info(f"Job {job_id} completed successfully")
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {e}")
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = f'Error: {str(e)}'

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Handle analysis requests."""
    if request.method == 'POST':
        # Check if URL or file was provided
        url = request.form.get('url')
        file = request.files.get('file')
        
        if not url and not file:
            return jsonify({'error': 'Please provide either a URL or a file'}), 400
        
        # Generate a unique job ID
        job_id = f"job_{int(time.time())}_{hash(url or str(file))}"
        
        # Initialize job status
        jobs[job_id] = {
            'id': job_id,
            'status': 'pending',
            'progress': 0,
            'message': 'Job initialized',
            'created_at': datetime.now().isoformat(),
            'results': None
        }
        
        if url:
            # Process URL in background
            thread = threading.Thread(target=process_restaurant_url, args=(job_id, url))
            thread.daemon = True
            thread.start()
            
            return redirect(url_for('job_status', job_id=job_id))
        
        elif file and allowed_file(file.filename):
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process file in background
            thread = threading.Thread(target=process_uploaded_file, args=(job_id, file_path))
            thread.daemon = True
            thread.start()
            
            return redirect(url_for('job_status', job_id=job_id))
        
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    
    # GET request - render the analysis form
    return render_template('analyze.html')

@app.route('/job/<job_id>')
def job_status(job_id):
    """Render the job status page."""
    if job_id not in jobs:
        return render_template('error.html', message='Job not found'), 404
    
    return render_template('job_status.html', job_id=job_id)

@app.route('/api/job/<job_id>')
def api_job_status(job_id):
    """API endpoint to get job status."""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

@app.route('/results/<job_id>')
def results(job_id):
    """Render the results page."""
    if job_id not in jobs or jobs[job_id]['status'] != 'completed':
        return render_template('error.html', message='Results not available'), 404
    
    return render_template('results.html', job_id=job_id, results=jobs[job_id]['results'])

@app.route('/reports/<filename>')
def download_report(filename):
    """Download a report file."""
    return send_from_directory(app.config['REPORTS_FOLDER'], filename)

@app.route('/api/examples')
def api_examples():
    """API endpoint to get example restaurants."""
    examples = [
        {
            'name': 'Shake Shack',
            'url': 'https://www.ubereats.com/store/shake-shack-madison-square-park/OTU3YTBjYWUtMDAwMC00YWIxLWE3NDYtYjkyNDM5NzRlZGMx',
            'image': '/static/img/examples/shake_shack.jpg',
            'description': 'Popular burger chain known for its Angus beef burgers, flat-top hot dogs, and frozen custard.'
        },
        {
            'name': 'Sweetgreen',
            'url': 'https://www.ubereats.com/store/sweetgreen-nomad/NmM0ZDQ5ZDYtZGE5Ny00YWU2LTg1ZDYtNDRlZGFjYzFkMGMw',
            'image': '/static/img/examples/sweetgreen.jpg',
            'description': 'Fast-casual restaurant chain serving salads and grain bowls made with seasonal, locally-sourced ingredients.'
        },
        {
            'name': 'Chipotle',
            'url': 'https://www.ubereats.com/store/chipotle-mexican-grill-28th-park-ave/NWI1YWVlYTktMDAwMC00YWIxLWE3NDYtYjkyNDM5NzRlZGMx',
            'image': '/static/img/examples/chipotle.jpg',
            'description': 'Fast-casual Mexican restaurant chain known for its build-your-own burritos, bowls, and tacos.'
        }
    ]
    return jsonify(examples)

@app.route('/api/train', methods=['POST'])
def api_train():
    """API endpoint to train the model with examples."""
    data = request.json
    
    if not data or 'examples' not in data:
        return jsonify({'error': 'No examples provided'}), 400
    
    # In a real implementation, this would update the model based on examples
    # For now, just return success
    return jsonify({'success': True, 'message': 'Training data received'})

@app.route('/train')
def train():
    """Render the training page."""
    return render_template('train.html')

@app.route('/api/metrics')
def api_metrics():
    """API endpoint to get system metrics."""
    metrics = {
        'total_jobs': len(jobs),
        'completed_jobs': sum(1 for job in jobs.values() if job['status'] == 'completed'),
        'failed_jobs': sum(1 for job in jobs.values() if job['status'] == 'failed'),
        'in_progress_jobs': sum(1 for job in jobs.values() if job['status'] not in ['completed', 'failed']),
        'average_grade': 'B+',  # Placeholder - would calculate from actual results
        'top_issues': [
            'Limited menu item images',
            'Inconsistent pricing strategy',
            'Few customer reviews'
        ]
    }
    return jsonify(metrics)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', message='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html', message='Server error'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/env python3
"""
Uber Eats Grader - Deployment Script
This script sets up and runs the Uber Eats Grader application.
"""

import os
import sys
import logging
import argparse
import subprocess
import webbrowser
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("deployment")

def check_dependencies():
    """Check if all required dependencies are installed."""
    logger.info("Checking dependencies...")
    
    required_packages = [
        'flask', 'werkzeug', 'requests', 'beautifulsoup4', 'cloudscraper', 
        'selenium', 'nltk', 'pandas', 'numpy', 'matplotlib', 'seaborn',
        'fpdf', 'python-pptx'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '--quiet', *missing_packages
            ])
            logger.info("All dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    else:
        logger.info("All dependencies are already installed.")
    
    # Download NLTK data
    try:
        import nltk
        nltk_resources = ['punkt', 'stopwords', 'vader_lexicon']
        for resource in nltk_resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                logger.info(f"Downloading NLTK resource: {resource}")
                nltk.download(resource, quiet=True)
    except Exception as e:
        logger.error(f"Failed to download NLTK resources: {e}")
        return False
    
    return True

def setup_application(app_dir):
    """Set up the application directory structure."""
    logger.info(f"Setting up application in {app_dir}")
    
    # Create necessary directories
    os.makedirs(os.path.join(app_dir, 'data'), exist_ok=True)
    os.makedirs(os.path.join(app_dir, 'output'), exist_ok=True)
    os.makedirs(os.path.join(app_dir, 'logs'), exist_ok=True)
    
    # Create empty __init__.py files to make directories importable
    Path(os.path.join(app_dir, '__init__.py')).touch()
    
    return True

def run_application(app_dir, host='0.0.0.0', port=5000, debug=False):
    """Run the Flask web application."""
    logger.info(f"Starting Uber Eats Grader application on {host}:{port}")
    
    try:
        # Change to the app directory
        os.chdir(app_dir)
        
        # Import the Flask app
        sys.path.insert(0, app_dir)
        from web_app.app import app
        
        # Open browser
        if host in ('0.0.0.0', '127.0.0.1', 'localhost'):
            url = f"http://localhost:{port}"
            logger.info(f"Opening browser at {url}")
            webbrowser.open(url)
        
        # Run the app
        app.run(host=host, port=port, debug=debug)
        
        return True
    except Exception as e:
        logger.error(f"Failed to run application: {e}")
        return False

def main():
    """Main entry point for the deployment script."""
    parser = argparse.ArgumentParser(description='Uber Eats Grader Deployment')
    parser.add_argument('--host', default='0.0.0.0', help='Host to run the application on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the application on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()
    
    # Get the application directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Failed to check or install dependencies. Exiting.")
        return 1
    
    # Setup application
    if not setup_application(app_dir):
        logger.error("Failed to set up application. Exiting.")
        return 1
    
    # Run application
    if not run_application(app_dir, args.host, args.port, args.debug):
        logger.error("Failed to run application. Exiting.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

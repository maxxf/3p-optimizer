import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import tempfile
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app.app import app

class TestWebApp:
    
    def setup_method(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        app.config['REPORTS_FOLDER'] = tempfile.mkdtemp()
        self.client = app.test_client()
        
        # Create necessary directories
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
    
    def teardown_method(self):
        # Clean up test directories
        import shutil
        shutil.rmtree(app.config['UPLOAD_FOLDER'], ignore_errors=True)
        shutil.rmtree(app.config['REPORTS_FOLDER'], ignore_errors=True)
    
    def test_index_page(self):
        response = self.client.get('/')
        
        # Verify response
        assert response.status_code == 200
        assert b"What's your restaurant's name?" in response.data
        assert b"I'll scan your 3P storefront" in response.data
        
        # Verify search form exists
        assert b'<form action="/analyze"' in response.data
        assert b'<input type="text" class="form-control' in response.data
    
    def test_about_page(self):
        response = self.client.get('/about')
        
        # Verify response
        assert response.status_code == 200
        assert b"About 3P Delivery Optimizer" in response.data
        assert b"What We Do" in response.data
        assert b"How It Works" in response.data
        assert b"About Spice Agency" in response.data
    
    def test_analyze_page_get(self):
        response = self.client.get('/analyze')
        
        # Verify response
        assert response.status_code == 200
        assert b"Analyze Your Restaurant" in response.data
        assert b'<form action="/analyze" method="post"' in response.data
        assert b'Uber Eats Restaurant URL' in response.data
    
    @patch('web_app.app.process_restaurant_url')
    def test_analyze_page_post_with_url(self, mock_process):
        # Mock the background processing function
        mock_process.return_value = None
        
        # Test form submission with URL
        response = self.client.post('/analyze', data={
            'url': 'https://www.ubereats.com/store/test-restaurant/123456'
        }, follow_redirects=True)
        
        # Verify response
        assert response.status_code == 200
        assert b"Analysis in Progress" in response.data
        
        # Verify background process was started
        assert mock_process.call_count == 1
    
    @patch('web_app.app.process_uploaded_file')
    def test_analyze_page_post_with_file(self, mock_process):
        # Mock the background processing function
        mock_process.return_value = None
        
        # Create a test JSON file
        test_data = {
            'restaurant_info': {'name': 'Test Restaurant'},
            'menu_items': [{'name': 'Test Item', 'price': 9.99}]
        }
        
        test_file = os.path.join(app.config['UPLOAD_FOLDER'], 'test_data.json')
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test form submission with file
        with open(test_file, 'rb') as f:
            response = self.client.post('/analyze', data={
                'file': (f, 'test_data.json')
            }, content_type='multipart/form-data', follow_redirects=True)
        
        # Verify response
        assert response.status_code == 200
        assert b"Analysis in Progress" in response.data
        
        # Verify background process was started
        assert mock_process.call_count == 1
    
    def test_job_status_page(self):
        # Add a test job to the jobs dictionary
        from web_app.app import jobs
        job_id = 'test_job_123'
        jobs[job_id] = {
            'id': job_id,
            'status': 'analyzing',
            'progress': 40,
            'message': 'Analyzing restaurant data...',
            'created_at': '2025-04-13T12:00:00',
            'results': None
        }
        
        response = self.client.get(f'/job/{job_id}')
        
        # Verify response
        assert response.status_code == 200
        assert b"Analysis in Progress" in response.data
        assert b'<div id="progress-bar"' in response.data
        
        # Clean up
        del jobs[job_id]
    
    def test_job_status_api(self):
        # Add a test job to the jobs dictionary
        from web_app.app import jobs
        job_id = 'test_job_123'
        jobs[job_id] = {
            'id': job_id,
            'status': 'analyzing',
            'progress': 40,
            'message': 'Analyzing restaurant data...',
            'created_at': '2025-04-13T12:00:00',
            'results': None
        }
        
        response = self.client.get(f'/api/job/{job_id}')
        
        # Verify response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == job_id
        assert data['status'] == 'analyzing'
        assert data['progress'] == 40
        
        # Clean up
        del jobs[job_id]
    
    def test_results_page(self):
        # Add a test job with results to the jobs dictionary
        from web_app.app import jobs
        job_id = 'test_job_123'
        
        # Create test report files
        pdf_path = os.path.join(app.config['REPORTS_FOLDER'], 'test_report.pdf')
        with open(pdf_path, 'w') as f:
            f.write('Test PDF content')
        
        pptx_path = os.path.join(app.config['REPORTS_FOLDER'], 'test_presentation.pptx')
        with open(pptx_path, 'w') as f:
            f.write('Test PPTX content')
        
        viz_path = os.path.join(app.config['REPORTS_FOLDER'], 'test_viz.png')
        with open(viz_path, 'w') as f:
            f.write('Test visualization content')
        
        # Create job with results
        jobs[job_id] = {
            'id': job_id,
            'status': 'completed',
            'progress': 100,
            'message': 'Analysis completed successfully',
            'created_at': '2025-04-13T12:00:00',
            'results': {
                'grading_results': {
                    'restaurant_info': {'name': 'Test Restaurant'},
                    'overall_grade': 'A',
                    'component_grades': {
                        'menu_structure': 'A-',
                        'pricing': 'B+',
                        'customer_sentiment': 'A+',
                        'visual_presentation': 'B',
                        'promotion_strategy': 'B-'
                    },
                    'component_scores': {
                        'menu_structure': 0.85,
                        'pricing': 0.75,
                        'customer_sentiment': 0.95,
                        'visual_presentation': 0.70,
                        'promotion_strategy': 0.65
                    },
                    'strengths': ['Great customer reviews', 'Well-organized menu'],
                    'weaknesses': ['Limited promotions', 'Some image quality issues'],
                    'recommendations': ['Improve promotion visibility', 'Upgrade image quality'],
                    'component_details': {
                        'menu_structure': {
                            'metrics': {'category_count': 5},
                            'recommendations': ['Add more categories']
                        },
                        'pricing': {
                            'metrics': {'average_price': 12.99},
                            'recommendations': ['Add value options']
                        },
                        'customer_sentiment': {
                            'metrics': {'average_rating': 4.8},
                            'recommendations': ['Respond to reviews']
                        },
                        'visual_presentation': {
                            'metrics': {'image_coverage': 0.8},
                            'recommendations': ['Improve image quality']
                        },
                        'promotion_strategy': {
                            'metrics': {'active_promotions': 1},
                            'recommendations': ['Add more promotions']
                        }
                    },
                    'benchmark_comparisons': {
                        'menu_structure': {'benchmark_avg': 0.75, 'difference': 0.1, 'percentile': 80},
                        'pricing': {'benchmark_avg': 0.70, 'difference': 0.05, 'percentile': 65},
                        'customer_sentiment': {'benchmark_avg': 0.80, 'difference': 0.15, 'percentile': 90},
                        'visual_presentation': {'benchmark_avg': 0.65, 'difference': 0.05, 'percentile': 70},
                        'promotion_strategy': {'benchmark_avg': 0.60, 'difference': 0.05, 'percentile': 60}
                    }
                },
                'reports': {
                    'pdf': 'test_report.pdf',
                    'pptx': 'test_presentation.pptx',
                    'visualizations': {
                        'component_scores': 'test_viz.png'
                    }
                }
            }
        }
        
        response = self.client.get(f'/results/{job_id}')
        
        # Verify response
        assert response.status_code == 200
        assert b"Test Restaurant Analysis" in response.data
        assert b"Overall Grade" in response.data
        assert b"Component Grades" in response.data
        assert b"Priority Recommendations" in response.data
        
        # Clean up
        del jobs[job_id]
    
    def test_train_page(self):
        response = self.client.get('/train')
        
        # Verify response
        assert response.status_code == 200
        assert b"Train the Analysis Model" in response.data
        assert b"How Training Works" in response.data
        assert b"Add Training Examples" in response.data
        
        # Verify form exists
        assert b'<form id="training-form"' in response.data
        assert b'Restaurant URL' in response.data
        assert b'Why is this a good example?' in response.data
    
    @patch('web_app.app.extractor')
    @patch('web_app.app.analyzer')
    @patch('web_app.app.grader')
    def test_end_to_end_flow(self, mock_grader, mock_analyzer, mock_extractor):
        # Mock the components
        mock_extractor.extract_restaurant_data.return_value = {
            'restaurant_info': {'name': 'Test Restaurant'},
            'menu_items': [{'name': 'Test Item', 'price': 9.99}]
        }
        
        mock_analyzer.analyze_restaurant.return_value = {
            'restaurant_info': {'name': 'Test Restaurant'},
            'menu_structure': {'score': 0.85},
            'pricing': {'score': 0.75},
            'customer_sentiment': {'score': 0.90},
            'visual_presentation': {'score': 0.80},
            'promotion_strategy': {'score': 0.70},
            'overall_score': 0.80
        }
        
        mock_grader.process_analysis_results.return_value = {
            'restaurant_info': {'name': 'Test Restaurant'},
            'overall_grade': 'A-',
            'component_grades': {
                'menu_structure': 'A-',
                'pricing': 'B+',
                'customer_sentiment': 'A',
                'visual_presentation': 'A-',
                'promotion_strategy': 'B'
            }
        }
        
        mock_grader.generate_pdf_report.return_value = '/tmp/test_report.pdf'
        mock_grader.generate_presentation.return_value = '/tmp/test_presentation.pptx'
        mock_grader.generate_visualizations.return_value = {
            'component_scores': '/tmp/component_scores.png',
            'radar_chart': '/tmp/radar_chart.png'
        }
        
        # Test the analyze endpoint
        response = self.client.post('/analyze', data={
            'url': 'https://www.ubereats.com/store/test-restaurant/123456'
        }, follow_redirects=True)
        
        # Verify initial response
        assert response.status_code == 200
        assert b"Analysis in Progress" in response.data
        
        # Get the job ID from the URL
        job_id = response.request.path.split('/')[-1]
        
        # Manually update job status to simulate completion
        from web_app.app import jobs
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['results'] = {
            'grading_results': mock_grader.process_analysis_results.return_value,
            'reports': {
                'pdf': 'test_report.pdf',
                'pptx': 'test_presentation.pptx',
                'visualizations': {
                    'component_scores': 'component_scores.png',
                    'radar_chart': 'radar_chart.png'
                }
            }
        }
        
        # Test the results page
        response = self.client.get(f'/results/{job_id}')
        
        # Verify results response
        assert response.status_code == 200
        assert b"Test Restaurant Analysis" in response.data
        assert b"Overall Grade" in response.data
        
        # Clean up
        del jobs[job_id]

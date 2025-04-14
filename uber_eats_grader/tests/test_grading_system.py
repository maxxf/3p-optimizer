import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import tempfile

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grading_system import GradingSystem

class TestGradingSystem:
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.grader = GradingSystem(output_dir=self.temp_dir)
        
        # Sample analysis results for testing
        self.sample_analysis = {
            'restaurant_info': {
                'name': 'Test Restaurant',
                'rating': 4.5,
                'review_count': 120,
                'price_range': '$$',
                'cuisine': 'American',
                'address': '123 Test St, New York, NY'
            },
            'menu_structure': {
                'score': 0.85,
                'metrics': {
                    'category_count': 4,
                    'items_per_category': 5.2,
                    'description_quality': 0.88,
                    'popular_items_highlighted': True
                },
                'strengths': ['Well-organized categories', 'Detailed descriptions'],
                'weaknesses': ['Limited filtering options'],
                'recommendations': ['Add dietary restriction filters', 'Highlight bestsellers more prominently']
            },
            'pricing': {
                'score': 0.75,
                'metrics': {
                    'average_price': 12.99,
                    'price_range': '$$',
                    'price_comparison': {
                        'relative_position': 'similar',
                        'price_difference_percentage': 5.2
                    },
                    'value_options': True
                },
                'strengths': ['Competitive pricing', 'Good value options'],
                'weaknesses': ['Limited premium options'],
                'recommendations': ['Add a premium category', 'Create more combo options for better value']
            },
            'customer_sentiment': {
                'score': 0.90,
                'metrics': {
                    'average_rating': 4.5,
                    'review_count': 120,
                    'sentiment_analysis': {
                        'positive': 75,
                        'negative': 15,
                        'neutral': 10
                    },
                    'common_themes': {
                        'positive': ['Great food', 'Fast delivery'],
                        'negative': ['Packaging issues', 'Occasional delays']
                    }
                },
                'strengths': ['High overall rating', 'Strong positive sentiment'],
                'weaknesses': ['Some packaging complaints'],
                'recommendations': ['Address packaging issues', 'Respond to negative reviews']
            },
            'visual_presentation': {
                'score': 0.80,
                'metrics': {
                    'image_coverage': 0.85,
                    'image_quality': 0.78,
                    'visual_consistency': 0.82
                },
                'strengths': ['Good image coverage', 'Consistent visual style'],
                'weaknesses': ['Some images could be higher quality'],
                'recommendations': ['Upgrade image quality for top items', 'Add more lifestyle photos']
            },
            'promotion_strategy': {
                'score': 0.70,
                'metrics': {
                    'active_promotions': 2,
                    'promotion_types': ['discount', 'free delivery'],
                    'promotion_visibility': 0.65
                },
                'strengths': ['Good variety of promotions'],
                'weaknesses': ['Limited visibility of promotions'],
                'recommendations': ['Increase promotion visibility', 'Add time-limited offers']
            },
            'overall_score': 0.80
        }
    
    def teardown_method(self):
        # Clean up test files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_process_analysis_results(self):
        result = self.grader.process_analysis_results(self.sample_analysis)
        
        # Verify result structure
        assert 'restaurant_info' in result
        assert 'overall_grade' in result
        assert 'component_grades' in result
        assert 'component_scores' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'recommendations' in result
        assert 'component_details' in result
        assert 'benchmark_comparisons' in result
        
        # Verify component grades
        assert 'menu_structure' in result['component_grades']
        assert 'pricing' in result['component_grades']
        assert 'customer_sentiment' in result['component_grades']
        assert 'visual_presentation' in result['component_grades']
        assert 'promotion_strategy' in result['component_grades']
        
        # Verify grade format (should be letter grades like A+, B, etc.)
        assert len(result['overall_grade']) <= 2
        assert result['overall_grade'][0] in 'ABCDF'
        
        # Verify strengths and weaknesses are lists
        assert isinstance(result['strengths'], list)
        assert isinstance(result['weaknesses'], list)
        assert len(result['strengths']) > 0
        assert len(result['weaknesses']) > 0
        
        # Verify recommendations are prioritized
        assert isinstance(result['recommendations'], list)
        assert len(result['recommendations']) > 0
    
    def test_calculate_grade(self):
        # Test various score ranges
        assert self.grader.calculate_grade(0.95) == 'A+'
        assert self.grader.calculate_grade(0.85) == 'A'
        assert self.grader.calculate_grade(0.80) == 'A-'
        assert self.grader.calculate_grade(0.75) == 'B+'
        assert self.grader.calculate_grade(0.70) == 'B'
        assert self.grader.calculate_grade(0.65) == 'B-'
        assert self.grader.calculate_grade(0.60) == 'C+'
        assert self.grader.calculate_grade(0.55) == 'C'
        assert self.grader.calculate_grade(0.50) == 'C-'
        assert self.grader.calculate_grade(0.45) == 'D+'
        assert self.grader.calculate_grade(0.40) == 'D'
        assert self.grader.calculate_grade(0.35) == 'D-'
        assert self.grader.calculate_grade(0.30) == 'F'
    
    def test_prioritize_recommendations(self):
        # Create sample component results with recommendations
        component_results = {
            'menu_structure': {
                'score': 0.60,
                'recommendations': ['Improve menu organization', 'Add more categories']
            },
            'pricing': {
                'score': 0.85,
                'recommendations': ['Add premium options']
            },
            'customer_sentiment': {
                'score': 0.90,
                'recommendations': ['Respond to reviews']
            },
            'visual_presentation': {
                'score': 0.70,
                'recommendations': ['Improve image quality', 'Add more photos']
            },
            'promotion_strategy': {
                'score': 0.50,
                'recommendations': ['Add more promotions', 'Increase visibility', 'Create limited-time offers']
            }
        }
        
        # Test recommendation prioritization
        recommendations = self.grader.prioritize_recommendations(component_results)
        
        # Verify recommendations are prioritized by lowest scores first
        assert len(recommendations) > 0
        assert 'Add more promotions' in recommendations[0:3]  # Promotion strategy has lowest score
        assert 'Improve menu organization' in recommendations[0:5]  # Menu structure has second lowest score
    
    @patch('grading_system.plt')
    @patch('grading_system.Figure')
    def test_generate_visualizations(self, mock_figure, mock_plt):
        # Mock the figure and save methods
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        mock_fig.savefig.return_value = None
        
        # Test visualization generation
        grading_results = self.grader.process_analysis_results(self.sample_analysis)
        viz_paths = self.grader.generate_visualizations(grading_results)
        
        # Verify visualization paths
        assert 'component_scores' in viz_paths
        assert 'radar_chart' in viz_paths
        assert os.path.exists(os.path.dirname(viz_paths['component_scores']))
        
        # Verify methods were called
        assert mock_figure.call_count > 0
        assert mock_fig.savefig.call_count > 0
    
    @patch('grading_system.FPDF')
    def test_generate_pdf_report(self, mock_fpdf):
        # Mock PDF generation
        mock_pdf = MagicMock()
        mock_fpdf.return_value = mock_pdf
        
        # Test PDF generation
        grading_results = self.grader.process_analysis_results(self.sample_analysis)
        pdf_path = self.grader.generate_pdf_report(grading_results)
        
        # Verify PDF path
        assert pdf_path is not None
        assert pdf_path.endswith('.pdf')
        
        # Verify methods were called
        assert mock_pdf.add_page.call_count > 0
        assert mock_pdf.output.call_count > 0
    
    @patch('grading_system.Presentation')
    def test_generate_presentation(self, mock_presentation):
        # Mock presentation generation
        mock_pres = MagicMock()
        mock_presentation.return_value = mock_pres
        
        # Test presentation generation
        grading_results = self.grader.process_analysis_results(self.sample_analysis)
        pptx_path = self.grader.generate_presentation(grading_results)
        
        # Verify presentation path
        assert pptx_path is not None
        assert pptx_path.endswith('.pptx')
        
        # Verify methods were called
        assert mock_pres.save.call_count > 0
    
    def test_compare_to_benchmarks(self):
        # Test benchmark comparison
        component_scores = {
            'menu_structure': 0.85,
            'pricing': 0.75,
            'customer_sentiment': 0.90,
            'visual_presentation': 0.80,
            'promotion_strategy': 0.70
        }
        
        comparisons = self.grader.compare_to_benchmarks(component_scores)
        
        # Verify comparison structure
        for component in component_scores:
            assert component in comparisons
            assert 'benchmark_avg' in comparisons[component]
            assert 'difference' in comparisons[component]
            assert 'percentile' in comparisons[component]
            
            # Verify values are in expected ranges
            assert 0 <= comparisons[component]['benchmark_avg'] <= 1
            assert -1 <= comparisons[component]['difference'] <= 1
            assert 0 <= comparisons[component]['percentile'] <= 100

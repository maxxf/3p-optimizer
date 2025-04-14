import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import tempfile
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis_engine import AnalysisEngine

class TestAnalysisEngine:
    
    def setup_method(self):
        self.analyzer = AnalysisEngine()
        
        # Sample restaurant data for testing
        self.sample_data = {
            'restaurant_info': {
                'name': 'Test Restaurant',
                'rating': 4.5,
                'review_count': 120,
                'price_range': '$$',
                'cuisine': 'American',
                'address': '123 Test St, New York, NY',
                'banner_image': 'https://example.com/banner.jpg'  # Added banner image
            },
            'menu_items': [
                {
                    'name': 'Burger',
                    'price': 12.99,
                    'description': 'Delicious beef burger with cheese and special sauce',
                    'image_url': 'https://example.com/burger.jpg',
                    'category': 'Main',
                    'popular': True
                },
                {
                    'name': 'Fries',
                    'price': 4.99,
                    'description': 'Crispy golden fries',
                    'image_url': 'https://example.com/fries.jpg',
                    'category': 'Sides',
                    'popular': True
                },
                {
                    'name': 'Salad',
                    'price': 8.99,
                    'description': 'Fresh garden salad',
                    'image_url': 'https://example.com/salad.jpg',
                    'category': 'Healthy Options',
                    'popular': False
                }
            ],
            'reviews': [
                {
                    'rating': 5,
                    'text': 'Great food and fast delivery!',
                    'date': '2025-03-15'
                },
                {
                    'rating': 4,
                    'text': 'Food was good but delivery took longer than expected.',
                    'date': '2025-03-10'
                },
                {
                    'rating': 5,
                    'text': 'Best burger in town!',
                    'date': '2025-03-05'
                }
            ],
            'categories': [
                'Main', 'Sides', 'Healthy Options', 'Drinks'
            ],
            'promotions': [
                {
                    'type': 'discount',
                    'description': '20% off your first order',
                    'active': True
                }
            ]
        }
        
        # Sample competitor data
        self.competitor_data = [
            {
                'restaurant_info': {
                    'name': 'Competitor 1',
                    'rating': 4.2,
                    'review_count': 85,
                    'price_range': '$$',
                    'cuisine': 'American'
                },
                'menu_items': [
                    {
                        'name': 'Classic Burger',
                        'price': 11.99,
                        'category': 'Burgers'
                    },
                    {
                        'name': 'Fries',
                        'price': 3.99,
                        'category': 'Sides'
                    }
                ]
            },
            {
                'restaurant_info': {
                    'name': 'Competitor 2',
                    'rating': 4.7,
                    'review_count': 150,
                    'price_range': '$$$',
                    'cuisine': 'American'
                },
                'menu_items': [
                    {
                        'name': 'Gourmet Burger',
                        'price': 15.99,
                        'category': 'Burgers'
                    },
                    {
                        'name': 'Truffle Fries',
                        'price': 6.99,
                        'category': 'Sides'
                    }
                ]
            }
        ]
    
    def test_analyze_restaurant(self):
        # Mock the component analysis methods
        self.analyzer.analyze_menu_structure = MagicMock(return_value={'score': 0.85})
        self.analyzer.analyze_pricing = MagicMock(return_value={'score': 0.75})
        self.analyzer.analyze_customer_sentiment = MagicMock(return_value={'score': 0.90})
        self.analyzer.analyze_visual_presentation = MagicMock(return_value={'score': 0.80})
        self.analyzer.analyze_promotion_strategy = MagicMock(return_value={'score': 0.70})
        
        # Test the main analysis method
        result = self.analyzer.analyze_restaurant(self.sample_data)
        
        # Verify the result structure
        assert 'restaurant_info' in result
        assert 'menu_structure' in result
        assert 'pricing' in result
        assert 'customer_sentiment' in result
        assert 'visual_presentation' in result
        assert 'promotion_strategy' in result
        assert 'overall_score' in result
        
        # Verify the component methods were called
        self.analyzer.analyze_menu_structure.assert_called_once()
        self.analyzer.analyze_pricing.assert_called_once()
        self.analyzer.analyze_customer_sentiment.assert_called_once()
        self.analyzer.analyze_visual_presentation.assert_called_once()
        self.analyzer.analyze_promotion_strategy.assert_called_once()
        
        # Verify overall score calculation
        assert result['overall_score'] == 0.8  # Average of all component scores
    
    def test_analyze_menu_structure(self):
        result = self.analyzer.analyze_menu_structure(self.sample_data)
        
        # Verify result structure
        assert 'score' in result
        assert 'metrics' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'recommendations' in result
        
        # Verify metrics
        assert 'category_count' in result['metrics']
        assert 'items_per_category' in result['metrics']
        assert 'description_quality' in result['metrics']
        assert 'popular_items_highlighted' in result['metrics']
        
        # Verify score is within range
        assert 0 <= result['score'] <= 1
    
    def test_analyze_pricing(self):
        result = self.analyzer.analyze_pricing(self.sample_data, self.competitor_data)
        
        # Verify result structure
        assert 'score' in result
        assert 'metrics' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'recommendations' in result
        
        # Verify metrics
        assert 'average_price' in result['metrics']
        assert 'price_range' in result['metrics']
        assert 'price_comparison' in result['metrics']
        assert 'value_options' in result['metrics']
        
        # Verify score is within range
        assert 0 <= result['score'] <= 1
    
    def test_analyze_customer_sentiment(self):
        result = self.analyzer.analyze_customer_sentiment(self.sample_data)
        
        # Verify result structure
        assert 'score' in result
        assert 'metrics' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'recommendations' in result
        
        # Verify metrics
        assert 'average_rating' in result['metrics']
        assert 'review_count' in result['metrics']
        assert 'sentiment_analysis' in result['metrics']
        assert 'common_themes' in result['metrics']
        
        # Verify score is within range
        assert 0 <= result['score'] <= 1
        
        # Verify sentiment analysis
        assert 'positive' in result['metrics']['sentiment_analysis']
        assert 'negative' in result['metrics']['sentiment_analysis']
        assert 'neutral' in result['metrics']['sentiment_analysis']
    
    def test_analyze_visual_presentation(self):
        result = self.analyzer.analyze_visual_presentation(self.sample_data)
        
        # Verify result structure
        assert 'score' in result
        assert 'metrics' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'recommendations' in result
        
        # Verify metrics
        assert 'image_coverage' in result['metrics']
        assert 'image_quality' in result['metrics']
        assert 'visual_consistency' in result['metrics']
        
        # Verify score is within range
        assert 0 <= result['score'] <= 1
    
    def test_analyze_promotion_strategy(self):
        result = self.analyzer.analyze_promotion_strategy(self.sample_data)
        
        # Verify result structure
        assert 'score' in result
        assert 'metrics' in result
        assert 'strengths' in result
        assert 'weaknesses' in result
        assert 'recommendations' in result
        
        # Verify metrics
        assert 'active_promotions' in result['metrics']
        assert 'promotion_types' in result['metrics']
        assert 'promotion_visibility' in result['metrics']
        
        # Verify score is within range
        assert 0 <= result['score'] <= 1
    
    def test_calculate_description_quality(self):
        descriptions = [item['description'] for item in self.sample_data['menu_items']]
        quality_score = self.analyzer.calculate_description_quality(descriptions)
        
        # Verify score is within range
        assert 0 <= quality_score <= 1
    
    def test_compare_prices_with_competitors(self):
        comparison = self.analyzer.compare_prices_with_competitors(
            self.sample_data['menu_items'], 
            [comp['menu_items'] for comp in self.competitor_data]
        )
        
        # Verify comparison structure
        assert 'relative_position' in comparison
        assert 'price_difference_percentage' in comparison
        assert 'item_comparisons' in comparison
        
        # Verify relative position is one of: lower, similar, higher
        assert comparison['relative_position'] in ['lower', 'similar', 'higher', 'unknown']
        
        # Verify price difference is a number
        assert isinstance(comparison['price_difference_percentage'], (int, float))
    
    def test_analyze_sentiment(self):
        reviews = self.sample_data['reviews']
        sentiment = self.analyzer.analyze_sentiment(reviews)
        
        # Verify sentiment structure
        assert 'positive' in sentiment
        assert 'negative' in sentiment
        assert 'neutral' in sentiment
        assert 'common_positive_themes' in sentiment
        assert 'common_negative_themes' in sentiment
        
        # Verify percentages sum to approximately 100%
        total = sentiment['positive'] + sentiment['negative'] + sentiment['neutral']
        assert 99.0 <= total <= 101.0  # Allow for small rounding errors

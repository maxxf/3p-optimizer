import os
import sys
import unittest
from unittest.mock import MagicMock, patch
import tempfile
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_extraction_module import UberEatsExtractor

class TestUberEatsExtractor:
    
    def setup_method(self):
        # Create temp directory for test output
        self.test_output_dir = tempfile.mkdtemp()
        self.extractor = UberEatsExtractor(output_dir=self.test_output_dir)
    
    def teardown_method(self):
        # Clean up test files
        import shutil
        shutil.rmtree(self.test_output_dir, ignore_errors=True)
    
    @patch('data_extraction_module.requests.get')
    def test_validate_url(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test valid URL
        valid_url = "https://www.ubereats.com/store/shake-shack/123456"
        assert self.extractor.validate_url(valid_url) == True
        
        # Test invalid URLs
        assert self.extractor.validate_url(None) == False
        assert self.extractor.validate_url("") == False
        assert self.extractor.validate_url("https://www.example.com") == False
        assert self.extractor.validate_url("https://www.ubereats.com/menu") == False
        
        # Test URL with error
        mock_get.side_effect = Exception("Connection error")
        assert self.extractor.validate_url(valid_url) == False
    
    @patch('data_extraction_module.UberEatsExtractor.save_restaurant_data')
    def test_extract_restaurant_data(self, mock_save):
        # Setup mock for save_restaurant_data to avoid file system operations
        mock_save.return_value = "/tmp/test_output/test_restaurant.json"
        
        # Create a mock scraper
        mock_scraper = MagicMock()
        self.extractor.scraper = mock_scraper
        
        # Mock the validate_url method
        self.extractor.validate_url = MagicMock(return_value=True)
        
        # Mock the _extract_store_id method
        self.extractor._extract_store_id = MagicMock(return_value="123456")
        
        # Create mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        # Read sample HTML from fixture
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'sample_restaurant_page.html')
        with open(fixture_path, 'r') as f:
            mock_response.text = f.read()
        mock_scraper.get.return_value = mock_response
        
        # Test extraction
        url = "https://www.ubereats.com/store/shake-shack/123456"
        result = self.extractor.extract_restaurant_data(url)
        
        # Verify extraction results
        assert result is not None
        assert 'restaurant_info' in result
        assert 'menu_items' in result
        assert 'reviews' in result
    
    def test_save_restaurant_data(self):
        # Test data
        restaurant_data = {
            'restaurant_info': {
                'name': 'Test Restaurant',
                'rating': 4.5,
                'address': '123 Test St'
            },
            'menu_items': [
                {'name': 'Item 1', 'price': 9.99, 'description': 'Test item'}
            ],
            'reviews': [
                {'rating': 5, 'text': 'Great food!'}
            ]
        }
        
        # Test saving
        store_id = "test123"
        file_path = self.extractor.save_restaurant_data(restaurant_data, store_id)
        
        # Verify file was created
        assert os.path.exists(file_path)
        
        # Verify file contents
        with open(file_path, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data['restaurant_info']['name'] == 'Test Restaurant'
        assert len(saved_data['menu_items']) == 1
        assert len(saved_data['reviews']) == 1
    
    @patch('data_extraction_module.requests.get')
    def test_find_competitors(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {'name': 'Competitor 1', 'url': 'https://www.ubereats.com/store/competitor-1/123'},
                {'name': 'Competitor 2', 'url': 'https://www.ubereats.com/store/competitor-2/456'}
            ]
        }
        mock_get.return_value = mock_response
        
        # Test competitor finding
        restaurant_data = {
            'restaurant_info': {
                'name': 'Test Restaurant',
                'cuisine': 'Burgers',
                'location': {'latitude': 40.7128, 'longitude': -74.0060}
            }
        }
        
        # Add alias method for compatibility with tests
        self.extractor.find_competitors = self.extractor.search_competitors
        
        competitors = self.extractor.find_competitors(restaurant_data)
        
        # Verify competitors
        assert len(competitors) == 2
        assert competitors[0]['name'] == 'Competitor 1'
        assert competitors[1]['name'] == 'Competitor 2'
    
    def test_extract_from_json_file(self):
        # Create test JSON file
        test_data = {
            'restaurant_info': {
                'name': 'Test Restaurant',
                'rating': 4.5
            },
            'menu_items': [
                {'name': 'Item 1', 'price': 9.99}
            ]
        }
        
        import json
        test_file = os.path.join(self.test_output_dir, "test_restaurant.json")
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Test extraction from file
        result = self.extractor.extract_from_json_file(test_file)
        
        # Verify extraction results
        assert result is not None
        assert result['restaurant_info']['name'] == 'Test Restaurant'
        assert len(result['menu_items']) == 1

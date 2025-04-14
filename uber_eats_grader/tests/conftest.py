import os
import sys
import pytest

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules to ensure they're discovered
from tests.test_data_extraction import TestUberEatsExtractor
from tests.test_analysis_engine import TestAnalysisEngine
from tests.test_grading_system import TestGradingSystem
from tests.test_web_app import TestWebApp

# Configuration for pytest
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line("markers", "unit: mark a test as a unit test")
    config.addinivalue_line("markers", "integration: mark a test as an integration test")
    config.addinivalue_line("markers", "web: mark a test as a web interface test")

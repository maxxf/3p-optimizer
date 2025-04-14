# Uber Eats Grader

A web application that analyzes and grades restaurant delivery storefronts on Uber Eats, providing actionable insights to improve performance.

## Features

- **Data Extraction**: Scrapes Uber Eats restaurant pages to extract menu structure, pricing, and customer reviews
- **Comprehensive Analysis**: Evaluates menu structure, pricing strategy, customer sentiment, visual presentation, and promotion strategy
- **Competitive Benchmarking**: Compares restaurant performance against industry benchmarks and direct competitors
- **Actionable Recommendations**: Provides prioritized recommendations for improvement
- **Visual Reports**: Generates visualizations, PDF reports, and PowerPoint presentations
- **Training Capability**: Learns from high-performing examples to improve analysis

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/uber-eats-grader.git
   cd uber-eats-grader
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Download NLTK resources (automatically handled by the application, but can be done manually):
   ```
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('vader_lexicon')"
   ```

### Deployment to Replit

For easy deployment to Replit, follow the instructions in [REPLIT_DEPLOYMENT.md](REPLIT_DEPLOYMENT.md).

## Usage

### Running the Application

1. Start the application:
   ```
   python run.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Enter a restaurant name or paste an Uber Eats URL to begin analysis

### Command Line Options

- `--host`: Host to run the application on (default: 0.0.0.0)
- `--port`: Port to run the application on (default: 5000)
- `--debug`: Run in debug mode

Example:
```
python run.py --host 127.0.0.1 --port 8080 --debug
```

## Analysis Components

The application grades restaurants on five key components:

1. **Menu Structure**: Evaluates category organization, description quality, and item highlighting
2. **Pricing Strategy**: Analyzes price points, value options, and competitive positioning
3. **Customer Sentiment**: Examines ratings, review themes, and sentiment patterns
4. **Visual Presentation**: Assesses image quality, coverage, and visual consistency
5. **Promotion Strategy**: Evaluates promotion types, visibility, and effectiveness

## Training the System

To improve analysis accuracy, you can train the system with examples of high-performing storefronts:

1. Navigate to the "Train" section in the web interface
2. Enter URLs of high-performing restaurant storefronts
3. Add notes about what makes these examples effective
4. Submit to enhance the analysis algorithms

## Known Limitations

- Some advanced visualization features may require further refinement
- PDF report generation may have formatting limitations
- The system works best with restaurants that have a substantial number of reviews

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed for Spice agency to help restaurants optimize their delivery presence
- Uses NLTK for natural language processing of customer reviews
- Visualization components powered by Matplotlib and Seaborn

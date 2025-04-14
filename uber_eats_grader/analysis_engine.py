import os
import sys
import logging
import json
import numpy as np
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AnalysisEngine")

class AnalysisEngine:
    """
    A class for analyzing restaurant data from delivery platforms.
    """
    
    def __init__(self):
        """
        Initialize the Analysis Engine.
        """
        logger.info("Initializing Analysis Engine...")
        
        # Initialize NLTK components
        try:
            self.sid = SentimentIntensityAnalyzer()
            self.stop_words = set(stopwords.words('english'))
            logger.info("NLTK components initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing NLTK components: {e}")
            # Download required NLTK data if not available
            nltk.download('vader_lexicon')
            nltk.download('punkt')
            nltk.download('stopwords')
            self.sid = SentimentIntensityAnalyzer()
            self.stop_words = set(stopwords.words('english'))
        
        # Load benchmark data
        self.benchmarks = self._load_benchmarks()
    
    def _load_benchmarks(self):
        """
        Load benchmark data for comparison.
        
        Returns:
            dict: Benchmark data
        """
        try:
            # In a real implementation, this would load from a database or file
            # For now, we'll use hardcoded benchmark values
            return {
                'menu_structure': {
                    'avg_score': 0.75,
                    'percentiles': {
                        90: 0.90,
                        75: 0.82,
                        50: 0.75,
                        25: 0.65,
                        10: 0.55
                    }
                },
                'pricing': {
                    'avg_score': 0.70,
                    'percentiles': {
                        90: 0.85,
                        75: 0.78,
                        50: 0.70,
                        25: 0.62,
                        10: 0.55
                    }
                },
                'customer_sentiment': {
                    'avg_score': 0.80,
                    'percentiles': {
                        90: 0.92,
                        75: 0.85,
                        50: 0.80,
                        25: 0.70,
                        10: 0.60
                    }
                },
                'visual_presentation': {
                    'avg_score': 0.65,
                    'percentiles': {
                        90: 0.85,
                        75: 0.75,
                        50: 0.65,
                        25: 0.55,
                        10: 0.45
                    }
                },
                'promotion_strategy': {
                    'avg_score': 0.60,
                    'percentiles': {
                        90: 0.80,
                        75: 0.70,
                        50: 0.60,
                        25: 0.50,
                        10: 0.40
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error loading benchmarks: {e}")
            return {}
    
    def analyze_restaurant(self, restaurant_data):
        """
        Analyze restaurant data and generate comprehensive analysis.
        
        Args:
            restaurant_data (dict): Restaurant data to analyze
            
        Returns:
            dict: Analysis results
        """
        try:
            # Extract restaurant info
            restaurant_info = restaurant_data.get('restaurant_info', {})
            
            # Analyze menu structure
            menu_structure_analysis = self.analyze_menu_structure(restaurant_data)
            
            # Analyze pricing
            pricing_analysis = self.analyze_pricing(restaurant_data)
            
            # Analyze customer sentiment
            customer_sentiment_analysis = self.analyze_customer_sentiment(restaurant_data)
            
            # Analyze visual presentation
            visual_presentation_analysis = self.analyze_visual_presentation(restaurant_data)
            
            # Analyze promotion strategy
            promotion_strategy_analysis = self.analyze_promotion_strategy(restaurant_data)
            
            # Calculate overall score
            component_scores = [
                menu_structure_analysis.get('score', 0),
                pricing_analysis.get('score', 0),
                customer_sentiment_analysis.get('score', 0),
                visual_presentation_analysis.get('score', 0),
                promotion_strategy_analysis.get('score', 0)
            ]
            overall_score = sum(component_scores) / len(component_scores)
            
            # Combine all analysis results
            analysis_results = {
                'restaurant_info': restaurant_info,
                'menu_structure': menu_structure_analysis,
                'pricing': pricing_analysis,
                'customer_sentiment': customer_sentiment_analysis,
                'visual_presentation': visual_presentation_analysis,
                'promotion_strategy': promotion_strategy_analysis,
                'overall_score': overall_score
            }
            
            return analysis_results
        except Exception as e:
            logger.error(f"Error analyzing restaurant: {e}")
            return {
                'restaurant_info': restaurant_data.get('restaurant_info', {}),
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review data for completeness']
            }
    
    def analyze_menu_structure(self, restaurant_data):
        """
        Analyze menu structure, organization, and content quality.
        
        Args:
            restaurant_data (dict): Restaurant data to analyze
            
        Returns:
            dict: Menu structure analysis results
        """
        try:
            logger.info("Analyzing menu structure...")
            
            # Extract menu items and categories
            menu_items = restaurant_data.get('menu_items', [])
            categories = restaurant_data.get('categories', [])
            
            if not menu_items:
                raise ValueError("'items'")
            
            # Calculate metrics
            category_count = len(categories)
            
            # Calculate items per category
            items_by_category = {}
            for item in menu_items:
                category = item.get('category', 'Uncategorized')
                if category not in items_by_category:
                    items_by_category[category] = 0
                items_by_category[category] += 1
            
            avg_items_per_category = sum(items_by_category.values()) / len(items_by_category) if items_by_category else 0
            
            # Calculate description quality
            descriptions = [item.get('description', '') for item in menu_items if item.get('description')]
            description_quality = self.calculate_description_quality(descriptions)
            
            # Check if popular items are highlighted
            popular_items_highlighted = any(item.get('popular', False) for item in menu_items)
            
            # Calculate overall score
            score_components = [
                min(1.0, category_count / 10) * 0.3,  # More categories is better, up to 10
                min(1.0, avg_items_per_category / 5) * 0.2,  # 5 items per category is optimal
                description_quality * 0.4,  # Description quality is important
                0.1 if popular_items_highlighted else 0  # Highlighting popular items is good
            ]
            score = sum(score_components)
            
            # Identify strengths
            strengths = []
            if category_count >= 5:
                strengths.append("Well-organized menu with multiple categories")
            if description_quality >= 0.8:
                strengths.append("Detailed and appealing item descriptions")
            if popular_items_highlighted:
                strengths.append("Popular items are highlighted for easy discovery")
            if avg_items_per_category >= 3 and avg_items_per_category <= 7:
                strengths.append("Good balance of items per category")
            
            # Identify weaknesses
            weaknesses = []
            if category_count < 3:
                weaknesses.append("Limited menu organization with few categories")
            if description_quality < 0.6:
                weaknesses.append("Item descriptions could be more detailed and appealing")
            if not popular_items_highlighted:
                weaknesses.append("Popular items are not highlighted")
            if avg_items_per_category < 3:
                weaknesses.append("Some categories have too few items")
            if avg_items_per_category > 10:
                weaknesses.append("Some categories have too many items, which can overwhelm customers")
            
            # Generate recommendations
            recommendations = []
            if category_count < 5:
                recommendations.append("Add more menu categories for better organization")
            if description_quality < 0.8:
                recommendations.append("Improve item descriptions with more details about ingredients and preparation")
            if not popular_items_highlighted:
                recommendations.append("Highlight popular items to guide customer choices")
            if avg_items_per_category < 3 or avg_items_per_category > 10:
                recommendations.append("Aim for 4-7 items per category for optimal customer experience")
            
            return {
                'score': score,
                'metrics': {
                    'category_count': category_count,
                    'items_per_category': avg_items_per_category,
                    'description_quality': description_quality,
                    'popular_items_highlighted': popular_items_highlighted
                },
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error analyzing menu structure: {e}")
            return {
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review menu structure data for completeness'],
                'strengths': [],
                'weaknesses': ['Incomplete menu data']
            }
    
    def analyze_pricing(self, restaurant_data, competitor_data=None):
        """
        Analyze pricing strategy and competitiveness.
        
        Args:
            restaurant_data (dict): Restaurant data to analyze
            competitor_data (list, optional): Competitor restaurant data for comparison
            
        Returns:
            dict: Pricing analysis results
        """
        try:
            logger.info("Analyzing pricing strategy...")
            
            # Extract menu items
            menu_items = restaurant_data.get('menu_items', [])
            
            if not menu_items:
                raise ValueError("No menu items found")
            
            # Calculate average price
            prices = [item.get('price', 0) for item in menu_items]
            average_price = sum(prices) / len(prices) if prices else 0
            
            # Determine price range
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0
            price_range = max_price - min_price
            
            # Compare with competitors if available
            price_comparison = None
            if competitor_data:
                competitor_menu_items = []
                for competitor in competitor_data:
                    competitor_menu_items.extend(competitor.get('menu_items', []))
                
                price_comparison = self.compare_prices_with_competitors(menu_items, [competitor.get('menu_items', []) for competitor in competitor_data])
            
            # Check for value options
            value_options = any(item.get('price', 0) <= average_price * 0.7 for item in menu_items)
            
            # Calculate overall score
            score_components = [
                0.5,  # Base score
                0.2 if value_options else 0,  # Value options are good
                0.3 if price_comparison and price_comparison.get('relative_position') == 'similar' else 0  # Competitive pricing is good
            ]
            score = sum(score_components)
            
            # Adjust score based on price comparison if available
            if price_comparison:
                relative_position = price_comparison.get('relative_position')
                if relative_position == 'lower':
                    score += 0.1  # Slightly better to be lower priced
                elif relative_position == 'higher':
                    score -= 0.1  # Slightly worse to be higher priced
            
            # Identify strengths
            strengths = []
            if value_options:
                strengths.append("Offers good value options")
            if price_comparison and price_comparison.get('relative_position') == 'lower':
                strengths.append("More affordable than competitors")
            if price_comparison and price_comparison.get('relative_position') == 'similar':
                strengths.append("Competitively priced compared to similar restaurants")
            if max_price > average_price * 1.5:
                strengths.append("Offers premium options for upselling")
            
            # Identify weaknesses
            weaknesses = []
            if not value_options:
                weaknesses.append("Limited value options for price-conscious customers")
            if price_comparison and price_comparison.get('relative_position') == 'higher':
                weaknesses.append("Higher priced than competitors")
            if price_range < average_price * 0.5:
                weaknesses.append("Limited price range may not appeal to diverse customer base")
            
            # Generate recommendations
            recommendations = []
            if not value_options:
                recommendations.append("Add value options or combo deals to attract price-conscious customers")
            if price_comparison and price_comparison.get('relative_position') == 'higher':
                recommendations.append("Consider adjusting prices to be more competitive or emphasize quality justification")
            if price_range < average_price * 0.5:
                recommendations.append("Expand price range with both value and premium options")
            
            return {
                'score': score,
                'metrics': {
                    'average_price': average_price,
                    'price_range': f"${min_price:.2f} - ${max_price:.2f}",
                    'price_comparison': price_comparison,
                    'value_options': value_options
                },
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error analyzing pricing: {e}")
            return {
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review pricing data for completeness'],
                'strengths': [],
                'weaknesses': ['Incomplete pricing data']
            }
    
    def analyze_customer_sentiment(self, restaurant_data):
        """
        Analyze customer reviews and ratings.
        
        Args:
            restaurant_data (dict): Restaurant data to analyze
            
        Returns:
            dict: Customer sentiment analysis results
        """
        try:
            logger.info("Analyzing customer sentiment...")
            
            # Extract reviews and ratings
            reviews = restaurant_data.get('reviews', [])
            restaurant_info = restaurant_data.get('restaurant_info', {})
            
            # Get overall rating and review count
            average_rating = restaurant_info.get('rating', 0)
            review_count = restaurant_info.get('review_count', 0) or len(reviews)
            
            # Analyze sentiment in reviews
            sentiment_analysis = self.analyze_sentiment(reviews)
            
            # Calculate overall score
            score_components = [
                min(1.0, average_rating / 5) * 0.4,  # Rating score
                min(1.0, review_count / 100) * 0.2,  # More reviews is better, up to 100
                sentiment_analysis.get('positive', 0) / 100 * 0.4  # Positive sentiment percentage
            ]
            score = sum(score_components)
            
            # Identify strengths
            strengths = []
            if average_rating >= 4.5:
                strengths.append("Excellent overall rating")
            elif average_rating >= 4.0:
                strengths.append("Strong overall rating")
            if review_count >= 100:
                strengths.append("Large number of customer reviews")
            if sentiment_analysis.get('positive', 0) >= 70:
                strengths.append("Highly positive customer sentiment")
            if sentiment_analysis.get('common_positive_themes'):
                strengths.append(f"Consistently praised for: {', '.join(sentiment_analysis['common_positive_themes'][:3])}")
            
            # Identify weaknesses
            weaknesses = []
            if average_rating < 4.0:
                weaknesses.append("Below average rating")
            if review_count < 20:
                weaknesses.append("Limited number of reviews")
            if sentiment_analysis.get('negative', 0) >= 30:
                weaknesses.append("Significant negative sentiment in reviews")
            if sentiment_analysis.get('common_negative_themes'):
                weaknesses.append(f"Common complaints about: {', '.join(sentiment_analysis['common_negative_themes'][:3])}")
            
            # Generate recommendations
            recommendations = []
            if average_rating < 4.0:
                recommendations.append("Address common complaints to improve overall rating")
            if review_count < 20:
                recommendations.append("Encourage more customers to leave reviews")
            if sentiment_analysis.get('negative', 0) >= 20:
                recommendations.append("Respond to negative reviews and address recurring issues")
            if sentiment_analysis.get('common_negative_themes'):
                for theme in sentiment_analysis['common_negative_themes'][:2]:
                    recommendations.append(f"Improve {theme.lower()} based on customer feedback")
            
            return {
                'score': score,
                'metrics': {
                    'average_rating': average_rating,
                    'review_count': review_count,
                    'sentiment_analysis': {
                        'positive': sentiment_analysis.get('positive', 0),
                        'negative': sentiment_analysis.get('negative', 0),
                        'neutral': sentiment_analysis.get('neutral', 0)
                    },
                    'common_themes': {
                        'positive': sentiment_analysis.get('common_positive_themes', []),
                        'negative': sentiment_analysis.get('common_negative_themes', [])
                    }
                },
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error analyzing customer sentiment: {e}")
            return {
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review customer review data for completeness'],
                'strengths': [],
                'weaknesses': ['Incomplete review data']
            }
    
    def analyze_visual_presentation(self, restaurant_data):
        """
        Analyze visual presentation of the restaurant storefront.
        
        Args:
            restaurant_data (dict): Restaurant data to analyze
            
        Returns:
            dict: Visual presentation analysis results
        """
        try:
            logger.info("Analyzing visual presentation...")
            
            # Extract menu items
            menu_items = restaurant_data.get('menu_items', [])
            
            if not menu_items:
                raise ValueError("No menu items found")
            
            # Check for restaurant banner image
            restaurant_info = restaurant_data.get('restaurant_info', {})
            has_banner = 'banner_image' in restaurant_info
            
            if not has_banner:
                raise ValueError("'restaurant_banner'")
            
            # Calculate image coverage
            items_with_images = [item for item in menu_items if item.get('image_url')]
            image_coverage = len(items_with_images) / len(menu_items) if menu_items else 0
            
            # Estimate image quality (in a real implementation, this would use image analysis)
            # For now, we'll assume all images are of medium quality
            image_quality = 0.7
            
            # Estimate visual consistency
            visual_consistency = 0.8  # Placeholder value
            
            # Calculate overall score
            score_components = [
                0.2 if has_banner else 0,  # Having a banner is good
                image_coverage * 0.4,  # Image coverage is important
                image_quality * 0.2,  # Image quality matters
                visual_consistency * 0.2  # Consistency is good
            ]
            score = sum(score_components)
            
            # Identify strengths
            strengths = []
            if has_banner:
                strengths.append("Effective restaurant banner image")
            if image_coverage >= 0.8:
                strengths.append("Excellent image coverage for menu items")
            elif image_coverage >= 0.5:
                strengths.append("Good image coverage for menu items")
            if image_quality >= 0.8:
                strengths.append("High-quality food photography")
            if visual_consistency >= 0.8:
                strengths.append("Consistent visual style across images")
            
            # Identify weaknesses
            weaknesses = []
            if not has_banner:
                weaknesses.append("Missing restaurant banner image")
            if image_coverage < 0.5:
                weaknesses.append("Limited image coverage for menu items")
            if image_quality < 0.6:
                weaknesses.append("Image quality could be improved")
            if visual_consistency < 0.6:
                weaknesses.append("Inconsistent visual style across images")
            
            # Generate recommendations
            recommendations = []
            if not has_banner:
                recommendations.append("Add an appealing restaurant banner image")
            if image_coverage < 0.8:
                recommendations.append(f"Add images for more menu items (currently at {image_coverage*100:.0f}%)")
            if image_quality < 0.8:
                recommendations.append("Improve image quality with professional food photography")
            if visual_consistency < 0.8:
                recommendations.append("Maintain consistent visual style across all images")
            
            return {
                'score': score,
                'metrics': {
                    'image_coverage': image_coverage,
                    'image_quality': image_quality,
                    'visual_consistency': visual_consistency
                },
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error analyzing visual presentation: {e}")
            return {
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review visual elements for completeness'],
                'strengths': [],
                'weaknesses': ['Incomplete visual data']
            }
    
    def analyze_promotion_strategy(self, restaurant_data):
        """
        Analyze promotion strategy and effectiveness.
        
        Args:
            restaurant_data (dict): Restaurant data to analyze
            
        Returns:
            dict: Promotion strategy analysis results
        """
        try:
            logger.info("Analyzing promotion strategy...")
            
            # Extract promotions
            promotions = restaurant_data.get('promotions', [])
            
            # Count active promotions
            active_promotions = [p for p in promotions if p.get('active', True)]
            active_count = len(active_promotions)
            
            # Identify promotion types
            promotion_types = list(set(p.get('type', 'unknown') for p in active_promotions))
            
            # Estimate promotion visibility (in a real implementation, this would be based on UI analysis)
            # For now, we'll use a placeholder value
            promotion_visibility = 0.7 if active_count > 0 else 0
            
            # Calculate overall score
            score_components = [
                min(1.0, active_count / 3) * 0.4,  # More promotions is better, up to 3
                min(1.0, len(promotion_types) / 2) * 0.3,  # More variety is better, up to 2 types
                promotion_visibility * 0.3  # Visibility is important
            ]
            score = sum(score_components)
            
            # Identify strengths
            strengths = []
            if active_count >= 2:
                strengths.append("Multiple active promotions")
            if len(promotion_types) >= 2:
                strengths.append("Good variety of promotion types")
            if promotion_visibility >= 0.8:
                strengths.append("Promotions are highly visible")
            if 'discount' in promotion_types:
                strengths.append("Offers price discounts to attract customers")
            if 'free_delivery' in promotion_types:
                strengths.append("Free delivery promotion reduces barrier to purchase")
            
            # Identify weaknesses
            weaknesses = []
            if active_count == 0:
                weaknesses.append("No active promotions")
            elif active_count < 2:
                weaknesses.append("Limited number of promotions")
            if len(promotion_types) < 2:
                weaknesses.append("Limited variety of promotion types")
            if promotion_visibility < 0.6:
                weaknesses.append("Promotions have low visibility")
            
            # Generate recommendations
            recommendations = []
            if active_count < 2:
                recommendations.append("Add more promotions to attract customers")
            if len(promotion_types) < 2:
                recommendations.append("Diversify promotion types (e.g., discounts, free delivery, BOGO)")
            if promotion_visibility < 0.8:
                recommendations.append("Increase promotion visibility on the storefront")
            if 'limited_time' not in promotion_types:
                recommendations.append("Add limited-time offers to create urgency")
            
            return {
                'score': score,
                'metrics': {
                    'active_promotions': active_count,
                    'promotion_types': promotion_types,
                    'promotion_visibility': promotion_visibility
                },
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error analyzing promotion strategy: {e}")
            return {
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review promotion data for completeness'],
                'strengths': [],
                'weaknesses': ['Incomplete promotion data']
            }
    
    def calculate_description_quality(self, descriptions):
        """
        Calculate the quality of menu item descriptions.
        
        Args:
            descriptions (list): List of item descriptions
            
        Returns:
            float: Description quality score (0-1)
        """
        try:
            if not descriptions:
                return 0
            
            # Calculate average length
            avg_length = sum(len(d) for d in descriptions) / len(descriptions)
            
            # Calculate keyword richness
            food_keywords = ['fresh', 'homemade', 'delicious', 'signature', 'special', 'organic', 'local', 'premium', 'authentic']
            keyword_counts = []
            
            for desc in descriptions:
                words = word_tokenize(desc.lower())
                keyword_count = sum(1 for word in words if word in food_keywords)
                keyword_counts.append(keyword_count)
            
            avg_keywords = sum(keyword_counts) / len(keyword_counts) if keyword_counts else 0
            
            # Calculate scores
            length_score = min(1.0, avg_length / 100)  # 100 characters is optimal
            keyword_score = min(1.0, avg_keywords / 3)  # 3 keywords is optimal
            
            # Combine scores
            quality_score = length_score * 0.7 + keyword_score * 0.3
            
            return quality_score
        except Exception as e:
            logger.error(f"Error calculating description quality: {e}")
            return 0.5  # Default to medium quality
    
    def compare_prices_with_competitors(self, menu_items, competitor_menu_items_list):
        """
        Compare prices with competitors.
        
        Args:
            menu_items (list): Restaurant menu items
            competitor_menu_items_list (list): List of competitor menu items lists
            
        Returns:
            dict: Price comparison results
        """
        try:
            if not menu_items or not competitor_menu_items_list:
                return {
                    'relative_position': 'unknown',
                    'price_difference_percentage': 0,
                    'item_comparisons': []
                }
            
            # Calculate average price for restaurant
            restaurant_prices = [item.get('price', 0) for item in menu_items]
            restaurant_avg_price = sum(restaurant_prices) / len(restaurant_prices) if restaurant_prices else 0
            
            # Calculate average prices for competitors
            competitor_avg_prices = []
            for competitor_items in competitor_menu_items_list:
                prices = [item.get('price', 0) for item in competitor_items]
                if prices:
                    competitor_avg_prices.append(sum(prices) / len(prices))
            
            # Calculate overall competitor average
            competitor_overall_avg = sum(competitor_avg_prices) / len(competitor_avg_prices) if competitor_avg_prices else 0
            
            # Calculate price difference
            if competitor_overall_avg > 0:
                price_difference_percentage = (restaurant_avg_price - competitor_overall_avg) / competitor_overall_avg * 100
            else:
                price_difference_percentage = 0
            
            # Determine relative position
            if abs(price_difference_percentage) <= 10:
                relative_position = 'similar'
            elif price_difference_percentage < -10:
                relative_position = 'lower'
            else:
                relative_position = 'higher'
            
            # Compare similar items (simplified for now)
            item_comparisons = []
            
            return {
                'relative_position': relative_position,
                'price_difference_percentage': price_difference_percentage,
                'item_comparisons': item_comparisons
            }
        except Exception as e:
            logger.error(f"Error comparing prices: {e}")
            return {
                'relative_position': 'unknown',
                'price_difference_percentage': 0,
                'item_comparisons': []
            }
    
    def analyze_sentiment(self, reviews):
        """
        Analyze sentiment in customer reviews.
        
        Args:
            reviews (list): Customer reviews
            
        Returns:
            dict: Sentiment analysis results
        """
        try:
            if not reviews:
                return {
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0,
                    'common_positive_themes': [],
                    'common_negative_themes': []
                }
            
            # Analyze sentiment scores
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            # Collect words for theme analysis
            positive_words = []
            negative_words = []
            
            for review in reviews:
                text = review.get('text', '')
                if not text:
                    continue
                
                # Get sentiment score
                sentiment_score = self.sid.polarity_scores(text)
                compound = sentiment_score['compound']
                
                # Classify sentiment
                if compound >= 0.05:
                    positive_count += 1
                    # Extract key positive words
                    words = [w.lower() for w in word_tokenize(text) if w.isalpha() and w.lower() not in self.stop_words]
                    positive_words.extend(words)
                elif compound <= -0.05:
                    negative_count += 1
                    # Extract key negative words
                    words = [w.lower() for w in word_tokenize(text) if w.isalpha() and w.lower() not in self.stop_words]
                    negative_words.extend(words)
                else:
                    neutral_count += 1
            
            # Calculate percentages
            total_reviews = positive_count + negative_count + neutral_count
            positive_percent = (positive_count / total_reviews * 100) if total_reviews > 0 else 0
            negative_percent = (negative_count / total_reviews * 100) if total_reviews > 0 else 0
            neutral_percent = (neutral_count / total_reviews * 100) if total_reviews > 0 else 0
            
            # Extract common themes (simplified)
            food_related = ['food', 'delicious', 'taste', 'flavor', 'fresh', 'quality']
            service_related = ['service', 'staff', 'friendly', 'quick', 'slow', 'rude']
            delivery_related = ['delivery', 'time', 'late', 'fast', 'packaging', 'cold', 'hot']
            
            # Count theme occurrences
            positive_themes = {
                'Food Quality': sum(1 for word in positive_words if word in food_related),
                'Service': sum(1 for word in positive_words if word in service_related),
                'Delivery': sum(1 for word in positive_words if word in delivery_related)
            }
            
            negative_themes = {
                'Food Quality': sum(1 for word in negative_words if word in food_related),
                'Service': sum(1 for word in negative_words if word in service_related),
                'Delivery': sum(1 for word in negative_words if word in delivery_related)
            }
            
            # Sort themes by frequency
            common_positive_themes = sorted(positive_themes.items(), key=lambda x: x[1], reverse=True)
            common_negative_themes = sorted(negative_themes.items(), key=lambda x: x[1], reverse=True)
            
            # Extract theme names
            common_positive_themes = [theme for theme, count in common_positive_themes if count > 0]
            common_negative_themes = [theme for theme, count in common_negative_themes if count > 0]
            
            return {
                'positive': positive_percent,
                'negative': negative_percent,
                'neutral': neutral_percent,
                'common_positive_themes': common_positive_themes,
                'common_negative_themes': common_negative_themes
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'error': str(e),
                'grade': 'F',
                'recommendations': ['Review sentiment data for completeness'],
                'strengths': [],
                'weaknesses': ['Incomplete sentiment data']
            }

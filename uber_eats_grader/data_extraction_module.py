import os
import sys
import json
import logging
import requests
import cloudscraper
import re
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UberEatsExtractor")

class UberEatsExtractor:
    """
    A class for extracting restaurant data from Uber Eats.
    """
    
    def __init__(self, output_dir="/tmp/uber_eats_data"):
        """
        Initialize the Uber Eats data extractor.
        
        Args:
            output_dir (str): Directory to save extracted data
        """
        logger.info("Initializing Uber Eats data extractor...")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
    
    def validate_url(self, url):
        """
        Validate if the URL is a valid Uber Eats restaurant URL.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not url:
            return False
            
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return False
                
            # Check if it's an Uber Eats URL
            if "ubereats.com" not in parsed_url.netloc:
                return False
                
            # Check if it's a store URL
            if "/store/" not in parsed_url.path:
                return False
                
            # Check if the URL is accessible
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error validating URL: {e}")
            return False
    
    def extract_restaurant_data(self, url):
        """
        Extract restaurant data from Uber Eats URL.
        
        Args:
            url (str): Uber Eats restaurant URL
            
        Returns:
            dict: Extracted restaurant data
        """
        logger.info(f"Extracting data from URL: {url}")
        
        try:
            # Validate URL
            if not self.validate_url(url):
                logger.error(f"Invalid URL: {url}")
                return None
            
            # Extract store ID from URL
            store_id = self._extract_store_id(url)
            if not store_id:
                logger.error("Could not extract store ID from URL")
                return None
            
            # Get page content
            response = self.scraper.get(url)
            if response.status_code != 200:
                logger.error(f"Failed to fetch page: {response.status_code}")
                return None
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract restaurant info
            restaurant_info = self._extract_restaurant_info(soup)
            
            # Extract menu items
            menu_items = self._extract_menu_items(soup)
            
            # Extract reviews
            reviews = self._extract_reviews(soup)
            
            # Extract categories
            categories = self._extract_categories(soup)
            
            # Extract promotions
            promotions = self._extract_promotions(soup)
            
            # Combine all data
            restaurant_data = {
                'restaurant_info': restaurant_info,
                'menu_items': menu_items,
                'reviews': reviews,
                'categories': categories,
                'promotions': promotions
            }
            
            # Save data to file
            file_path = self.save_restaurant_data(restaurant_data, store_id)
            logger.info(f"Data saved to {file_path}")
            
            return restaurant_data
            
        except Exception as e:
            logger.error(f"Error extracting restaurant data: {e}")
            return None
    
    def _extract_store_id(self, url):
        """
        Extract store ID from Uber Eats URL.
        
        Args:
            url (str): Uber Eats restaurant URL
            
        Returns:
            str: Store ID
        """
        try:
            # Extract store ID from URL path
            match = re.search(r'/store/[^/]+/([^/?]+)', url)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            logger.error(f"Error extracting store ID: {e}")
            return None
    
    def _extract_restaurant_info(self, soup):
        """
        Extract restaurant information from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            dict: Restaurant information
        """
        try:
            # Extract restaurant name
            name_elem = soup.find('h1')
            name = name_elem.text.strip() if name_elem else "Unknown Restaurant"
            
            # Extract rating
            rating_elem = soup.select_one('.rating-value, [data-testid="rating-value"]')
            rating = float(rating_elem.text.strip()) if rating_elem else None
            
            # Extract review count
            review_count_elem = soup.select_one('.review-count, [data-testid="review-count"]')
            review_count_text = review_count_elem.text.strip() if review_count_elem else "0"
            review_count = int(re.search(r'\d+', review_count_text).group()) if re.search(r'\d+', review_count_text) else 0
            
            # Extract price range
            price_elem = soup.select_one('.price-range, [data-testid="price-range"]')
            price_range = price_elem.text.strip() if price_elem else None
            
            # Extract cuisine
            cuisine_elem = soup.select_one('.cuisine, [data-testid="cuisine"]')
            cuisine = cuisine_elem.text.strip() if cuisine_elem else None
            
            # Extract address
            address_elem = soup.select_one('.address, [data-testid="address"]')
            address = address_elem.text.strip() if address_elem else None
            
            # Extract delivery time
            delivery_time_elem = soup.select_one('.delivery-time, [data-testid="delivery-time"]')
            delivery_time = delivery_time_elem.text.strip() if delivery_time_elem else None
            
            # Extract delivery fee
            delivery_fee_elem = soup.select_one('.delivery-fee, [data-testid="delivery-fee"]')
            delivery_fee_text = delivery_fee_elem.text.strip() if delivery_fee_elem else "0"
            delivery_fee = float(re.search(r'\d+\.\d+', delivery_fee_text).group()) if re.search(r'\d+\.\d+', delivery_fee_text) else 0
            
            return {
                'name': name,
                'rating': rating,
                'review_count': review_count,
                'price_range': price_range,
                'cuisine': cuisine,
                'address': address,
                'delivery_time': delivery_time,
                'delivery_fee': delivery_fee
            }
        except Exception as e:
            logger.error(f"Error extracting restaurant info: {e}")
            return {'name': "Unknown Restaurant"}
    
    def _extract_menu_items(self, soup):
        """
        Extract menu items from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            list: Menu items
        """
        try:
            menu_items = []
            
            # Find all menu item elements
            item_elements = soup.select('.menu-item, [data-testid="menu-item"]')
            
            for item_elem in item_elements:
                # Extract item name
                name_elem = item_elem.select_one('.item-name, [data-testid="item-name"]')
                name = name_elem.text.strip() if name_elem else "Unknown Item"
                
                # Extract price
                price_elem = item_elem.select_one('.item-price, [data-testid="item-price"]')
                price_text = price_elem.text.strip() if price_elem else "0"
                price = float(re.search(r'\d+\.\d+', price_text).group()) if re.search(r'\d+\.\d+', price_text) else 0
                
                # Extract description
                desc_elem = item_elem.select_one('.item-description, [data-testid="item-description"]')
                description = desc_elem.text.strip() if desc_elem else None
                
                # Extract image URL
                img_elem = item_elem.select_one('img')
                image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else None
                
                # Extract category
                category_elem = item_elem.find_previous('h2')
                category = category_elem.text.strip() if category_elem else "Uncategorized"
                
                # Check if item is popular
                popular_badge = item_elem.select_one('.popular-badge, [data-testid="popular-badge"]')
                popular = popular_badge is not None
                
                menu_items.append({
                    'name': name,
                    'price': price,
                    'description': description,
                    'image_url': image_url,
                    'category': category,
                    'popular': popular
                })
            
            return menu_items
        except Exception as e:
            logger.error(f"Error extracting menu items: {e}")
            return []
    
    def _extract_reviews(self, soup):
        """
        Extract customer reviews from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            list: Customer reviews
        """
        try:
            reviews = []
            
            # Find all review elements
            review_elements = soup.select('.review, [data-testid="review"]')
            
            for review_elem in review_elements:
                # Extract reviewer name
                reviewer_elem = review_elem.select_one('.reviewer-name, [data-testid="reviewer-name"]')
                reviewer = reviewer_elem.text.strip() if reviewer_elem else "Anonymous"
                
                # Extract review date
                date_elem = review_elem.select_one('.review-date, [data-testid="review-date"]')
                date_text = date_elem.text.strip() if date_elem else None
                date = self._parse_review_date(date_text) if date_text else datetime.now().strftime('%Y-%m-%d')
                
                # Extract rating
                rating_elem = review_elem.select_one('.review-rating, [data-testid="review-rating"]')
                rating_text = rating_elem.text.strip() if rating_elem else "0"
                rating = int(re.search(r'\d+', rating_text).group()) if re.search(r'\d+', rating_text) else 0
                
                # Extract review text
                text_elem = review_elem.select_one('.review-text, [data-testid="review-text"]')
                text = text_elem.text.strip() if text_elem else None
                
                reviews.append({
                    'reviewer': reviewer,
                    'date': date,
                    'rating': rating,
                    'text': text
                })
            
            return reviews
        except Exception as e:
            logger.error(f"Error extracting reviews: {e}")
            return []
    
    def _parse_review_date(self, date_text):
        """
        Parse review date text into standard format.
        
        Args:
            date_text (str): Date text from review
            
        Returns:
            str: Formatted date (YYYY-MM-DD)
        """
        try:
            # Handle various date formats
            if 'today' in date_text.lower():
                return datetime.now().strftime('%Y-%m-%d')
            elif 'yesterday' in date_text.lower():
                yesterday = datetime.now() - timedelta(days=1)
                return yesterday.strftime('%Y-%m-%d')
            else:
                # Try to parse with various formats
                for fmt in ['%b %d, %Y', '%B %d, %Y', '%m/%d/%Y']:
                    try:
                        dt = datetime.strptime(date_text, fmt)
                        return dt.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            
            # Default to current date if parsing fails
            return datetime.now().strftime('%Y-%m-%d')
        except Exception as e:
            logger.error(f"Error parsing review date: {e}")
            return datetime.now().strftime('%Y-%m-%d')
    
    def _extract_categories(self, soup):
        """
        Extract menu categories from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            list: Menu categories
        """
        try:
            categories = []
            
            # Find all category elements
            category_elements = soup.select('.category-title, h2[data-testid="category-title"]')
            
            for category_elem in category_elements:
                category = category_elem.text.strip()
                if category:
                    categories.append(category)
            
            return categories
        except Exception as e:
            logger.error(f"Error extracting categories: {e}")
            return []
    
    def _extract_promotions(self, soup):
        """
        Extract promotions from BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            
        Returns:
            list: Promotions
        """
        try:
            promotions = []
            
            # Find all promotion elements
            promo_elements = soup.select('.promotion, [data-testid="promotion"]')
            
            for promo_elem in promo_elements:
                # Extract promotion title
                title_elem = promo_elem.select_one('.promotion-title, [data-testid="promotion-title"]')
                title = title_elem.text.strip() if title_elem else None
                
                # Extract promotion description
                desc_elem = promo_elem.select_one('.promotion-description, [data-testid="promotion-description"]')
                description = desc_elem.text.strip() if desc_elem else None
                
                # Extract promotion code
                code_elem = promo_elem.select_one('.promotion-code, [data-testid="promotion-code"]')
                code = code_elem.text.strip() if code_elem else None
                
                # Determine promotion type
                promo_type = 'unknown'
                if title:
                    if 'discount' in title.lower() or '%' in title or 'off' in title.lower():
                        promo_type = 'discount'
                    elif 'free delivery' in title.lower():
                        promo_type = 'free_delivery'
                    elif 'buy' in title.lower() and 'get' in title.lower():
                        promo_type = 'bogo'
                
                promotions.append({
                    'type': promo_type,
                    'description': description or title,
                    'code': code,
                    'active': True
                })
            
            return promotions
        except Exception as e:
            logger.error(f"Error extracting promotions: {e}")
            return []
    
    def save_restaurant_data(self, restaurant_data, store_id):
        """
        Save restaurant data to JSON file.
        
        Args:
            restaurant_data (dict): Restaurant data to save
            store_id (str): Store ID for filename
            
        Returns:
            str: Path to saved file
        """
        try:
            # Create filename based on restaurant name and store ID
            restaurant_name = restaurant_data['restaurant_info']['name']
            safe_name = re.sub(r'[^\w\-_]', '_', restaurant_name)
            filename = f"{safe_name}_{store_id}.json"
            file_path = os.path.join(self.output_dir, filename)
            
            # Save data to file
            with open(file_path, 'w') as f:
                json.dump(restaurant_data, f, indent=2)
            
            return file_path
        except Exception as e:
            logger.error(f"Error saving restaurant data: {e}")
            return None
    
    def search_competitors(self, restaurant_data):
        """
        Find competitor restaurants based on cuisine and location.
        
        Args:
            restaurant_data (dict): Restaurant data
            
        Returns:
            list: Competitor restaurants
        """
        try:
            # Extract restaurant info
            restaurant_info = restaurant_data['restaurant_info']
            cuisine = restaurant_info.get('cuisine')
            
            # If no cuisine or location, return empty list
            if not cuisine:
                logger.warning("Missing cuisine or location information")
                return []
            
            # Construct search query
            query = f"{cuisine} restaurants"
            if 'address' in restaurant_info and restaurant_info['address']:
                # Extract city from address
                address = restaurant_info['address']
                city_match = re.search(r'([^,]+),\s*([^,]+)$', address)
                if city_match:
                    city = city_match.group(1).strip()
                    query += f" in {city}"
            
            # Make API request to search for competitors
            url = "https://www.ubereats.com/api/search"
            params = {
                "query": query,
                "limit": 10
            }
            
            response = requests.get(url, params=params)
            if response.status_code != 200:
                logger.error(f"Failed to search competitors: {response.status_code}")
                return []
            
            # Parse response
            data = response.json()
            results = data.get('results', [])
            
            # Filter out the original restaurant
            competitors = [r for r in results if r.get('name') != restaurant_info.get('name')]
            
            return competitors[:5]  # Return top 5 competitors
        except Exception as e:
            logger.error(f"Error finding competitors: {e}")
            return []
    
    def extract_from_json_file(self, file_path):
        """
        Extract restaurant data from JSON file.
        
        Args:
            file_path (str): Path to JSON file
            
        Returns:
            dict: Restaurant data
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"Error extracting from JSON file: {e}")
            return None

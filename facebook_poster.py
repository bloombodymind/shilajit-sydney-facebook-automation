import os
import json
import requests
from datetime import datetime
import pytz
import sys

class FacebookPoster:
    def __init__(self):
        self.page_id = os.environ.get('FACEBOOK_PAGE_ID')
        self.access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        self.base_url = f"https://graph.facebook.com/v18.0/{self.page_id}"
        
        # Validate required environment variables
        if not self.page_id:
            raise ValueError("FACEBOOK_PAGE_ID environment variable is not set")
        if not self.access_token:
            raise ValueError("FACEBOOK_ACCESS_TOKEN environment variable is not set")
    
    def validate_token(self):
        """Validate the access token and check expiry"""
        print("\nValidating access token...")
        url = "https://graph.facebook.com/v18.0/debug_token"
        params = {
            'input_token': self.access_token,
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json().get('data', {})
                is_valid = data.get('is_valid', False)
                expires_at = data.get('expires_at', 0)
                
                if not is_valid:
                    print("⚠️  WARNING: Access token is INVALID!")
                    print("\n" + "="*60)
                    print("TOKEN EXPIRED - ACTION REQUIRED")
                    print("="*60)
                    print("Your Facebook access token has expired.")
                    print("Please follow the instructions in README.md to generate")
                    print("a new permanent Page Access Token.")
                    print("="*60)
                    return False
                
                # Check if token expires (0 means never expires)
                if expires_at == 0:
                    print("✓ Token is valid and NEVER expires (Permanent Page Token)")
                else:
                    expiry_date = datetime.fromtimestamp(expires_at)
                    days_until_expiry = (expiry_date - datetime.now()).days
                    print(f"✓ Token is valid until: {expiry_date}")
                    print(f"  Days remaining: {days_until_expiry}")
                    
                    if days_until_expiry < 7:
                        print(f"\n⚠️  WARNING: Token expires in {days_until_expiry} days!")
                        print("   Please generate a new permanent token soon.")
                
                return True
            else:
                print(f"✗ Failed to validate token: {response.text}")
                return False
        except Exception as e:
            print(f"✗ Error validating token: {str(e)}")
            return False
    
    def load_posts(self):
        """Load posts from JSON file"""
        with open('posts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def get_today_post(self, posts):
        """Get post for today based on day number (1-30)"""
        sydney_tz = pytz.timezone('Australia/Sydney')
        today = datetime.now(sydney_tz)
        day_of_month = today.day
        
        # Cycle through posts if day > 30
        post_index = (day_of_month - 1) % len(posts)
        return posts[post_index]
    
    def post_immediately(self, message):
        """Post immediately to Facebook page"""
        url = f"{self.base_url}/feed"
        
        params = {
            'message': message,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code != 200:
            error_data = response.json()
            error_message = error_data.get('error', {}).get('message', 'Unknown error')
            
            # Check if it's a token expiration error
            if 'expired' in error_message.lower() or 'session' in error_message.lower():
                print("\n" + "="*60)
                print("TOKEN EXPIRED - ACTION REQUIRED")
                print("="*60)
                print("Your Facebook access token has expired.")
                print("\nError details:")
                print(f"{error_message}")
                print("\nTo fix this issue:")
                print("1. Follow the instructions in README.md")
                print("2. Generate a new PERMANENT Page Access Token")
                print("3. Update the FACEBOOK_ACCESS_TOKEN secret in GitHub")
                print("="*60)
            
            raise Exception(f"API Error: {response.text}")
        
        return response.json()
    
    def run(self):
        """Main execution method"""
        print("="*60)
        print("Facebook Auto-Poster for Shilajit Sydney")
        print("="*60)
        
        # Validate token first
        if not self.validate_token():
            print("\n✗ Token validation failed. Exiting.")
            sys.exit(1)
        
        # Load posts
        posts = self.load_posts()
        print(f"\nLoaded {len(posts)} posts from posts.json")
        
        # Get today's post
        today_post = self.get_today_post(posts)
        print(f"\nToday's post (Day {today_post['day']}):")
        print(f"Message: {today_post['message'][:100]}...")
        
        # Post immediately
        print("\n--- Posting to Facebook now ---")
        try:
            result = self.post_immediately(today_post['message'])
            print(f"✓ Successfully posted! Post ID: {result.get('id')}")
        except Exception as e:
            print(f"✗ Failed to post: {str(e)}")
            raise
        
        print("\n" + "="*60)
        print("Automation completed successfully!")
        print("="*60)

if __name__ == "__main__":
    poster = FacebookPoster()
    poster.run()

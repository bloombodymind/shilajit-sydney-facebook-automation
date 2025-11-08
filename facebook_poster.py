import os
import json
import requests
from datetime import datetime
import pytz

class FacebookPoster:
    def __init__(self):
        self.page_id = os.environ.get('FACEBOOK_PAGE_ID')
        self.access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        self.base_url = f"https://graph.facebook.com/v18.0/{self.page_id}"
    
    def load_posts(self):
        """Load posts from JSON file"""
        with open('posts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['posts']
    
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
            raise Exception(f"API Error: {response.text}")
        
        return response.json()
    
    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("Facebook Auto-Poster for Shilajit Sydney")
        print("=" * 60)
        
        # Load posts
        posts = self.load_posts()
        print(f"Loaded {len(posts)} posts from posts.json")
        
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
        
        print("\n" + "=" * 60)
        print("Automation completed successfully!")
        print("=" * 60)

if __name__ == "__main__":
    poster = FacebookPoster()
    poster.run()

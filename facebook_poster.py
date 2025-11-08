import os
import json
import requests
from datetime import datetime, timedelta
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
    
    def schedule_posts(self, posts):
        """Schedule next 30 days of posts"""
        sydney_tz = pytz.timezone('Australia/Sydney')
        now = datetime.now(sydney_tz)
        
        scheduled_count = 0
        
        for i in range(30):
            post_date = now + timedelta(days=i+1)
            post_time = post_date.replace(hour=9, minute=0, second=0, microsecond=0)
            scheduled_time = int(post_time.timestamp())
            
            post_index = ((post_date.day - 1) % len(posts))
            post = posts[post_index]
            
            try:
                self.create_scheduled_post(post['text'], scheduled_time)
                scheduled_count += 1
                print(f"✓ Scheduled post for {post_time.strftime('%Y-%m-%d %H:%M %Z')}")
            except Exception as e:
                print(f"✗ Failed to schedule post for {post_time.strftime('%Y-%m-%d')}: {str(e)}")
        
        return scheduled_count
    
    def create_scheduled_post(self, message, scheduled_time):
        """Create a scheduled post on Facebook"""
        url = f"{self.base_url}/feed"
        
        params = {
            'message': message,
            'published': 'false',
            'scheduled_publish_time': scheduled_time,
            'access_token': self.access_token
        }
        
        response = requests.post(url, data=params)
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
        
        return response.json()
    
    def get_scheduled_posts(self):
        """Get all scheduled posts"""
        url = f"{self.base_url}/scheduled_posts"
        params = {'access_token': self.access_token}
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    
    def delete_all_scheduled_posts(self):
        """Delete all existing scheduled posts"""
        scheduled_posts = self.get_scheduled_posts()
        deleted_count = 0
        
        for post in scheduled_posts:
            try:
                url = f"https://graph.facebook.com/v18.0/{post['id']}"
                params = {'access_token': self.access_token}
                response = requests.delete(url, params=params)
                
                if response.status_code == 200:
                    deleted_count += 1
                    print(f"✓ Deleted scheduled post: {post['id']}")
            except Exception as e:
                print(f"✗ Failed to delete post {post['id']}: {str(e)}")
        
        return deleted_count
    
    def run(self):
        """Main execution method"""
        print("=" * 60)
        print("Facebook Auto-Poster for Shilajit Sydney")
        print("=" * 60)
        
        # Load posts
        posts = self.load_posts()
        print(f"Loaded {len(posts)} posts from posts.json")
        
        # Delete existing scheduled posts
        print("\n--- Clearing existing scheduled posts ---")
        deleted = self.delete_all_scheduled_posts()
        print(f"Deleted {deleted} existing scheduled posts")
        
        # Schedule new posts
        print("\n--- Scheduling new posts ---")
        scheduled = self.schedule_posts(posts)
        print(f"\nScheduled {scheduled} posts for the next 30 days")
        
        # Get today's post info
        today_post = self.get_today_post(posts)
        print(f"\n--- Today's Post Preview ---")
        print(f"Text: {today_post['text'][:100]}...")
        
        print("\n" + "=" * 60)
        print("✓ Automation run completed successfully!")
        print("=" * 60)

if __name__ == "__main__":
    poster = FacebookPoster()
    poster.run()

import logging
import requests
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
import schedule
import time
import os
import sys
from io import BytesIO
from dotenv import load_dotenv

# Enhanced logging configuration
logging.basicConfig(
    level=logging.DEBUG,  # More verbose logging
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

class InstagramPoster:
    def _init_(self):
        load_dotenv('details.env')
        self.client = self._init_instagram_client()
        self._verify_credentials()

    def _init_instagram_client(self):
        """Initialize Instagram client with proper settings"""
        client = Client()
        # Configure to mimic real browser behavior
        client.delay_range = [1, 3]
        client.max_retries = 3
        client.request_timeout = 30
        return client

    def _verify_credentials(self):
        """Verify all required credentials exist"""
        required = {
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
            'INSTA_USERNAME': os.getenv('INSTA_USERNAME'),
            'INSTA_PASSWORD': os.getenv('INSTA_PASSWORD')
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing credentials: {', '.join(missing)}")

    def generate_image(self, prompt):
        """Generate image using DALL-E API with enhanced debugging"""
        try:
            logger.debug(f"Generating image with prompt: {prompt}")
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024",
                    "response_format": "url"
                },
                timeout=30
            )
            response.raise_for_status()
            image_url = response.json()['data'][0]['url']
            logger.debug(f"Image generated successfully at {image_url}")
            return self._process_image(image_url)
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            if hasattr(e, 'response'):
                logger.debug(f"API Response: {e.response.text}")
            raise

    def _process_image(self, image_url):
        """Download and prepare image for Instagram"""
        try:
            response = requests.get(image_url, stream=True, timeout=30)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create Instagram-compatible square image
            img = self._resize_image(img)
            img = self._add_watermark(img)
            
            output_path = 'instagram_ready.jpg'
            img.save(output_path, quality=95, optimize=True)
            logger.debug(f"Image processed and saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Image processing failed: {str(e)}")
            raise

    def _resize_image(self, img):
        """Resize image to Instagram dimensions"""
        target_size = (1080, 1080)
        img.thumbnail(target_size, Image.LANCZOS)
        
        # Center the image on a square canvas
        new_img = Image.new('RGB', target_size, (255, 255, 255))
        offset = ((target_size[0] - img.width) // 2, (target_size[1] - img.height) // 2)
        new_img.paste(img, offset)
        return new_img

    def _add_watermark(self, img):
        """Add watermark to image"""
        try:
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                font = ImageFont.load_default()
            
            watermark = "@YourBrand"
            text_width = font.getlength(watermark)
            
            # Position at bottom right
            x = img.width - text_width - 20
            y = img.height - 60
            
            # Add background for better visibility
            draw.rectangle(
                [x-10, y-10, x+text_width+10, y+50],
                fill=(0, 0, 0, 128)
            )
            draw.text((x, y), watermark, font=font, fill="white")
            return img
        except Exception as e:
            logger.warning(f"Watermarking failed: {str(e)}")
            return img

    def post_to_instagram(self, image_path, caption):
        """Post image to Instagram with detailed debugging"""
        try:
            logger.debug("Attempting Instagram login...")
            login_result = self.client.login(
                os.getenv('INSTA_USERNAME'),
                os.getenv('INSTA_PASSWORD')
            )
            
            if not login_result:
                raise ConnectionError("Login failed - check credentials")
            
            logger.debug("Uploading media...")
            result = self.client.photo_upload(
                image_path,
                caption=caption,
                extra_data={
                    "custom_accessibility_caption": "AI-generated content",
                    "like_and_view_counts_disabled": False,
                    "disable_comments": False,
                }
            )
            
            logger.info(f"Successfully posted! Media ID: {result.id}")
            logger.debug(f"Full response: {result}")
            return True
        except Exception as e:
            logger.error(f"Instagram posting failed: {str(e)}")
            logger.debug("Client settings:", self.client.get_settings())
            raise

def main():
    print("\n=== Instagram AI Poster ===\n")
    
    try:
        poster = InstagramPoster()
        
        # Get user input
        prompt = input("Image description: ").strip()
        caption = input("Instagram caption: ").strip()
        schedule_time = input("Post time (HH:MM or 'now'): ").strip().lower()
        
        def post_job():
            try:
                image_path = poster.generate_image(prompt)
                poster.post_to_instagram(image_path, caption)
            except Exception as e:
                logger.error(f"Posting job failed: {str(e)}")
                return False
            return True
        
        if schedule_time == 'now':
            success = post_job()
            if not success:
                sys.exit(1)
        else:
            schedule.every().day.at(schedule_time).do(post_job)
            logger.info(f"Post scheduled for {schedule_time}")
            
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Scheduler stopped")
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if _name_ == "_main_":
    main()
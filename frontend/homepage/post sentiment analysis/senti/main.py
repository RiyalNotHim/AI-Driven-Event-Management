from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Selenium WebDriver (Ensure `chromedriver` is installed)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# Function to log in to Instagram
def login_instagram(username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password, Keys.RETURN)
    time.sleep(5)

# Function to scrape comments from an Instagram post
def scrape_comments(post_url, max_comments=20):
    driver.get(post_url)
    time.sleep(5)
    comments = []
    elements = driver.find_elements(By.CSS_SELECTOR, "ul li div span")
    for element in elements[:max_comments]:
        comments.append(element.text)
    return comments

# Function to analyze sentiment
def analyze_sentiment(comments):
    analyzer = SentimentIntensityAnalyzer()
    results = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for comment in comments:
        score = analyzer.polarity_scores(comment)
        if score['compound'] >= 0.05:
            results["Positive"] += 1
        elif score['compound'] <= -0.05:
            results["Negative"] += 1
        else:
            results["Neutral"] += 1
    return results

# API Route to trigger Instagram Sentiment Analysis
@app.post("/analyze")
def analyze(username: str = Form(...), password: str = Form(...), post_url: str = Form(...)):
    try:
        login_instagram(username, password)
        comments = scrape_comments(post_url)
        sentiment_results = analyze_sentiment(comments)
        driver.quit()
        return {"Sentiment Analysis Results": sentiment_results}
    except Exception as e:
        return {"error": str(e)}

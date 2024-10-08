from pytrends.request import TrendReq
import numpy as np
import time
import re
from collections import Counter

# Initialize the Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# Function to fetch Google Trends data for a keyword
def get_search_volume(keyword):
    try:
        # Build the payload for the keyword
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='', gprop='')
        data = pytrends.interest_over_time()

        if data.empty:
            print(f"No data found for '{keyword}'")
            return None

        # Calculate the average interest over the past 12 months
        search_volume = np.mean(data[keyword])
        return search_volume
    except Exception as e:
        print(f"Error fetching data for '{keyword}': {e}")
        return None

# Function to estimate competition (simulated based on common keywords)
def estimate_competition(keyword):
    # Simulate competition value
    simulated_competition = np.random.uniform(0.1, 1.0)
    return simulated_competition

# Function to calculate topic score based on search volume and competition
def calculate_topic_score(keyword):
    search_volume = get_search_volume(keyword)
    if search_volume is None:
        return None

    competition = estimate_competition(keyword)

    # Formula for calculating topic score
    topic_score = (search_volume / competition) * 100

    # Normalize to a score between 0 and 100
    normalized_score = min(max(topic_score, 0), 100)
    return normalized_score

# Function to clean up video titles and extract potential keywords
def extract_keywords_from_title(video_title):
    # Basic keyword extraction by removing common stop words
    stop_words = set([
        'the', 'is', 'in', 'of', 'and', 'a', 'to', 'it', 'with', 'on', 'for', 
        'this', 'that', 'you', 'your', 'as', 'are', 'by', 'or', 'can', 'be', 'an'
    ])

    # Clean up the title by removing punctuation and converting to lowercase
    cleaned_title = re.sub(r'[^\w\s]', '', video_title.lower())
    
    # Tokenize and remove stop words
    keywords = [word for word in cleaned_title.split() if word not in stop_words]
    
    # Use a Counter to get word frequencies, if needed for further analysis
    keyword_counter = Counter(keywords)
    
    return keywords

# Main function to get the topic and score based on a keyword (or video title)
def get_topic_score_from_title(video_title):
    keywords = extract_keywords_from_title(video_title)

    if not keywords:
        print("No keywords found in title.")
        return None, None

    # Get scores for each keyword in the title
    scores = {}
    for keyword in keywords:
        score = calculate_topic_score(keyword)
        if score is not None:
            scores[keyword] = score

    # If no scores were found
    if not scores:
        return None, None

    # Choose the keyword with the highest score as the primary topic
    main_topic = max(scores, key=scores.get)
    main_topic_score = scores[main_topic]

    return main_topic, main_topic_score

# Example of using the main function
if __name__ == "__main__":
    video_title = "Can you guess the top ten animals that humans eat per year?"  # Replace with your actual video title
    topic, topic_score = get_topic_score_from_title(video_title)

    if topic:
        print(f"Main Topic: {topic}")
        print(f"Topic Score: {topic_score}/100")
    else:
        print("No significant topic found.")

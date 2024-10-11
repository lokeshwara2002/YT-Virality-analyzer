import os
import googleapiclient.discovery
import logging
import re
import html

# Replace with your YouTube Data API key
API_KEY = "AIzaSyCKuURoscr8GES6QWsCJKvJ1T4hzN1JZ4Q"

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to clean comments by unescaping HTML entities and stripping HTML tags
def clean_comment(comment):
    # Unescape HTML entities
    comment = html.unescape(comment)
    # Remove HTML tags using regex
    comment = re.sub(r'<.*?>', '', comment)  # Remove any HTML tags
    return comment.strip()

# Function to extract video ID from YouTube URL
def get_video_id(youtube_url):
    if "v=" in youtube_url:
        return youtube_url.split("v=")[1].split("&")[0]
    elif "shorts/" in youtube_url:
        return youtube_url.split("shorts/")[1].split("?")[0]
        # Case for shortened youtu.be URL
    elif "youtu.be/" in youtube_url:
        return youtube_url.split("youtu.be/")[1].split("?")[0]
    return None

# Function to fetch top comments
def fetch_top_comments(video_id, api_key, max_results=1000):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    comments = []
    next_page_token = None

    try:
        while len(comments) < max_results:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results - len(comments), 1000),
                pageToken=next_page_token,
                order="relevance",
            )
            response = request.execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comment = clean_comment(comment)  # Clean the comment
                # Filter out empty comments
                if comment:
                    comments.append(comment)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        logging.error(f"An error occurred while fetching comments: {e}")

    return comments

# Function to save comments to a text file
def save_comments_to_file(comments, file_name="comments.txt"):
    with open(file_name, "w", encoding="utf-8") as f:
        for idx, comment in enumerate(comments, 1):
            f.write(f"{idx}. {comment}\n\n")
    print(f"Comments saved to {file_name}")

# Main function to get top comments from a YouTube link and save them to a file
def main(youtube_url):
    video_id = get_video_id(youtube_url)
    if not video_id:
        print("Invalid YouTube URL")
        return

    comments = fetch_top_comments(video_id, API_KEY)
    save_comments_to_file(comments)

if __name__ == "__main__":
    youtube_link = "link.txt"
    if os.path.exists(youtube_link):
        with open(youtube_link, 'r') as file:
            video_link = file.read().strip()
            logging.debug(f"Read link: {video_link}")
            main(video_link)
    else:
        logging.error(f"Link file {youtube_link} does not exist")

import os
import googleapiclient.discovery

# Replace with your YouTube Data API key
API_KEY = "AIzaSyCKuURoscr8GES6QWsCJKvJ1T4hzN1JZ4Q"

# Function to extract video ID from YouTube URL
def get_video_id(youtube_url):
    if "v=" in youtube_url:
        return youtube_url.split("v=")[1].split("&")[0]
    return None

# Function to fetch top comments
def fetch_top_comments(video_id, api_key, max_results=200):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    comments = []
    next_page_token = None

    while len(comments) < max_results:
        # Make a request to the YouTube API to get video comments
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_results - len(comments), 200),
            pageToken=next_page_token,
            order="relevance",  # Fetch top comments (can change to 'time' for recent comments)
        )
        response = request.execute()

        # Extract comments from the response
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # Check if there's another page of comments
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

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
    # Replace this with the YouTube video link you want to analyze
    youtube_link = "https://www.youtube.com/watch?v=GBeI4hLkUL0"
    main(youtube_link)

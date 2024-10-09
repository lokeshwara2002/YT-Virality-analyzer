import re
import spacy
from transformers import pipeline
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import string

# Load the spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Function to load and read comments from the file
def load_comments(file_name="comments.txt"):
    with open(file_name, "r", encoding="utf-8") as f:
        comments = f.readlines()
    return [comment.strip() for comment in comments if comment.strip()]

# Function to extract timestamps mentioned in comments
def extract_timestamps(comments):
    timestamp_pattern = re.compile(r'\b(\d{1,2}:\d{2})\b')
    timestamp_comments = []

    for comment in comments:
        timestamps = timestamp_pattern.findall(comment)
        if timestamps:
            timestamp_comments.append((timestamps, comment))

    return timestamp_comments

# Perform summarization using a pre-trained BART Large CNN model
def summarize_comments(comments):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    combined_text = " ".join(comments)

    max_chunk_length = 1024
    summary_chunks = []

    for i in range(0, len(combined_text), max_chunk_length):
        chunk = combined_text[i:i + max_chunk_length]
        summary_chunk = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
        summary_chunks.append(summary_chunk)

    final_summary = " ".join(summary_chunks)
    word_limit = 500
    truncated_summary = ' '.join(final_summary.split()[:word_limit])

    return truncated_summary

# Perform sentiment analysis on each comment
def analyze_sentiment(comments):
    sentiments = {"positive": 0, "neutral": 0, "negative": 0}

    for comment in comments:
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            sentiments["positive"] += 1
        elif analysis.sentiment.polarity == 0:
            sentiments["neutral"] += 1
        else:
            sentiments["negative"] += 1

    total_comments = len(comments)
    for sentiment, count in sentiments.items():
        sentiments[sentiment] = round((count / total_comments) * 100, 2)

    return sentiments

# Function to extract top 20 most repeated single words
def extract_top_keywords(comments, top_n=20):
    all_words = " ".join(comments).lower()
    words = re.findall(r'\b\w+\b', all_words)
    words = [word for word in words if word not in spacy.lang.en.stop_words.STOP_WORDS and word not in string.punctuation]
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

# Read the transcribe summary
def read_transcribe_summary(file_path='transcribe-summary.txt'):
    with open(file_path, 'r') as file:
        return file.read()

# Main analysis function
def main(file_name="comments.txt"):
    comments = load_comments(file_name)

    # Cluster comments to group them into detailed topics
    def cluster_comments(comments, num_clusters=3):
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(comments)

        kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X)
        clusters = {i: [] for i in range(num_clusters)}

        for idx, label in enumerate(kmeans.labels_):
            clusters[label].append(comments[idx])

        return clusters

    # Extract timestamps and their associated comments
    timestamp_comments = extract_timestamps(comments)
    if timestamp_comments:
        print("Comments mentioning specific parts of the video (timestamps):")
        for timestamps, comment in timestamp_comments:
            print(f"Timestamps: {timestamps}, Comment: {comment}\n")

    # Summarize comments to describe what the video is about
    summary = summarize_comments(comments)
    print("Summary of Comments (What the video is about):\n", summary)

    # Sentiment analysis to describe viewers' opinions
    sentiments = analyze_sentiment(comments)
    print("\nSentiment Analysis (Viewers' opinions):")
    print(f"Positive: {sentiments['positive']}%")
    print(f"Neutral: {sentiments['neutral']}%")
    print(f"Negative: {sentiments['negative']}%")

    # Cluster comments to group them into detailed topics
    clusters = cluster_comments(comments)
    print("\nKey Topics in Comments (Detailed):")
    for cluster_id, cluster_comments in clusters.items():
        print(f"\nTopic {cluster_id + 1}:")
        for comment in cluster_comments[:5]:
            print(f"- {comment}")

    # Extract top 20 most repeated single-worded keywords
    top_keywords = extract_top_keywords(comments)
    print("\nTop 20 Keywords (Most Repeated Words):")
    for word, count in top_keywords:
        print(f"{word}: {count}")

    # Read the transcribe summary
    transcribe_summary = read_transcribe_summary()

    # Save the insights to comments-analysis.txt
    with open("comments-analysis.txt", "w", encoding="utf-8") as f:
        if timestamp_comments:
            f.write("Comments mentioning specific parts of the video (timestamps):\n")
            for timestamps, comment in timestamp_comments:
                f.write(f"Timestamps: {timestamps}, Comment: {comment}\n")
            f.write("\n")

        f.write("Summary of Comments (What the video is about):\n")
        f.write(f"{summary}\n\n")

        f.write("Transcribe Summary:\n")
        f.write(f"{transcribe_summary}\n\n")  # Write the transcribe summary here

        f.write("Sentiment Analysis (Viewers' opinions):\n")
        f.write(f"Positive: {sentiments['positive']}%\n")
        f.write(f"Neutral: {sentiments['neutral']}%\n")
        f.write(f"Negative: {sentiments['negative']}%\n\n")

        f.write("Key Topics in Comments (Detailed):\n")
        for cluster_id, cluster_comments in clusters.items():
            f.write(f"\nTopic {cluster_id + 1}:\n")
            for comment in cluster_comments[:5]:
                f.write(f"- {comment}\n")

        f.write("\nTop 20 Keywords (Most Repeated Words):\n")
        for word, count in top_keywords:
            f.write(f"{word}: {count}\n")

if __name__ == "__main__":
    main()

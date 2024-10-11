import re
import spacy
from transformers import pipeline
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

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

# Function to clean and tokenize comments
def clean_and_tokenize(text):
    # Remove HTML tags and unwanted characters
    cleaned_text = re.sub(r'<.*?>', '', text)  # Removes HTML tags like <br>, <b>
    cleaned_text = re.sub(r'&quot;', '', cleaned_text)  # Remove &quot;
    cleaned_text = re.sub(r'\d+', '', cleaned_text)  # Remove numbers
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuation
    cleaned_text = cleaned_text.lower()  # Convert to lowercase
    words = cleaned_text.split()
    return words

# Function to extract top 20 most repeated two-word keywords (bigrams)
def extract_top_keywords(comments, top_n=20):
    # Initialize the CountVectorizer for bigrams
    vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words='english')
    X = vectorizer.fit_transform(comments)

    # Get the counts of each bigram
    bigram_counts = X.toarray().sum(axis=0)
    bigram_feature_names = vectorizer.get_feature_names_out()

    # Combine bigrams and their counts into a dictionary
    bigram_dict = dict(zip(bigram_feature_names, bigram_counts))

    # Updated list of irrelevant words to ignore
    ignore_words = [
        'br', 'quot', 'nbsp', 'amp','video','videos', '39', 's', 'the', 'a', 'an', 'and', 
        'is', 'to', 'in', 'on', 'no', 'i', 'of', 'this', 'that', 'for', 
        'it', 'as', 'are', 'with', 'was', 'but', 'be', 'at', 'by', 
        'not', 'you', 'so', 'he', 'she', 'they', 'them', 'their', 
        'theirs', 'my', 'me', 'us', 'we', 'our', 'hers', 'him', 
        'himself', 'herself', 'itself', 'what', 'which', 'who', 
        'whom', 'whose', 'if', 'than', 'then', 'because', 'when', 
        'where', 'while', 'although', 'since', 'after', 'before', 
        'during', 'but', 'or', 'yet', 'for', 'nor', 'so', 'either', 
        'neither', 'each', 'every', 'some', 'any', 'all', 'most', 
        'few', 'less', 'more', 'such', 'like', 'just', 'now', 'only', 
        'also', 'too', 'very', 'just', 'then', 'than', 'whoever', 
        'whenever', 'whatever', 'whichever', 'something', 'anything',
        'never', 'has', 'were', 'about', 'how', 'can', 'its', 'everything', 
        'nothing', 'somebody', 'anybody', 'everybody', 'nobody', 
        'somewhere', 'anywhere', 'everywhere', 'nowhere', 'together', 
        'alone', 'first', 'next', 'last', 'main', 'man', 'primary', 
        'secondary', 'major', 'minor'
    ]  # Add more if needed

    # Filter out irrelevant bigrams
    filtered_bigrams = {k: v for k, v in bigram_dict.items() if k not in ignore_words}

    # Get the 20 most common bigrams
    top_bigrams = sorted(filtered_bigrams.items(), key=lambda item: item[1], reverse=True)[:top_n]
    return top_bigrams

# Read the transcribe summary
def read_transcribe_summary(file_path='transcribe-summary.txt'):
    with open(file_path, 'r') as file:
        return file.read()

# Function to cluster comments and assign descriptive topics
def perform_clustering(comments, num_clusters=3):
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(comments)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)  # Ensure KMeans is fitted

    clusters = {i: [] for i in range(num_clusters)}

    for idx, label in enumerate(kmeans.labels_):
        clusters[label].append(comments[idx])

    # Extract top terms for each cluster
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    cluster_topics = {}
    for i in range(num_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :5]]
        cluster_topics[i] = " ".join(top_terms)

    return clusters, cluster_topics

# Main analysis function
def main(file_name="comments.txt"):
    comments = load_comments(file_name)

    # Extract timestamps and their associated comments
    timestamp_comments = extract_timestamps(comments)
    
    # Summarize comments to describe what the video is about
    summary = summarize_comments(comments)

    # Read the transcribe summary
    transcribe_summary = read_transcribe_summary()

    # Sentiment analysis to describe viewers' opinions
    sentiments = analyze_sentiment(comments)

    # Extracting top 20 most repeated two-word keywords
    top_keywords = extract_top_keywords(comments)

    # Clustering comments to identify main topics
    clusters, cluster_topics = perform_clustering(comments)

    # Writing the analysis to a file
    with open("comments-analysis.txt", "w", encoding="utf-8") as f:


        f.write("Transcription Summary:\n")
        f.write(transcribe_summary + "\n\n")  # Write the transcription summary
        
        f.write("Summary of Comments:\n")
        f.write(summary + "\n\n")

        f.write("Sentiment Analysis:\n")
        for sentiment, percentage in sentiments.items():
            f.write(f"{sentiment.capitalize()}: {percentage}%\n")
        f.write("\n")

        f.write("Top 20 Keywords (Most Repeated Two-Word Phrases):\n")
        for bigram, count in top_keywords:
            f.write(f"{bigram}: {count}\n")
        f.write("\n")

        # Write timestamp-related comments to the file
        if timestamp_comments:
            f.write("Comments mentioning specific parts of the video (timestamps):\n")
            for timestamps, comment in timestamp_comments:
                f.write(f"Timestamps: {', '.join(timestamps)}, Comment: {comment}\n")
            f.write("\n")

        f.write("Clustered Comments with Identified Topics:\n")
        for cluster_id, cluster_comments in clusters.items():
            topic_name = cluster_topics[cluster_id]
            f.write(f"\nTopic: {topic_name}\n")
            for comment in cluster_comments[:5]:
                f.write(f"- {comment}\n")

# Run the analysis
if __name__ == "__main__":
    main()
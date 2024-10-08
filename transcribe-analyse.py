import os
from transformers import pipeline

# Function to load and read transcription from the file
def load_transcription(file_name="transcribe.txt"):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} not found.")
        
    with open(file_name, "r", encoding="utf-8") as f:
        transcription = f.read()
    return transcription

# Function to summarize the transcription using a pre-trained model
def summarize_transcription(transcription, max_words=500):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Summarize in chunks if the text is too long for the model
    max_length = 1024
    summary = ""

    for i in range(0, len(transcription), max_length):
        chunk = transcription[i:i + max_length]
        summary += summarizer(chunk, max_length=max_words, min_length=50, do_sample=False)[0]["summary_text"]

    return summary

# Main function to load, summarize, and save the summary to a file
def main(input_file="transcribe.txt", output_file="transcribe-summary.txt"):
    try:
        # Load the transcription
        transcription = load_transcription(input_file)
        print("Transcription loaded successfully.")
        
        # Summarize the transcription
        summary = summarize_transcription(transcription)
        print("Summary generated successfully.")
        
        # Save the summary to the output file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

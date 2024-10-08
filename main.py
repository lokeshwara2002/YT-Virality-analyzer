from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
import sys

app = FastAPI()

# Endpoint to process the YouTube link
@app.post("/process")
async def process_youtube_link():
    try:
        # Execute the Python scripts in sequence using the correct Python interpreter
        python_exec = sys.executable  # Get the correct Python executable path
        subprocess.run([python_exec, "audio_download.py"], check=True)
        subprocess.run([python_exec, "mp3 to wav.py"], check=True)
        subprocess.run([python_exec, "transcribe.py"], check=True)
        subprocess.run([python_exec, "transcribe-analyse.py"], check=True)
        subprocess.run([python_exec, "comments.py"], check=True)
        subprocess.run([python_exec, "analyse-comments.py"], check=True)
        return {"message": "Processing completed successfully"}
    except subprocess.CalledProcessError as e:
        return {"error": f"Script failed with error: {str(e)}"}

# Endpoint to view the results
@app.get("/results")
async def get_results():
    file_path = "comments-analysis.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='text/plain', filename="comments-analysis.txt")
    else:
        raise HTTPException(status_code=404, detail="Results file not found")

# Serve the main HTML page
@app.get("/")
async def get_index():
    return FileResponse("index.html")

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import sys
import asyncio

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Global variables to store analysis results
sentiment_data = []  # Format: [positive, negative, neutral]
keywords_data = []   # List of top keywords

# Endpoint to process the YouTube link
@app.post("/process")
async def process_youtube_link(link: str = Form(...)):
    # Save the link to link.txt
    with open("link.txt", "w") as f:
        f.write(link)

    # Introduce a 3-second delay
    await asyncio.sleep(3)

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


# Endpoint to download the results file
@app.get("/results", response_class=FileResponse)
async def download_results():
    file_path = "comments-analysis.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename="comments-analysis.txt")
    else:
        raise HTTPException(status_code=404, detail="Results file not found")

# Endpoint to serve the results HTML page
@app.get("/results-page", response_class=HTMLResponse)
async def get_results_page():
    file_path = "comments-analysis.txt"
    if os.path.exists(file_path):
        return FileResponse("results.html")  # Serve the results page
    else:
        raise HTTPException(status_code=404, detail="Results file not found")

# Endpoint to serve the visual analysis page
@app.get("/visual-page", response_class=HTMLResponse)
async def get_visual_page():
    return FileResponse("visual.html")  # Serve the visual HTML page

# Serve the main HTML page
@app.get("/", response_class=HTMLResponse)
async def get_index():
    return FileResponse("index.html")

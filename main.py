from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import FileResponse
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

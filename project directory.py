import os

def list_files_in_root(directory):
    # Get the list of all files in the root directory (excluding subdirectories)
    files_in_root = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Print each file in the root directory
    print("Files in the root folder:")
    for f in files_in_root:
        print(f)

# Set the directory to your project folder (you can replace '.' with your directory path)
project_directory = "."
list_files_in_root(project_directory)

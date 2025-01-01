
import os
import requests

clear_video_folder = 0
search_query = "ocean waves aerial"  # Replace with your search term
num_videos = 8

# Configure your Pexels API key here
PEXELS_API_KEY = "tqC7pqI0UOgIAAinMKOMj24ywXQl688o8NizpkGZyWkQsnyu36lBXqst"

# Create a folder to store downloaded videos
VIDEOS_FOLDER = "videos"
os.makedirs(VIDEOS_FOLDER, exist_ok=True)
  
# Clear the videos folder
if clear_video_folder:
    for file in os.listdir(VIDEOS_FOLDER):
        file_path = os.path.join(VIDEOS_FOLDER, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print(f"Cleared the '{VIDEOS_FOLDER}' folder.")



def download_videos(query, n, orientation="portrait"):
    """
    Download `n` videos from Pexels matching the query and orientation.
    
    Parameters:
        query (str): Search term for videos (e.g., 'nature').
        n (int): Number of videos to download.
        orientation (str): Orientation of videos ('portrait' for vertical).
    """
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    # Pexels API endpoint for video search
    endpoint = f"https://api.pexels.com/videos/search"
    
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": min(n, 80),  # Maximum videos per request is 80
        "page": 1
    }
    
    downloaded = 0
    
    while downloaded < n:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        videos = response.json().get("videos", [])
        
        if not videos:
            print("No more videos found matching the criteria.")
            break
        
        for video in videos:
            video_url = video["video_files"][0]["link"]
            video_id = video["id"]
            file_path = os.path.join(VIDEOS_FOLDER, f"video_{video_id}.mp4")
            
            # Download video
            print(f"Downloading video {video_id} from {video_url}")
            video_data = requests.get(video_url).content
            with open(file_path, "wb") as video_file:
                video_file.write(video_data)
            
            downloaded += 1
            if downloaded >= n:
                break
        
        # Increment page for next batch
        params["page"] += 1

    print(f"Downloaded {downloaded} videos to the '{VIDEOS_FOLDER}' folder.")


# Example usage
if __name__ == "__main__":
    search_query = search_query  # Replace with your search term
    num_videos = num_videos # Replace with the number of videos you want to download
    download_videos(search_query, num_videos, orientation='landscape')


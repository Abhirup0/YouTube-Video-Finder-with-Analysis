"""
YouTube search module
Handles searching YouTube videos with filters for duration and upload date
"""
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def search_youtube(query, api_key, max_results=20, min_duration=240, max_duration=1200, days_ago=14):
    """
    Search YouTube for videos matching query with filtering
    
    Args:
        query (str): Search query
        api_key (str): YouTube API key
        max_results (int): Maximum number of results to return
        min_duration (int): Minimum video duration in seconds
        max_duration (int): Maximum video duration in seconds
        days_ago (int): Only include videos published in the last X days
    
    Returns:
        list: List of video dictionaries with metadata
    """
    try:
        # Calculate the date for filtering
        published_after = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).isoformat() + "Z"
        
        # Create YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Initial search to get video IDs
        search_response = youtube.search().list(
            q=query,
            part='id',
            maxResults=max_results * 2,  # Get more than needed to allow for filtering
            type='video',
            publishedAfter=published_after,
            relevanceLanguage='en'  # Focus on English results but will still return other languages
        ).execute()
        
        video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
        if not video_ids:
            return []
            
        # Get video details including duration
        videos_response = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()
        
        # Process and filter videos
        result_videos = []
        for item in videos_response.get('items', []):
            # Parse duration in ISO 8601 format
            duration_str = item['contentDetails']['duration']
            duration_seconds = parse_duration(duration_str)
            
            # Filter by duration
            if min_duration <= duration_seconds <= max_duration:
                # Format the data
                video_data = {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'published': item['snippet']['publishedAt'],
                    'duration': round(duration_seconds / 60, 1),  # Convert to minutes
                    'views': item['statistics'].get('viewCount', '0'),
                    'thumbnail': item['snippet']['thumbnails']['high']['url']
                }
                result_videos.append(video_data)
                
                # Stop if we have enough videos
                if len(result_videos) >= max_results:
                    break
        
        return result_videos
        
    except HttpError as e:
        print(f"YouTube API error: {e}")
        return []
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []

def parse_duration(duration_str):
    """
    Parse ISO 8601 duration format (PT#H#M#S) to seconds
    Example: PT1H22M33S => 1 hour, 22 minutes, 33 seconds
    
    Args:
        duration_str (str): Duration string in ISO 8601 format
        
    Returns:
        int: Duration in seconds
    """
    duration_str = duration_str[2:]  # Remove PT prefix
    
    hours = 0
    minutes = 0
    seconds = 0
    
    # Extract hours
    if 'H' in duration_str:
        hours_str, duration_str = duration_str.split('H')
        hours = int(hours_str)
    
    # Extract minutes
    if 'M' in duration_str:
        minutes_str, duration_str = duration_str.split('M')
        minutes = int(minutes_str)
    
    # Extract seconds
    if 'S' in duration_str:
        seconds_str = duration_str.split('S')[0]
        seconds = int(seconds_str)
    
    return hours * 3600 + minutes * 60 + seconds 
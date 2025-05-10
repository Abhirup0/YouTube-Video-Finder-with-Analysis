"""
LLM Analysis using Google's Gemini API
Analyzes YouTube video titles to find the most relevant one for the query
"""
import google.generativeai as genai

def analyze_titles(videos, query, api_key):
    """
    Analyze video titles using Gemini LLM to find the most relevant
    
    Args:
        videos (list): List of video dictionaries from YouTube search
        query (str): The original search query
        api_key (str): Gemini API key
        
    Returns:
        dict: Best matching video with analysis
    """
    if not videos:
        return None
        
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Create a list of video titles for analysis
    video_data = []
    for idx, video in enumerate(videos):
        video_data.append(f"{idx+1}. Title: '{video['title']}' | Channel: {video['channel']} | Duration: {video['duration']} min")
    
    # Create the prompt for Gemini
    prompt = f"""
    Original Search Query: "{query}"
    
    Analyze the following YouTube video titles and determine which ONE is most likely to be the highest quality, 
    most informative, and most relevant to the search query. Consider factors like clarity, 
    specificity, information density, and relevance.
    
    VIDEO OPTIONS:
    {chr(10).join(video_data)}
    
    Select the BEST video option by providing:
    1. The number of the best video (e.g., "3")
    2. A brief explanation of why it's the best choice (2-3 sentences maximum)
    
    Format your response exactly like this:
    BEST_VIDEO: [Number]
    REASON: [Your explanation]
    """
    
    try:
        # Generate content with Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Parse the response to get the best video index
        response_text = response.text
        
        best_video_idx = None
        reason = ""
        
        # Extract the best video number
        for line in response_text.split('\n'):
            if line.startswith("BEST_VIDEO:"):
                try:
                    best_video_idx = int(line.split("BEST_VIDEO:")[1].strip()) - 1
                except:
                    # Try to extract just the number if the format is different
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        best_video_idx = int(numbers[0]) - 1
            elif line.startswith("REASON:"):
                reason = line.split("REASON:")[1].strip()
        
        # If no index was found or it's invalid, default to the first video
        if best_video_idx is None or best_video_idx < 0 or best_video_idx >= len(videos):
            best_video_idx = 0
            reason = "Unable to determine best video from analysis. Showing first result."
        
        # Get the best video and add the analysis
        best_video = videos[best_video_idx].copy()
        best_video['analysis'] = reason
        
        return best_video
        
    except Exception as e:
        print(f"Error analyzing titles with Gemini: {e}")
        # Fall back to the first video
        return {**videos[0], 'analysis': "Error analyzing titles. Returning first result."} 
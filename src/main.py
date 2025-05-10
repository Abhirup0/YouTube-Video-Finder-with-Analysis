#!/usr/bin/env python3
"""
YouTube Video Finder with Analysis
Main application that orchestrates searching, filtering and analyzing YouTube videos
"""
import os
import sys
import time
from youtube_search import search_youtube
from text_input import get_user_input, print_colored
from llm_analysis import analyze_titles
from config_manager import load_config
from datetime import datetime

def format_duration(minutes):
    """Format minutes into a readable duration string"""
    hours, mins = divmod(int(minutes), 60)
    seconds = int((minutes - int(minutes)) * 60)
    
    if hours > 0:
        return f"{hours}h {mins}m {seconds}s"
    else:
        return f"{mins}m {seconds}s"

def format_date(date_str):
    """Format ISO date to readable format"""
    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return date_obj.strftime("%b %d, %Y")

def print_progress(message, steps=3, delay=0.3):
    """Print progress animation"""
    print(message, end="")
    for _ in range(steps):
        time.sleep(delay)
        print(".", end="", flush=True)
    print()

def display_video_results(videos, query):
    """Display a summary of found videos"""
    print_colored("\n🎬 Videos found matching your criteria:", "cyan", "bold")
    
    # Print basic stats
    print_colored(f"  • Found {len(videos)} videos matching: '{query}'", "white")
    
    # Show first few videos
    if videos:
        print_colored("\n📋 Top results preview:", "yellow")
        for i, video in enumerate(videos[:5], 1):
            title = video['title']
            channel = video['channel']
            duration = format_duration(video['duration'])
            print_colored(f"  {i}. {title}", "white")
            print_colored(f"     ↪ Channel: {channel} | Duration: {duration}", "white")
        
        if len(videos) > 5:
            print_colored(f"  ... and {len(videos) - 5} more", "white")

def display_best_video(video):
    """Display the best video recommendation with enhanced formatting"""
    print_colored("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓", "green")
    print_colored("┃                 🏆 BEST RECOMMENDATION 🏆           ┃", "green", "bold")
    print_colored("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛", "green")
    
    print_colored(f"\n📽️  Title: {video['title']}", "yellow", "bold")
    print_colored(f"👤 Channel: {video['channel']}", "cyan")
    print_colored(f"⏱️  Duration: {format_duration(video['duration'])}", "cyan")
    print_colored(f"📅 Published: {format_date(video['published'])}", "cyan")
    print_colored(f"👁️  Views: {int(video['views']):,}", "cyan")
    print_colored(f"🔗 URL: https://www.youtube.com/watch?v={video['id']}", "blue", "underline")
    
    print_colored("\n💡 Why this video was chosen:", "magenta", "bold")
    print_colored(f"   {video['analysis']}", "white")
    
    print_colored("\n✨ Enjoy your video! ✨\n", "green", "bold")

def main():
    """Main function to run the YouTube Video Finder application"""
    # Load configuration
    config = load_config()
    if not config:
        print_colored("❌ Failed to load configuration. Exiting.", "red", "bold")
        return 1
    
    # Get user input (text/voice)
    query = get_user_input()
    if not query:
        print_colored("❌ No input provided. Exiting.", "red", "bold")
        return 1
    
    # Search YouTube with filters
    print_progress("🔍 Searching YouTube", steps=5, delay=0.3)
    videos = search_youtube(
        query=query,
        api_key=config["youtube_api_key"],
        max_results=20,
        min_duration=4 * 60,  # 4 minutes in seconds
        max_duration=20 * 60,  # 20 minutes in seconds
        days_ago=14
    )
    
    if not videos:
        print_colored("\n❌ No videos found matching your criteria.", "red", "bold")
        return 0
    
    # Display found videos
    display_video_results(videos, query)
    
    # Analyze titles with Gemini
    print_colored("\n🧠 Analyzing video titles with AI...", "magenta")
    print_progress("   Processing", steps=5, delay=0.4)
    
    best_video = analyze_titles(
        videos=videos,
        query=query,
        api_key=config["gemini_api_key"]
    )
    
    # Display results
    display_best_video(best_video)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_colored("\n\n🛑 Search cancelled by user. Goodbye!", "yellow", "bold")
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n❌ An unexpected error occurred: {e}", "red", "bold")
        sys.exit(1) 
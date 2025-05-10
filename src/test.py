#!/usr/bin/env python3
"""
Test module for YouTube Video Finder
Tests functionality without calling real APIs
"""
import unittest
import os
import sys
from unittest.mock import patch, MagicMock
from config_manager import load_config
from text_input import get_text_input
from youtube_search import parse_duration, search_youtube
from llm_analysis import analyze_titles

class TestYouTubeVideoFinder(unittest.TestCase):
    """Tests for YouTube Video Finder"""
    
    def test_parse_duration(self):
        """Test parsing ISO 8601 duration format"""
        self.assertEqual(parse_duration("PT1H22M33S"), 4953)
        self.assertEqual(parse_duration("PT5M30S"), 330)
        self.assertEqual(parse_duration("PT45S"), 45)
        self.assertEqual(parse_duration("PT1H"), 3600)
    
    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('os.path.exists')
    def test_load_config(self, mock_exists, mock_open, mock_json_load):
        """Test loading configuration from file"""
        # Set up mocks
        mock_exists.return_value = True
        mock_json_load.return_value = {
            "youtube_api_key": "test_yt_key",
            "gemini_api_key": "test_gemini_key"
        }
        
        # Test loading config
        config = load_config()
        self.assertIsNotNone(config)
        self.assertEqual(config["youtube_api_key"], "test_yt_key")
        self.assertEqual(config["gemini_api_key"], "test_gemini_key")
    
    @patch('builtins.input')
    def test_get_text_input(self, mock_input):
        """Test text input functionality"""
        mock_input.return_value = "test query"
        query = get_text_input()
        self.assertEqual(query, "test query")
    
    @patch('googleapiclient.discovery.build')
    def test_search_youtube(self, mock_build):
        """Test YouTube search functionality (mocked)"""
        # Mock YouTube API response
        mock_search = MagicMock()
        mock_videos = MagicMock()
        mock_build.return_value.search.return_value.list.return_value.execute.return_value = {
            'items': [{'id': {'videoId': 'test_id'}}]
        }
        mock_build.return_value.videos.return_value.list.return_value.execute.return_value = {
            'items': [{
                'id': 'test_id',
                'snippet': {
                    'title': 'Test Video',
                    'channelTitle': 'Test Channel',
                    'publishedAt': '2023-07-01T00:00:00Z',
                    'thumbnails': {'high': {'url': 'http://example.com/thumbnail.jpg'}}
                },
                'contentDetails': {'duration': 'PT10M30S'},
                'statistics': {'viewCount': '1000'}
            }]
        }
        
        # Test search
        results = search_youtube('test', 'test_api_key')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Video')
        self.assertEqual(results[0]['duration'], 10.5)  # 10 minutes and 30 seconds
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_analyze_titles(self, mock_configure, mock_model):
        """Test LLM analysis of video titles (mocked)"""
        # Mock videos and response
        videos = [
            {'id': 'vid1', 'title': 'Test Video 1', 'channel': 'Channel 1', 'duration': 10},
            {'id': 'vid2', 'title': 'Test Video 2', 'channel': 'Channel 2', 'duration': 15}
        ]
        
        mock_response = MagicMock()
        mock_response.text = "BEST_VIDEO: 2\nREASON: This is the best video because it's more detailed."
        mock_model.return_value.generate_content.return_value = mock_response
        
        # Test analysis
        result = analyze_titles(videos, 'test query', 'test_api_key')
        self.assertEqual(result['id'], 'vid2')
        self.assertEqual(result['title'], 'Test Video 2')
        self.assertEqual(result['analysis'], "This is the best video because it's more detailed.")

if __name__ == "__main__":
    unittest.main() 
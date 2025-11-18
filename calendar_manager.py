"""
Calendar Manager Module using Google Calendar API
This module handles Google Calendar authentication and event retrieval.

Citation:
- Google Calendar API Documentation: https://developers.google.com/calendar
- Google Auth Library: https://google-auth.readthedocs.io/
"""

import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

# Scopes required for Google Calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class CalendarManager:
    """
    Manages Google Calendar authentication and event retrieval.
    Handles OAuth2 flow and provides methods to fetch calendar events.
    """
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Initialize the Calendar Manager with Google OAuth credentials.
        
        Args:
            client_id (str, optional): Google OAuth client ID
            client_secret (str, optional): Google OAuth client secret
        """
        self.client_id = client_id or os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Google Calendar credentials are required")
        
        self.creds = None
        self.service = None
        self.token_file = 'token.pickle'
        
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API using OAuth2 flow.
        Loads existing credentials or initiates new OAuth flow.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Load existing credentials from token file
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    self.creds = pickle.load(token)
            
            # Refresh or create new credentials if needed
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    # Refresh expired credentials
                    self.creds.refresh(Request())
                    print("✓ Credentials refreshed successfully")
                else:
                    # Create client config for OAuth flow
                    client_config = {
                        "installed": {
                            "client_id": self.client_id,
                            "client_secret": self.client_secret,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://localhost"]
                        }
                    }
                    
                    # Initiate OAuth flow
                    flow = InstalledAppFlow.from_client_config(
                        client_config, 
                        SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                    print("✓ New credentials obtained successfully")
                
                # Save credentials for future use
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.creds, token)
            
            # Build the Calendar API service
            self.service = build('calendar', 'v3', credentials=self.creds)
            print("✓ Google Calendar API service initialized")
            return True
            
        except Exception as e:
            print(f"✗ Authentication error: {str(e)}")
            return False
    
    def get_events(self, time_min: Optional[datetime] = None, 
                   time_max: Optional[datetime] = None, 
                   max_results: int = 10) -> List[Dict]:
        """
        Retrieve calendar events within a specified time range.
        
        Args:
            time_min (datetime, optional): Start of time range. Defaults to now.
            time_max (datetime, optional): End of time range. Defaults to 7 days from now.
            max_results (int): Maximum number of events to retrieve
            
        Returns:
            list: List of calendar event dictionaries
        """
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            # Set default time range if not provided
            if not time_min:
                time_min = datetime.utcnow()
            if not time_max:
                time_max = time_min + timedelta(days=7)
            
            # Format times for Google Calendar API
            time_min_str = time_min.isoformat() + 'Z'
            time_max_str = time_max.isoformat() + 'Z'
            
            # Call the Calendar API
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min_str,
                timeMax=time_max_str,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            print(f"✓ Retrieved {len(events)} events from calendar")
            return events
            
        except HttpError as error:
            print(f"✗ An error occurred: {error}")
            return []
    
    def get_today_events(self) -> List[Dict]:
        """
        Get all events for today.
        
        Returns:
            list: List of today's calendar events
        """
        now = datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        return self.get_events(time_min=start_of_day, time_max=end_of_day)
    
    def get_week_events(self) -> List[Dict]:
        """
        Get all events for the current week.
        
        Returns:
            list: List of this week's calendar events
        """
        now = datetime.utcnow()
        end_of_week = now + timedelta(days=7)
        
        return self.get_events(time_min=now, time_max=end_of_week, max_results=50)
    
    def format_event(self, event: Dict) -> str:
        """
        Format a calendar event into a readable string.
        
        Args:
            event (dict): Calendar event dictionary
            
        Returns:
            str: Formatted event string
        """
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event.get('summary', 'No title')
        location = event.get('location', 'No location')
        description = event.get('description', 'No description')
        
        # Parse and format datetime
        try:
            if 'T' in start:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
                date_str = start_dt.strftime('%A, %B %d, %Y')
            else:
                # All-day event
                date_str = datetime.fromisoformat(start).strftime('%A, %B %d, %Y')
                time_str = "All day"
        except Exception:
            time_str = "Time not available"
            date_str = start
        
        formatted = f"📅 {summary}\n"
        formatted += f"   Date: {date_str}\n"
        formatted += f"   Time: {time_str}\n"
        if location and location != 'No location':
            formatted += f"   Location: {location}\n"
        if description and description != 'No description':
            formatted += f"   Description: {description[:100]}...\n" if len(description) > 100 else f"   Description: {description}\n"
        
        return formatted
    
    def format_events_list(self, events: List[Dict]) -> str:
        """
        Format a list of events into a readable string.
        
        Args:
            events (list): List of calendar event dictionaries
            
        Returns:
            str: Formatted events list
        """
        if not events:
            return "No events found for the specified time period."
        
        formatted = f"Found {len(events)} event(s):\n\n"
        for i, event in enumerate(events, 1):
            formatted += f"{i}. {self.format_event(event)}\n"
        
        return formatted
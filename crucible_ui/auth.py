from flask import session, redirect, url_for, request, jsonify, current_app
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json

# Google OAuth configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile']

def get_google_auth_flow():
    """Create and return a Google OAuth flow"""
    client_config = {
        "web": {
            "client_id": current_app.config['GOOGLE_CLIENT_ID'],
            "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:5000/callback"]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES
    )
    flow.redirect_uri = "http://localhost:5000/callback"
    return flow

def authenticate_with_google():
    """Initiate Google OAuth flow"""
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return authorization_url

def exchange_code_for_tokens(code):
    """Exchange authorization code for tokens"""
    flow = get_google_auth_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return credentials

def get_user_info(credentials):
    """Get user info from Google"""
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    return user_info

def is_authorized_user(email):
    """Check if the email belongs to an authorized supervisor"""
    # In a real implementation, you would check against a database of authorized users
    # For now, we'll allow specific emails
    authorized_emails = [
        "adividan1012@gmail.com",  # Replace with your actual email
        # Add other authorized supervisor emails here
    ]
    return email in authorized_emails
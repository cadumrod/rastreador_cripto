from dotenv import load_dotenv
import os

# Sensitive data file for API connection
load_dotenv("access.env")

API_TOKEN = os.getenv("API_TOKEN")

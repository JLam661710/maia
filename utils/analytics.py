import os
import logging
import atexit
from typing import Dict, Any, Optional
from posthog import Posthog
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AnalyticsClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalyticsClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        api_key = os.getenv("POSTHOG_API_KEY")
        host = os.getenv("POSTHOG_HOST", "https://us.i.posthog.com")

        self.api_key = api_key
        self.host = host
        self.enabled = bool(api_key)
        self.posthog: Any = None

        if not api_key:
            logging.warning("PostHog API key not found. Analytics disabled.")
            return

        try:
            self.posthog = Posthog(api_key, host=host)
            logging.info("PostHog analytics initialized successfully.")
            atexit.register(self.shutdown)
        except Exception as e:
            logging.error(f"Failed to initialize PostHog: {e}")
            self.enabled = False
            self.posthog = None

    def identify_user(self, user_id: str, traits: Optional[Dict[str, Any]] = None):
        """
        Identify a user with their unique ID and optional traits.
        """
        if not self.enabled or not self.posthog:
            return
            
        try:
            self.posthog.identify(user_id, properties=traits or {})
        except Exception as e:
            logging.error(f"Failed to identify user in PostHog: {e}")

    def track_event(self, user_id: str, event_name: str, properties: Optional[Dict[str, Any]] = None):
        """
        Track an event for a specific user.
        """
        if not self.enabled or not self.posthog:
            return
            
        try:
            self.posthog.capture(user_id, event_name, properties=properties or {})
        except Exception as e:
            logging.error(f"Failed to track event '{event_name}' in PostHog: {e}")

    def shutdown(self):
        """
        Flush any remaining events and close the client.
        """
        if self.posthog:
            try:
                self.posthog.shutdown()
            except Exception as e:
                logging.error(f"Failed to shutdown PostHog client: {e}")

# Global instance
analytics = AnalyticsClient()

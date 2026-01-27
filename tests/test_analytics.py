import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.analytics import AnalyticsClient

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        # Reset singleton
        AnalyticsClient._instance = None
        
    @patch('utils.analytics.Posthog')
    def test_initialization(self, mock_posthog_cls):
        # Mock environment variables
        with patch.dict(os.environ, {"POSTHOG_API_KEY": "test_key", "POSTHOG_HOST": "test_host"}):
            client = AnalyticsClient()
            mock_posthog_cls.assert_called_with("test_key", host="test_host")
            self.assertTrue(client.enabled)

    @patch('utils.analytics.Posthog')
    def test_track_event(self, mock_posthog_cls):
        mock_instance = MagicMock()
        mock_posthog_cls.return_value = mock_instance
        
        with patch.dict(os.environ, {"POSTHOG_API_KEY": "test_key"}):
            client = AnalyticsClient()
            client.track_event("user123", "test_event", {"prop": "val"})
            
            mock_instance.capture.assert_called_with("user123", "test_event", properties={"prop": "val"})

    @patch('utils.analytics.Posthog')
    def test_error_swallowing(self, mock_posthog_cls):
        mock_instance = MagicMock()
        mock_instance.capture.side_effect = Exception("Network error")
        mock_posthog_cls.return_value = mock_instance
        
        with patch.dict(os.environ, {"POSTHOG_API_KEY": "test_key"}):
            client = AnalyticsClient()
            # This should NOT raise an exception
            try:
                client.track_event("user123", "test_event")
            except Exception:
                self.fail("track_event raised Exception unexpectedly!")

    def test_disabled_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            client = AnalyticsClient()
            self.assertFalse(client.enabled)
            self.assertIsNone(client.posthog)

if __name__ == '__main__':
    unittest.main()

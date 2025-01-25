import os
from dotenv import load_dotenv


class Config:
    """Configuration class to manage environment variables."""

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Initialize configuration variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

    @property
    def is_configured(self) -> bool:
        """Check if all required API keys are set."""
        return bool(self.openai_api_key and self.tavily_api_key)


# Create a singleton instance
config = Config()

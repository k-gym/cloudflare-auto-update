from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Define the environment variables
ENV_KEY__CLOUD_FLARE__API_EMAIL = "CLOUD_FLARE__API_EMAIL"
ENV_KEY__CLOUD_FLARE__API_KEY = "CLOUD_FLARE__API_KEY"
ENV_KEY__CLOUD_FLARE__DOMAIN = "CLOUD_FLARE__DOMAIN"


# Load the environment variables
CLOUD_FLARE__BASE_URL = "https://api.cloudflare.com/client/v4"
CLOUD_FLARE__API_EMAIL = os.environ.get(ENV_KEY__CLOUD_FLARE__API_EMAIL)
CLOUD_FLARE__API_KEY = os.environ.get(ENV_KEY__CLOUD_FLARE__API_KEY)
CLOUD_FLARE__DOMAIN = os.environ.get(ENV_KEY__CLOUD_FLARE__DOMAIN)
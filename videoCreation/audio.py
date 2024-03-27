from elevenlabs import generate, set_api_key, save, RateLimitError
import subprocess
import random
import os

elevenlabs_key = os.environ.get("ELEVENLABS_API_KEY")
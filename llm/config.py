from dotenv import load_dotenv
import os
load_dotenv()
MODEL = os.getenv("MODEL", "llama3.2")

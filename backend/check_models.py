import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env from parent dir
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("No GOOGLE_API_KEY found.")
else:
    genai.configure(api_key=api_key)
    try:
        with open("models.txt", "w") as f:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    f.write(m.name + "\n")
        print("Models written to models.txt")
    except Exception as e:
        print(f"Error listing models: {e}")

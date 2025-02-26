import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def test_openai_config():
    # Load configuration from config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    print(f"Loaded configuration: {config}")
    
    # Load environment variables from .env
    load_dotenv(dotenv_path=config.get('env', '.env'))
    
    # Check if OPENAI_API_KEY is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in .env file")
        return False
    
    print("API key loaded successfully from .env")
    
    try:
        # Initialize the OpenAI client 
        client = OpenAI(
            base_url=config['base_url'],
            api_key=api_key
        )
        
        print(f"Making a test call to {config['model']} model...")
        
        # Make a simple API call
        response = client.chat.completions.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello world!"}
            ],
            temperature=config['temperature'],
            max_tokens=20
        )
        
        # Print response
        message = response.choices[0].message.content
        print(f"Received response: {message}")
        print("\nConnection successful! Your configuration is working.")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to connect to OpenAI API: {str(e)}")
        return False

if __name__ == "__main__":
    test_openai_config()
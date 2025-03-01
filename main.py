import asyncio
import os
from dotenv import load_dotenv
from DeeperSeek import DeepSeek

async def main():
    # Load credentials from .env file
    load_dotenv()
    email = os.getenv("DEEPSEEK_EMAIL")
    password = os.getenv("DEEPSEEK_PASSWORD")
    token = os.getenv("DEEPSEEK_TOKEN")
    
    # Initialize the API with headless mode
    api = DeepSeek(
        email=email,
        password=password,
        token=token,
        headless=True,
        verbose=True
    )
    
    try:
        print("Connecting to DeepSeek...")
        await api.initialize()
        print("Connected successfully!")
        
        # Keep the conversation going until user wants to exit
        while True:
            message = input("\nEnter your message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
                
            use_deepthink = input("Use DeepThink? (y/n): ").lower().startswith('y')
            
            print("Sending message, please wait...")
            response = await api.send_message(
                message,
                deepthink=use_deepthink,
                timeout=180
            )
            
            print("\n" + "=" * 50 + "\nDeepSeek response:\n" + "=" * 50)
            print(response.text)
            
            if hasattr(response, 'deepthink_content') and response.deepthink_content:
                print("\n" + "-" * 30 + " DeepThink content " + "-" * 30)
                print(response.deepthink_content)
                
        print("\nLogging out...")
        await api.logout()
        print("Session ended. Goodbye!")
        
    except Exception as e:
        print(f"\nError occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
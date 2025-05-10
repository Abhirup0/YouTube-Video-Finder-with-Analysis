"""
Text and voice input handling for YouTube Video Finder
Supports both text input and basic voice recognition
"""
import sys
import time

def print_colored(text, color=None, style=None):
    """Print colored text if supported by the terminal"""
    # ANSI color codes
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }
    styles = {
        'bold': '\033[1m',
        'underline': '\033[4m'
    }
    reset = '\033[0m'
    
    prefix = ''
    if color and color in colors:
        prefix += colors[color]
    if style and style in styles:
        prefix += styles[style]
        
    if prefix:
        print(f"{prefix}{text}{reset}")
    else:
        print(text)

def print_header():
    """Print a fancy header for the application"""
    header = """
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃                                                     ┃
    ┃   🎬 YouTube Video Finder with AI Analysis 🔍       ┃
    ┃                                                     ┃
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """
    print_colored(header, 'cyan', 'bold')

def print_menu():
    """Print the input method selection menu"""
    print_colored("\n📋 Choose your input method:", 'yellow', 'bold')
    print_colored("  1️⃣  Text input (type your query)", 'white')
    print_colored("  2️⃣  Voice input (speak your query) 🎤", 'white')
    print()

def get_user_input():
    """
    Get user input as text
    Returns the user's query as a string
    
    Voice input is commented out as optional functionality if SpeechRecognition is installed
    """
    print_header()
    print_menu()
    
    choice = input("Select option (1-2): ").strip()
    
    if choice == '1':
        return get_text_input()
    elif choice == '2':
        return get_voice_input()
    else:
        print_colored("\n❌ Invalid choice. Using text input instead.", 'red')
        return get_text_input()

def get_text_input():
    """Get search query from text input"""
    print_colored("\n🔍 Enter your search query (Hindi or English):", 'green', 'bold')
    print_colored("Examples: 'latest tech news', 'python tutorial', 'cooking recipes'", 'white')
    query = input("> ").strip()
    
    if not query:
        print_colored("\n❌ No query provided.", 'red')
        return None
    
    print_colored(f"\n🔎 Searching for: '{query}'", 'cyan')
    # Add loading animation
    print("Processing", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print("\n")
    
    return query

def get_voice_input():
    """
    Get search query from voice input
    Requires the SpeechRecognition package
    """
    try:
        import speech_recognition as sr
    except ImportError:
        print_colored("\n❌ SpeechRecognition package not installed.", 'red')
        print_colored("   Install with: pip install SpeechRecognition", 'yellow')
        print_colored("   Falling back to text input.", 'yellow')
        return get_text_input()
    
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print_colored("\n🎤 Listening... Speak your search query (Hindi or English)", 'magenta', 'bold')
        print_colored("   (Speak clearly into your microphone)", 'white')
        try:
            # Show preparation
            print_colored("   Adjusting for ambient noise...", 'yellow')
            recognizer.adjust_for_ambient_noise(source)
            
            print_colored("   Ready! Speak now...", 'green', 'bold')
            audio = recognizer.listen(source, timeout=5)
            
            # Try recognition with Google (supports multiple languages)
            print_colored("   Processing speech...", 'cyan')
            # Add loading animation
            print("   ", end="")
            for _ in range(5):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print()
            
            query = recognizer.recognize_google(audio)
            print_colored(f"\n✅ You said: '{query}'", 'green', 'bold')
            
            return query
            
        except sr.WaitTimeoutError:
            print_colored("\n❌ No speech detected. Timeout.", 'red')
            return None
        except sr.UnknownValueError:
            print_colored("\n❌ Could not understand audio.", 'red')
            return None
        except sr.RequestError as e:
            print_colored(f"\n❌ Speech recognition service error: {e}", 'red')
            return None
        except Exception as e:
            print_colored(f"\n❌ Error during voice recognition: {e}", 'red')
            return None 
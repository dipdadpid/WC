import random
import asyncio
import aiohttp
import aiohttp_retry
from colorama import init, Fore, Style
from aiohttp_retry import RetryClient

init(autoreset=True)  # Initialize colorama

CHARACTER_CHOICES = 'abcdefghijklmnopqrstuvwxyz0123456789_.'
NUM_TASKS = 1

USER_AGENT_LIST = [
    # Add a list of user agents here
]

PLATFORMS = {
    'tiktok': 'https://www.tiktok.com/@{}',
    'instagram': 'https://www.instagram.com/{}',
    'twitter': 'https://twitter.com/{}',
    'github': 'https://github.com/{}',
    'facebook': 'https://www.facebook.com/{}',
    'linkedin': 'https://www.linkedin.com/in/{}',
    'snapchat': 'https://www.snapchat.com/add/{}',
    'pinterest': 'https://www.pinterest.com/{}',
    'reddit': 'https://www.reddit.com/user/{}',
    'youtube': 'https://www.youtube.com/user/{}',
    'twitch': 'https://www.twitch.tv/{}',
    'rumble': 'https://rumble.com/user/{}',
    'steam': 'https://steamcommunity.com/id/{}',

}

unavailable_keywords = {
    'tiktok': [
        "This username isn't available.",
        "Sorry, the username you've entered doesn't belong to an account."
    ],
    'instagram': [
        "this username isn't available"
    ],
    'twitter': [
        "This account doesn’t exist",
        "This account has been suspended"
    ],
    'gitHub': [
        "There isn't a GitHub Pages site here",
        "This user does not exist"
    ],
    'facebook': [
        "Sorry, this page isn't available.",
        "The link you followed may be broken, or the page may have been removed."
    ],
    'linkedIn': [
        "This page could not be found.",
        "No LinkedIn account is associated with this URL."
    ],
    'snapchat': [
        "username isn't available",
        "username is already taken"
    ],
    'pinterest': [
        "username is not available",
        "username is already taken"
    ],
    'reddit': [
        "this username isn't available",
        "this username is taken"
    ],
    'youtube': [
        "username isn't available",
        "username is already taken"
    ],
    'twitch': [
        "username is not available",
        "username is already taken"
    ],
    'rumble': [
        "Not found",
        "404"
    ],
    'steam': [
        "the specified profile could not be found.",
        "username is taken",
        "sorry"
    ],
}

availability_statements = {
    'tiktok': {
        'available': False,
        'unavailable': True,
    },
    'instagram': {
        'available': False,
        'unavailable': True,
    },
    'twitter': {
        'available': False,
        'unavailable': True,
    },
    'github': {
        'available': False,
        'unavailable': True,
    },
    'facebook': {
        'available': True,
        'unavailable': False,
    },
    'linkedin': {
        'available': False,
        'unavailable': True,
    },
    'snapchat': {
        'available': False,
        'unavailable': True,
    },
    'pinterest': {
        'available': True,
        'unavailable': False,
    },
    'reddit': {
        'available': True,
        'unavailable': False,
    },
    'youtube': {
        'available': False,
        'unavailable': True,
    },
    'twitch': {
        'available': True,
        'unavailable': False,
    },
    'steam': {
        'available': False,
        'unavailable': True,
    },
    'rumble': {
        'available': True,
        'unavailable': False,
    },
}


async def check_availability(username, platform, session):
    url_template = PLATFORMS.get(platform)
    if not url_template:
        raise ValueError("Invalid platform")

    url = url_template.format(username)

    async with session.get(url) as response:
        if response.status == 404:
            return availability_statements[platform]['unavailable']
        elif response.status == 200:
            content = await response.text()
            lowercase_content = content.lower()

            for keyword in unavailable_keywords.get(platform, []):
                if keyword in lowercase_content:
                    return availability_statements[platform]['unavailable']

            return availability_statements[platform]['available']
        else:
            return availability_statements[platform]['unavailable']

async def save_to_file(filename, username):
    with open(filename, "a") as file:
        file.write(username + '\n')

async def generate_and_check(user_length, platform, session):
    word_list = load_words("words.txt")

    if user_length is not None:
        filename = f"{user_length}_letter_{platform}_list.txt"
    else:
        filename = f"RW_{platform}_list.txt"

    while True:
        if user_length is not None:
            username = generate_username(user_length)
        else:
            username = random.choice(word_list)
            
        is_available = await check_availability(username, platform, session)

        if is_available:
            await save_to_file(filename, username)
            print(f"Username '{username}' is available on {platform} ({Fore.GREEN}available{Style.RESET_ALL}).")
        else:
            print(f"Username '{username}' is not available on {platform} ({Fore.RED}unavailable{Style.RESET_ALL}).")

def generate_username(length):
    return ''.join(random.choice(CHARACTER_CHOICES) for _ in range(length))

def load_words(filename):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words

def print_platform_options():
    print("Available platforms:")
    for platform in PLATFORMS:
        print(f"- {platform}")

async def main():
    logo = """
      __                  __               __                  __     
     /\\ \\  __            /\\ \\             /\\ \\          __    /\\ \\    
     \\_\\ \\/\\_\\  _____    \\_\\ \\     __     \\_\\ \\  _____ /\\_\\   \\_\\ \\   
     /'_` \\/\\ \\/\\ '__`\\  /'_` \\  /'__`\\   /'_` \\/\\ '__`\\/\\ \\  /'_` \\  
    /\\ \\L\\ \\ \\ \\ \\ \\L\\ \\ \\ \\L\\ \\ /\\ \\L\\.\\_/\\ \\L\\ \\ \\ \\L\\ \\ \\ \\/\\ \\L\\ \\ 
    \\ \\___,_\\ \\_\\ \\ ,__/\\ \\___,_\\ \\ \\__/\\_\\ \\___,_\\ \\ ,__\\/\\_\\ \\___,_\\
     \\/__,_ /\\/_/\\ \\ \\/  \\/__,_ /\\/__/\\/_/\\/__,_ /\\ \\ \\/  \\/_/\\/__,_ /
                  \\ \\_\\                            \\ \\_\\              
                   \\/_/                             \\/_/              
    """
    print(f"{Fore.RED}{Style.BRIGHT}{logo}{Style.RESET_ALL}")

    generate_option = input("Generate usernames randomly (R) or from words (W)? ").lower()

    if generate_option not in ['r', 'w']:
        print(Fore.RED + "Invalid choice. Please select 'R' or 'W'.")
        return

    if generate_option == 'r':
        user_length = int(input("Enter the desired username length (3, 4, 5, or 6): "))
        
        print_platform_options()
        selected_platform = input("Enter the platform to check: ").lower()

        if selected_platform not in PLATFORMS:
            print(Fore.RED + "Invalid platform. Please select from the available platforms.")
            return

        async with RetryClient() as session:
            await generate_and_check(user_length, selected_platform, session)

    elif generate_option == 'w':
        print_platform_options()
        selected_platform = input("Enter the platform to check: ").lower()

        if selected_platform not in PLATFORMS:
            print(Fore.RED + "Invalid platform. Please select from the available platforms.")
            return
        
        #word_list = load_words("words.txt")
        
        async with RetryClient() as session:
            await generate_and_check(None, selected_platform, session)

if __name__ == "__main__":
    asyncio.run(main())

from colorama import Fore, Style

name = input("Enter your name: ")

try:
    age = int(input("Please enter your age: "))
    age_in_months = age * 12
    
    print(f"{Fore.CYAN}Hello {name}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}How are you doing?{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}You are {age} years old, which is {age_in_months} months.{Style.RESET_ALL}")
    
    if age >= 18:
        print(f"{Fore.BLUE}You are a Major.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}You are a Minor.{Style.RESET_ALL}")
except ValueError:
    print(f"{Fore.RED}Invalid input! Please enter a numerical age.{Style.RESET_ALL}")

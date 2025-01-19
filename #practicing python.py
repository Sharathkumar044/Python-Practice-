name = input("Enter your name: ")

try:
    age = int(input("Please enter your age: "))
    age_in_months = age * 12
    print("Hello", name)
    print("How are you doing?")
    print(f"You are {age} years old, which is {age_in_months} months.")
    
    if age >= 18:
        print("You are a Major.")
    else:
        print("You are a Minor.")
except ValueError:
    print("Invalid input! Please enter a numerical age.")

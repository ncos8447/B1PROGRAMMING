import string
import random

#Part A

def check_min_length(password, min_length=8):
    return len(password) >= min_length

def has_uppercase(password):
    return any(c.isupper() for c in password)

def has_lowercase(password):
    return any(c.islower() for c in password)

def has_digit(password):
    return any(c.isdigit() for c in password)

def has_special(password):
    return any(char in string.punctuation for char in password)

#Part B

def validate_password(password):
    results = {
      'check_min_length': check_min_length(password),
      'has_uppercase': has_uppercase(password),
      'has_lowercase': has_lowercase(password),
      'has_digit': has_digit(password),
      'has_special': has_special(password)
    }

    results['is_valid'] = all(results.values())

    return results

#Part C

def main():
    print("=" * 50)
    print("PASSWORD STRENGTH VALIDATOR")
    print("=" * 50)
    print("\nPassword Requirements:")
    print("Minimum 8 characters")
    print("At least one uppercase character")
    print("At least one lowercase character")
    print("At least one digit")
    print("At least one special character (!@#$%^&* etc.)")

    password = input("Enter password to validate: ")
    results = validate_password(password)

    print("\n" + "=" * 50)
    print("VALIDATION RESULTS")
    print("=" * 50)

    check_symbol = "7" if results['has_uppercase'] else ""
    print(f"{check_symbol}Contains uppercase: {results['has_uppercase']}")

    check_symbol = "7" if results['has_lowercase'] else ""
    print(f"{check_symbol}Contains lowercase: {results['has_lowercase']}")

    check_symbol = "7" if results['has_digit'] else ""
    print(f"{check_symbol}Contains digit: {results['has_digit']}")

    check_symbol = "7" if results['has_special'] else ""
    print(f"{check_symbol}Contains special character: {results['has_special']}")

    #Result print

    print("\n" + "=" * 50)
    if results['is_valid']:
        print("PASSWORD IS STRONG")
    else:
        print("PASSWORD IS WEAK")
        print("=" * 50)

#Encouragements after results

    encouragements = [
        "You ate that down",
        "Good job I guess",
        "Wow you ACTUALLY did it",
        "Wowza",
        "Boomshakalaka"
]

    if all(results.values()):
        print(random.choice(encouragements))

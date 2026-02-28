import string

#Part A

def check_min_length(password, min_len=8):
    return len(password) >= min_len

def has_uppercase(password):
    return any(char in string.ascii_uppercase for char in password)

def has_lowercase(password):
    return any(char in string.ascii_lowercase for char in password)

def has_digit(password):
    return any(char in string.digits for char in password)

def has_special_char(password):
    return any(char in string.punctuation for char in password)

#Part B

def validate_password(password):
    results = {
        "min_length": check_min_length(password),
        "has_uppercase": has_uppercase(password),
        "has_lowercase": has_lowercase(password),
        "has_digit": has_digit(password),
        "has_special": has_special_char(password)
    }
    results["is_valid"] = all(results.values())
    return results

def user_interface():
    print("PASSWORD VALIDATOR\n"
          "\nPassword requirements:\n"
          "Minimum 8 characters\n"
          "At least one uppercase letter\n"
          "At least one lowercase letter\n"
          "At least one digit\n"
          "At least one special character (!@#$%^&* etc.)\n"
          )

#Part C

    password = str(input("Enter password: "))

    valid = validate_password(password)

    print("")
    check = "✓" if valid["min_length"] else " "
    print(f"{check} Minimum length: {"Met" if valid["min_length"] else "Not met"}\n")

    check = "✓" if valid["has_uppercase"] else " "
    print(f"{check} Contains uppercase: {"Met" if valid["has_uppercase"] else "Not met"}\n")

    check = "✓" if valid["has_lowercase"] else " "
    print(f"{check} Contains lowercase: {"Met" if valid["has_lowercase"] else "Not met"}\n")

    check = "✓" if valid["has_digit"] else " "
    print(f"{check} Contains digit: {"Met" if valid["has_digit"] else "Not met"}\n")

    check = "✓" if valid["has_special"] else " "
    print(f"{check} Contains special character: {"Met" if valid["has_special"] else "Not met"}\n")

    if valid["is_valid"]:
        print("Password is strong\n")
    else:
        print("Password is weak\n")

    if not valid["min_length"]:
        print(f"Password is too short")

    if not valid["has_uppercase"]:
        print(f"Add an uppercase letter")

    if not valid["has_lowercase"]:
        print(f"Add a lowercase letter")

    if not valid["has_digit"]:
        print(f"Add a number")

    if not valid["has_special"]:
        print(f"Add a special character")


print()

user_interface()
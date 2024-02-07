import bleach
def sanitize_input(user_input):
    sanitized_input = bleach.clean(user_input)
    return sanitized_input

def not_valid(user_input):
    print("we check if user input is valid...")
    if len(user_input) > 400:
        return True
    return False
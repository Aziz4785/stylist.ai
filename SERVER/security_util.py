import bleach
def sanitize_input(user_input):
    sanitized_input = bleach.clean(user_input)
    return sanitized_input

def not_valid(user_input):
    if len(user_input) > 400 or len(user_input)<2:
        return True
    return False
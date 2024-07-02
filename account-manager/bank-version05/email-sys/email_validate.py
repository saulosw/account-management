structure_email = "@gmail.com"

def check_structure_email(user_email: str) -> bool:
    if structure_email in user_email:
        return True
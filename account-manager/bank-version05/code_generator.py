from secrets import SystemRandom
import string

def generate_client_code():
    client_code = ''.join(SystemRandom().choices(string.ascii_letters + string.digits, k=6))
    return client_code
def calculate_check_digit(cpf, initial_weight):
    total_sum = 0
    for index in range(len(cpf)):
        total_sum += int(cpf[index]) * (initial_weight - index)
    remainder = total_sum % 11
    return 0 if remainder < 2 else 11 - remainder

def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * len(cpf):
        return False
    
    first_check_digit = calculate_check_digit(cpf[:9], 10)
    second_check_digit = calculate_check_digit(cpf[:9] + str(first_check_digit), 11)
    
    return cpf[-2:] == f"{first_check_digit}{second_check_digit}"
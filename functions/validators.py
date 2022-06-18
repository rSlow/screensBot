def validate_name(name: str, words=3):
    list_initials = name.split()
    if len(list_initials) < words:
        return False

    last_initial = list_initials[-1]
    first_initials = list_initials[:-1]

    if len(last_initial) == 1:
        if last_initial.isalpha():
            last_initial += "."

    elif len(last_initial) > 2:
        last_initial = last_initial[0] + "."

    first_initials.append(last_initial)

    validated_name = " ".join(
        map(str.capitalize, first_initials)
    )

    return validated_name


def validate_sum(transfer_sum: str):
    transfer_sum_edited = transfer_sum.replace(",", ".")
    try:
        float_transfer_sum = round(float(transfer_sum_edited), 2)
        int_transfer_sum = int(float_transfer_sum)
        if float_transfer_sum == int_transfer_sum:
            return int_transfer_sum
        else:
            return float_transfer_sum
    except ValueError:
        return False


def validate_phone_num(phone_num: str):
    digits = list(filter(str.isdigit, phone_num))

    if (digits[0] == "8" or digits[0] == "7") and len(digits) == 11:
        digits[0] = "+7"
    elif digits[0] == "9" and len(digits) == 10:
        digits.insert(0, "+7")
    else:
        return False

    return f"{digits[0]} " \
           f"({''.join(digits[1:4])})" \
           f" {''.join(digits[4:7])}" \
           f"-{''.join(digits[7:9])}" \
           f"-{''.join(digits[9:11])}"

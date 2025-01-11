def check_name(name):
    for word in name.split(" "):
        if not word.isalpha():
            return False

    return True


def check_age(age):
    if not age.isdigit():
        return False

    age = int(age)
    return 0 < age <= 120

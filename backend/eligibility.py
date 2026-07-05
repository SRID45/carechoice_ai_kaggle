def check_eligibility(user):
    if user["age"] >= 65:
        return "Medicare"
    elif user["income"] < 40000:
        return "Medicaid"
    else:
        return "Commercial"

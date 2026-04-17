ALLOWED_EXPENSE_CATEGORIES = {
    "platform_software",
    "market_data",
    "analytics_research",
    "internet_phone",
    "cloud_it_security",
    "professional_fees",
    "office_supplies",
    "home_office",
    "bank_fees",
    "education",
}


def validate_expense_category(category: str):
    if category not in ALLOWED_EXPENSE_CATEGORIES:
        raise ValueError(f"Unsupported expense category: {category}")

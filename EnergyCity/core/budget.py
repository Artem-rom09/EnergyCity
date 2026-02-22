# core/budget.py

def update_budget(city, spent, savings, base_budget=100):
    remaining = city.budget
    city.budget = base_budget + remaining + savings
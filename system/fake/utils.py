"""Utilities for database seeding"""
from random import randint
from faker import Faker

fake = Faker()

def generate_currency():
    """Generate some currency"""
    return randint(0, 900_000)

import pandas as pd


# Функция для нахождения минимальной цены
def find_min_fare(data):
    return data["Fare"].min()


# Функция для нахождения максимальной цены
def find_max_fare(data):
    return data["Fare"].max()


# Функция для нахождения средней цены
def find_avg_fare(data):
    return data["Fare"].mean()

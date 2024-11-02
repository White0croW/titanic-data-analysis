from io import BytesIO
import pytest
import pandas as pd
from app import process_uploaded_files, load_data
from func import (
    find_min_fare,
    find_max_fare,
    find_avg_fare,
)

# Тестовые данные
test_csv_path = "test_titanic_train.csv"
test_image = "titanic.jpg"
test_csv_path = "test_titanic_train.csv"


# Фикстуры для тестирования
@pytest.fixture
def test_data():
    return pd.read_csv(test_csv_path)


# Тесты для функции find_min_fare
def test_find_min_fare(test_data):
    # Вызов функции
    min_fare = find_min_fare(test_data)

    # Проверка, что результат является числом
    assert isinstance(min_fare, (int, float))

    # Проверка, что результат совпадает с ожидаемым
    expected_min_fare = test_data["Fare"].min()
    assert min_fare == expected_min_fare


# Тесты для функции find_max_fare
def test_find_max_fare(test_data):
    # Вызов функции
    max_fare = find_max_fare(test_data)

    # Проверка, что результат является числом
    assert isinstance(max_fare, (int, float))

    # Проверка, что результат совпадает с ожидаемым
    expected_max_fare = test_data["Fare"].max()
    assert max_fare == expected_max_fare


# Тесты для функции find_avg_fare
def test_find_avg_fare(test_data):
    # Вызов функции
    avg_fare = find_avg_fare(test_data)

    # Проверка, что результат является числом
    assert isinstance(avg_fare, (int, float))

    # Проверка, что результат совпадает с ожидаемым
    expected_avg_fare = test_data["Fare"].mean()
    assert avg_fare == expected_avg_fare


# Тесты для функции process_uploaded_files
def test_process_uploaded_files(test_image):
    # Сохранение изображения в буфер
    image_bytes = BytesIO()
    test_image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Вызов функции
    result_image_bytes, caption = process_uploaded_files(image_bytes)

    # Проверка, что результат является изображением
    assert isinstance(result_image_bytes, BytesIO)

    # Проверка, что результат является строкой (описание)
    assert isinstance(caption, str)


# Тесты для функции load_data
def test_load_data(test_csv):
    # Вызов функции
    data = load_data()

    # Проверка, что результат является DataFrame
    assert isinstance(data, pd.DataFrame)

    # Проверка, что данные совпадают с тестовыми данными
    pd.testing.assert_frame_equal(data, test_csv)

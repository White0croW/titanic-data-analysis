# test_model.py
import pytest
from io import BytesIO
from PIL import Image
from app import (
    process_uploaded_files,
)


@pytest.fixture
def sample_image():
    # Создание тестового изображения
    image = Image.new("RGB", (100, 100), color="blue")
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return image_bytes


def test_process_uploaded_files(sample_image):
    # Обработка тестового изображения
    image_bytes, caption = process_uploaded_files(sample_image)

    # Проверка, что изображение сохранено корректно
    assert image_bytes is not None

    # Проверка, что описание сгенерировано корректно
    assert isinstance(caption, str)
    assert len(caption) > 0

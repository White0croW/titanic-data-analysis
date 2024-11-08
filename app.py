import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from io import BytesIO
import pandas as pd
from func import (
    find_min_fare,
    find_max_fare,
    find_avg_fare,
)

# Загрузка модели и процессора
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# Настройка параметров процессора
processor.clean_up_tokenization_spaces = True


# Функция для обработки загруженных файлов
def process_uploaded_files(uploaded_file):
    # Открытие загруженного изображения
    image = Image.open(uploaded_file)

    # Проверка формата изображения и преобразование в PNG, если необходимо
    if image.format.lower() not in ["png", "jpeg", "jpg"]:
        image = image.convert("RGB")
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        image = Image.open(image_bytes)

    # Подготовка изображения для модели
    inputs = processor(images=image, return_tensors="pt")

    # Генерация описания
    outputs = model.generate(**inputs, max_new_tokens=20)
    caption = processor.decode(
        outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True
    )

    # Сохранение изображения в буфер для отображения
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    return image_bytes, caption


# Загрузка данных
def load_data():
    try:
        data = pd.read_csv("titanic_train.csv")
        return data
    except FileNotFoundError:
        st.error(
            "Файл titanic_train.csv не найден. Пожалуйста, убедитесь, что файл существует."
        )
        return None


# Основная функция приложения
def main():
    st.title("Генерация описания для картинок")

    # Загрузка изображения
    uploaded_file = st.file_uploader(
        "Загрузите изображение", type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        # Обработка загруженного файла
        image_bytes, caption = process_uploaded_files(uploaded_file)

        # Отображение изображения и описания
        st.image(image_bytes, caption="Загруженное изображение", use_column_width=True)
        st.write(f"Сгенерированное описание: {caption}")

    st.title("Анализ данных пассажиров Титаника")

    # Загрузка данных
    data = load_data()
    if data is not None:
        # Добавление картинки перед заголовком
        try:
            st.image("titanic.jpg", caption="Titanic", use_column_width=True)
        except FileNotFoundError:
            st.error(
                "Изображение titanic.jpg не найдено. Пожалуйста, убедитесь, что файл существует."
            )

        # Добавление селектора для выбора статистики
        fare_option = st.selectbox(
            "Выберите статистику цены билета:",
            ["Минимальная", "Максимальная", "Средняя"],
        )

        # Фильтрация данных для мужчин и женщин
        male_data = data[data["Sex"] == "male"].dropna(subset=["Fare"])
        female_data = data[data["Sex"] == "female"].dropna(subset=["Fare"])

        # Нахождение минимальной, максимальной и средней цены билета для мужчин
        min_fare_male = find_min_fare(male_data)
        max_fare_male = find_max_fare(male_data)
        avg_fare_male = find_avg_fare(male_data)

        # Нахождение минимальной, максимальной и средней цены билета для женщин
        min_fare_female = find_min_fare(female_data)
        max_fare_female = find_max_fare(female_data)
        avg_fare_female = find_avg_fare(female_data)

        # Отображение результатов в зависимости от выбора
        st.subheader("Статистика цен билетов для мужчин")
        if fare_option == "Минимальная":
            st.write(f"Минимальная цена билета: {min_fare_male}")
            st.dataframe(male_data[male_data["Fare"] == min_fare_male][["Sex", "Fare"]])
        elif fare_option == "Максимальная":
            st.write(f"Максимальная цена билета: {max_fare_male}")
            st.dataframe(male_data[male_data["Fare"] == max_fare_male][["Sex", "Fare"]])
        elif fare_option == "Средняя":
            st.write(f"Средняя цена билета: {avg_fare_male:.2f}")
            avg_fare_df_male = pd.DataFrame({"Sex": ["male"], "Fare": [avg_fare_male]})
            st.dataframe(avg_fare_df_male)

        st.subheader("Статистика цен билетов для женщин")
        if fare_option == "Минимальная":
            st.write(f"Минимальная цена билета: {min_fare_female}")
            st.dataframe(
                female_data[female_data["Fare"] == min_fare_female][["Sex", "Fare"]]
            )
        elif fare_option == "Максимальная":
            st.write(f"Максимальная цена билета: {max_fare_female}")
            st.dataframe(
                female_data[female_data["Fare"] == max_fare_female][["Sex", "Fare"]]
            )
        elif fare_option == "Средняя":
            st.write(f"Средняя цена билета: {avg_fare_female:.2f}")
            avg_fare_df_female = pd.DataFrame(
                {"Sex": ["female"], "Fare": [avg_fare_female]}
            )
            st.dataframe(avg_fare_df_female)


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from io import BytesIO
import requests

# Загрузка модели и процессора
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


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
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    # Сохранение изображения в буфер для отображения
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    return image_bytes, caption


# Загрузка данных
def load_data():
    data = pd.read_csv("titanic_train.csv")
    return data


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

    # Добавление картинки перед заголовком
    st.image("titanic.jpg", caption="Titanic", use_column_width=True)

    # Добавление селектора для выбора статистики
    fare_option = st.selectbox(
        "Выберите статистику цены билета:", ["Минимальная", "Максимальная", "Средняя"]
    )

    # Фильтрация данных для мужчин и женщин
    male_data = data[data["Sex"] == "male"].dropna(subset=["Fare"])
    female_data = data[data["Sex"] == "female"].dropna(subset=["Fare"])

    # Нахождение минимальной, максимальной и средней цены билета для мужчин
    min_fare_male = male_data["Fare"].min()
    max_fare_male = male_data["Fare"].max()
    avg_fare_male = male_data["Fare"].mean()

    # Нахождение минимальной, максимальной и средней цены билета для женщин
    min_fare_female = female_data["Fare"].min()
    max_fare_female = female_data["Fare"].max()
    avg_fare_female = female_data["Fare"].mean()

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

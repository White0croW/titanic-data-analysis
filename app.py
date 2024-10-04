import streamlit as st
import pandas as pd


# Загрузка данных
def load_data():
    data = pd.read_csv("titanic_train.csv")
    return data


# Основная функция приложения
def main():
    st.title("Анализ данных пассажиров Титаника")

    # Загрузка данных
    data = load_data()

    # Фильтрация данных для мужчин
    male_data = data[data["Sex"] == "male"]

    # Удаление строк с пропущенными значениями в поле 'Fare'
    male_data = male_data.dropna(subset=["Fare"])

    # Нахождение минимальной, максимальной и средней цены билета
    min_fare = male_data["Fare"].min()
    max_fare = male_data["Fare"].max()
    avg_fare = male_data["Fare"].mean()

    # Добавление картинки перед заголовком
    st.image("titanic.jpg", caption="Titanic", use_column_width=True)

    # Добавление селектора для выбора статистики
    fare_option = st.selectbox(
        "Выберите статистику цены билета:", ["Минимальная", "Максимальная", "Средняя"]
    )

    # Отображение результатов в зависимости от выбора
    st.subheader("Статистика цен билетов для мужчин")
    if fare_option == "Минимальная":
        st.write(f"Минимальная цена билета: {min_fare}")
        st.dataframe(male_data[male_data["Fare"] == min_fare])
    elif fare_option == "Максимальная":
        st.write(f"Максимальная цена билета: {max_fare}")
        st.dataframe(male_data[male_data["Fare"] == max_fare])
    elif fare_option == "Средняя":
        st.write(f"Средняя цена билета: {avg_fare:.2f}")
        st.dataframe(male_data)


if __name__ == "__main__":
    main()

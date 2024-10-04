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

    # Отображение данных в табличном виде
    st.subheader("Данные пассажиров")
    st.dataframe(data)

    # Фильтрация данных для мужчин
    male_data = data[data["Sex"] == "male"]

    # Удаление строк с пропущенными значениями в поле 'Fare'
    male_data = male_data.dropna(subset=["Fare"])

    # Нахождение минимальной, максимальной и средней цены билета
    min_fare = male_data["Fare"].min()
    max_fare = male_data["Fare"].max()
    avg_fare = male_data["Fare"].mean()

    # Отображение результатов
    st.subheader("Статистика цен билетов для мужчин")
    st.write(f"Минимальная цена билета: {min_fare}")
    st.write(f"Максимальная цена билета: {max_fare}")
    st.write(f"Средняя цена билета: {avg_fare:.2f}")


if __name__ == "__main__":
    main()

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

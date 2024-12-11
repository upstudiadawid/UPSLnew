import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Funkcja do wczytywania danych z pamięcią podręczną Streamlit
@st.cache
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Dodanie przykładowych nowych kolumn dla analizy
if "Payment Method" not in data.columns:
    data["Payment Method"] = np.random.choice(["Card", "Cash", "Transfer"], size=len(data))

if "Customer Satisfaction" not in data.columns:
    data["Customer Satisfaction"] = np.random.randint(1, 6, size=len(data))

if "Store Type" not in data.columns:
    data["Store Type"] = np.random.choice(["Online", "Physical"], size=len(data))

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry wiekowe i kategorie produktów
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())

# Filtrowanie danych
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter))]

# Wyświetlanie filtrowanych danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy analizy wizualnej
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots()
category_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
season_mean.plot(kind="bar", ax=ax)
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
filtered_data["Age"].hist(bins=20, ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)

# Wykres 4: Średnia kwota zakupów wg formy płatności
st.write("### Średnia kwota zakupów wg formy płatności")
if "Payment Method" in filtered_data.columns:
    payment_mean = filtered_data.groupby("Payment Method")["Purchase Amount (USD)"].mean()
    fig, ax = plt.subplots()
    payment_mean.plot(kind="bar", ax=ax)
    ax.set_xlabel("Forma płatności")
    ax.set_ylabel("Średnia kwota zakupów (USD)")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące formy płatności nie są dostępne.")

# Wykres 5: Dystrybucja ocen satysfakcji klientów
st.write("### Dystrybucja ocen satysfakcji klientów")
if "Customer Satisfaction" in filtered_data.columns:
    fig, ax = plt.subplots()
    filtered_data["Customer Satisfaction"].hist(bins=5, ax=ax)
    ax.set_xlabel("Ocena satysfakcji")
    ax.set_ylabel("Liczba klientów")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące ocen satysfakcji nie są dostępne.")

# Wykres 6: Liczba zakupów wg rodzaju sklepu
st.write("### Liczba zakupów wg rodzaju sklepu")
if "Store Type" in filtered_data.columns:
    store_counts = filtered_data["Store Type"].value_counts()
    fig, ax = plt.subplots()
    store_counts.plot(kind="bar", ax=ax)
    ax.set_xlabel("Rodzaj sklepu")
    ax.set_ylabel("Liczba zakupów")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące rodzaju sklepu nie są dostępne.")

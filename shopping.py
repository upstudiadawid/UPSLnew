import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

if "Subcategory" not in data.columns:
    data["Subcategory"] = np.random.choice(["Electronics", "Clothing", "Home", "Toys", "Books"], size=len(data))

if "Gender" not in data.columns:
    data["Gender"] = np.random.choice(["Male", "Female"], size=len(data))

if "Region" not in data.columns:
    data["Region"] = np.random.choice(["North", "South", "East", "West"], size=len(data))

if "Discount Used" not in data.columns:
    data["Discount Used"] = np.random.choice(["Yes", "No"], size=len(data))

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry wiekowe i kategorie produktów
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
gender_filter = st.sidebar.selectbox("Płeć klienta", ["Wszystkie", "Male", "Female"], index=0)
region_filter = st.sidebar.multiselect("Region", data["Region"].unique(), data["Region"].unique())
discount_filter = st.sidebar.radio("Czy klient użył zniżki?", ["Wszystkie", "Yes", "No"], index=0)

# Filtrowanie danych
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter))]

if gender_filter != "Wszystkie":
    filtered_data = filtered_data[filtered_data["Gender"] == gender_filter]

if discount_filter != "Wszystkie":
    filtered_data = filtered_data[filtered_data["Discount Used"] == discount_filter]

if region_filter:
    filtered_data = filtered_data[filtered_data["Region"].isin(region_filter)]

# Wyświetlanie filtrowanych danych
st.write("### Filtrowane dane", filtered_data)

# Wykresy analizy wizualnej
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax, palette="viridis")
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots()
sns.barplot(x=season_mean.index, y=season_mean.values, ax=ax, palette="coolwarm")
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots()
sns.histplot(filtered_data["Age"], bins=20, kde=True, color="blue", ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
st.pyplot(fig)

# Wykres 4: Średnia kwota zakupów wg formy płatności
st.write("### Średnia kwota zakupów wg formy płatności")
if "Payment Method" in filtered_data.columns:
    payment_mean = filtered_data.groupby("Payment Method")["Purchase Amount (USD)"].mean()
    fig, ax = plt.subplots()
    sns.barplot(x=payment_mean.index, y=payment_mean.values, ax=ax, palette="magma")
    ax.set_xlabel("Forma płatności")
    ax.set_ylabel("Średnia kwota zakupów (USD)")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące formy płatności nie są dostępne.")

# Wykres 5: Dystrybucja ocen satysfakcji klientów
st.write("### Dystrybucja ocen satysfakcji klientów")
if "Customer Satisfaction" in filtered_data.columns:
    fig, ax = plt.subplots()
    sns.histplot(filtered_data["Customer Satisfaction"], bins=5, kde=False, color="green", ax=ax)
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
    sns.barplot(x=store_counts.index, y=store_counts.values, ax=ax, palette="Set2")
    ax.set_xlabel("Rodzaj sklepu")
    ax.set_ylabel("Liczba zakupów")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące rodzaju sklepu nie są dostępne.")

# Wykres 7: Zakupy wg podkategorii
st.write("### Zakupy wg podkategorii produktów")
if "Subcategory" in filtered_data.columns:
    subcategory_counts = filtered_data["Subcategory"].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=subcategory_counts.index, y=subcategory_counts.values, ax=ax, palette="cubehelix")
    ax.set_xlabel("Podkategoria")
    ax.set_ylabel("Liczba zakupów")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące podkategorii nie są dostępne.")

# Wykres 8: Korelacja między oceną satysfakcji a kwotą zakupu
st.write("### Korelacja między oceną satysfakcji a kwotą zakupu")
if "Customer Satisfaction" in filtered_data.columns and "Purchase Amount (USD)" in filtered_data.columns:
    fig, ax = plt.subplots()
    sns.scatterplot(x=filtered_data["Customer Satisfaction"], 
                    y=filtered_data["Purchase Amount (USD)"], ax=ax, color="purple")
    ax.set_xlabel("Ocena satysfakcji")
    ax.set_ylabel("Kwota zakupu (USD)")
    st.pyplot(fig)
else:
    st.write("Dane dotyczące korelacji nie są dostępne.")

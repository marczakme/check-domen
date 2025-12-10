import io
import pandas as pd
import streamlit as st

# Konfiguracja strony
st.set_page_config(page_title="Porównywarka domen", layout="centered")

st.title("🔍 Porównywarka domen – cennik vs. domeny klienta")

st.write(
    """
    Wgraj dwa pliki XLSX:

    1. **Cennik** – domeny w **kolumnie A**  
    2. **Lista domen klienta** – domeny w **kolumnie A**  

    Aplikacja uzupełni kolumnę **B** w cenniku wpisując:  
    - **TAK**, jeśli domena znajduje się w liście klienta  
    - **NIE**, jeśli jej nie ma.
    """
)

# Upload plików
cennik_file = st.file_uploader("Plik Cennik (XLSX)", type=["xlsx"])
domeny_file = st.file_uploader("Plik Lista domen klienta (XLSX)", type=["xlsx"])

if st.button("🚀 Przetwórz pliki"):

    if cennik_file is None or domeny_file is None:
        st.error("❗ Wgraj oba pliki przed przetworzeniem.")
    else:
        try:
            # Wczytanie danych z plików
            cennik = pd.read_excel(cennik_file)
            domeny = pd.read_excel(domeny_file)

            # Normalizacja domen – bierzemy pierwszą kolumnę (A)
            cennik_domains = (
                cennik.iloc[:, 0]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            klient_domains = (
                domeny.iloc[:, 0]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            domeny_set = set(klient_domains)

            # Jeżeli nie ma kolumny B – dodaj pustą
            if cenn

import io
import pandas as pd
import streamlit as st

# ----------------------------------------------------
# Konfiguracja aplikacji
# ----------------------------------------------------
st.set_page_config(page_title="Porównywarka domen", layout="centered")

st.title("🔍 Porównywarka domen – cennik vs. domeny klienta")

st.write(
    """
    Wgraj dwa pliki XLSX:

    1. **Cennik** – domeny w **kolumnie A**  
    2. **Lista domen klienta** – domeny w **kolumnie A**  

    Aplikacja uzupełni kolumnę **B** wpisując:  
    - **TAK** – jeśli domena znajduje się w liście klienta  
    - **NIE** – jeśli jej nie ma
    """
)

# ----------------------------------------------------
# Upload plików
# ----------------------------------------------------
cennik_file = st.file_uploader("Plik Cennik (XLSX)", type=["xlsx"])
domeny_file = st.file_uploader("Plik Lista domen klienta (XLSX)", type=["xlsx"])

# ----------------------------------------------------
# Logika przetwarzania
# ----------------------------------------------------
if st.button("🚀 Przetwórz pliki"):

    if cennik_file is None or domeny_file is None:
        st.error("❗ Wgraj oba pliki przed przetwarzaniem.")
    else:
        try:
            # Wczytywanie plików
            cennik = pd.read_excel(cennik_file)
            domeny = pd.read_excel(domeny_file)

            # Normalizacja domen (kolumna A)
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

            # ----------------------------------------------------
            # Dodanie kolumny B jeśli nie istnieje
            # ----------------------------------------------------
            if cennik.shape[1] < 2:
                cennik.insert(1, "B", "")

            # Uzupełnianie TAK / NIE
            cennik.iloc[:, 1] = cennik_domains.apply(
                lambda d: "TAK" if d in domeny_set else "NIE"
            )

            # ----------------------------------------------------
            # Przygotowanie pliku wynikowego
            # ----------------------------------------------------
            output = io.BytesIO()
            cennik.to_excel(output, index=False)
            output.seek(0)

            st.success("✅ Plik został poprawnie przetworzony!")

            st.download_button(
                "📥 Pobierz cennik_wynik.xlsx",
                data=output,
                file_name="cennik_wynik.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
            )

            st.write("🔎 Podgląd pierwszych wierszy:")
            st.dataframe(cennik.head())

        except Exception as e:
            st.error(f"❌ Błąd przetwarzania: {e}")

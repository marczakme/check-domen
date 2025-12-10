import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Porównywarka domen", layout="centered")

st.title("🔍 Porównywarka domen – cennik vs. domeny klienta")

st.write(
    """
    Wgraj dwa pliki XLSX:
    1. **Cennik** – domeny w kolumnie A  
    2. **Lista domen klienta** – domeny w kolumnie A  
    
    Aplikacja uzupełni kolumnę **B** w cenniku wpisując:  
    - **TAK**, jeśli domena znajduje się w liście klienta  
    - **NIE**, jeśli jej nie ma  
    """
)

cennik_file = st.file_uploader("Plik Cennik (XLSX)", type=["xlsx"])
domeny_file = st.file_uploader("Plik Lista domen klienta (XLSX)", type=["xlsx"])

if st.button("🚀 Przetwórz pliki"):

    if not cennik_file or not domeny_file:
        st.error("❗ Wgraj oba pliki.")
    else:
        try:
            cennik = pd.read_excel(cennik_file)
            domeny = pd.read_excel(domeny_file)

            cennik_domains = cennik.iloc[:, 0].astype(str).strip().str.lower()
            klient_domains = domeny.iloc[:, 0].astype(str).strip().str.lower()

            domeny_set = set(klient_domains)

            if cennik.shape[1] < 2:
                cennik.insert(1, "B", "")

            cennik.iloc[:, 1] = cennik_domains.apply(
                lambda d: "TAK" if d in domeny_set else "NIE"
            )

            output = io.BytesIO()
            cennik.to_excel(output, index=False)
            output.seek(0)

            st.success("✅ Gotowe! Możesz pobrać wynik poniżej:")

            st.download_button(
                "📥 Pobierz cennik_wynik.xlsx",
                data=output,
                file_name="cennik_wynik.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

            st.write("🔎 Podgląd wyniku:")
            st.dataframe(cennik.head())

        except Exception as e:
            st.error(f"❌ Błąd przetwarzania: {e}")

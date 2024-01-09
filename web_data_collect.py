import streamlit as st
import requests
import json
import os

# Initialize environment variables
env_airtable_token = os.getenv('AIRTABLE_TOKEN')
env_base_id = os.getenv('BASE_ID')
env_table_id = os.getenv('TABLE_ID')

# URL and headers for Airtable API
url2 = f"https://api.airtable.com/v0/{env_base_id}/{env_table_id}"
headers = {
    "Authorization": "Bearer " + str(env_airtable_token),
    "Content-Type": "application/json",
}

# Options for selectboxes
options_list = ["Inspekcje", "Incydenty", "Aplikacja", "Osoby", "Powiadomienia", "Raporty", "Konfiguracja", "Raporty", "Systemowe", "Handlowe", "Funkcjonalne"]
options_list2 = ["Adam", "Asia", "Ewa", "Kira", "Maria", "Sławek"]

# Streamlit UI layout
st.header("Zbieranie danych dla systemu KOIOS")
st.subheader("ver.1.9")

# Initialize session state for input fields and success message flag
if 'input1' not in st.session_state:
    st.session_state['input1'] = ""
if 'input2' not in st.session_state:
    st.session_state['input2'] = ""
if 'show_success' not in st.session_state:
    st.session_state['show_success'] = False

# Input fields
input1 = st.text_input("Pytanie:", value=st.session_state['input1'], key='input1')
input2 = st.text_area("Odpowiedź", value=st.session_state['input2'], key='input2')
selected_option = st.selectbox("Wybierz sekcję", options_list)
selected_option2 = st.selectbox("Osoba uzupełniająca dane", options_list2)

# Prepare data to send to Airtable
data = {
    "fields": {
        "Question": input1,
        "Answer": input2,
        "Section": selected_option,
        "Person": selected_option2
    }
}

# Button to save data
if st.button("Zapisz"):
    if input1.strip() and input2.strip():
        response = requests.post(url2, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            st.session_state['show_success'] = True
            st.session_state['input1'] = ''
            st.session_state['input2'] = ''
            st.experimental_rerun()
        else:
            st.error("Airtable post error: Status code " + str(response.status_code))
    else:
        st.warning("Wypełnij wszytkie pola")

# Display success message
if st.session_state['show_success']:
    st.success("Dane zapisane pomyślnie")
    st.session_state['show_success'] = False

if st.button('Pobierz z wszytkimi pytaniami formacie CSV'):
    records = fetch_all_records(url2, headers)
    if records:
        csv_data = convert_to_csv(records)
        st.download_button(
            label="Pobierz CSV",
            data=csv_data,
            file_name='airtable_data.csv',
            mime='text/csv',
        )
    else:
        st.error("Błąd przy pobieraniu danych z Airtable")


def main():
    exit()


if __name__ == "__main__":
    main()

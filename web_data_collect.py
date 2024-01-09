import streamlit as st
import requests
import json
import os
import io
import pandas as pd

# from configuration import airtable_token, base_id, table_id

env_airtable_token = os.getenv('AIRTABLE_TOKEN')
env_base_id = os.getenv('BASE_ID')
env_table_id = os.getenv('TABLE_ID')

# Initialize session state variables for input1 and input2
if 'input1' not in st.session_state:
    st.session_state['input1'] = ""
if 'input2' not in st.session_state:
    st.session_state['input2'] = ""
if 'input_key' not in st.session_state:
    st.session_state['input_key'] = 0  # Initial key for input widgets




# auth url and headers
url2 = f"https://api.airtable.com/v0/{env_base_id}/{env_table_id}"
headers = {
    "Authorization": "Bearer " + str(env_airtable_token),
    "Content-Type": "application/json",
}
# clases of answers
options_list = ["Inspekcje", "Incydenty", "Aplikacja", "Osoby", "Powiadomienia", "Raporty", "Konfiguracja", "Raporty",
                "Systemowe", "Handlowe", "Funkcjonalne"]
options_list2 = ["Adam", "Asia", "Ewa", "Kira", "Maria", "Sławek"]
st.header("Zbieranie danych dla systemu KOIOS")
st.subheader("ver.1.9")

response = requests.get(url2, headers=headers)  # authenticate in airtable

input1 = st.text_input("Pytanie:", value=st.session_state['input1'], key=f'input1_{st.session_state["input_key"]}')
input2 = st.text_area("Odpowiedź", value=st.session_state['input2'], key=f'input2_{st.session_state["input_key"]}')


selected_option = st.selectbox("Wybierz sekcję", options_list)
selected_option2 = st.selectbox("Osoba uzupełniająca dane", options_list2)

data_to_save = f"{input1},{input2},{selected_option},{selected_option},\n"
print(data_to_save)
data = {
    "fields": {
        "Question": f"{input1}",
        "Answer": f"{input2}",
        "Section": f"{selected_option}",
        "Person": f"{selected_option2}"
        # Add other fields here.
    }
}


def fetch_all_records(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)['records']
    else:
        return None


# Function to convert records to CSV.
def convert_to_csv(records):
    # Ensure that all records have a 'fields' key and the value is a dictionary
    valid_records = [record['fields'] for record in records if
                     'fields' in record and isinstance(record['fields'], dict)]

    # Convert the valid records to a DataFrame
    df = pd.DataFrame(valid_records)

    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()


# save collected inputrs to airbase
if st.button("Zapisz"):
    if input1.strip() and input2.strip():  # Use strip to check for non-empty strings
        response = requests.post(url2, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            # Clear the session state variables
            st.session_state['input1'] = ''
            st.session_state['input2'] = ''
            # Increment the key to force refresh the input widgets
            st.session_state['input_key'] += 1
            st.success("Dane zapisane pomyślnie")
            st.rerun()
        else:
            st.error("Airtable post error: Status code " + str(response.status_code))
    else:
        st.warning("Wypełnij wszytkie pola")

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

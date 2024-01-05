import streamlit as st
import requests
import json
import os

# from configuration import airtable_token, base_id, table_id

env_airtable_token = os.getenv('AIRTABLE_TOKEN')
env_base_id = os.getenv('BASE_ID')
env_table_id = os.getenv('TABLE_ID')

# auth url and headers
url2 = f"https://api.airtable.com/v0/{env_base_id}/{env_table_id}"
headers = {
    "Authorization": "Bearer " + str(env_airtable_token),
    "Content-Type": "application/json",
}
# clases of answers
options_list = ["Inspekcje", "Incydenty", "Aplikacja", "Osoby", "Konfiguracja", "Raporty", "Systemowe"]
options_list2 = ["Adam", "Asia", "Ewa", "Kira", "Maria", "Sławek"]
st.header("Zbieranie danych dla KOIOS")
st.subheader("ver.1.5")

response = requests.get(url2, headers=headers)  # authenticate in airtable

input1 = st.text_input("Pytanie:")
input2 = st.text_area("Odpowiedź")
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
        # Add other fields here
    }
}

# save collected inputrs to airbase
if st.button("Zapisz"):
    if input1 and input2:
        response = requests.post(url2, headers=headers, data=json.dumps(data))  # push to airtable
        if response.status_code == 200:
            pass
        else:
            print("Airtable post error")
    else:
        st.warning("Wypełnij wszytkie pola")


if st.button("Pokaż wszystkie pytania"):
    get_response = requests.get(url2, headers=headers)
    print(get_response)
    if get_response.status_code == 200:
        all_records = json.loads(get_response.text)['records']
        for record in all_records:
            st.write(record['fields'])
    else:
        st.error("Błąd przy pobieraniu danych")
def main():
    exit()


if __name__ == "__main__":
    main()

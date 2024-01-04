import streamlit as st
import requests
import json
from configuration import airtable_token, base_id, table_id

# auth url and headers
url2 = f"https://api.airtable.com/v0/{base_id}/{table_id}"
headers = {
    "Authorization": "Bearer " + str(airtable_token),
    "Content-Type": "application/json",
}
# clases of answers
options_list = ["Inspekcje", "Incydenty", "Mobilne", "Osoby"]
st.title("Zbieranie danych do KOIOS v.1.3")

response = requests.get(url2, headers=headers)  # authenticate in airtable

input1 = st.text_input("Pytanie:")
input2 = st.text_input("Odpowiedź")
selected_option = st.selectbox("Choose an option", options_list)

data_to_save = f"{input1},{input2},{selected_option},\n"
print(data_to_save)
data = {
    "fields": {
        "Question": f"{input1}",
        "Answer": f"{input2}",
        "Section": f"{selected_option}",
        "Person": "default",
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


def main():
    exit()


if __name__ == "__main__":
    main()

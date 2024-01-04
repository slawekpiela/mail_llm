import streamlit as st
import requests
import json
import os
#from configuration import airtable_token, base_id, table_id


env_airtable_token = os.getenv('AIRTABLE_TOKEN')
env_base_id = os.getenv('BASE_ID')
env_table_id = os.getenv('TABLE_ID')

print(env_airtable_token)

# auth url and headers
url2 = f"https://api.airtable.com/v0/{env_base_id}/{env_table_id}"
headers = {
    "Authorization": "Bearer " + str(env_airtable_token),
    "Content-Type": "application/json",
}
# clases of answers
options_list = ["Inspekcje", "Incydenty", "Mobilne", "Osoby"]
st.title("Zbieranie danych do KOIOS v.1.4")

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

if st.button("Pokaż wszystkie pytania"):

    response=requests.get(url2,headers=headers)
    data3= json.loads(response.text)
    for record in data3['records']:
        print(record['fields'])

        # url3=url2+"/rec1"
        # response2 = requests.get(url3, headers=headers, data=json.dumps(data))  # push to airtable
        # if response.status_code == 200:
        #    print("all",response2)
        # else:
        #     print("Airtable post error")



def main():
    exit()


if __name__ == "__main__":
    main()

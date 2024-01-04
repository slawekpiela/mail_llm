import streamlit as st
import requests
from configuration import airtable_token, base_id, table_id

url2 = f"https://api.airtable.com/v0/{base_id}/{table_id}"

print(url2)

headers = {
    "Authorization": "Bearer " + str(airtable_token),
    "Content-Type": "application/json",
}

response = requests.get(url2, headers=headers)
print("resp:", response)

if response.status_code == 200:
    print("OK")
else:
    print("nok")


options_list = ["Inspekcje", "Incydenty", "Mobilne", "Osoby"]  # clases of answers
st.title("Zbieranie danych do KOIOS v.1.2")
if "input1" not in st.session_state:
    st.session_state.input1 = ""

# Create one text input boxes
# Create three text input boxes
input1 = st.text_input("Pytanie:")
input2 = st.text_input("Odpowiedź")
selected_option = st.selectbox("Choose an option", options_list)

data_to_save = f"{input1},{input2},{selected_option},\n"
print(data_to_save)

        # Add other fields here
    }
}


# Create a button that when clicked, shows a message with the input values
if st.button("Zapisz"):
    if input1 and input2:
        with open("output.txt", "a") as file:
            file.write(data_to_save)

            print(data_to_save)
    else:
        st.warning("Wypełnij wszytkie pola")


def main():
    exit()


if __name__ == "__main__":
    main()

import streamlit as st

def main():exit()
options_list = ["Inspekcje", "Incydenty", "Mobilne", "Osoby"]

st.title("Zbieranie danych do KOIOS")

# Create two text input boxes
input1 = st.text_input("Pytanie:")
input2 = st.text_input("Odpowiedź")
selected_option = st.selectbox("Choose an option", options_list)

data_to_save=f'{input1},{input2},{st.selectbox}'
print(data_to_save)

# Create a button that when clicked, shows a message with the input values
if st.button('Zapisz'):
    with open('output.txt', 'w') as file:
        file.write(data_to_save)
    st.success('Data successfully saved to "output.txt"')
print(data_to_save)

if __name__ == "__main__":
    main()

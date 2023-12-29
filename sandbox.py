import streamlit as st

def main():exit()
st.title("Simple Streamlit App")

# Create two text input boxes
input1 = st.text_input("Enter first value")
input2 = st.text_input("Enter second value")

# Create a button that when clicked, shows a message with the input values
if st.button("Show Inputs"):
        st.success(f"You entered: {input1} and {input2}")

if __name__ == "__main__":
    main()

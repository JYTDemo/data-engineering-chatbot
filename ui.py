import streamlit as st
from main import datachat as dc

data_file = "./data/input/data.csv"
uploaded_file = st.file_uploader("Choose a file")
# Write the uploaded file to a specific location
if uploaded_file is not None:
    with open(data_file, "wb") as f:
        f.write(uploaded_file.read())

#chat_object= dc(file_path='./data/employees.csv')
chat_object= dc(file_path=data_file)

st.title("Data Engineering Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == 'user':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if message["role"] == 'assistant':
        with st.chat_message(message["role"]):
            st.dataframe(message["content"],hide_index=True)


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chat_object.data_ops(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        #st.markdown(response)
        st.dataframe(response,hide_index=True)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# split the salary and define 10% as HRA, 70% as Basic and 20% as Allowance.
# mask the SSN columns as *********1234
# convert the hire date column from string to date time and format it as DD-MON-YYYY
# combine the first name and last name columns
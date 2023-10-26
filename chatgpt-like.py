import openai
import streamlit as st

openai.api_key = "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"
# openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("ChatGPT-like")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write("User")
        st.markdown(prompt)
        print("prompt:", prompt, "\n")

    with st.chat_message("assistant"):
        st.write("Chatbot")
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    print("st.session_state:\n", st.session_state, "\n")
    print("st.session_state.messages:\n", st.session_state.messages, "\n")

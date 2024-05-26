from openai import OpenAI
import streamlit as st 
import json
import os

def main():

    client = OpenAI(api_key=st.secrets["openai_key"])

    st.set_page_config(
    page_title="Assistant",
    page_icon="🥫",
    )

    product_details_str = json.dumps(st.session_state['prodDetails'])




    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = [ {"role": "system", "content": f'You are a nutrition assistant. Answer questions regarding this product,{product_details_str}'}]

    

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    if prompt := st.chat_input("Any doubts?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()

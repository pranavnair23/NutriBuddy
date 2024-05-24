from openai import OpenAI
import streamlit as st 
import json
import os

def main():

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    st.set_page_config(
    page_title="Assistant",
    page_icon="🥫",
    )

    product_details = {
    "product_name": "Britannia NutriChoice Digestive High Fibre Biscuits",
    "product_image": "https://www.bigbasket.com/media/uploads/p/l/40197803_7-britannia-nutrichoice-digestive-high-fibre-biscuits-super-saver-family-pack.jpg",
    "category": "Snacks & Branded Foods",
    "subcategory": "Biscuits & Cookies",
    "type": "Marie, Health, Digestive",
    "ingredients": "Refined Wheat Flour, Whole Wheat Flour, Edible Vegetable Oil (Palm), Sugar, Wheat Bran, Liquid Glucose, Milk Solids, Maltodextrin, Raising Agents (503, 500), Iodised Salt, Emulsifiers (322, 471, 472E), Malt Extract, Dough Conditioner (223)",
    "nutrition_facts": {
        "Sodium": 0.0,
        "Protein": 8.0,
        "Calories": 493.0,
        "Total Fat": {
            "Value": 21.0,
            "Trans Fat": 0.0,
            "Saturated Fat": 10.0,
            "Monounsaturated Fat": 8.5,
            "Polyunsaturated Fat": 2.5
        },
        "Cholesterol": 0.0,
        "Carbohydrates": {
            "Value": 68.0,
            "Total Sugars": {
                "Value": 14.5,
                "Added Sugars": None
            },
        "Dietary Fiber": 6.0
        }
    },
    "price": 85,
    "brand": "D"
}

    product_details_str = json.dumps(product_details)




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

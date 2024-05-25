import streamlit as st 
import cv2
import numpy as np
from PIL import Image
from openai import OpenAI
import mysql.connector
import json
import re
import matplotlib.pyplot as plt
import os


def main():

    st.set_page_config(
    page_title="Homepage",
    page_icon="🥫",
    )

    client = OpenAI(api_key=st.secrets["openai_key"])
    
    connection = mysql.connector.connect(
        host="mysql-19ebb7c1-nutribuddy.a.aivencloud.com",
        port=10331,
        user=" avnadmin",
        password=st.secrets["db_password"],
        database="PRODUCTS"
    )

    

    cursor = connection.cursor()

    if 'imageCaptured' not in st.session_state.keys():
        st.session_state['imageCaptured'] = None
    
    if 'ean' not in st.session_state.keys():
        st.session_state['ean'] = None
    
    
    if 'prodNo' not in st.session_state.keys():
        st.session_state['prodNo'] = None


    #st.markdown("<h1 style='text-align: center; '>NutriBuddy</h1>", unsafe_allow_html=True)
    st.title("NutriBuddy🔎")
    with st.container(height=350):
        st.markdown("### How this works:")
        st.markdown("1. **Scan Barcode**:  Use the scanner in the sidebar to scan the barcode of the item you want to explore.  ")    
        st.markdown("2. **Nutritional Information**:  Once scanned, all the nutritional information will be displayed on the home page for your reference.  ")
        st.markdown("3. **Navigate to Assistant**:  You can easily navigate to the assistant page via the sidebar.  ")  
        st.markdown("4. **Assistant Queries**:  On the assistant page, feel free to ask any queries related to the product or its ingredients. The assistant is here to help you with any questions you may have.  ") 
    

    with st.sidebar:    

        captureQrCode = st.camera_input("Scan the barcode here ", key = "captureQrCode", help = "Make sure the image barcode is clearly visible ")

        if captureQrCode:
            st.session_state['imageCaptured'] = captureQrCode

        if st.session_state['imageCaptured']:
            img = Image.open(st.session_state['imageCaptured'])
            openCVimage = np.array(img)
            barCodeDetector = cv2.barcode.BarcodeDetector()
            data = barCodeDetector.detectAndDecode(openCVimage)
            if img:
                if data[0]: 
                    st.session_state['ean'] = int(data[0])
                else:
                    st.write("Barcode not scanned, please try again!")
    
    st.divider()
    if st.session_state['ean']:
        #cursor.execute(f"Select product_no from eans where ean={st.session_state['ean']}")
        #buff = cursor.fetchone()
        #prodNo = buff[0]

        #cursor.execute(f"SELECT * from products where product_no={prodNo}")
        #st.session_state['prodDetails'] = cursor.fetchone()

        cursor.execute("SELECT * from products where product_no=1")
        details = cursor.fetchone()
        
        st.header(details[1])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image(details[2])
        with col3:
            st.write(' ')

        st.write(f"Keywords: {details[5]}, {details[4]}, {details[3]}")

        col4,col5 = st.columns(2)

        with col4:
            with st.container(height=250):
                st.markdown("### Ingredients List")
                pattern = r",(?!\s*\d)"
                ingredients = re.split(pattern,details[6])  
                c=1
                for i in ingredients:
                    st.write(f'{c}. {i}')
                    c+=1 
        with col5:
            with st.container(height=250):
                st.markdown("### Allergen Information")
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Give allergen risks in concise list format"},
                        {"role": "user", "content": f"{details[6]}"}],
                    temperature=0,
                    max_tokens=1000
                    )
                st.write(response.choices[0].message.content)


        nutri = json.loads(details[7])
        protein = nutri["Protein"]
        total_fat = nutri["Total Fat"]["Value"]
        carbohydrates = nutri["Carbohydrates"]["Value"]
        sugar = nutri['Carbohydrates']['Total Sugars']['Value']
        Cholesterol = nutri['Cholesterol']
        fiber = nutri['Carbohydrates']['Dietary Fiber']

        labels = ['Protein', 'Total Fat', 'Carbohydrates']
        values = [protein, total_fat, carbohydrates]

        plt.style.use('bmh')
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        tab1, tab2 = st.tabs(["Macronutrient Distribution", "Other Information"])
        with tab1:
            st.pyplot(fig)
        with tab2:
            col1, col2, col3 = st.columns(3)
            col1.metric("Sugar", f"{sugar} gms")
            col2.metric("Cholesterol", f"{Cholesterol} mgs")
            col3.metric("Dietary Fiber", f"{fiber} gms")



    



        

    

if __name__ == '__main__':
    main()

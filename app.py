import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def get_country_data(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]
    return None

def display_country_info(country):
    st.title(country['name']['common'])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        flag_url = country['flags']['png']
        response = requests.get(flag_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f"Flag of {country['name']['common']}", use_column_width=True)
    
    with col2:
        st.write(f"**Official Name:** {country['name']['official']}")
        st.write(f"**Capital:** {', '.join(country['capital']) if 'capital' in country else 'N/A'}")
        st.write(f"**Population:** {country['population']:,}")
        st.write(f"**Region:** {country['region']}")
        st.write(f"**Subregion:** {country['subregion']}")
        st.write(f"**Currency:** {', '.join([v['name'] for v in country['currencies'].values()]) if 'currencies' in country else 'N/A'}")
        st.write(f"**Language(s):** {', '.join(country['languages'].values()) if 'languages' in country else 'N/A'}")

# Streamlit App UI
st.set_page_config(page_title="Country Info Cards", layout="centered")
st.header("🌍 Country Information Cards")

country_name = st.text_input("Enter a country name:")

if st.button("Get Info"):
    if country_name:
        country_data = get_country_data(country_name)
        if country_data:
            display_country_info(country_data)
        else:
            st.error("Country not found. Please check the spelling and try again.")
    else:
        st.warning("Please enter a country name.")

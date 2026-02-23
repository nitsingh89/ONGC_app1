import streamlit as st
import requests
from bs4 import BeautifulSoup

URL = "http://10.207.195.198/dynparm_2.htm"

st.set_page_config(page_title="ONGC Live Pressure", layout="centered")
st.title("ONGC – Live Pressure Monitor")

st.markdown(
    "<meta http-equiv='refresh' content='5'>",
    unsafe_allow_html=True
)

def fetch_pressure():
    try:
        r = requests.get(URL, timeout=5)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.find("td", class_="gross")

        if tag:
            value = float(tag.text.strip())
            return value, "LIVE FROM DCS"
        else:
            return None, "TAG NOT FOUND"

    except Exception as e:
        return None, f"ERROR: {e}"

pressure, status = fetch_pressure()

if pressure is not None:
    st.success(status)
    st.metric("Pressure (kgf/cm²)", pressure)
else:
    st.error(status)

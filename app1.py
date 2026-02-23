import streamlit as st
import requests
from bs4 import BeautifulSoup

INTRANET_URL = "http://10.207.195.198/dynparm_2.htm"

st.set_page_config(page_title="ONGC Live Pressure", layout="centered")
st.title("ONGC – Live Pressure Monitor")

def fetch_pressure():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
            "Connection": "keep-alive"
        }

        r = requests.get(INTRANET_URL, headers=headers, timeout=5)

        soup = BeautifulSoup(r.text, "html.parser")

        tag = soup.find("td", {"id": "drk"})

        if tag:
            value = float(tag.text.strip())
            return value, "LIVE"

        return None, "TAG NOT FOUND"

    except Exception as e:
        return None, f"INTRANET ERROR: {e}"
pressure, status = fetch_pressure()

if pressure:
    st.metric("Pressure (kgf/cm²)", f"{pressure}")
    st.success("LIVE DATA FROM DCS")
else:
    st.error(status)


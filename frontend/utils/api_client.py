import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

class APIClient:
    @staticmethod
    def _get_headers():
        headers = {}
        token = st.session_state.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @classmethod
    def _get_session(cls):
        # Cache requests.Session in Streamlit session state to reuse TCP connections (Keep-Alive)
        if "api_session" not in st.session_state:
            st.session_state["api_session"] = requests.Session()
        return st.session_state["api_session"]

    @classmethod
    def get(cls, endpoint: str, params: dict = None):
        try:
            url = f"{BACKEND_URL}{endpoint}"
            session = cls._get_session()
            response = session.get(url, headers=cls._get_headers(), params=params)
            return response
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the SmartBuy AI backend server. Please verify it is running on port 8000.")
            return None

    @classmethod
    def post(cls, endpoint: str, data: dict = None, json_data: dict = None):
        try:
            url = f"{BACKEND_URL}{endpoint}"
            session = cls._get_session()
            response = session.post(url, headers=cls._get_headers(), data=data, json=json_data)
            return response
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the SmartBuy AI backend server. Please verify it is running on port 8000.")
            return None

    @classmethod
    def delete(cls, endpoint: str, params: dict = None):
        try:
            url = f"{BACKEND_URL}{endpoint}"
            session = cls._get_session()
            response = session.delete(url, headers=cls._get_headers(), params=params)
            return response
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the SmartBuy AI backend server. Please verify it is running on port 8000.")
            return None

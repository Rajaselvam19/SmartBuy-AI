import streamlit as st
from utils.api_client import APIClient

class AuthHelper:
    @staticmethod
    def login(email: str, password: str) -> bool:
        # OAuth2 password flow expects form data (data=...) instead of JSON
        response = APIClient.post(
            "/api/auth/login", 
            data={"username": email, "password": password}
        )
        if response and response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["user"] = data["user"]
            st.success("Successfully logged in!")
            return True
        elif response:
            error_detail = response.json().get("detail", "Incorrect email or password")
            st.error(f"Login failed: {error_detail}")
        return False

    @staticmethod
    def register(name: str, email: str, password: str) -> bool:
        response = APIClient.post(
            "/api/auth/register", 
            json_data={"name": name, "email": email, "password": password}
        )
        if response and response.status_code == 201:
            st.success("Successfully registered! Please switch to the Log In tab to access your account.")
            return True
        elif response:
            error_detail = response.json().get("detail", "Registration failed")
            st.error(f"Registration failed: {error_detail}")
        return False

    @staticmethod
    def logout():
        st.session_state.pop("token", None)
        st.session_state.pop("user", None)
        st.session_state.pop("selected_category", None)
        st.session_state.pop("query_results", None)
        st.session_state.pop("selected_product_id", None)
        st.session_state.pop("compare_list", None)
        st.success("Logged out successfully!")
        st.switch_page("app.py")

    @staticmethod
    def is_logged_in() -> bool:
        return "token" in st.session_state and st.session_state["token"] is not None

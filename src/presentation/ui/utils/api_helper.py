import streamlit as st
import requests

def get_auth_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def authenticated_request(method: str, endpoint: str, **kwargs):
    headers = get_auth_headers()
    if "headers" in kwargs:
        headers.update(kwargs["headers"])
        del kwargs["headers"]
    return requests.request(method, endpoint, headers=headers, **kwargs)
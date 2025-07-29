import streamlit as st
from auth import login_page
from phones import display_inventory

# Session to store login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def main():
    st.set_page_config(page_title="Refurbished Phone Seller", layout="wide")

    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.title("📦 Inventory & Listing")
        platform = st.sidebar.selectbox("Select Selling Platform", ["Platform X", "Platform Y", "Platform Z"])
        display_inventory(platform)

if __name__ == "__main__":
    main()

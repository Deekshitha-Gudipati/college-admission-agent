import streamlit as st
import pandas as pd
from rag_chatbot import ask_ibm_granite

st.set_page_config(page_title="College Admission Agent", layout="centered")

# --- Caching data loading ---
@st.cache_data
def load_college_data():
    return pd.read_csv("colleges.csv")

colleges_df = load_college_data()

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Load users ---
def load_users():
    try:
        df = pd.read_csv("users.csv")
        return dict(zip(df.username, df.password))
    except:
        return {}

# --- Save new user ---
def save_user(username, password):
    with open("users.csv", "a") as f:
        f.write(f"{username},{password}\n")

# --- Sidebar for Login/Register ---
st.sidebar.title("🔐 Login / Register")
auth_mode = st.sidebar.radio("Select Option", ["Login", "Register"])

if auth_mode == "Login":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid credentials!")

elif auth_mode == "Register":
    new_user = st.sidebar.text_input("New Username")
    new_pass = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Register"):
        users = load_users()
        if new_user in users:
            st.warning("Username already exists!")
        else:
            save_user(new_user, new_pass)
            st.success("Registration successful. You can now login.")

# --- Main App Content ---
st.title("🎓 College Admission Assistant Chatbot")

if st.session_state.logged_in:
    st.markdown(f"Hello **{st.session_state.username}**, ask anything below!")

    # --- College Recommender ---
    with st.expander("🎯 Get College Recommendation"):
        marks = st.number_input("Enter your Intermediate Marks (out of 1000):", min_value=0, max_value=1000, step=10)
        eamcet_rank = st.number_input("Enter your EAMCET Rank:", min_value=0, max_value=200000, step=1000)
        location = st.selectbox("Preferred Location", sorted(colleges_df['district'].unique()))

        if st.button("Recommend Colleges"):
            filtered = colleges_df[
                (colleges_df["district"] == location) &
                (colleges_df["cutoff_rank"] >= eamcet_rank)
            ].sort_values("cutoff_rank")
            if not filtered.empty:
                st.success("🎉 Recommended Colleges:")
                st.dataframe(filtered[["college_name", "branch", "cutoff_rank"]])
            else:
                st.warning("No matching colleges found for your input. Try changing filters.")

    # --- RAG Chatbot ---
    st.markdown("### 🤖 Ask our AI Chatbot")
    user_query = st.text_area("Ask a question related to admission, branches, location, etc.")

    if st.button("Get Answer"):
        if user_query.strip() != "":
            with st.spinner("Generating answer using IBM Granite model..."):
                try:
                    answer = ask_ibm_granite(user_query)
                    st.success("✅ Answer:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")

else:
    st.info("🔐 Please login or register to use the assistant.")

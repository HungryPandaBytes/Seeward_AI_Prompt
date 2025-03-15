import streamlit as st
from openai import OpenAI
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader  
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Set the page width
st.set_page_config(layout="wide")  # Makes the app use the full width of the page

# Custom CSS to modify padding
st.markdown("""
<style>
    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def load_config():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def save_config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def register_user(username, name, password):
    if not username or not name or not password:
        return "Please fill in all fields"
    
    config = load_config()
    if username in config['credentials']['usernames']:
        return "Username already exists"
    
    config['credentials']['usernames'][username] = {
        'name': name,
        'password': password,
        'permission_level': 'viewer',  # Add default permission level, 
        'email':'random@email.com'
    }
    save_config(config)
    return "Registration successful"

def analyze_security_data(csv_data, question):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return
    
    model = "gpt-3.5-turbo"
    
    # Create a summary of the CSV data to include in the prompt
    data_summary = csv_data.head(10).to_string()
    
    messages = [
        {"role": "system", "content": "You are a cybersecurity expert who analyzes scanner data and provides insights."},
        {"role": "user", "content": f"Here's some scanner data (first 10 rows as sample):\n\n{data_summary}\n\nThe complete dataset has {len(csv_data)} rows and columns: {', '.join(csv_data.columns.tolist())}.\n\nBased on this data, please provide insights on: {question}. Can you explain how you came up with recommended insights?"}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


def main_app():
    st.title("🔒 Cybersecurity Insights Assistant")

    st.markdown('Upload scanner data to get cybersecurity insights.')
    
    uploaded_file = st.file_uploader("Upload your scanner data CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file into a pandas DataFrame
        csv_data = pd.read_csv(uploaded_file)
        
        # Display a sample of the data
        st.subheader("Data Preview")
        st.dataframe(csv_data.head())
        
        # Allow user to ask specific questions about the data
        question = st.text_area("What insights would you like to get from this data?", 
                               "Identify the top 5 critical vulnerabilities from this scan data that pose the highest risk, and provide specific mitigation steps.")
        
        if st.button('Generate Insights'):
            with st.spinner('Analyzing data...'):
                insights = analyze_security_data(csv_data, question)
                
                st.subheader("Security Insights")
                st.write(insights)


def main():
    
    # Create default config if it doesn't exist
    try:
        config = load_config()
    except FileNotFoundError:
        config = {
            'credentials': {
                'usernames': {}
            },
            'cookie': {
                'name': 'auth_token',
                'key': 'random_signature_key',
                'expiry_days': 30
            }
        }
        save_config(config)

    # Create the authenticator object
    authenticator = stauth.Authenticate(
        credentials=config['credentials'],
        cookie_name=config['cookie']['name'],
        key=config['cookie']['key'],
        cookie_expiry_days=config['cookie']['expiry_days']
    )

    
    with st.sidebar:

        # Login/Register tabs
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab2:
            st.header("Register")
            with st.form("register_form"):
                reg_username = st.text_input("Username")
                reg_name = st.text_input("Name")
                reg_password = st.text_input("Password", type="password")
                register_button = st.form_submit_button("Register")
                
                if register_button:
                    result = register_user(reg_username, reg_name, reg_password)
                    st.write(result)

        with tab1:
            try: 
                authenticator.login('main')

            except Exception as e:
                st.error(f"An error occurred: {e}")

            if st.session_state.get('authentication_status'):
                st.write(f'Welcome *{st.session_state["name"]}*')
                authenticator.logout('Logout')

    
    if st.session_state.get('authentication_status'):


        main_tab1, main_tab2, main_tab3 = st.tabs(["AI Insights", "CISO", "Developer"])

        with main_tab1:

            if st.session_state.get('authentication_status'):
                main_app()
            
            

        with main_tab2:
            # Define the URL of your Looker Studio report
            report_url = "https://lookerstudio.google.com/reporting/f3ad9ed5-bf70-436f-9793-6dec28a6fe81"

            # Create an iframe to embed the report
            st.components.v1.html(
                f"""
                <iframe
                    width="100%"
                    height="700"
                    src="{report_url}"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
                """,
                height=700,
            )

        with main_tab3:
            # Define the URL of your Looker Studio report
            report_url = "https://lookerstudio.google.com/embed/reporting/67160775-9563-45e9-a9e7-a01b3bb00868/page/p_f2mnuhz8pd"

            # Create an iframe to embed the report
            st.components.v1.html(
                f"""
                <iframe
                    width="100%"
                    height="700"
                    src="{report_url}"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
                """,
                height=700,
            )

    elif st.session_state.get('authentication_status') == False:
            st.error('Username/password is incorrect')
    else:
        st.warning('Please enter your username and password')


            
if __name__ == '__main__':
    main()
import streamlit as st
from openai import OpenAI
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader  
import os

# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

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
    
    hashed_password = stauth.generate_hash(password)
    config['credentials']['usernames'][username] = {
        'name': name,
        'password': hashed_password
    }
    save_config(config)
    return "Registration successful"

def analyze_text(text):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return
    
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are an assistant who helps craft social media posts."},
        {"role": "user", "content": f"Please help me write a social media post based on the following:\n{text}"}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def generate_image(text):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return

    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def main_app():
    st.title('🤖 AI Content Assistant')
    st.markdown('I was made to help you craft interesting Social media posts.')
    
    user_input = st.text_area("Enter a brief for your post:", "Panda eating a big fake cake")

    if st.button('Generate Post Content'):
        with st.spinner('Generating Text...'):
            post_text = analyze_text(user_input)
            st.write(post_text)

        with st.spinner('Generating Thumbnail...'):
            thumbnail_url = generate_image(user_input)
            st.image(thumbnail_url, caption='Generated Thumbnail')


def main():
    st.title("My Application")
    
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
            authenticator.logout('main')
            st.write(f'Welcome *{st.session_state["name"]}*')
            main_app()
        elif st.session_state.get('authentication_status') == False:
            st.error('Username/password is incorrect')
        else:
            st.warning('Please enter your username and password')

if __name__ == '__main__':
    main()
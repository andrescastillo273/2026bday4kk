import streamlit as st
import google.generativeai as genai
import random

# Page Configuration
st.set_page_config(page_title="For Kate ❤️", page_icon="✨", layout="centered")

# Hide Streamlit's default menu and footer for a cleaner look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Authenticate with Google AI Studio using Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-flash-latest')
except KeyError:
    st.error("API Key not found. Please set GEMINI_API_KEY in Streamlit Secrets.")

def get_affirmation_and_horoscope():
    prompt = """
    Write a short, unique, and highly personalized positive affirmation for my girlfriend, Kate. 
    She is 26, a USPTO attorney, a former college soccer player, a hopeless romantic, a left-leaning Republican, and fiercely loyal. 
    She loves horses, cooking, fitness, museums, decorating her apartment, and concerts. 
    She also manages ADHD, anxiety, debt, and a close but difficult relationship with her family.

    Instructions:
    1. Validate how hard she works and how much she is loved.
    2. Pick just 1 or 2 of her interests or traits to weave into the message naturally (don't list them all, keep it fresh each time).
    3. Provide a sweet, empowering affirmation to soothe her anxiety and ADHD.
    4. Provide a short, ultra-positive daily horoscope for a Libra (born Oct 4).
    5. Keep the tone warm, loving, encouraging, and authentic.

    Format exactly like this in Markdown:
    ### ✨ Just For You, Kate
    [Your affirmation here]

    ### ♎ Today's Libra Horoscope
    [Your horoscope here]
    """
    response = model.generate_content(prompt)
    return response.text

def get_short_affirmation():
    prompt = """
    Write a very short, punchy 1 to 2 sentence maximum positive affirmation for my girlfriend, Kate. 
    She is an incredibly hardworking 26-year-old USPTO attorney who manages anxiety and ADHD. 
    Make it a quick, empowering pick-me-up that reminds her she is deeply loved and totally capable.
    Do not include a horoscope or any extra text.
    """
    response = model.generate_content(prompt)
    return response.text

def get_rotating_image():
    # Rotate between the requested themes
    themes = ['dog', 'cat', 'horse', 'beach', 'mountains', 'rainfall']
    choice = random.choice(themes)
    
    # We add a random number to the URL so the browser doesn't cache the previous image
    cache_buster = random.randint(1, 10000)
    return f"https://loremflickr.com/800/600/{choice}?random={cache_buster}"

# --- UI Design ---
st.title("✨ A Little Positivity for Kate ✨")
st.write("Whenever things feel heavy, or you just need a reminder of how amazing you are, push a button.")

# Create two buttons side-by-side
col1, col2 = st.columns(2)

with col1:
    full_vibes = st.button("Push for Good Vibes ✨", type="primary", use_container_width=True)

with col2:
    quick_vibes = st.button("Quick Dose of Sunshine ☀️", use_container_width=True)

# Logic for Button 1 (Full message + Horoscope)
if full_vibes:
    with st.spinner("Gathering love, horoscopes, and good vibes..."):
        message = get_affirmation_and_horoscope()
        img_url = get_rotating_image()
        
        st.markdown(message)
        st.image(img_url, use_column_width=True)
        st.balloons()

# Logic for Button 2 (Short 1-2 sentences)
if quick_vibes:
    with st.spinner("Catching a quick ray of sunshine..."):
        message = get_short_affirmation()
        
        # FIX FOR THE FONT ISSUE: Strip out AI line breaks so Markdown treats it all as one single header block
        message = message.replace("\n", " ")
        img_url = get_rotating_image()
        
        st.markdown(f"### 💛 {message}")
        st.image(img_url, use_column_width=True)
        st.snow()

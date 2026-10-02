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

def stream_affirmation_and_horoscope():
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
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text

def stream_short_affirmation():
    prompt = """
    Write a very short, punchy 1 to 2 sentence maximum positive affirmation for my girlfriend, Kate. 
    She is an incredibly hardworking 26-year-old USPTO attorney who manages anxiety and ADHD. 
    Make it a quick, empowering pick-me-up that reminds her she is deeply loved and totally capable.
    Do not include a horoscope or any extra text. Do not use line breaks.
    """
    response = model.generate_content(prompt, stream=True)
    yield "### 💛 " 
    for chunk in response:
        yield chunk.text.replace("\n", " ")

def get_rotating_image():
    # A curated, fail-proof list of high-quality Unsplash images
    images = [
        "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=800&q=80", 
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1495360010541-f48722b34f7d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1598974357801-cb86b72946c1?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80", 
        "https://images.unsplash.com/photo-1449158743715-0a90ebb6d2d8?auto=format&fit=crop&w=800&q=80", 
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80", 
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80", 
        "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=800&q=80"  
    ]
    return random.choice(images)

# --- UI Design ---
st.title("✨ A Little Positivity for Kate ✨")
st.write("Whenever things feel heavy, or you just need a reminder of how amazing you are, push a button.")

col1, col2 = st.columns(2)

with col1:
    full_vibes = st.button("Push for Good Vibes ✨", type="primary", use_container_width=True)

with col2:
    quick_vibes = st.button("Quick Dose of Sunshine ☀️", use_container_width=True)

# Logic for Button 1 (Full message + Horoscope)
if full_vibes:
    try:
        img_url = get_rotating_image()
        st.image(img_url, use_column_width=True)
        
        st.write_stream(stream_affirmation_and_horoscope())
        st.balloons()
    except Exception as e:
        # Catch-all for ANY error during the streaming process
        if "429" in str(e) or "Quota" in str(e) or "ResourceExhausted" in str(e):
            st.warning("💛 Whoa there! The universe is gathering vibes as fast as it can. Take a deep breath and try the button again in about a minute.")
        else:
            st.warning("✨ The cosmic connection stuttered for a second. Try pushing the button again!")

# Logic for Button 2 (Short 1-2 sentences)
if quick_vibes:
    try:
        img_url = get_rotating_image()
        st.image(img_url, use_column_width=True)
        
        st.write_stream(stream_short_affirmation())
    except Exception as e:
        # Catch-all for ANY error during the streaming process
        if "429" in str(e) or "Quota" in str(e) or "ResourceExhausted" in str(e):
            st.warning("💛 Whoa there! The universe is gathering vibes as fast as it can. Take a deep breath and try the button again in about a minute.")
        else:
            st.warning("✨ The cosmic connection stuttered for a second. Try pushing the button again!")

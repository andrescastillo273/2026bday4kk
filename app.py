import streamlit as st
import google.generativeai as genai
import random
import requests

# Page Configuration
st.set_page_config(page_title="For Kate ❤️️", page_icon="✨", layout="centered")

# Hide Streamlit's default menu and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Authenticate with Google AI Studio
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        'gemini-flash-latest',
        generation_config=genai.types.GenerationConfig(temperature=0.9)
    )
except KeyError:
    st.error("API Key not found. Please set GEMINI_API_KEY in Streamlit Secrets.")

def get_dynamic_elements():
    traits = [
        "her days playing college soccer",
        "her demanding work as a USPTO attorney",
        "her love for horses",
        "her passion for cooking",
        "her dedication to fitness",
        "her love for museums and learning",
        "her eye for decorating her apartment",
        "her love for live concerts and friends",
        "her fiercely loyal nature",
        "her hopeless romantic heart"
    ]
    vibes = [
        "deeply romantic and comforting",
        "fiercely empowering (major hype-energy)",
        "gentle, cozy, and soothing to help her ADHD/anxiety",
        "incredibly proud and validating of her hard work",
        "lighthearted, playful, and uplifting"
    ]
    return random.sample(traits, 2), random.choice(vibes)

def stream_affirmation_and_horoscope():
    selected_traits, vibe = get_dynamic_elements()
    
    prompt = f"""
    Write a short, totally unique positive affirmation for my girlfriend, Kate. 
    She is 26 (born Oct 4) and manages anxiety, ADHD, debt, and tricky family dynamics.
    
    CRITICAL INSTRUCTIONS TO MAKE THIS UNIQUE:
    1. Write this in a {vibe} tone.
    2. ONLY mention these two things about her: {selected_traits[0]} and {selected_traits[1]}. Do not list any of her other hobbies.
    3. Remind her she is totally capable and deeply loved.
    4. Provide a short, ultra-positive daily horoscope for a Libra.
    
    Format exactly like this in Markdown:
    ### ✨ Just For You, Kate
    [Your dynamic affirmation here]

    ### ♎ Today's Libra Horoscope
    [Your horoscope here]
    """
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text

def stream_short_affirmation():
    selected_traits, vibe = get_dynamic_elements()
    
    prompt = f"""
    Write a completely unique, 1 to 2 sentence positive affirmation for my girlfriend, Kate. 
    She is a 26-year-old USPTO attorney who manages anxiety and ADHD.
    
    CRITICAL INSTRUCTIONS:
    1. Write this in a {vibe} tone.
    2. Briefly weave in a reference to {selected_traits[0]}.
    3. Make it a quick, empowering pick-me-up. Do not include a horoscope. Do not use line breaks.
    """
    response = model.generate_content(prompt, stream=True)
    yield "### 💛 " 
    for chunk in response:
        yield chunk.text.replace("\n", " ")

def get_rotating_image():
    themes = ['dog', 'cat', 'horse', 'beach', 'mountains', 'rainfall', 'forest cabin', 'ocean waves', 'national park']
    query = random.choice(themes)
    
    # The fail-safe backup list just in case the API limit is hit
    fallback_images = [
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
    
    if "last_image" not in st.session_state:
        st.session_state.last_image = None

    try:
        # Search the entire Unsplash library live
        unsplash_url = f"https://api.unsplash.com/photos/random?query={query}&client_id={st.secrets['UNSPLASH_API_KEY']}"
        response = requests.get(unsplash_url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            new_image = data["urls"]["regular"]
        else:
            # If rate limit is hit, use the fallback list
            new_image = random.choice(fallback_images)
            while new_image == st.session_state.last_image:
                new_image = random.choice(fallback_images)
                
    except Exception:
        # If the network drops, use the fallback list
        new_image = random.choice(fallback_images)
        while new_image == st.session_state.last_image:
            new_image = random.choice(fallback_images)

    st.session_state.last_image = new_image
    return new_image

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
        st.write_stream(stream_affirmation_and_horoscope())
        
        img_url = get_rotating_image()
        st.image(img_url, use_column_width=True)
            
    except Exception as e:
        if "429" in str(e) or "Quota" in str(e) or "ResourceExhausted" in str(e):
            st.warning("💛 Whoa there! The universe is gathering vibes as fast as it can. Take a deep breath and try the button again in about a minute.")
        else:
            st.warning("✨ The cosmic connection stuttered for a second. Try pushing the button again!")

# Logic for Button 2 (Short 1-2 sentences)
if quick_vibes:
    try:
        st.write_stream(stream_short_affirmation())
        
        img_url = get_rotating_image()
        st.image(img_url, use_column_width=True)
            
    except Exception as e:
        if "429" in str(e) or "Quota" in str(e) or "ResourceExhausted" in str(e):
            st.warning("💛 Whoa there! The universe is gathering vibes as fast as it can. Take a deep breath and try the button again in about a minute.")
        else:
            st.warning("✨ The cosmic connection stuttered for a second. Try pushing the button again!")

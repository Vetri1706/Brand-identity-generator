"""
Zoviz-Style Brand Identity Generator
A complete Streamlit app for generating brand assets including logos, taglines, fonts, and color palettes.
"""

import streamlit as st
import io
import json
import zipfile
import base64
from PIL import Image, ImageDraw, ImageFont
import colorsys
import math
import random
from datetime import datetime
import os

# ==================== API CONFIGURATION ====================
# API Keys - Load from environment variables (secure for Nimbus deployment)
# IMPORTANT: Set these as environment variables in Nimbus dashboard
# Never commit API keys to Git or include in deployment ZIP

# Load from environment variables ONLY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # OpenAI disabled
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "")  # Google Gemini - Set in Nimbus
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")  # Stability AI - Set in Nimbus
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY", "")  # Freepik AI - Set in Nimbus

# AI Configuration
USE_AI_BY_DEFAULT = os.getenv("USE_AI_BY_DEFAULT", "False").lower() == "true"
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "Freepik")

# Page configuration
st.set_page_config(
    page_title="Brand Identity Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",  # Sidebar always expanded
    menu_items={
        'Get Help': 'https://github.com/yourusername/brand-identity-generator',
        'Report a bug': None,
        'About': "# Brand Identity Generator\nCreate professional brand assets with AI!"
    }
)

# Custom CSS for modern styling
def load_custom_css():
    """Load custom CSS for a premium, high-end appearance"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Main Container */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2d3748;
        }
        
        /* All Text Elements - Better Visibility */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #2d3748;
        }
        
        /* Streamlit Labels */
        label {
            color: #2d3748 !important;
            font-weight: 500;
            font-size: 0.95rem;
        }
        
        /* Main Content Text */
        .main .stMarkdown {
            color: #2d3748;
        }
        
        /* Hero Section - Premium Gradient */
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            padding: 4rem 3rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 3rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 15s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            letter-spacing: -1px;
            position: relative;
            z-index: 1;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            opacity: 0.95;
            font-weight: 400;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }
        
        /* Section Headers - Modern Design */
        .section-header {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 3rem 0 1.5rem 0;
            padding-bottom: 0.8rem;
            border-bottom: 3px solid transparent;
            border-image: linear-gradient(90deg, #667eea, #764ba2, transparent);
            border-image-slice: 1;
            letter-spacing: -0.5px;
        }
        
        /* Color Swatch - Premium Elevation */
        .color-swatch {
            display: inline-block;
            width: 140px;
            height: 140px;
            border-radius: 16px;
            margin: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 3px solid white;
        }
        
        .color-swatch:hover {
            transform: translateY(-8px) scale(1.05);
            box-shadow: 0 16px 48px rgba(0,0,0,0.25);
        }
        
        .color-label {
            text-align: center;
            font-weight: 700;
            margin-top: 0.8rem;
            color: #2d3748;
            font-size: 0.95rem;
            letter-spacing: 0.3px;
        }
        
        /* Font Preview Card - Glass Morphism */
        .font-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 16px;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-left: 5px solid #667eea;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .font-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 48px rgba(0,0,0,0.15);
        }
        
        /* Tagline Card - Modern Interactive */
        .tagline-card {
            background: white;
            padding: 1.8rem;
            border-radius: 14px;
            margin: 1rem 0;
            border: 2px solid #e2e8f0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .tagline-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .tagline-card:hover::before {
            left: 100%;
        }
        
        .tagline-card:hover {
            border-color: #667eea;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
            transform: translateX(4px);
        }
        
        /* Button Styling - Premium */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.9rem 2.5rem;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
            font-size: 1.05rem;
            letter-spacing: 0.3px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 28px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Download Button - Special Styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            font-weight: 700;
            border: none;
            padding: 1rem 2.5rem;
            border-radius: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(17, 153, 142, 0.3);
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 28px rgba(17, 153, 142, 0.5);
        }
        
        /* Input Fields - Modern Premium */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            padding: 0.8rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white !important;
            color: #1a202c !important;
        }
        
        /* Input Placeholder Text */
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #a0aec0 !important;
            opacity: 1;
        }
        
        /* Input Focus State */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
            outline: none;
            background: white !important;
            color: #1a202c !important;
        }
        
        /* Select Dropdown in Main Area */
        .stSelectbox > div > div > select,
        .stSelectbox [data-baseweb="select"] {
            background: white !important;
            color: #1a202c !important;
        }
        
        /* Sidebar Styling - Premium Dark Theme */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            border-right: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Sidebar Headers - White Text */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: white !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        }
        
        /* Sidebar Labels - White Text */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown {
            color: white !important;
            font-weight: 500 !important;
        }
        
        /* Sidebar Select Box Container */
        [data-testid="stSidebar"] .stSelectbox > div > div {
            background: white !important;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }
        
        /* Sidebar Select Box - ALL TEXT DARK */
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stSelectbox *,
        [data-testid="stSidebar"] .stSelectbox select,
        [data-testid="stSidebar"] .stSelectbox option,
        [data-testid="stSidebar"] .stSelectbox div,
        [data-testid="stSidebar"] .stSelectbox span,
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"],
        [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] *,
        [data-testid="stSidebar"] .stSelectbox [role="option"] {
            color: #1a202c !important;
            font-weight: 500 !important;
        }
        
        /* Sidebar Select Box Label - Keep White */
        [data-testid="stSidebar"] .stSelectbox > label {
            color: white !important;
        }
        
        /* Sidebar Select Box Dropdown Background */
        [data-testid="stSidebar"] .stSelectbox [role="listbox"] {
            background: white !important;
        }
        
        /* Dropdown Menu Options (renders outside sidebar) */
        [role="listbox"] [role="option"],
        [role="listbox"] li,
        [data-baseweb="menu"] [role="option"],
        [data-baseweb="menu"] li,
        ul[role="listbox"] li,
        ul[role="listbox"] div {
            color: #1a202c !important;
            background: white !important;
        }
        
        /* Dropdown Menu Container */
        [role="listbox"],
        [data-baseweb="menu"],
        ul[role="listbox"] {
            background: white !important;
        }
        
        /* Dropdown Option Hover State */
        [role="option"]:hover,
        [data-baseweb="menu"] li:hover {
            background: #f7fafc !important;
            color: #1a202c !important;
        }
        
        /* Sidebar Checkbox */
        [data-testid="stSidebar"] .stCheckbox {
            color: white !important;
        }
        
        /* Sidebar Checkbox Label */
        [data-testid="stSidebar"] .stCheckbox label {
            color: white !important;
        }
        
        /* Sidebar Checkbox Span Text */
        [data-testid="stSidebar"] .stCheckbox span {
            color: white !important;
        }
        
        /* Sidebar Info/Success/Warning Boxes */
        [data-testid="stSidebar"] .stAlert {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }
        
        /* Sidebar Divider */
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.2) !important;
            margin: 1.5rem 0;
        }
        
        /* Sidebar Caption */
        [data-testid="stSidebar"] .stCaption {
            color: rgba(255, 255, 255, 0.7) !important;
            text-align: center;
            margin-top: 2rem;
        }
        
        /* Logo Container - Premium Card */
        .logo-container {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .logo-container:hover {
            box-shadow: 0 15px 60px rgba(0,0,0,0.15);
            transform: translateY(-5px);
        }
        
        /* Badge Styling */
        .badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 0.5rem 0.3rem;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        /* Success/Info Messages */
        .stSuccess {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            border-radius: 12px;
            padding: 1rem;
            color: white;
            font-weight: 500;
        }
        
        .stInfo {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 1rem;
            color: white;
            font-weight: 500;
        }
        
        /* Divider */
        hr {
            margin: 3rem 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
        }
    </style>
    """, unsafe_allow_html=True)


# ==================== LOGO GENERATION ====================
def generate_logo(company_name, industry, theme_style, use_ai=False, api_provider=None, num_variations=3):
    """
    Generate logo(s) based on company name and industry.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector of the company
        theme_style (str): Design theme (Minimal, Modern, Retro, etc.)
        use_ai (bool): Whether to use AI API for generation
        api_provider (str): AI provider name ("OpenAI", "Google Gemini", or "Stability AI")
        num_variations (int): Number of logo variations to generate (for AI)
    
    Returns:
        list[PIL.Image]: List of generated logo images (single logo wrapped in list for non-AI)
    """
    
    # Get API key based on provider
    api_key = None
    if use_ai and api_provider:
        if api_provider == "OpenAI":
            api_key = OPENAI_API_KEY
        elif api_provider == "Google Gemini":
            api_key = GENAI_API_KEY
        elif api_provider == "Stability AI":
            api_key = STABILITY_API_KEY
        elif api_provider == "Freepik":
            api_key = FREEPIK_API_KEY
    
    if use_ai and api_key:
        # Check if API key is configured
        if not api_key or api_key.strip() == "":
            st.warning(f"⚠️ {api_provider} API key not configured in code. Using built-in generator instead.")
            return [create_placeholder_logo(company_name, industry, theme_style)]
        
        # AI API integration
        try:
            if api_provider == "OpenAI":
                logos = generate_logo_openai(company_name, industry, theme_style, api_key, num_variations)
                return logos if isinstance(logos, list) else [logos]
            elif api_provider == "Google Gemini":
                # Gemini doesn't support image generation, use enhanced placeholder
                st.info("💡 Google Gemini doesn't generate images. Showing creative built-in designs.")
                return [create_placeholder_logo(company_name, industry, style) for style in ['Minimal', 'Modern', 'Bold']]
            elif api_provider == "Stability AI":
                return generate_logo_stability(company_name, industry, theme_style, api_key, num_variations)
            elif api_provider == "Freepik":
                return generate_logo_freepik(company_name, industry, theme_style, api_key, num_variations)
        except Exception as e:
            st.error(f"❌ AI generation failed: {str(e)}")
            st.info("⏳ Falling back to built-in generator...")
            return [create_placeholder_logo(company_name, industry, theme_style)]
    
    # Fallback: Generate multiple built-in logo variations
    return [create_placeholder_logo(company_name, industry, theme_style)]


def generate_logo_openai(company_name, industry, theme_style, api_key, num_variations=3):
    """
    Generate multiple logo variations using OpenAI DALL-E API.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        theme_style (str): Design theme
        api_key (str): OpenAI API key
        num_variations (int): Number of logo variations to generate
    
    Returns:
        list[PIL.Image]: List of generated logos
    """
    try:
        import requests
        
        # OpenAI DALL-E 3 API endpoint
        api_url = "https://api.openai.com/v1/images/generations"
        
        style_modifiers = {
            'Minimalist': 'minimalist, clean lines, simple geometric, Apple-style, Google-inspired',
            'Corporate': 'professional, corporate, trustworthy, IBM-style, business',
            'Creative': 'creative, artistic, unique, Airbnb-style, innovative',
            'Luxury': 'luxury, premium, elegant, Chanel-inspired, high-end',
            'Tech/Modern': 'modern tech, futuristic, Tesla-style, cutting-edge',
            'Playful': 'playful, fun, friendly, Lego-style, approachable',
            'Elegant': 'elegant, sophisticated, classic, Tiffany-style, refined',
            'Bold/Impactful': 'bold, strong, powerful, Nike-inspired, impactful'
        }
        
        logos = []
        
        with st.spinner(f"🎨 Generating {num_variations} AI logo variations..."):
            for i in range(num_variations):
                prompt = f"Professional logo design for {company_name}, {industry} company, {style_modifiers.get(theme_style, 'modern professional')} style, vector art, white background, centered, high quality, brand identity, variation {i+1}"
                
                response = requests.post(
                    api_url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    },
                    json={
                        "model": "dall-e-3",
                        "prompt": prompt,
                        "n": 1,
                        "size": "1024x1024",
                        "quality": "standard"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    image_url = data['data'][0]['url']
                    img_response = requests.get(image_url)
                    img = Image.open(io.BytesIO(img_response.content))
                    logos.append(img)
                    st.success(f"✅ Generated logo variation {i+1}/{num_variations}")
                else:
                    st.error(f"❌ API Error (variation {i+1}): {response.status_code}")
                    logos.append(create_placeholder_logo(company_name, industry, theme_style))
        
        return logos if logos else [create_placeholder_logo(company_name, industry, theme_style)]
        
    except Exception as e:
        st.error(f"❌ OpenAI error: {str(e)}")
        return [create_placeholder_logo(company_name, industry, theme_style)]


def generate_logo_stability(company_name, industry, theme_style, api_key, num_variations=3):
    """
    Generate multiple logo variations using Stability AI API.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        theme_style (str): Design theme
        api_key (str): Stability AI API key
        num_variations (int): Number of logo variations to generate
    
    Returns:
        list[PIL.Image]: List of generated logo images
    """
    try:
        import requests
        
        # Stability AI API endpoint for text-to-image
        api_host = "https://api.stability.ai"
        # Updated engine ID - check https://platform.stability.ai/docs/api-reference for latest
        engine_id = "stable-diffusion-xl-1024-v1-0"  # SDXL 1.0 - current stable version
        
        # Create detailed prompt based on style and industry
        style_modifiers = {
            'Minimalist': 'minimalist clean lines simple geometric Apple Google style negative space',
            'Corporate': 'professional corporate business IBM Deloitte style trustworthy formal',
            'Creative': 'creative artistic unique Airbnb Dropbox style innovative organic',
            'Luxury': 'luxury premium elegant Chanel Louis Vuitton style high-end sophisticated',
            'Tech/Modern': 'modern tech futuristic Tesla Spotify style sleek cutting-edge',
            'Playful': 'playful fun friendly Lego Disney style approachable colorful',
            'Elegant': 'elegant sophisticated classic Tiffany Cartier style refined timeless',
            'Bold/Impactful': 'bold strong impactful Nike Red Bull style powerful dramatic'
        }
        
        base_prompt = f"Professional logo design for {company_name}, {industry} company, {style_modifiers.get(theme_style, 'modern professional')}, vector style, white background, centered composition, high quality, brand identity"
        
        logos = []
        
        # Generate multiple variations
        with st.spinner(f"🎨 Generating {num_variations} AI logo variations..."):
            for i in range(num_variations):
                # Add slight variation to each prompt
                variation_seeds = ['elegant', 'creative', 'innovative']
                prompt = f"{base_prompt}, {variation_seeds[i % len(variation_seeds)]} design"
                
                response = requests.post(
                    f"{api_host}/v1/generation/{engine_id}/text-to-image",
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    },
                    json={
                        "text_prompts": [
                            {
                                "text": prompt,
                                "weight": 1
                            },
                            {
                                "text": "blurry, low quality, distorted, text, watermark, signature",
                                "weight": -1
                            }
                        ],
                        "cfg_scale": 7,
                        "height": 1024,
                        "width": 1024,
                        "samples": 1,
                        "steps": 30,
                        "seed": random.randint(0, 4294967295)
                    },
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for image_data in data["artifacts"]:
                        image_bytes = base64.b64decode(image_data["base64"])
                        img = Image.open(io.BytesIO(image_bytes))
                        logos.append(img)
                        st.success(f"✅ Generated logo variation {i+1}/{num_variations}")
                else:
                    st.error(f"❌ API Error (variation {i+1}): {response.status_code} - {response.text}")
                    # Add placeholder for failed generation
                    logos.append(create_placeholder_logo(company_name, industry, theme_style))
        
        if not logos:
            st.warning("⚠️ All AI generations failed. Using built-in generator.")
            return [create_placeholder_logo(company_name, industry, theme_style)]
        
        return logos
        
    except Exception as e:
        st.error(f"❌ Stability AI error: {str(e)}")
        st.info("⏳ Falling back to built-in generator...")
        return [create_placeholder_logo(company_name, industry, theme_style)]


def generate_logo_gemini(company_name, industry, theme_style, api_key):
    """
    Generate logo using Google Gemini (Imagen) API.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        theme_style (str): Design theme
        api_key (str): Google Gemini API key
    
    Returns:
        PIL.Image: Generated logo
    """
    # Uncomment and install: pip install google-generativeai requests
    """
    import google.generativeai as genai
    import requests
    from io import BytesIO
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Note: Gemini primarily does text generation
    # For image generation, you'd use Google's Imagen API or Vertex AI
    # This is a placeholder showing the pattern
    
    prompt = f"Professional {theme_style} style logo for {company_name}, a {industry} company, simple, modern, vector style, white background, minimalist"
    
    # Using Gemini for prompt enhancement, then fallback to geometric
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    response = model.generate_content(f"Create a brief design description for: {prompt}")
    
    # For actual image generation, you would use Imagen API
    # For now, using enhanced placeholder
    st.info(f"🎨 Gemini suggests: {response.text[:100]}...")
    """
    st.info("💡 Google Gemini integration: For image generation, use Vertex AI Imagen. Using built-in generator with Gemini-style design.")
    return create_placeholder_logo(company_name, industry, theme_style)


def generate_logo_freepik(company_name, industry, theme_style, api_key, num_variations=3):
    """
    Generate multiple logo variations using Freepik AI API.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        theme_style (str): Design theme
        api_key (str): Freepik API key
        num_variations (int): Number of logo variations to generate
    
    Returns:
        list[PIL.Image]: List of generated logo images
    """
    try:
        import requests
        import time
        
        # Freepik AI API endpoint
        api_host = "https://api.freepik.com"
        
        # Create detailed prompt based on style and industry
        style_modifiers = {
            'Minimalist': 'minimalist, clean, simple geometric shapes, Apple Google style, negative space, modern',
            'Corporate': 'professional, corporate, business, IBM Deloitte style, trustworthy, formal',
            'Creative': 'creative, artistic, unique, Airbnb Dropbox style, innovative, organic',
            'Luxury': 'luxury, premium, elegant, Chanel Louis Vuitton style, high-end, sophisticated',
            'Tech/Modern': 'modern tech, futuristic, Tesla Spotify style, sleek, cutting-edge',
            'Playful': 'playful, fun, friendly, Lego Disney style, approachable, colorful',
            'Elegant': 'elegant, sophisticated, classic, Tiffany Cartier style, refined, timeless',
            'Bold/Impactful': 'bold, strong, impactful, Nike Red Bull style, powerful, dramatic'
        }
        
        base_prompt = f"Professional logo design for {company_name}, {industry} company, {style_modifiers.get(theme_style, 'modern professional')}, vector style, white background, centered, high quality brand identity"
        
        logos = []
        
        # Generate multiple variations
        with st.spinner(f"🎨 Generating {num_variations} AI logo variations with Freepik..."):
            for i in range(num_variations):
                try:
                    # Add variation to prompt
                    variation_words = ['elegant sophisticated', 'creative unique', 'innovative modern']
                    prompt = f"{base_prompt}, {variation_words[i % len(variation_words)]} style"
                    
                    # Create image generation request
                    response = requests.post(
                        f"{api_host}/v1/ai/text-to-image",
                        headers={
                            "Content-Type": "application/json",
                            "x-freepik-api-key": api_key
                        },
                        json={
                            "prompt": prompt,
                            "negative_prompt": "blurry, low quality, distorted, text, watermark, signature, letters, words",
                            "guidance_scale": 7.5,
                            "num_images": 1,
                            "image": {
                                "size": "square_1_1"  # 1024x1024
                            },
                            "styling": {
                                "style": "photo"
                            }
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check if we got a direct image URL or need to wait for generation
                        if 'data' in data and len(data['data']) > 0:
                            image_data = data['data'][0]
                            
                            # If we have a direct base64 image
                            if 'base64' in image_data:
                                image_bytes = base64.b64decode(image_data['base64'])
                                img = Image.open(io.BytesIO(image_bytes))
                                logos.append(img)
                                st.success(f"✅ Generated logo variation {i+1}/{num_variations}")
                            
                            # If we have an image URL
                            elif 'url' in image_data:
                                img_response = requests.get(image_data['url'], timeout=30)
                                if img_response.status_code == 200:
                                    img = Image.open(io.BytesIO(img_response.content))
                                    logos.append(img)
                                    st.success(f"✅ Generated logo variation {i+1}/{num_variations}")
                                else:
                                    st.warning(f"⚠️ Could not download variation {i+1}")
                                    logos.append(create_placeholder_logo(company_name, industry, theme_style))
                            else:
                                st.warning(f"⚠️ Unexpected response format for variation {i+1}")
                                logos.append(create_placeholder_logo(company_name, industry, theme_style))
                        else:
                            st.warning(f"⚠️ No image data in response for variation {i+1}")
                            logos.append(create_placeholder_logo(company_name, industry, theme_style))
                    
                    elif response.status_code == 401:
                        st.error(f"❌ Authentication failed. Please check your Freepik API key.")
                        logos.append(create_placeholder_logo(company_name, industry, theme_style))
                    
                    elif response.status_code == 429:
                        st.warning(f"⚠️ Rate limit reached. Waiting before retry...")
                        time.sleep(2)
                        logos.append(create_placeholder_logo(company_name, industry, theme_style))
                    
                    else:
                        st.error(f"❌ Freepik API Error (variation {i+1}): {response.status_code}")
                        if response.text:
                            st.error(f"Response: {response.text[:200]}")
                        logos.append(create_placeholder_logo(company_name, industry, theme_style))
                    
                    # Small delay between requests to avoid rate limiting
                    if i < num_variations - 1:
                        time.sleep(1)
                
                except requests.exceptions.Timeout:
                    st.warning(f"⚠️ Request timeout for variation {i+1}")
                    logos.append(create_placeholder_logo(company_name, industry, theme_style))
                except Exception as e:
                    st.error(f"❌ Error generating variation {i+1}: {str(e)}")
                    logos.append(create_placeholder_logo(company_name, industry, theme_style))
        
        if not logos:
            st.warning("⚠️ All Freepik AI generations failed. Using built-in generator.")
            return [create_placeholder_logo(company_name, industry, theme_style)]
        
        return logos
        
    except Exception as e:
        st.error(f"❌ Freepik AI error: {str(e)}")
        st.info("⏳ Falling back to built-in generator...")
        return [create_placeholder_logo(company_name, industry, theme_style)]


def create_placeholder_logo(company_name, industry, theme_style):
    """
    Create a professional geometric logo with global design standards.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        theme_style (str): Design theme (Global standards)
    
    Returns:
        PIL.Image: Generated logo
    """
    # Create a 1000x1000 canvas with subtle background
    img_size = 1000
    img = Image.new('RGB', (img_size, img_size), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    # Get initials (up to 2 characters)
    initials = ''.join([word[0].upper() for word in company_name.split()[:2]])
    
    # Premium industry color palette - Global standards
    industry_colors = {
        'Technology': '#0066FF',      # Microsoft/IBM Blue
        'Finance': '#00875A',         # Trust Green
        'Healthcare': '#D32F2F',      # Medical Red
        'Education': '#FF6F00',       # Learning Orange
        'Retail': '#7B1FA2',         # Premium Purple
        'Food & Beverage': '#E65100', # Appetite Orange
        'Real Estate': '#424242',     # Solid Gray
        'Entertainment': '#C2185B',   # Entertainment Pink
        'Fashion': '#000000',         # Fashion Black
        'Other': '#1976D2'           # Professional Blue
    }
    
    primary_color = industry_colors.get(industry, '#1976D2')
    
    # Global standard theme implementations
    if theme_style == 'Minimalist':
        # Apple/Google style - Clean circle
        circle_radius = 350
        circle_center = (img_size // 2, img_size // 2)
        # Subtle shadow effect
        shadow_offset = 10
        draw.ellipse(
            [circle_center[0] - circle_radius + shadow_offset, 
             circle_center[1] - circle_radius + shadow_offset,
             circle_center[0] + circle_radius + shadow_offset, 
             circle_center[1] + circle_radius + shadow_offset],
            fill='#E0E0E0'
        )
        # Main circle
        draw.ellipse(
            [circle_center[0] - circle_radius, circle_center[1] - circle_radius,
             circle_center[0] + circle_radius, circle_center[1] + circle_radius],
            fill=primary_color
        )
    
    elif theme_style == 'Corporate':
        # IBM/Deloitte style - Professional square with rounded corners
        rect_size = 700
        offset = (img_size - rect_size) // 2
        corner_radius = 60
        # Shadow
        draw.rounded_rectangle(
            [offset + 8, offset + 8, offset + rect_size + 8, offset + rect_size + 8],
            radius=corner_radius,
            fill='#DDDDDD'
        )
        # Main shape
        draw.rounded_rectangle(
            [offset, offset, offset + rect_size, offset + rect_size],
            radius=corner_radius,
            fill=primary_color
        )
        # Accent line
        draw.rectangle(
            [offset, offset + rect_size - 20, offset + rect_size, offset + rect_size],
            fill='#FFFFFF'
        )
    
    elif theme_style == 'Creative':
        # Airbnb/Dropbox style - Organic rounded shape
        center_x, center_y = img_size // 2, img_size // 2
        radius = 320
        # Create rounded organic shape
        points = []
        for i in range(8):
            angle = 45 * i
            r = radius + (50 if i % 2 == 0 else 0)
            x = center_x + r * math.cos(math.radians(angle))
            y = center_y + r * math.sin(math.radians(angle))
            points.append((x, y))
        draw.polygon(points, fill=primary_color)
    
    elif theme_style == 'Luxury':
        # Chanel/Louis Vuitton style - Elegant diamond
        center_x, center_y = img_size // 2, img_size // 2
        size = 400
        diamond_points = [
            (center_x, center_y - size),  # Top
            (center_x + size//1.5, center_y),  # Right
            (center_x, center_y + size),  # Bottom
            (center_x - size//1.5, center_y)   # Left
        ]
        # Gold accent outline
        draw.polygon(diamond_points, fill='#000000')
        # Inner diamond
        inner_size = size - 40
        inner_points = [
            (center_x, center_y - inner_size),
            (center_x + inner_size//1.5, center_y),
            (center_x, center_y + inner_size),
            (center_x - inner_size//1.5, center_y)
        ]
        draw.polygon(inner_points, fill=primary_color)
    
    elif theme_style == 'Tech/Modern':
        # Tesla/Spotify style - Sleek geometric
        center_x, center_y = img_size // 2, img_size // 2
        size = 350
        # Hexagon for tech feel
        hexagon = []
        for i in range(6):
            angle = 60 * i
            x = center_x + size * math.cos(math.radians(angle))
            y = center_y + size * math.sin(math.radians(angle))
            hexagon.append((x, y))
        # Gradient simulation with overlapping shapes
        draw.polygon(hexagon, fill=primary_color)
        # Inner accent
        inner_size = size - 80
        inner_hex = []
        for i in range(6):
            angle = 60 * i
            x = center_x + inner_size * math.cos(math.radians(angle))
            y = center_y + inner_size * math.sin(math.radians(angle))
            inner_hex.append((x, y))
        draw.polygon(inner_hex, fill='#FFFFFF')
    
    elif theme_style == 'Playful':
        # Lego/Disney style - Fun rounded square
        rect_size = 650
        offset = (img_size - rect_size) // 2
        corner_radius = 120
        # Multiple overlapping shapes for depth
        colors = [primary_color, '#FFFFFF', primary_color]
        sizes = [rect_size, rect_size - 100, rect_size - 200]
        for i, (color, size) in enumerate(zip(colors, sizes)):
            off = (img_size - size) // 2
            draw.rounded_rectangle(
                [off, off, off + size, off + size],
                radius=corner_radius - i*20,
                fill=color
            )
    
    elif theme_style == 'Elegant':
        # Tiffany/Cartier style - Classic shield
        center_x, center_y = img_size // 2, img_size // 2
        width, height = 600, 700
        # Shield shape
        shield_points = [
            (center_x, center_y - height//2),  # Top center
            (center_x + width//2, center_y - height//3),  # Top right
            (center_x + width//2, center_y + height//4),  # Right
            (center_x, center_y + height//2),  # Bottom point
            (center_x - width//2, center_y + height//4),  # Left
            (center_x - width//2, center_y - height//3),  # Top left
        ]
        draw.polygon(shield_points, fill=primary_color)
        # Inner border
        inner_points = [(x + (center_x - x) * 0.15, y + (center_y - y) * 0.15) 
                       for x, y in shield_points]
        draw.polygon(inner_points, fill='#FFFFFF')
    
    else:  # Bold/Impactful (default)
        # Nike/Red Bull style - Strong square
        rect_size = 700
        offset = (img_size - rect_size) // 2
        # Bold square
        draw.rectangle(
            [offset, offset, offset + rect_size, offset + rect_size],
            fill=primary_color
        )
        # Diagonal accent
        draw.polygon([
            (offset, offset),
            (offset + 150, offset),
            (offset, offset + 150)
        ], fill='#FFFFFF')
    
    # Add initials text with premium font sizing
    try:
        font_size = 380 if theme_style == 'Luxury' else 350
        try:
            # Try to use a premium font
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    text_x = (img_size - text_width) // 2 - bbox[0]
    text_y = (img_size - text_height) // 2 - bbox[1]
    
    # Text color based on theme
    text_color = '#000000' if theme_style == 'Luxury' else '#FFFFFF'
    draw.text((text_x, text_y), initials, fill=text_color, font=font)
    
    return img


def generate_favicon(logo_image):
    """
    Generate a favicon (small icon) from the logo.
    
    Args:
        logo_image (PIL.Image): Original logo image
    
    Returns:
        PIL.Image: Resized favicon (256x256)
    """
    favicon = logo_image.copy()
    favicon.thumbnail((256, 256), Image.Resampling.LANCZOS)
    return favicon


# ==================== TAGLINE GENERATION ====================
def generate_taglines(company_name, industry, description, use_ai=False, api_provider=None):
    """
    Generate tagline suggestions for the brand.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        description (str): Company description
        use_ai (bool): Whether to use AI API
        api_provider (str): AI provider name
    
    Returns:
        list: List of tagline suggestions
    """
    
    # Get API key based on provider
    api_key = None
    if use_ai and api_provider:
        if api_provider == "OpenAI":
            api_key = OPENAI_API_KEY
        elif api_provider == "Google Gemini":
            api_key = GENAI_API_KEY
        elif api_provider == "Stability AI":
            api_key = STABILITY_API_KEY
    
    if use_ai and api_key:
        # Check if API key is configured
        if not api_key or api_key.strip() == "":
            st.warning(f"⚠️ {api_provider} API key not configured in code. Using built-in generator instead.")
            return create_placeholder_taglines(company_name, industry, description)
        
        # AI API integration (OpenAI and Gemini for text generation)
        try:
            if api_provider == "OpenAI":
                return generate_taglines_openai(company_name, industry, description, api_key)
            elif api_provider == "Google Gemini":
                return generate_taglines_gemini(company_name, industry, description, api_key)
            else:
                # Stability AI is for images only, use built-in for taglines
                return create_placeholder_taglines(company_name, industry, description)
        except Exception as e:
            st.error(f"❌ AI tagline generation failed: {str(e)}")
            st.info("⏳ Falling back to built-in generator...")
            return create_placeholder_taglines(company_name, industry, description)
    
    # Fallback: Generate template-based taglines
    return create_placeholder_taglines(company_name, industry, description)


def generate_taglines_openai(company_name, industry, description, api_key):
    """
    Generate taglines using OpenAI GPT API.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        description (str): Company description
        api_key (str): OpenAI API key
    
    Returns:
        list: List of tagline suggestions
    """
    try:
        import requests
        
        prompt = f'''Generate 5 creative and professional taglines for {company_name}, 
                     a {industry} company. Description: {description}
                     
                     Return only the taglines, one per line, without any numbering or extra text.'''
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "gpt-3.5-turbo",  # More affordable than gpt-4
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 200
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            taglines_text = data['choices'][0]['message']['content'].strip()
            taglines = taglines_text.split('\n')
            # Clean up taglines
            import re
            cleaned = [re.sub(r'^[\d\.\)\-\*\•\s]+', '', t.strip()) for t in taglines if t.strip()]
            return cleaned[:5]
        else:
            st.error(f"❌ OpenAI API Error: {response.status_code}")
            return create_placeholder_taglines(company_name, industry, description)
            
    except Exception as e:
        st.error(f"❌ OpenAI error: {str(e)}")
        return create_placeholder_taglines(company_name, industry, description)


def generate_taglines_gemini(company_name, industry, description, api_key):
    """
    Generate taglines using Google Gemini API.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        description (str): Company description
        api_key (str): Google Gemini API key
    
    Returns:
        list: List of tagline suggestions
    """
    # Install: pip install google-generativeai
    try:
        import google.generativeai as genai
        
        # Configure Gemini with API key
        genai.configure(api_key=api_key)
        
        # Use updated Gemini model name (gemini-pro is deprecated)
        model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        
        prompt = f'''Generate 5 creative and professional taglines for {company_name}, 
                     a {industry} company. Description: {description}
                     
                     Return only the taglines, one per line, without any numbering or extra text.'''
        
        response = model.generate_content(prompt)
        
        # Parse the response
        taglines = response.text.strip().split('\n')
        # Clean up the taglines (remove numbering, dashes, etc.)
        cleaned_taglines = []
        for t in taglines:
            # Remove common prefixes like "1.", "1)", "-", "*", etc.
            cleaned = t.strip()
            # Remove leading numbers and punctuation
            import re
            cleaned = re.sub(r'^[\d\.\)\-\*\•\s]+', '', cleaned)
            if cleaned and len(cleaned) > 5:  # Ensure it's not empty or too short
                cleaned_taglines.append(cleaned)
        
        # Return up to 5 taglines
        return cleaned_taglines[:5] if cleaned_taglines else create_placeholder_taglines(company_name, industry, description)
        
    except ImportError:
        st.warning("Google Gemini integration requires installing: pip install google-generativeai")
        return create_placeholder_taglines(company_name, industry, description)
    except Exception as e:
        st.error(f"Gemini API error: {str(e)}")
        return create_placeholder_taglines(company_name, industry, description)


def create_placeholder_taglines(company_name, industry, description):
    """
    Create template-based tagline suggestions.
    
    Args:
        company_name (str): Name of the company
        industry (str): Industry/sector
        description (str): Company description
    
    Returns:
        list: List of tagline suggestions
    """
    
    # Industry-specific action words and themes
    templates = {
        'Technology': [
            f"Innovating the Future of {industry}",
            f"Where Technology Meets Excellence",
            f"Empowering Tomorrow, Today",
            f"Your Partner in Digital Transformation",
            f"Building Solutions That Matter"
        ],
        'Finance': [
            f"Your Trusted Financial Partner",
            f"Growing Wealth, Building Futures",
            f"Smart Money, Smarter Decisions",
            f"Financial Freedom Starts Here",
            f"Securing Your Tomorrow"
        ],
        'Healthcare': [
            f"Caring for Your Health, Always",
            f"Excellence in Healthcare",
            f"Your Health, Our Priority",
            f"Healing Lives, Building Hope",
            f"Compassionate Care, Expert Service"
        ],
        'Education': [
            f"Shaping Minds, Building Futures",
            f"Learn Today, Lead Tomorrow",
            f"Education That Empowers",
            f"Knowledge Without Boundaries",
            f"Inspiring Excellence in Learning"
        ],
        'Retail': [
            f"Quality You Can Trust",
            f"Where Style Meets Value",
            f"Your Shopping Destination",
            f"Experience the Difference",
            f"More Than Just Shopping"
        ],
        'Food & Beverage': [
            f"Taste the Difference",
            f"Fresh Flavors, Happy Moments",
            f"Where Quality Meets Flavor",
            f"Delicious Experiences Every Time",
            f"Crafted with Passion, Served with Love"
        ]
    }
    
    # Get industry-specific taglines or use generic ones
    if industry in templates:
        taglines = templates[industry]
    else:
        taglines = [
            f"Excellence Delivered Every Time",
            f"Your Success, Our Mission",
            f"Quality That Speaks for Itself",
            f"Innovation Meets Dedication",
            f"Building Better Together"
        ]
    
    return taglines


# ==================== FONT SUGGESTIONS ====================
def suggest_fonts(industry, theme_style):
    """
    Suggest fonts based on industry and theme.
    
    Args:
        industry (str): Industry/sector
        theme_style (str): Design theme
    
    Returns:
        list: List of font suggestions with descriptions
    """
    
    # Font database categorized by industry and style
    font_database = {
        'Technology': {
            'Minimal': [
                {'name': 'Roboto', 'category': 'Sans-serif', 'description': 'Clean, modern, and highly readable'},
                {'name': 'Inter', 'category': 'Sans-serif', 'description': 'Designed specifically for screens'},
                {'name': 'Space Grotesk', 'category': 'Sans-serif', 'description': 'Geometric and futuristic'}
            ],
            'Modern': [
                {'name': 'Montserrat', 'category': 'Sans-serif', 'description': 'Urban and contemporary'},
                {'name': 'Poppins', 'category': 'Sans-serif', 'description': 'Geometric with a friendly feel'},
                {'name': 'Raleway', 'category': 'Sans-serif', 'description': 'Elegant and sophisticated'}
            ],
            'Bold': [
                {'name': 'Bebas Neue', 'category': 'Display', 'description': 'Strong and impactful'},
                {'name': 'Oswald', 'category': 'Sans-serif', 'description': 'Condensed and powerful'},
                {'name': 'Anton', 'category': 'Display', 'description': 'Bold and attention-grabbing'}
            ]
        },
        'Finance': {
            'Minimal': [
                {'name': 'Lato', 'category': 'Sans-serif', 'description': 'Professional and trustworthy'},
                {'name': 'Open Sans', 'category': 'Sans-serif', 'description': 'Clear and approachable'},
                {'name': 'Source Sans Pro', 'category': 'Sans-serif', 'description': 'Refined and readable'}
            ],
            'Modern': [
                {'name': 'Helvetica Neue', 'category': 'Sans-serif', 'description': 'Classic and timeless'},
                {'name': 'Gotham', 'category': 'Sans-serif', 'description': 'Strong and confident'},
                {'name': 'Avenir', 'category': 'Sans-serif', 'description': 'Balanced and harmonious'}
            ]
        },
        'Healthcare': {
            'Minimal': [
                {'name': 'Nunito', 'category': 'Sans-serif', 'description': 'Friendly and approachable'},
                {'name': 'Quicksand', 'category': 'Sans-serif', 'description': 'Soft and welcoming'},
                {'name': 'Karla', 'category': 'Sans-serif', 'description': 'Clean and gentle'}
            ]
        },
        'Fashion': {
            'Modern': [
                {'name': 'Playfair Display', 'category': 'Serif', 'description': 'Elegant and sophisticated'},
                {'name': 'Cormorant', 'category': 'Serif', 'description': 'Luxurious and refined'},
                {'name': 'Libre Baskerville', 'category': 'Serif', 'description': 'Classic and stylish'}
            ],
            'Retro': [
                {'name': 'Pacifico', 'category': 'Script', 'description': 'Vintage and playful'},
                {'name': 'Lobster', 'category': 'Display', 'description': 'Retro and bold'},
                {'name': 'Satisfy', 'category': 'Script', 'description': 'Handwritten charm'}
            ]
        }
    }
    
    # Default fonts for industries not in database
    default_fonts = [
        {'name': 'Roboto', 'category': 'Sans-serif', 'description': 'Clean, modern, and highly readable'},
        {'name': 'Montserrat', 'category': 'Sans-serif', 'description': 'Urban and contemporary'},
        {'name': 'Lato', 'category': 'Sans-serif', 'description': 'Professional and trustworthy'}
    ]
    
    # Get fonts based on industry and theme
    if industry in font_database and theme_style in font_database[industry]:
        return font_database[industry][theme_style]
    elif industry in font_database:
        # Return first available theme for the industry
        return list(font_database[industry].values())[0]
    else:
        return default_fonts


# ==================== COLOR PALETTE GENERATION ====================
def generate_palette(industry, theme_style):
    """
    Generate a color palette for the brand.
    
    Args:
        industry (str): Industry/sector
        theme_style (str): Design theme
    
    Returns:
        dict: Color palette with primary, secondary, accent colors
    """
    
    # Industry-based base colors
    industry_base_colors = {
        'Technology': '#4A90E2',
        'Finance': '#2ECC71',
        'Healthcare': '#E74C3C',
        'Education': '#F39C12',
        'Retail': '#9B59B6',
        'Food & Beverage': '#E67E22',
        'Real Estate': '#34495E',
        'Entertainment': '#E91E63',
        'Fashion': '#8E44AD',
        'Other': '#667eea'
    }
    
    base_color = industry_base_colors.get(industry, '#667eea')
    
    # Generate complementary colors based on theme
    if theme_style == 'Minimal':
        palette = generate_minimal_palette(base_color)
    elif theme_style == 'Modern':
        palette = generate_modern_palette(base_color)
    elif theme_style == 'Retro':
        palette = generate_retro_palette(base_color)
    elif theme_style == 'Bold':
        palette = generate_bold_palette(base_color)
    else:
        palette = generate_modern_palette(base_color)
    
    return palette


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def adjust_color_brightness(hex_color, factor):
    """Adjust the brightness of a color"""
    rgb = hex_to_rgb(hex_color)
    adjusted = tuple(max(0, min(255, int(c * factor))) for c in rgb)
    return rgb_to_hex(adjusted)


def generate_complementary_color(hex_color):
    """Generate complementary color"""
    rgb = hex_to_rgb(hex_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    h = (h + 0.5) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return rgb_to_hex((r*255, g*255, b*255))


def generate_minimal_palette(base_color):
    """Generate a minimal color palette"""
    return {
        'primary': base_color,
        'secondary': adjust_color_brightness(base_color, 0.7),
        'accent': adjust_color_brightness(base_color, 1.3),
        'neutral_light': '#F8F9FA',
        'neutral_dark': '#343A40',
        'complementary': [
            base_color,
            adjust_color_brightness(base_color, 0.8),
            adjust_color_brightness(base_color, 1.2),
            '#FFFFFF',
            '#212529'
        ]
    }


def generate_modern_palette(base_color):
    """Generate a modern color palette"""
    rgb = hex_to_rgb(base_color)
    h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    # Generate analogous colors
    h1 = (h + 0.083) % 1.0  # +30 degrees
    h2 = (h - 0.083) % 1.0  # -30 degrees
    
    r1, g1, b1 = colorsys.hsv_to_rgb(h1, s, v)
    r2, g2, b2 = colorsys.hsv_to_rgb(h2, s, v)
    
    secondary = rgb_to_hex((r1*255, g1*255, b1*255))
    accent = rgb_to_hex((r2*255, g2*255, b2*255))
    
    return {
        'primary': base_color,
        'secondary': secondary,
        'accent': accent,
        'neutral_light': '#ECF0F1',
        'neutral_dark': '#2C3E50',
        'complementary': [
            base_color,
            secondary,
            accent,
            adjust_color_brightness(base_color, 1.2),
            adjust_color_brightness(base_color, 0.7)
        ]
    }


def generate_retro_palette(base_color):
    """Generate a retro color palette"""
    return {
        'primary': base_color,
        'secondary': '#F39C12',
        'accent': '#E74C3C',
        'neutral_light': '#FFF8E7',
        'neutral_dark': '#5D4037',
        'complementary': [
            base_color,
            '#F39C12',
            '#E74C3C',
            '#27AE60',
            '#8E44AD'
        ]
    }


def generate_bold_palette(base_color):
    """Generate a bold color palette"""
    comp = generate_complementary_color(base_color)
    
    return {
        'primary': base_color,
        'secondary': comp,
        'accent': '#FF6B6B',
        'neutral_light': '#FFFFFF',
        'neutral_dark': '#000000',
        'complementary': [
            base_color,
            comp,
            '#FF6B6B',
            '#4ECDC4',
            '#FFE66D'
        ]
    }


# ==================== SOCIAL MEDIA MOCKUP ====================
def create_social_media_mockup(logo_image, company_name, tagline, palette):
    """
    Create a social media post mockup (Instagram/LinkedIn style).
    
    Args:
        logo_image (PIL.Image): Company logo
        company_name (str): Name of the company
        tagline (str): Selected tagline
        palette (dict): Color palette
    
    Returns:
        PIL.Image: Social media mockup image
    """
    # Create 1080x1080 canvas (Instagram square format)
    mockup_size = (1080, 1080)
    mockup = Image.new('RGB', mockup_size, color=palette['neutral_light'])
    draw = ImageDraw.Draw(mockup)
    
    # Add gradient background
    for y in range(mockup_size[1]):
        factor = y / mockup_size[1]
        start_rgb = hex_to_rgb(palette['primary'])
        end_rgb = hex_to_rgb(palette['secondary'])
        
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * factor)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * factor)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * factor)
        
        draw.line([(0, y), (mockup_size[0], y)], fill=(r, g, b))
    
    # Resize and place logo
    logo_resized = logo_image.copy()
    logo_resized.thumbnail((400, 400), Image.Resampling.LANCZOS)
    
    logo_x = (mockup_size[0] - logo_resized.width) // 2
    logo_y = 200
    
    mockup.paste(logo_resized, (logo_x, logo_y), logo_resized if logo_resized.mode == 'RGBA' else None)
    
    # Add company name and tagline
    try:
        try:
            title_font = ImageFont.truetype("arialbd.ttf", 70)
            tagline_font = ImageFont.truetype("arial.ttf", 40)
        except:
            title_font = ImageFont.load_default()
            tagline_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
    
    # Company name
    name_bbox = draw.textbbox((0, 0), company_name, font=title_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (mockup_size[0] - name_width) // 2 - name_bbox[0]
    name_y = 650
    
    draw.text((name_x, name_y), company_name, fill='white', font=title_font)
    
    # Tagline
    tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = (mockup_size[0] - tagline_width) // 2 - tagline_bbox[0]
    tagline_y = 750
    
    draw.text((tagline_x, tagline_y), tagline, fill='white', font=tagline_font)
    
    return mockup


# ==================== DOWNLOAD ASSETS ====================
def download_assets(logo_images, favicon, company_name, tagline, fonts, palette, mockup):
    """
    Create a ZIP file with all brand assets.
    
    Args:
        logo_images (list or PIL.Image): Logo image(s) - can be single image or list
        favicon (PIL.Image): Favicon image
        company_name (str): Company name
        tagline (str): Selected tagline
        fonts (list): Font suggestions
        palette (dict): Color palette
        mockup (PIL.Image): Social media mockup
    
    Returns:
        bytes: ZIP file content
    """
    zip_buffer = io.BytesIO()
    
    # Ensure logo_images is a list
    if not isinstance(logo_images, list):
        logo_images = [logo_images]
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add logo(s)
        if len(logo_images) > 1:
            # Multiple logo variations
            for idx, logo in enumerate(logo_images):
                logo_buffer = io.BytesIO()
                logo.save(logo_buffer, format='PNG')
                zip_file.writestr(f'{company_name}_logo_variation_{idx+1}.png', logo_buffer.getvalue())
        else:
            # Single logo
            logo_buffer = io.BytesIO()
            logo_images[0].save(logo_buffer, format='PNG')
            zip_file.writestr(f'{company_name}_logo.png', logo_buffer.getvalue())
        
        # Add favicon
        favicon_buffer = io.BytesIO()
        favicon.save(favicon_buffer, format='PNG')
        zip_file.writestr(f'{company_name}_favicon.png', favicon_buffer.getvalue())
        
        # Add social media mockup
        mockup_buffer = io.BytesIO()
        mockup.save(mockup_buffer, format='PNG')
        zip_file.writestr(f'{company_name}_social_mockup.png', mockup_buffer.getvalue())
        
        # Add brand guidelines (text file)
        guidelines = f"""
{company_name} - Brand Identity Guidelines
{'=' * 50}

TAGLINE:
{tagline}

FONT RECOMMENDATIONS:
"""
        for i, font in enumerate(fonts, 1):
            guidelines += f"\n{i}. {font['name']} ({font['category']})\n   {font['description']}\n"
        
        guidelines += f"""
COLOR PALETTE:
Primary Color: {palette['primary']}
Secondary Color: {palette['secondary']}
Accent Color: {palette['accent']}
Neutral Light: {palette['neutral_light']}
Neutral Dark: {palette['neutral_dark']}

COMPLEMENTARY COLORS:
"""
        for i, color in enumerate(palette['complementary'], 1):
            guidelines += f"{i}. {color}\n"
        
        guidelines += f"""
USAGE GUIDELINES:
- Use the primary color for main brand elements
- Secondary color for supporting elements
- Accent color for calls-to-action and highlights
- Maintain consistent spacing and proportions
- Ensure logo has clear space around it

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        zip_file.writestr(f'{company_name}_brand_guidelines.txt', guidelines)
        
        # Add color palette JSON
        palette_json = json.dumps(palette, indent=2)
        zip_file.writestr(f'{company_name}_color_palette.json', palette_json)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


# ==================== MAIN APP ====================
def main():
    """Main Streamlit application"""
    
    # Load custom CSS
    load_custom_css()
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎨 Create Unique Logos & Build Your Full Brand Identity Instantly</h1>
        <p class="hero-subtitle">
            Generate professional logos, taglines, color palettes, and font recommendations 
            with our AI-powered brand identity generator
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar hint
    st.info("👈 **Configure your brand settings in the sidebar** (click the arrow if you don't see it)", icon="💡")
    
    # Sidebar for theme settings
    st.sidebar.title("⚙️ Brand Settings")
    st.sidebar.markdown("---")
    
    # Design Style Selection
    st.sidebar.subheader("🎨 Design Style")
    theme_style = st.sidebar.selectbox(
        "Choose Your Theme",
        [
            "Minimalist", 
            "Corporate", 
            "Creative", 
            "Luxury", 
            "Tech/Modern",
            "Playful",
            "Elegant",
            "Bold/Impactful"
        ],
        help="Choose a design style based on global branding standards"
    )
    
    # Show theme description
    theme_descriptions = {
        "Minimalist": "🍎 Apple/Google Style - Clean, simple, timeless",
        "Corporate": "💼 IBM/Deloitte Style - Professional, trustworthy",
        "Creative": "🎨 Airbnb/Dropbox Style - Innovative, artistic",
        "Luxury": "💎 Chanel/LV Style - Premium, sophisticated",
        "Tech/Modern": "🚀 Tesla/Spotify Style - Futuristic, cutting-edge",
        "Playful": "🎮 Lego/Disney Style - Fun, friendly, approachable",
        "Elegant": "✨ Tiffany/Cartier Style - Refined, timeless",
        "Bold/Impactful": "⚡ Nike/Red Bull Style - Powerful, energetic"
    }
    st.sidebar.info(theme_descriptions.get(theme_style, ""))
    
    st.sidebar.markdown("---")
    
    # AI Generation Settings
    st.sidebar.subheader("🤖 AI Generation")
    use_ai = st.sidebar.checkbox("Enable AI Logo Generation", value=False)
    
    if use_ai:
        api_provider = st.sidebar.selectbox(
            "AI Provider", 
            ["Freepik", "Stability AI", "Google Gemini"],
            help="Select which AI service to use for logo generation"
        )
        st.sidebar.success("✅ Provider ready!")
        
        if api_provider == "Google Gemini":
            st.sidebar.warning("⚠️ Gemini works for taglines only (no images)")
    else:
        api_provider = None
        st.sidebar.info("💡 Using built-in generators for quick results!")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("🎨 Premium Brand Identity Generator v2.0")
    
    # API keys are now stored in the code (see top of file)
    api_key = None  # Will be loaded from environment or constants
    
    # Main input form
    st.markdown('<h2 class="section-header">📝 Company Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input(
            "Company Name *",
            placeholder="e.g., TechVision",
            help="Enter your company or brand name"
        )
        
        industry = st.selectbox(
            "Industry / Sector *",
            ["Technology", "Finance", "Healthcare", "Education", "Retail", 
             "Food & Beverage", "Real Estate", "Entertainment", "Fashion", "Other"],
            help="Select your primary industry"
        )
    
    with col2:
        user_tagline = st.text_input(
            "Current Tagline (Optional)",
            placeholder="e.g., Innovation at its best",
            help="If you have an existing tagline, enter it here"
        )
        
        description = st.text_area(
            "Company Description *",
            placeholder="Briefly describe what your company does...",
            help="Provide a short description of your business",
            height=100
        )
    
    # Generate button
    generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
    with generate_col2:
        generate_button = st.button(
            "🚀 Generate Brand Assets",
            use_container_width=True,
            type="primary"
        )
    
    # Generate assets when button is clicked
    if generate_button:
        if not company_name or not description:
            st.error("⚠️ Please fill in all required fields (Company Name and Description)")
        else:
            with st.spinner("✨ Generating your brand identity..."):
                
                # Store data in session state
                if 'brand_data' not in st.session_state:
                    st.session_state.brand_data = {}
                
                # Generate logo(s)
                logos = generate_logo(
                    company_name, industry, theme_style, use_ai, api_provider, num_variations=3
                )
                st.session_state.brand_data['logos'] = logos  # Store all logos
                st.session_state.brand_data['logo'] = logos[0]  # First logo as default
                
                # Initialize selected logo index
                if 'selected_logo_idx' not in st.session_state:
                    st.session_state.selected_logo_idx = 0
                
                # Generate favicon
                st.session_state.brand_data['favicon'] = generate_favicon(
                    st.session_state.brand_data['logo']
                )
                
                # Generate taglines
                st.session_state.brand_data['taglines'] = generate_taglines(
                    company_name, industry, description, use_ai, api_provider
                )
                
                # Suggest fonts
                st.session_state.brand_data['fonts'] = suggest_fonts(industry, theme_style)
                
                # Generate color palette
                st.session_state.brand_data['palette'] = generate_palette(industry, theme_style)
                
                # Store other data
                st.session_state.brand_data['company_name'] = company_name
                st.session_state.brand_data['user_tagline'] = user_tagline
                st.session_state.brand_data['industry'] = industry
                st.session_state.brand_data['description'] = description
                st.session_state.brand_data['theme_style'] = theme_style
                
                st.success("✅ Brand assets generated successfully!")
    
    # Display results if data exists in session state
    if 'brand_data' in st.session_state and st.session_state.brand_data:
        brand_data = st.session_state.brand_data
        
        st.divider()
        
        # ==================== LOGO SECTION ====================
        st.markdown('<h2 class="section-header">🎨 Your Logo Variations</h2>', unsafe_allow_html=True)
        
        # Display all logo variations
        logos = brand_data.get('logos', [brand_data['logo']])
        
        if len(logos) > 1:
            st.write("Select your favorite logo design:")
            
            # Create columns for logo variations
            cols = st.columns(min(len(logos), 3))
            
            for idx, logo in enumerate(logos):
                with cols[idx % 3]:
                    st.image(logo, use_container_width=True)
                    
                    # Selection button
                    if st.button(
                        f"{'✨ Selected' if st.session_state.get('selected_logo_idx', 0) == idx else '👆 Select This'}",
                        key=f"select_logo_{idx}",
                        use_container_width=True,
                        type="primary" if st.session_state.get('selected_logo_idx', 0) == idx else "secondary"
                    ):
                        st.session_state.selected_logo_idx = idx
                        st.session_state.brand_data['logo'] = logos[idx]
                        st.rerun()
                    
                    # Download button for each variation
                    logo_buffer = io.BytesIO()
                    logo.save(logo_buffer, format='PNG')
                    logo_buffer.seek(0)
                    
                    st.download_button(
                        label=f"📥 Download",
                        data=logo_buffer,
                        file_name=f"{brand_data['company_name']}_logo_v{idx+1}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"download_logo_{idx}"
                    )
            
            st.divider()
            
            # Show selected logo in large format
            st.markdown('<h3 class="section-header">Selected Logo</h3>', unsafe_allow_html=True)
            selected_idx = st.session_state.get('selected_logo_idx', 0)
            selected_logo = logos[selected_idx]
            
            logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
            with logo_col2:
                st.image(selected_logo, use_container_width=True)
        else:
            # Single logo display
            logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
            
            with logo_col2:
                st.image(brand_data['logo'], use_container_width=True)
                
                # Download logo button
                logo_buffer = io.BytesIO()
                brand_data['logo'].save(logo_buffer, format='PNG')
                logo_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Logo (PNG)",
                    data=logo_buffer,
                    file_name=f"{brand_data['company_name']}_logo.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        st.divider()
        
        # ==================== TAGLINE SECTION ====================
        st.markdown('<h2 class="section-header">💬 Tagline Suggestions</h2>', unsafe_allow_html=True)
        
        st.write("Select a tagline that best represents your brand:")
        
        # Initialize selected tagline
        if 'selected_tagline' not in st.session_state:
            st.session_state.selected_tagline = brand_data['taglines'][0]
        
        for i, tagline in enumerate(brand_data['taglines']):
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                if st.button("✓", key=f"select_tagline_{i}", help="Select this tagline"):
                    st.session_state.selected_tagline = tagline
            with col2:
                is_selected = (tagline == st.session_state.selected_tagline)
                st.markdown(
                    f"""<div class="tagline-card" style="{'border-color: #667eea; background: #f0f4ff;' if is_selected else ''}">
                    <strong>{'✨ ' if is_selected else ''}{tagline}</strong>
                    </div>""",
                    unsafe_allow_html=True
                )
        
        st.divider()
        
        # ==================== FONT SECTION ====================
        st.markdown('<h2 class="section-header">🔤 Font Recommendations</h2>', unsafe_allow_html=True)
        
        st.write("These fonts complement your brand's identity:")
        
        for i, font in enumerate(brand_data['fonts'], 1):
            st.markdown(f"""
            <div class="font-card">
                <h3 style="margin-top: 0;">{i}. {font['name']}</h3>
                <p style="color: #666; margin: 0.5rem 0;"><em>{font['category']}</em></p>
                <p style="margin-bottom: 0;">{font['description']}</p>
                <p style="font-size: 1.5rem; margin-top: 1rem; font-family: {font['name']}, sans-serif;">
                    The quick brown fox jumps over the lazy dog
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # ==================== COLOR PALETTE SECTION ====================
        st.markdown('<h2 class="section-header">🎨 Color Palette</h2>', unsafe_allow_html=True)
        
        st.write("Your brand's color scheme:")
        
        # Main colors
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="color-swatch" style="background-color: {brand_data['palette']['primary']}; margin: 0 auto;"></div>
                <p class="color-label">Primary<br/>{brand_data['palette']['primary']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="color-swatch" style="background-color: {brand_data['palette']['secondary']}; margin: 0 auto;"></div>
                <p class="color-label">Secondary<br/>{brand_data['palette']['secondary']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center;">
                <div class="color-swatch" style="background-color: {brand_data['palette']['accent']}; margin: 0 auto;"></div>
                <p class="color-label">Accent<br/>{brand_data['palette']['accent']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        st.write("**Complementary Colors:**")
        
        comp_cols = st.columns(5)
        for i, color in enumerate(brand_data['palette']['complementary']):
            with comp_cols[i]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 80px; height: 80px; background-color: {color}; 
                         border-radius: 8px; margin: 10px auto; 
                         box-shadow: 0 2px 8px rgba(0,0,0,0.2);"></div>
                    <p style="font-size: 0.85rem; font-weight: 600; color: #666;">{color}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # ==================== SOCIAL MEDIA MOCKUP SECTION ====================
        st.markdown('<h2 class="section-header">📱 Social Media Preview</h2>', unsafe_allow_html=True)
        
        st.write("See how your brand looks on social media:")
        
        # Generate mockup
        mockup = create_social_media_mockup(
            brand_data['logo'],
            brand_data['company_name'],
            st.session_state.selected_tagline,
            brand_data['palette']
        )
        
        mockup_col1, mockup_col2, mockup_col3 = st.columns([1, 2, 1])
        with mockup_col2:
            st.image(mockup, use_container_width=True, caption="Instagram/LinkedIn Post Preview")
        
        st.divider()
        
        # ==================== DOWNLOAD ALL ASSETS ====================
        st.markdown('<h2 class="section-header">📦 Download All Assets</h2>', unsafe_allow_html=True)
        
        st.write("Get all your brand assets in a single ZIP file:")
        
        download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
        
        with download_col2:
            # Generate ZIP file with all logo variations
            logos_to_download = brand_data.get('logos', [brand_data['logo']])
            zip_data = download_assets(
                logos_to_download,
                brand_data['favicon'],
                brand_data['company_name'],
                st.session_state.selected_tagline,
                brand_data['fonts'],
                brand_data['palette'],
                mockup
            )
            
            st.download_button(
                label="📥 Download Complete Brand Package (ZIP)",
                data=zip_data,
                file_name=f"{brand_data['company_name']}_brand_identity.zip",
                mime="application/zip",
                use_container_width=True,
                type="primary"
            )
            
            st.info("""
            **Package includes:**
            - Logo (PNG, high resolution)
            - Favicon (256x256 PNG)
            - Social media mockup
            - Brand guidelines (TXT)
            - Color palette (JSON)
            """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>Made with ❤️ using Streamlit | Brand Identity Generator v1.0</p>
        <p style="font-size: 0.9rem;">
            <strong>Note:</strong> AI features require API keys from OpenAI or Stability AI. 
            Built-in generators provide instant results without API keys.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

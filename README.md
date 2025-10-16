# 🎨 Brand Identity Generator - Premium Edition

A complete Streamlit web application that generates professional brand identities including AI-powered logos, taglines, color palettes, and font recommendations.

## 🚀 **NEW: Deploy to ByteXL Nimbus Platform!**

This app is **ready for production deployment** on ByteXL's Nimbus Platform!

**Quick Deploy:**
1. See `DEPLOYMENT_QUICK_START.md` for 5-step guide
2. Full instructions in `NIMBUS_DEPLOYMENT.md`
3. Use checklist in `DEPLOYMENT_CHECKLIST.md`

---

## ✨ Features

### Premium UI/UX (v2.0)
- **8 Global Design Themes** - Apple, IBM, Nike, Chanel, Tesla, Lego, Tiffany, Red Bull styles
- **Premium Glassmorphism UI** - Modern gradient design with smooth animations
- **Responsive Design** - Works beautifully on desktop, tablet, and mobile
- **Professional Typography** - Google Fonts integration
- **Interactive Elements** - Hover effects, transitions, and loading states

### AI-Powered Generation
- **Multiple Logo Variations** - Get 2-3 unique logo designs per generation
- **3 AI Providers** - Freepik AI, Stability AI, Google Gemini
- **Smart Fallbacks** - Built-in generators if AI unavailable
- **Tagline Generation** - AI-powered professional taglines
- **Industry-Specific** - Customized for your business sector

### Complete Brand Package
- **Professional Logos** - AI-generated or geometric designs
- **5 Tagline Options** - Choose the perfect message
- **Color Palettes** - Primary, secondary, accent colors with psychology
- **Font Recommendations** - Industry-appropriate typography
- **Social Media Mockups** - Instagram/LinkedIn post previews
- **ZIP Download** - All assets in one package

### Design Themes (Global Standards)
- 🍎 **Minimalist** - Apple/Google Style
- 💼 **Corporate** - IBM/Deloitte Style
- 🎨 **Creative** - Airbnb/Dropbox Style
- 💎 **Luxury** - Chanel/Louis Vuitton Style
- 🚀 **Tech/Modern** - Tesla/Spotify Style
- 🎮 **Playful** - Lego/Disney Style
- ✨ **Elegant** - Tiffany/Cartier Style
- ⚡ **Bold/Impactful** - Nike/Red Bull Style

### Industry Support
- Technology
- Finance
- Healthcare
- Education
- Retail
- Food & Beverage
- Real Estate
- Entertainment
- Fashion
- Other

---

## 🚀 Quick Start

### Local Development

1. **Clone or download this repository**

2. **Install dependencies**
```powershell
pip install -r requirements.txt
```

3. **Set up environment variables (optional)**
```powershell
# Copy template
copy .env.example .env

# Edit with your API keys (optional for built-in generators)
notepad .env
```

4. **Run the application**
```powershell
streamlit run app.py
```

5. **Open your browser**
The app will automatically open at `http://localhost:8501`

---

## ☁️ Cloud Deployment (Nimbus Platform)

### Quick Deploy to ByteXL Nimbus:

**See detailed guides:**
- 📘 `DEPLOYMENT_QUICK_START.md` - 5 simple steps
- 📗 `NIMBUS_DEPLOYMENT.md` - Complete deployment guide
- 📋 `DEPLOYMENT_CHECKLIST.md` - Verification checklist

## 📋 Usage Instructions

### Basic Usage (No API Key Required)

1. **Enter Company Information:**
   - Company Name (required)
   - Current Tagline (optional)
   - Industry/Sector (required)
   - Company Description (required)

2. **Select Design Theme:**
   - Choose from Minimal, Modern, Retro, or Bold in the sidebar

3. **Generate Brand Assets:**
   - Click the "Generate Brand Assets" button
   - Wait for the generation process to complete

4. **Review and Download:**
   - Browse through your generated logo, taglines, fonts, and colors
   - Select your preferred tagline
   - Download individual assets or the complete brand package

### Advanced Usage (With AI Integration)

To enable AI-powered generation for more creative and unique results:

1. **Get an API Key:**
   - OpenAI: https://platform.openai.com/api-keys
   - Stability AI: https://platform.stability.ai/

2. **Enable AI in Settings:**
   - Check "Enable AI Generation" in the sidebar
   - Select your AI provider
   - Enter your API key

3. **Uncomment Dependencies:**
   Edit `requirements.txt` and uncomment:
   ```
   openai>=1.0.0
   # or
   stability-sdk>=0.8.0
   ```

4. **Install AI Libraries:**
   ```powershell
   pip install -r requirements.txt
   ```

## 🔧 Configuration

### AI Integration Setup

#### OpenAI DALL-E (for logo generation)

In `app.py`, locate the `generate_logo()` function and add:

```python
import openai

if use_ai and api_key:
    openai.api_key = api_key
    
    prompt = f"Professional {theme_style} style logo for {company_name}, a {industry} company, simple, modern, vector style, white background"
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = response['data'][0]['url']
    # Download and return image
    import requests
    from io import BytesIO
    
    response = requests.get(image_url)
    logo_image = Image.open(BytesIO(response.content))
    return logo_image
```

#### OpenAI GPT (for tagline generation)

In `app.py`, locate the `generate_taglines()` function and add:

```python
import openai

if use_ai and api_key:
    openai.api_key = api_key
    
    prompt = f'''Generate 5 creative and professional taglines for {company_name}, 
                 a {industry} company. Description: {description}
                 
                 Return only the taglines, one per line.'''
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    
    taglines = response.choices[0].message.content.strip().split('\n')
    return [t.strip('- ').strip() for t in taglines if t.strip()]
```

## 📦 What's Included in the Download Package

When you download the complete brand package, you get:

1. **Logo.png** - High-resolution logo (1000x1000px)
2. **Favicon.png** - Website/app icon (256x256px)
3. **Social_mockup.png** - Social media post preview (1080x1080px)
4. **Brand_guidelines.txt** - Complete brand guidelines including:
   - Selected tagline
   - Font recommendations
   - Color palette with hex codes
   - Usage guidelines
5. **Color_palette.json** - Color data in JSON format for easy integration

## 🎨 Customization

### Adding New Industries

Edit the `industry_base_colors` dictionary in the `generate_palette()` function:

```python
industry_base_colors = {
    'Your Industry': '#HEXCODE',
    # Add more industries...
}
```

### Adding New Fonts

Edit the `font_database` dictionary in the `suggest_fonts()` function:

```python
font_database = {
    'Your Industry': {
        'Your Theme': [
            {'name': 'Font Name', 'category': 'Sans-serif', 'description': 'Description'},
            # Add more fonts...
        ]
    }
}
```

### Adding New Design Themes

1. Create a new palette generation function:
```python
def generate_your_theme_palette(base_color):
    return {
        'primary': base_color,
        'secondary': '#HEXCODE',
        'accent': '#HEXCODE',
        # ... more colors
    }
```

2. Add the theme to the `generate_palette()` function
3. Add the theme option to the sidebar selectbox

## 🛠️ Technical Details

### Tech Stack
- **Framework:** Streamlit 1.28+
- **Image Processing:** Pillow 10.0+
- **AI Integration (Optional):** OpenAI, Stability AI
- **Python Version:** 3.8+

### Project Structure
```
brand_identity_generator/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Key Functions

- `generate_logo()` - Creates logos (placeholder or AI-generated)
- `generate_taglines()` - Generates tagline suggestions
- `suggest_fonts()` - Recommends fonts based on industry/theme
- `generate_palette()` - Creates color palettes
- `create_social_media_mockup()` - Generates social media previews
- `download_assets()` - Packages all assets into a ZIP file

## 🐛 Troubleshooting

### Common Issues

**Issue:** Streamlit not found
```powershell
# Solution:
pip install streamlit --upgrade
```

**Issue:** PIL/Pillow errors
```powershell
# Solution:
pip uninstall PIL Pillow
pip install Pillow --upgrade
```

**Issue:** Font not found errors
- The app uses system fonts (Arial). If unavailable, it falls back to default fonts.
- To use custom fonts, add TTF files to the project directory and update font paths.

**Issue:** AI generation not working
- Verify your API key is correct
- Check API usage limits/quotas
- Ensure the AI library is installed (`openai` or `stability-sdk`)

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and enhance this application for your needs!

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the Streamlit documentation: https://docs.streamlit.io
3. Check API provider documentation for AI features

## 🎯 Future Enhancements

Potential features to add:
- [ ] More AI providers (Midjourney, Leonardo.AI)
- [ ] Custom font upload support
- [ ] More social media mockup templates
- [ ] Brand style variations
- [ ] Export to different file formats (SVG, PDF)
- [ ] Brand comparison tool
- [ ] Save/load brand profiles
- [ ] More detailed brand guidelines
- [ ] Business card mockups
- [ ] Letterhead templates

## 🌟 Credits

Created with ❤️ using Streamlit

Inspired by Zoviz and modern brand identity generators.

---

**Happy Branding! 🎨**

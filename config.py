# Configuration file for Brand Identity Generator
# Edit this file to customize the application behavior

# ==================== APP SETTINGS ====================

APP_TITLE = "Brand Identity Generator"
APP_ICON = "🎨"
HERO_TITLE = "Create Unique Logos & Build Your Full Brand Identity Instantly"
HERO_SUBTITLE = """Generate professional logos, taglines, color palettes, and font recommendations 
with our AI-powered brand identity generator"""

# ==================== DESIGN THEMES ====================

AVAILABLE_THEMES = [
    "Minimal",
    "Modern", 
    "Retro",
    "Bold"
]

# ==================== INDUSTRIES ====================

INDUSTRIES = [
    "Technology",
    "Finance",
    "Healthcare",
    "Education",
    "Retail",
    "Food & Beverage",
    "Real Estate",
    "Entertainment",
    "Fashion",
    "Other"
]

# ==================== AI PROVIDERS ====================

AI_PROVIDERS = [
    "OpenAI",
    "Stability AI"
]

# ==================== COLOR SETTINGS ====================

# Default gradient colors for hero section
HERO_GRADIENT_START = "#667eea"
HERO_GRADIENT_END = "#764ba2"

# Primary brand color for UI elements
UI_PRIMARY_COLOR = "#667eea"

# ==================== IMAGE SETTINGS ====================

# Logo dimensions
LOGO_SIZE = 1000  # pixels (square)

# Favicon dimensions
FAVICON_SIZE = 256  # pixels (square)

# Social media mockup dimensions
MOCKUP_WIDTH = 1080  # pixels
MOCKUP_HEIGHT = 1080  # pixels

# ==================== GENERATION SETTINGS ====================

# Number of taglines to generate
NUM_TAGLINES = 5

# Number of fonts to suggest
NUM_FONTS = 3

# Number of complementary colors in palette
NUM_COMPLEMENTARY_COLORS = 5

# ==================== API SETTINGS ====================

# OpenAI settings
OPENAI_MODEL = "gpt-4"
OPENAI_IMAGE_SIZE = "1024x1024"
OPENAI_TEMPERATURE = 0.8

# ==================== UI SETTINGS ====================

# Enable/disable features
SHOW_FAVICON = True
SHOW_SOCIAL_MOCKUP = True
SHOW_DOWNLOAD_ALL = True

# Layout settings
USE_WIDE_LAYOUT = True
SIDEBAR_STATE = "expanded"  # "expanded" or "collapsed"

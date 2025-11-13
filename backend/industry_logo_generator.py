"""
Revolutionary Industry-Specific Logo Generation System
Creates unique, contextually intelligent logos based on industry
NO OTHER PLATFORM HAS THIS LEVEL OF CUSTOMIZATION
"""
import logging
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
from typing import Dict, List, Tuple, Any
import hashlib

logger = logging.getLogger(__name__)


class IndustryLogoGenerator:
    """
    Next-generation logo generator with industry intelligence
    Each industry gets unique symbolic elements and design patterns
    """
    
    # Industry-specific design DNA
    INDUSTRY_PATTERNS = {
        "healthcare": {
            "symbols": ["stethoscope", "heart", "cross", "pulse", "shield", "medical_kit"],
            "shapes": ["shield", "circle", "heart"],
            "color_themes": ["healing_blue", "medical_green", "trust_purple"],
            "patterns": ["waves", "heartbeat", "cellular"],
            "style": "clean_medical",
            "keywords": ["care", "health", "wellness", "medical", "life"]
        },
        "healthtech": {
            "symbols": ["heart_tech", "medical_chip", "digital_cross", "health_shield"],
            "shapes": ["hexagon", "circuit", "shield"],
            "color_themes": ["tech_blue", "medical_cyan", "innovation_green"],
            "patterns": ["circuit", "digital_waves", "tech_grid"],
            "style": "modern_tech",
            "keywords": ["digital health", "innovation", "care", "technology"]
        },
        "floral": {
            "symbols": ["flower", "rose", "leaf", "bouquet", "petal", "garden"],
            "shapes": ["flower", "circle", "organic"],
            "color_themes": ["rose_pink", "garden_green", "floral_purple"],
            "patterns": ["petal_arrangement", "leaf_vines", "botanical"],
            "style": "natural_elegant",
            "keywords": ["flower", "bouquet", "floral", "garden", "bloom", "petal", "rose", "decoration"]
        },
        "food": {
            "symbols": ["plate", "chef_hat", "fork_knife", "dish", "recipe"],
            "shapes": ["circle", "plate", "rounded"],
            "color_themes": ["food_red", "fresh_green", "warm_orange"],
            "patterns": ["culinary", "ingredients", "dish_pattern"],
            "style": "appetizing_warm",
            "keywords": ["food", "restaurant", "dining", "cuisine", "chef", "meal", "recipe"]
        },
        "beauty": {
            "symbols": ["lotus", "spa_stones", "butterfly", "leaf", "droplet"],
            "shapes": ["circle", "lotus", "wave"],
            "color_themes": ["spa_blue", "calm_purple", "zen_green"],
            "patterns": ["zen_circles", "botanical", "flowing"],
            "style": "elegant_calm",
            "keywords": ["beauty", "spa", "wellness", "cosmetic", "skincare", "salon"]
        },
        "technology": {
            "symbols": ["circuit", "chip", "network", "binary", "lightning", "atom"],
            "shapes": ["hexagon", "triangle", "cube"],
            "color_themes": ["tech_blue", "electric_cyan", "future_purple"],
            "patterns": ["circuit_board", "network_nodes", "digital_matrix"],
            "style": "futuristic",
            "keywords": ["innovation", "digital", "tech", "future"]
        },
        "fintech": {
            "symbols": ["shield_coin", "secure_wallet", "blockchain", "graph_up", "diamond"],
            "shapes": ["shield", "diamond", "vault"],
            "color_themes": ["trust_blue", "wealth_gold", "secure_green"],
            "patterns": ["blockchain_chain", "security_grid", "currency_flow"],
            "style": "secure_professional",
            "keywords": ["secure", "finance", "trust", "growth"]
        },
        "ai_ml": {
            "symbols": ["neural_net", "brain", "nodes", "ai_chip", "infinity"],
            "shapes": ["neural", "sphere", "network"],
            "color_themes": ["ai_purple", "neural_blue", "intelligence_cyan"],
            "patterns": ["neural_network", "brain_waves", "data_flow"],
            "style": "intelligent_modern",
            "keywords": ["intelligence", "learning", "neural", "smart"]
        },
        "ecommerce": {
            "symbols": ["cart", "bag", "package", "tag", "storefront"],
            "shapes": ["bag", "circle", "rounded_square"],
            "color_themes": ["shopping_orange", "retail_red", "commerce_blue"],
            "patterns": ["retail_grid", "shopping_flow", "package_pattern"],
            "style": "friendly_modern",
            "keywords": ["shop", "buy", "commerce", "retail"]
        },
        "cybersecurity": {
            "symbols": ["shield_lock", "secure_key", "firewall", "encrypted", "fortress"],
            "shapes": ["shield", "hexagon", "fortress"],
            "color_themes": ["security_blue", "protect_red", "cyber_dark"],
            "patterns": ["security_grid", "encrypted_layer", "firewall_barrier"],
            "style": "secure_bold",
            "keywords": ["secure", "protect", "defense", "safe"]
        },
        "blockchain": {
            "symbols": ["chain", "block", "distributed", "crypto", "ledger"],
            "shapes": ["cube", "chain_link", "network"],
            "color_themes": ["crypto_gold", "chain_blue", "distributed_purple"],
            "patterns": ["blockchain_grid", "distributed_nodes", "crypto_pattern"],
            "style": "decentralized_modern",
            "keywords": ["decentralized", "chain", "crypto", "distributed"]
        },
        "saas": {
            "symbols": ["cloud", "layers", "infinity", "rocket", "star"],
            "shapes": ["cloud", "layers", "rounded"],
            "color_themes": ["saas_blue", "cloud_cyan", "software_purple"],
            "patterns": ["cloud_layer", "software_grid", "service_flow"],
            "style": "professional_clean",
            "keywords": ["software", "cloud", "service", "platform"]
        },
        "education": {
            "symbols": ["book", "graduation_cap", "light_bulb", "growth_tree", "star"],
            "shapes": ["book", "shield", "circle"],
            "color_themes": ["learning_blue", "knowledge_green", "wisdom_purple"],
            "patterns": ["book_pages", "learning_path", "growth_rings"],
            "style": "approachable_smart",
            "keywords": ["learn", "grow", "knowledge", "education"]
        }
    }
    
    def __init__(self):
        """Initialize industry-intelligent logo generator"""
        self.width = 1000  # Higher resolution for premium quality
        self.height = 1000
        self.cache = {}
        logger.info("✅ Revolutionary Industry Logo Generator initialized")
    
    def generate_industry_logo(
        self,
        company_name: str,
        industry: str,
        colors: List[str],
        style_preference: str = "auto"
    ) -> str:
        """
        Generate a unique industry-specific logo
        style_preference: "auto", "variation_1", "variation_2", "variation_3"
        """
        try:
            # Map industry to pattern
            industry_lower = industry.lower()
            industry_key = self._detect_industry(industry_lower)
            
            pattern = self.INDUSTRY_PATTERNS.get(industry_key, self.INDUSTRY_PATTERNS["technology"])
            
            # Include style_preference in cache key to ensure different variations
            cache_key = hashlib.md5(f"{company_name}{industry_key}{colors}{style_preference}v2".encode()).hexdigest()
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Determine which variation to generate based on style_preference
            variation_index = 0
            if style_preference == "variation_2":
                variation_index = 1
            elif style_preference == "variation_3":
                variation_index = 2
            
            # Generate based on industry with variation
            if industry_key == "healthcare":
                logo_data = self._generate_healthcare_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "healthtech":
                logo_data = self._generate_healthtech_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "floral":
                logo_data = self._generate_floral_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "food":
                logo_data = self._generate_food_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "beauty":
                logo_data = self._generate_beauty_logo(company_name, colors, pattern, variation_index)
            elif industry_key in ["technology", "ai_ml", "devtools"]:
                logo_data = self._generate_tech_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "fintech":
                logo_data = self._generate_fintech_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "cybersecurity":
                logo_data = self._generate_security_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "blockchain":
                logo_data = self._generate_blockchain_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "ecommerce":
                logo_data = self._generate_ecommerce_logo(company_name, colors, pattern, variation_index)
            elif industry_key == "saas":
                logo_data = self._generate_saas_logo(company_name, colors, pattern, variation_index)
            else:
                logo_data = self._generate_tech_logo(company_name, colors, pattern, variation_index)
            
            self.cache[cache_key] = logo_data
            return logo_data
            
        except Exception as e:
            logger.error(f"Error generating industry logo: {e}")
            raise
    
    def _detect_industry(self, industry_text: str) -> str:
        """Intelligent industry detection from text"""
        industry_text = industry_text.lower()
        
        # Floral/Bouquet detection (NEW!)
        floral_keywords = ["flower", "floral", "bouquet", "bloom", "petal", "rose", "garden", "florist", "botanical", "blossom", "plant"]
        food_keywords = ["food", "restaurant", "dining", "cuisine", "chef", "culinary", "meal", "recipe", "kitchen", "cafe", "bakery"]
        beauty_keywords = ["beauty", "spa", "salon", "cosmetic", "skincare", "wellness", "massage", "facial", "makeup"]
        
        # Healthcare detection with comprehensive keywords
        healthcare_keywords = ["health", "medical", "hospital", "clinic", "pharma", "wellness", "doctor", "patient", "medicine", "therapy", "care"]
        tech_keywords = ["tech", "digital", "ai", "platform", "app", "software", "technology"]
        
        has_floral = any(word in industry_text for word in floral_keywords)
        has_food = any(word in industry_text for word in food_keywords)
        has_beauty = any(word in industry_text for word in beauty_keywords)
        has_healthcare = any(word in industry_text for word in healthcare_keywords)
        has_tech = any(word in industry_text for word in tech_keywords)
        
        # Priority detection
        if has_floral:
            return "floral"
        
        if has_food:
            return "food"
        
        if has_beauty:
            return "beauty"
        
        if has_healthcare:
            # Distinguish between pure healthcare and healthtech
            if has_tech:
                return "healthtech"
            return "healthcare"
        
        # AI/ML detection (prioritize over general tech)
        if any(word in industry_text for word in ["ai", "ml", "machine learning", "artificial intelligence", "neural", "deep learning", "data science"]):
            return "ai_ml"
        
        # Finance detection
        if any(word in industry_text for word in ["finance", "fintech", "banking", "payment", "money", "trading", "investment", "wallet", "transaction"]):
            return "fintech"
        
        # Security detection
        if any(word in industry_text for word in ["security", "cyber", "protection", "defense", "encryption", "firewall", "antivirus", "threat"]):
            return "cybersecurity"
        
        # Blockchain detection
        if any(word in industry_text for word in ["blockchain", "crypto", "bitcoin", "ethereum", "web3", "defi", "nft", "token"]):
            return "blockchain"
        
        # E-commerce detection
        if any(word in industry_text for word in ["commerce", "shop", "retail", "marketplace", "store", "ecommerce", "e-commerce", "shopping", "cart"]):
            return "ecommerce"
        
        # SaaS detection
        if any(word in industry_text for word in ["saas", "software", "cloud", "platform", "service", "subscription", "b2b"]):
            return "saas"
        
        # Education detection
        if any(word in industry_text for word in ["education", "learning", "school", "training", "course", "university", "student", "teach"]):
            return "education"
        
        # Fallback to technology for tech-related keywords
        if has_tech:
            return "technology"
        
        return "saas"  # Default to SaaS for generic business
    
    def _generate_healthcare_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate healthcare-specific logo with medical symbols"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#0EA5E9')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#10B981')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#FFFFFF')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # VARIATION 0: Medical shield with STETHOSCOPE
        if variation == 0:
            shield_size = 350
            self._draw_medical_shield(draw, center_x, center_y, shield_size, primary, secondary)
            # Draw STETHOSCOPE instead of just cross!
            self._draw_stethoscope(draw, center_x, center_y, 280, (255, 255, 255, 255))
        
        # VARIATION 1: Heart symbol with pulse and MEDICAL KIT
        elif variation == 1:
            # Draw circular background
            for layer in range(30):
                progress = layer / 30
                color = self._blend_colors(primary, secondary, progress)
                scale = 1 - (layer * 0.015)
                radius = 350 * scale
                draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], fill=color)
            
            # Large heart symbol
            self._draw_heart_symbol(draw, center_x, center_y - 50, 200, (255, 255, 255, 255))
            # Pulse line
            self._draw_pulse_line(draw, center_x, center_y + 180, 280, accent)
            # Medical cross
            self._draw_medical_cross(draw, center_x, center_y - 50, 100, accent)
        
        # VARIATION 2: Medical badge with plus
        else:
            # Octagonal badge
            num_sides = 8
            badge_size = 340
            points = []
            for i in range(num_sides):
                angle = math.radians(i * (360 / num_sides) - 22.5)
                x = center_x + badge_size * math.cos(angle)
                y = center_y + badge_size * math.sin(angle)
                points.append((x, y))
            
            for layer in range(35):
                progress = layer / 35
                color = self._blend_colors(primary, secondary, progress)
                scale = 1 - (layer * 0.018)
                scaled_points = [(center_x + (x - center_x) * scale, center_y + (y - center_y) * scale) for x, y in points]
                draw.polygon(scaled_points, fill=color)
            
            # Medical cross
            self._draw_medical_cross(draw, center_x, center_y, 160, (255, 255, 255, 255))
        
        # NO TEXT - Pure visual medical logo!
        return self._image_to_base64(img)
    
    def _generate_healthtech_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate healthtech logo - fusion of medical + technology"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#06B6D4')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#3B82F6')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#10B981')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Hexagonal tech frame
        self._draw_tech_hexagon(draw, center_x, center_y, 320, primary, secondary)
        
        # Digital heartbeat/health wave
        self._draw_digital_health_wave(draw, center_x, center_y, 280, accent)
        
        # Circuit pattern background
        self._draw_mini_circuits(draw, center_x, center_y, 350, secondary, alpha=100)

        # Central medical chip icon
        self._draw_medical_chip(draw, center_x, center_y, 140, (255, 255, 255, 255))
        # No text overlay — symbol-first design

        return self._image_to_base64(img)
    
    def _generate_floral_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate floral/bouquet logo with flowers, petals, and leaves - PURE VISUAL!"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#EC4899')  # Pink
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#10B981')  # Green
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#A855F7')  # Purple
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # VARIATION 0: Rose with petals
        if variation == 0:
            # Draw leaves first (background)
            self._draw_leaf(draw, center_x - 200, center_y + 100, 120, 60, secondary, -30)
            self._draw_leaf(draw, center_x + 200, center_y + 100, 120, 60, secondary, 30)
            
            # Draw rose petals (layered)
            self._draw_rose_flower(draw, center_x, center_y, 280, primary, accent)
            
            # Small decorative flowers around
            self._draw_simple_flower(draw, center_x - 180, center_y - 180, 80, accent)
            self._draw_simple_flower(draw, center_x + 180, center_y - 180, 80, accent)
        
        # VARIATION 1: Botanical circle with multiple flowers
        elif variation == 1:
            # Circular leaf wreath
            num_leaves = 12
            for i in range(num_leaves):
                angle = math.radians(i * (360 / num_leaves))
                leaf_x = center_x + 320 * math.cos(angle)
                leaf_y = center_y + 320 * math.sin(angle)
                leaf_angle = math.degrees(angle) + 90
                self._draw_leaf(draw, leaf_x, leaf_y, 100, 45, secondary, leaf_angle)
            
            # Central flower bouquet - 3 flowers
            self._draw_simple_flower(draw, center_x, center_y - 60, 140, primary)
            self._draw_simple_flower(draw, center_x - 90, center_y + 40, 120, accent)
            self._draw_simple_flower(draw, center_x + 90, center_y + 40, 120, primary)
        
        # VARIATION 2: Single elegant flower with stem
        else:
            # Stem
            stem_width = 20
            stem_height = 280
            draw.rectangle([
                center_x - stem_width // 2, center_y,
                center_x + stem_width // 2, center_y + stem_height
            ], fill=secondary)
            
            # Leaves on stem
            self._draw_leaf(draw, center_x - 80, center_y + 100, 100, 50, secondary, -20)
            self._draw_leaf(draw, center_x + 80, center_y + 140, 100, 50, secondary, 20)
            
            # Large flower on top
            self._draw_detailed_flower(draw, center_x, center_y - 40, 250, primary, accent)
        
        # NO TEXT - Pure visual logo!
        return self._image_to_base64(img)
    
    def _generate_food_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate food/restaurant logo with culinary elements - PURE VISUAL!"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#EF4444')  # Red
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#F97316')  # Orange
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#10B981')  # Green
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # VARIATION 0: Chef hat with fork and spoon
        if variation == 0:
            # Chef hat
            self._draw_chef_hat(draw, center_x, center_y - 80, 240, (255, 255, 255, 255), primary)
            
            # Crossed fork and spoon below
            self._draw_fork(draw, center_x - 80, center_y + 140, 200, secondary, -30)
            self._draw_spoon(draw, center_x + 80, center_y + 140, 200, secondary, 30)
        
        # VARIATION 1: Plate with food elements
        elif variation == 1:
            # Large circular plate
            for layer in range(25):
                progress = layer / 25
                color = self._blend_colors(primary, secondary, progress)
                scale = 1 - (layer * 0.02)
                radius = 350 * scale
                draw.ellipse([
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius
                ], fill=color)
            
            # Food elements on plate
            self._draw_leaf(draw, center_x - 100, center_y - 50, 90, 40, accent, -15)
            self._draw_leaf(draw, center_x + 100, center_y - 50, 90, 40, accent, 15)
            self._draw_simple_flower(draw, center_x, center_y, 100, accent)  # Garnish flower
            
            # Fork and knife on sides
            self._draw_fork(draw, center_x - 280, center_y, 180, (255, 255, 255, 200), 90)
            self._draw_knife(draw, center_x + 280, center_y, 180, (255, 255, 255, 200), 90)
        
        # VARIATION 2: Dome/cloche reveal
        else:
            # Serving dome
            self._draw_serving_dome(draw, center_x, center_y, 300, primary, secondary)
            
            # Steam rising
            self._draw_steam(draw, center_x - 80, center_y - 180, accent)
            self._draw_steam(draw, center_x, center_y - 200, accent)
            self._draw_steam(draw, center_x + 80, center_y - 180, accent)
        
        return self._image_to_base64(img)
    
    def _generate_beauty_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate beauty/spa logo with elegant elements - PURE VISUAL!"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#A855F7')  # Purple
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#06B6D4')  # Cyan
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#EC4899')  # Pink
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # VARIATION 0: Lotus flower (spa symbol)
        if variation == 0:
            self._draw_lotus_flower(draw, center_x, center_y, 300, primary, secondary)
            
            # Water ripples
            for i in range(3):
                ripple_radius = 380 + (i * 40)
                alpha = 150 - (i * 40)
                ripple_color = (*secondary[:3], alpha)
                draw.ellipse([
                    center_x - ripple_radius, center_y - ripple_radius,
                    center_x + ripple_radius, center_y + ripple_radius
                ], outline=ripple_color, width=3)
        
        # VARIATION 1: Butterfly with flowers
        elif variation == 1:
            # Butterfly
            self._draw_butterfly(draw, center_x, center_y - 80, 280, primary, accent)
            
            # Flowers below
            self._draw_simple_flower(draw, center_x - 100, center_y + 180, 100, accent)
            self._draw_simple_flower(draw, center_x + 100, center_y + 180, 100, secondary)
        
        # VARIATION 2: Zen stones with leaf
        else:
            # Stack of spa stones
            self._draw_spa_stone(draw, center_x, center_y + 120, 280, 100, primary)
            self._draw_spa_stone(draw, center_x, center_y, 240, 90, secondary)
            self._draw_spa_stone(draw, center_x, center_y - 100, 200, 80, accent)
            
            # Elegant leaf on top
            green_color = self._parse_color('#10B981')
            self._draw_leaf(draw, center_x, center_y - 180, 160, 70, green_color, 0)
        
        return self._image_to_base64(img)
    
    def _generate_tech_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate technology logo with circuit/network elements"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#6366F1')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#8B5CF6')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#EC4899')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # VARIATION 0: Neural network
        if variation == 0:
            self._draw_neural_network(draw, center_x, center_y, 350, primary, secondary)
            self._draw_tech_core(draw, center_x, center_y, 180, accent)
            self._draw_connection_nodes(draw, center_x, center_y, 300, secondary, 8)
        
        # VARIATION 1: Hexagonal tech grid
        elif variation == 1:
            self._draw_tech_hexagon(draw, center_x, center_y, 340, primary, secondary)
            self._draw_mini_circuits(draw, center_x, center_y, 360, secondary, alpha=120)
            # Central tech symbol
            for i in range(6):
                angle = math.radians(i * 60)
                x1 = center_x + 100 * math.cos(angle)
                y1 = center_y + 100 * math.sin(angle)
                x2 = center_x + 160 * math.cos(angle)
                y2 = center_y + 160 * math.sin(angle)
                draw.line([(x1, y1), (x2, y2)], fill=accent, width=10)
                draw.ellipse([x2 - 15, y2 - 15, x2 + 15, y2 + 15], fill=accent)
        
        # VARIATION 2: Circuit board style
        else:
            # Circular gradient background
            for layer in range(40):
                progress = layer / 40
                color = self._blend_colors(primary, secondary, progress)
                scale = 1 - (layer * 0.015)
                radius = 360 * scale
                draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], fill=color)
            
            # Circuit patterns
            for i in range(12):
                angle = math.radians(i * 30)
                x1 = center_x + 280 * math.cos(angle)
                y1 = center_y + 280 * math.sin(angle)
                draw.line([(center_x, center_y), (x1, y1)], fill=accent, width=6)
                draw.ellipse([x1 - 20, y1 - 20, x1 + 20, y1 + 20], fill=accent)
        
    # No initials overlay — emphasize visual tech elements
        
        return self._image_to_base64(img)
    
    def _generate_fintech_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate fintech logo with security + finance elements"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#0EA5E9')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#10B981')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#F59E0B')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Diamond/vault shape for security
        self._draw_vault_shield(draw, center_x, center_y, 340, primary, secondary)
        
        # Growth arrow / financial chart
        self._draw_growth_chart(draw, center_x, center_y, 250, accent)
        
        # Security lock element
        self._draw_secure_lock(draw, center_x, center_y - 80, 120, (255, 255, 255, 255))
        
    # No initials overlay — emphasize vault/lock and chart visuals
        
        return self._image_to_base64(img)
    
    def _generate_security_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate cybersecurity logo with protection elements"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#3B82F6')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#EF4444')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#10B981')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Fortress/shield design
        self._draw_fortress_shield(draw, center_x, center_y, 360, primary, secondary)
        
        # Encryption layers
        self._draw_encryption_layers(draw, center_x, center_y, 320, secondary, alpha=120)
        
        # Central lock/key
        self._draw_secure_lock(draw, center_x, center_y, 150, (255, 255, 255, 255))
        
    # No initials overlay — emphasize shield and lock visuals
        
        return self._image_to_base64(img)
    
    def _generate_blockchain_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate blockchain logo with chain/distributed elements"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#F59E0B')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#8B5CF6')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#06B6D4')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Cubic/block structure
        self._draw_blockchain_cubes(draw, center_x, center_y, 320, primary, secondary)
        
        # Chain connections
        self._draw_chain_links(draw, center_x, center_y, 350, accent)
        
        # Distributed nodes
        self._draw_connection_nodes(draw, center_x, center_y, 380, secondary, 6)
        
    # No initials overlay — emphasize cubes and chains
        
        return self._image_to_base64(img)
    
    def _generate_ecommerce_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate e-commerce logo with shopping elements"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#F97316')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#EF4444')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#10B981')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Shopping bag/cart shape
        self._draw_shopping_bag(draw, center_x, center_y, 340, primary, secondary)
        
        # Price tag element
        self._draw_price_tag(draw, center_x + 120, center_y - 120, 80, accent)
        
    # No initials overlay — emphasize bag and tag visuals
        
        return self._image_to_base64(img)
    
    def _generate_saas_logo(self, name: str, colors: List[str], pattern: Dict, variation: int = 0) -> str:
        """Generate SaaS logo with cloud/layers elements"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        primary = self._parse_color(colors[0] if colors else '#0EA5E9')
        secondary = self._parse_color(colors[1] if len(colors) > 1 else '#8B5CF6')
        accent = self._parse_color(colors[2] if len(colors) > 2 else '#10B981')
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Cloud layers design
        self._draw_cloud_layers(draw, center_x, center_y, 340, primary, secondary)
        
        # Software infinity symbol
        self._draw_infinity_symbol(draw, center_x, center_y, 200, accent)
        
    # No initials overlay — emphasize cloud/infinity visuals
        
        return self._image_to_base64(img)
    
    # ==================== DRAWING HELPER METHODS ====================
    
    # MEDICAL HELPERS
    def _draw_stethoscope(self, draw, cx, cy, size, color):
        """Draw a stethoscope - iconic medical symbol!"""
        # Earpieces (top)
        ear_size = size * 0.15
        ear_spacing = size * 0.4
        draw.ellipse([
            cx - ear_spacing - ear_size, cy - size*0.4,
            cx - ear_spacing + ear_size, cy - size*0.4 + ear_size*2
        ], fill=color)
        draw.ellipse([
            cx + ear_spacing - ear_size, cy - size*0.4,
            cx + ear_spacing + ear_size, cy - size*0.4 + ear_size*2
        ], fill=color)
        
        # Tubing - curved lines
        # Left tube
        for i in range(20):
            t = i / 19
            x1 = cx - ear_spacing + t * ear_spacing
            y1 = cy - size*0.3 + math.sin(t * math.pi) * size * 0.2
            x2 = cx - ear_spacing + (t + 0.05) * ear_spacing
            y2 = cy - size*0.3 + math.sin((t + 0.05) * math.pi) * size * 0.2
            draw.line([x1, y1, x2, y2], fill=color, width=12)
        
        # Right tube
        for i in range(20):
            t = i / 19
            x1 = cx + ear_spacing - t * ear_spacing
            y1 = cy - size*0.3 + math.sin(t * math.pi) * size * 0.2
            x2 = cx + ear_spacing - (t + 0.05) * ear_spacing
            y2 = cy - size*0.3 + math.sin((t + 0.05) * math.pi) * size * 0.2
            draw.line([x1, y1, x2, y2], fill=color, width=12)
        
        # Main tube going down
        draw.line([cx, cy - size*0.1, cx, cy + size*0.3], fill=color, width=14)
        
        # Chest piece (diaphragm)
        chest_piece_size = size * 0.25
        draw.ellipse([
            cx - chest_piece_size, cy + size*0.3,
            cx + chest_piece_size, cy + size*0.3 + chest_piece_size*2
        ], fill=color)
        
        # Inner circle of chest piece
        inner_size = chest_piece_size * 0.6
        draw.ellipse([
            cx - inner_size, cy + size*0.3 + chest_piece_size - inner_size,
            cx + inner_size, cy + size*0.3 + chest_piece_size + inner_size
        ], outline=(100, 100, 100, 255), width=4)
    
    # FLORAL HELPERS
    def _draw_leaf(self, draw, cx, cy, length, width, color, angle_deg):
        """Draw a leaf shape"""
        # Convert angle to radians
        angle = math.radians(angle_deg)
        
        # Leaf is an ellipse rotated
        points = []
        for i in range(20):
            t = i / 19 * math.pi
            x = (math.sin(t) * width / 2) * math.cos(angle) - (math.cos(t) * length / 2) * math.sin(angle)
            y = (math.sin(t) * width / 2) * math.sin(angle) + (math.cos(t) * length / 2) * math.cos(angle)
            points.append((cx + x, cy + y))
        
        draw.polygon(points, fill=color)
    
    def _draw_rose_flower(self, draw, cx, cy, size, primary, accent):
        """Draw a layered rose flower"""
        # Multiple layers of petals
        for layer in range(5):
            petal_count = 8 - layer
            petal_size = size * (1 - layer * 0.15)
            rotation_offset = layer * 15
            
            for i in range(petal_count):
                angle = math.radians((360 / petal_count) * i + rotation_offset)
                petal_x = cx + (petal_size * 0.3) * math.cos(angle)
                petal_y = cy + (petal_size * 0.3) * math.sin(angle)
                
                # Petal color - lighter towards center
                color = self._blend_colors(primary, accent, layer / 5)
                
                # Draw petal (ellipse)
                petal_width = petal_size * 0.4
                petal_height = petal_size * 0.6
                draw.ellipse([
                    petal_x - petal_width/2, petal_y - petal_height/2,
                    petal_x + petal_width/2, petal_y + petal_height/2
                ], fill=color)
        
        # Center
        draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=accent)
    
    def _draw_simple_flower(self, draw, cx, cy, size, color):
        """Draw a simple 5-petal flower"""
        petal_count = 5
        petal_radius = size * 0.4
        
        for i in range(petal_count):
            angle = math.radians((360 / petal_count) * i - 90)
            petal_x = cx + (size * 0.35) * math.cos(angle)
            petal_y = cy + (size * 0.35) * math.sin(angle)
            
            draw.ellipse([
                petal_x - petal_radius, petal_y - petal_radius,
                petal_x + petal_radius, petal_y + petal_radius
            ], fill=color)
        
        # Center
        center_color = self._darken_color_rgba(color, 0.3)
        center_size = size * 0.2
        draw.ellipse([cx - center_size, cy - center_size, cx + center_size, cy + center_size], fill=center_color)
    
    def _draw_detailed_flower(self, draw, cx, cy, size, primary, accent):
        """Draw a detailed flower with multiple layers"""
        # Outer petals
        for i in range(8):
            angle = math.radians(i * 45)
            petal_x = cx + (size * 0.4) * math.cos(angle)
            petal_y = cy + (size * 0.4) * math.sin(angle)
            petal_size = size * 0.5
            draw.ellipse([
                petal_x - petal_size/2, petal_y - petal_size/2,
                petal_x + petal_size/2, petal_y + petal_size/2
            ], fill=primary)
        
        # Inner petals
        for i in range(6):
            angle = math.radians(i * 60 + 30)
            petal_x = cx + (size * 0.25) * math.cos(angle)
            petal_y = cy + (size * 0.25) * math.sin(angle)
            petal_size = size * 0.35
            draw.ellipse([
                petal_x - petal_size/2, petal_y - petal_size/2,
                petal_x + petal_size/2, petal_y + petal_size/2
            ], fill=accent)
        
        # Center
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 255, 255, 255))
    
    # FOOD HELPERS
    def _draw_chef_hat(self, draw, cx, cy, size, white_color, accent_color):
        """Draw a chef's hat"""
        # Puffy top
        puff_radius = size * 0.8
        draw.ellipse([
            cx - puff_radius, cy - puff_radius,
            cx + puff_radius, cy + puff_radius
        ], fill=white_color)
        
        # Band
        band_height = size * 0.4
        band_width = size * 1.2
        draw.rectangle([
            cx - band_width/2, cy + puff_radius - 20,
            cx + band_width/2, cy + puff_radius + band_height
        ], fill=accent_color)
    
    def _draw_fork(self, draw, cx, cy, length, color, angle_deg):
        """Draw a fork"""
        angle = math.radians(angle_deg)
        handle_length = length * 0.6
        prong_length = length * 0.4
        prong_width = 12
        
        # Rotate points
        def rotate(x, y):
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            return cx + rx, cy + ry
        
        # Handle
        handle_points = [
            rotate(-prong_width, -handle_length/2),
            rotate(prong_width, -handle_length/2),
            rotate(prong_width, handle_length/2),
            rotate(-prong_width, handle_length/2)
        ]
        draw.polygon(handle_points, fill=color)
        
        # Prongs (3)
        for i in range(3):
            offset = (i - 1) * 20
            prong_points = [
                rotate(offset - 5, handle_length/2),
                rotate(offset + 5, handle_length/2),
                rotate(offset + 5, handle_length/2 + prong_length),
                rotate(offset - 5, handle_length/2 + prong_length)
            ]
            draw.polygon(prong_points, fill=color)
    
    def _draw_spoon(self, draw, cx, cy, length, color, angle_deg):
        """Draw a spoon"""
        angle = math.radians(angle_deg)
        handle_length = length * 0.6
        bowl_size = length * 0.4
        
        def rotate(x, y):
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            return cx + rx, cy + ry
        
        # Handle
        handle_points = [
            rotate(-8, -handle_length/2),
            rotate(8, -handle_length/2),
            rotate(8, handle_length/2),
            rotate(-8, handle_length/2)
        ]
        draw.polygon(handle_points, fill=color)
        
        # Bowl (ellipse)
        bowl_center = handle_length/2 + bowl_size/2
        rx, ry = rotate(0, bowl_center)
        draw.ellipse([
            rx - bowl_size/2, ry - bowl_size/2,
            rx + bowl_size/2, ry + bowl_size/2
        ], fill=color)
    
    def _draw_knife(self, draw, cx, cy, length, color, angle_deg):
        """Draw a knife"""
        angle = math.radians(angle_deg)
        handle_length = length * 0.5
        blade_length = length * 0.5
        
        def rotate(x, y):
            rx = x * math.cos(angle) - y * math.sin(angle)
            ry = x * math.sin(angle) + y * math.cos(angle)
            return cx + rx, cy + ry
        
        # Handle
        handle_points = [
            rotate(-12, -handle_length/2),
            rotate(12, -handle_length/2),
            rotate(12, handle_length/2),
            rotate(-12, handle_length/2)
        ]
        draw.polygon(handle_points, fill=color)
        
        # Blade
        blade_points = [
            rotate(-8, handle_length/2),
            rotate(8, handle_length/2),
            rotate(0, handle_length/2 + blade_length)
        ]
        draw.polygon(blade_points, fill=color)
    
    def _draw_serving_dome(self, draw, cx, cy, size, primary, secondary):
        """Draw a serving dome/cloche"""
        # Dome arc
        for layer in range(25):
            progress = layer / 25
            color = self._blend_colors(primary, secondary, progress)
            scale = 1 - (layer * 0.02)
            width = size * scale
            height = size * 0.6 * scale
            draw.arc([
                cx - width/2, cy - height,
                cx + width/2, cy + height
            ], 0, 180, fill=color, width=8)
        
        # Base
        base_width = size * 1.2
        base_height = 30
        draw.rectangle([
            cx - base_width/2, cy - 10,
            cx + base_width/2, cy + base_height
        ], fill=secondary)
        
        # Handle on top
        handle_size = 40
        draw.ellipse([
            cx - handle_size/2, cy - size*0.6 - handle_size,
            cx + handle_size/2, cy - size*0.6
        ], fill=(255, 255, 255, 255))
    
    def _draw_steam(self, draw, cx, cy, color):
        """Draw rising steam curve"""
        points = []
        for i in range(15):
            t = i / 14
            x = cx + math.sin(t * math.pi * 2) * 30
            y = cy - t * 100
            points.append((x, y))
        
        if len(points) > 1:
            for i in range(len(points) - 1):
                draw.line([points[i], points[i+1]], fill=color, width=4)
    
    # BEAUTY/SPA HELPERS
    def _draw_lotus_flower(self, draw, cx, cy, size, primary, secondary):
        """Draw a lotus flower (spa symbol)"""
        # Bottom layer - 8 petals
        for i in range(8):
            angle = math.radians(i * 45)
            petal_x = cx + (size * 0.45) * math.cos(angle)
            petal_y = cy + (size * 0.45) * math.sin(angle)
            petal_size = size * 0.5
            draw.ellipse([
                petal_x - petal_size/2, petal_y - petal_size/2,
                petal_x + petal_size/2, petal_y + petal_size/2
            ], fill=primary)
        
        # Middle layer - 6 petals
        for i in range(6):
            angle = math.radians(i * 60 + 30)
            petal_x = cx + (size * 0.28) * math.cos(angle)
            petal_y = cy + (size * 0.28) * math.sin(angle)
            petal_size = size * 0.38
            draw.ellipse([
                petal_x - petal_size/2, petal_y - petal_size/2,
                petal_x + petal_size/2, petal_y + petal_size/2
            ], fill=secondary)
        
        # Center - small circle
        center_size = size * 0.12
        draw.ellipse([
            cx - center_size, cy - center_size,
            cx + center_size, cy + center_size
        ], fill=(255, 255, 255, 255))
    
    def _draw_butterfly(self, draw, cx, cy, size, primary, accent):
        """Draw a butterfly"""
        wing_size = size * 0.45
        
        # Left upper wing
        draw.ellipse([
            cx - size*0.6, cy - size*0.4,
            cx - size*0.1, cy + size*0.2
        ], fill=primary)
        
        # Right upper wing
        draw.ellipse([
            cx + size*0.1, cy - size*0.4,
            cx + size*0.6, cy + size*0.2
        ], fill=primary)
        
        # Left lower wing
        draw.ellipse([
            cx - size*0.5, cy,
            cx - size*0.05, cy + size*0.5
        ], fill=accent)
        
        # Right lower wing
        draw.ellipse([
            cx + size*0.05, cy,
            cx + size*0.5, cy + size*0.5
        ], fill=accent)
        
        # Body
        body_width = size * 0.08
        body_height = size * 0.6
        draw.ellipse([
            cx - body_width, cy - body_height/2,
            cx + body_width, cy + body_height/2
        ], fill=(50, 50, 50, 255))
        
        # Antennae
        draw.line([cx - 5, cy - body_height/2, cx - 20, cy - body_height/2 - 40], fill=(50, 50, 50, 255), width=3)
        draw.line([cx + 5, cy - body_height/2, cx + 20, cy - body_height/2 - 40], fill=(50, 50, 50, 255), width=3)
    
    def _draw_spa_stone(self, draw, cx, cy, width, height, color):
        """Draw a smooth spa stone"""
        # Smooth ellipse
        for layer in range(15):
            progress = layer / 15
            layer_color = self._darken_color_rgba(color, progress * 0.3)
            scale = 1 - (layer * 0.03)
            w = width * scale
            h = height * scale
            draw.ellipse([
                cx - w/2, cy - h/2,
                cx + w/2, cy + h/2
            ], fill=layer_color)
    
    def _draw_medical_shield(self, draw, cx, cy, size, primary, secondary):
        """Draw a medical-themed shield"""
        points = []
        for i in range(6):
            angle = math.radians(i * 60 - 90)
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.7
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        
        # Gradient layers
        for layer in range(30):
            progress = layer / 30
            color = self._blend_colors(primary, secondary, progress)
            scale = 1 - (layer * 0.02)
            scaled_points = [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in points]
            draw.polygon(scaled_points, fill=color)
    
    def _draw_pulse_line(self, draw, cx, cy, width, color):
        """Draw a heartbeat/pulse line"""
        points = [
            (cx - width, cy),
            (cx - width * 0.6, cy),
            (cx - width * 0.4, cy - 60),
            (cx - width * 0.2, cy + 60),
            (cx, cy),
            (cx + width * 0.2, cy),
            (cx + width * 0.4, cy - 80),
            (cx + width * 0.6, cy + 40),
            (cx + width * 0.8, cy),
            (cx + width, cy)
        ]
        draw.line(points, fill=color, width=8, joint="curve")
    
    def _draw_medical_cross(self, draw, cx, cy, size, color):
        """Draw a medical cross symbol"""
        thickness = size // 3
        # Vertical bar
        draw.rectangle([cx - thickness//2, cy - size, cx + thickness//2, cy + size], fill=color)
        # Horizontal bar
        draw.rectangle([cx - size, cy - thickness//2, cx + size, cy + thickness//2], fill=color)
    
    def _draw_heart_symbol(self, draw, cx, cy, size, color):
        """Draw a heart symbol"""
        points = []
        for i in range(360):
            angle = math.radians(i)
            # Heart curve parametric equation
            x = size * (16 * math.sin(angle) ** 3)
            y = -size * (13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle))
            points.append((cx + x / 16, cy + y / 16))
        draw.polygon(points, fill=color)
    
    def _draw_tech_hexagon(self, draw, cx, cy, size, primary, secondary):
        """Draw a tech-style hexagon with gradient"""
        for layer in range(40):
            progress = layer / 40
            color = self._blend_colors(primary, secondary, progress)
            scale = 1 - (layer * 0.015)
            current_size = size * scale
            
            points = []
            for i in range(6):
                angle = math.radians(i * 60)
                x = cx + current_size * math.cos(angle)
                y = cy + current_size * math.sin(angle)
                points.append((x, y))
            draw.polygon(points, fill=color)
    
    def _draw_digital_health_wave(self, draw, cx, cy, width, color):
        """Draw a digital health wave pattern"""
        points = []
        for i in range(100):
            x = cx - width + (i * width * 2 / 100)
            y = cy + 40 * math.sin(i * 0.3) * math.cos(i * 0.1)
            points.append((x, y))
        
        if len(points) > 1:
            draw.line(points, fill=color, width=12, joint="curve")
    
    def _draw_mini_circuits(self, draw, cx, cy, radius, color, alpha=100):
        """Draw mini circuit patterns"""
        num_circuits = 16
        for i in range(num_circuits):
            angle = math.radians(i * (360 / num_circuits))
            x1 = cx + radius * 0.7 * math.cos(angle)
            y1 = cy + radius * 0.7 * math.sin(angle)
            x2 = cx + radius * math.cos(angle)
            y2 = cy + radius * math.sin(angle)
            
            circuit_color = color[:3] + (alpha,)
            draw.line([(x1, y1), (x2, y2)], fill=circuit_color, width=4)
            draw.ellipse([x2 - 8, y2 - 8, x2 + 8, y2 + 8], fill=circuit_color)
    
    def _draw_medical_chip(self, draw, cx, cy, size, color):
        """Draw a medical chip icon"""
        # Chip outline
        draw.rectangle([cx - size, cy - size, cx + size, cy + size], outline=color, width=8)
        
        # Chip pins
        for i in range(4):
            pin_x = cx - size - 20 + i * 15
            draw.line([(pin_x, cy - size), (pin_x, cy - size - 25)], fill=color, width=6)
            draw.line([(pin_x, cy + size), (pin_x, cy + size + 25)], fill=color, width=6)
        
        # Heart in center
        self._draw_heart_symbol(draw, cx, cy, size // 2, color)
    
    def _draw_neural_network(self, draw, cx, cy, size, primary, secondary):
        """Draw neural network pattern"""
        layers = [4, 6, 4]
        layer_x_positions = [cx - size, cx, cx + size]
        
        for layer_idx, num_nodes in enumerate(layers):
            layer_x = layer_x_positions[layer_idx]
            node_spacing = size * 2 / (num_nodes + 1)
            
            for node_idx in range(num_nodes):
                node_y = cy - size + (node_idx + 1) * node_spacing
                color = self._blend_colors(primary, secondary, node_idx / num_nodes)
                draw.ellipse([layer_x - 15, node_y - 15, layer_x + 15, node_y + 15], fill=color)
                
                # Connect to next layer
                if layer_idx < len(layers) - 1:
                    next_layer_x = layer_x_positions[layer_idx + 1]
                    next_num_nodes = layers[layer_idx + 1]
                    next_node_spacing = size * 2 / (next_num_nodes + 1)
                    
                    for next_node_idx in range(next_num_nodes):
                        next_node_y = cy - size + (next_node_idx + 1) * next_node_spacing
                        line_color = color[:3] + (100,)
                        draw.line([(layer_x, node_y), (next_layer_x, next_node_y)], fill=line_color, width=3)
    
    def _draw_tech_core(self, draw, cx, cy, size, color):
        """Draw a tech core circle"""
        for i in range(20):
            progress = i / 20
            current_size = size * (1 - progress * 0.5)
            alpha = int(255 * (1 - progress))
            core_color = color[:3] + (alpha,)
            draw.ellipse([cx - current_size, cy - current_size, cx + current_size, cy + current_size], fill=core_color)
    
    def _draw_connection_nodes(self, draw, cx, cy, radius, color, num_nodes):
        """Draw connection nodes around a circle"""
        for i in range(num_nodes):
            angle = math.radians(i * (360 / num_nodes))
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            # Node
            draw.ellipse([x - 20, y - 20, x + 20, y + 20], fill=color)
            
            # Connection to center
            line_color = color[:3] + (150,)
            draw.line([(cx, cy), (x, y)], fill=line_color, width=4)
    
    def _draw_vault_shield(self, draw, cx, cy, size, primary, secondary):
        """Draw a vault/diamond shield"""
        # Diamond shape
        points = [
            (cx, cy - size),
            (cx + size * 0.7, cy),
            (cx, cy + size),
            (cx - size * 0.7, cy)
        ]
        
        for layer in range(30):
            progress = layer / 30
            color = self._blend_colors(primary, secondary, progress)
            scale = 1 - (layer * 0.02)
            scaled_points = [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in points]
            draw.polygon(scaled_points, fill=color)
    
    def _draw_growth_chart(self, draw, cx, cy, size, color):
        """Draw an upward growth chart arrow"""
        points = [
            (cx - size, cy + size * 0.5),
            (cx - size * 0.5, cy),
            (cx, cy - size * 0.3),
            (cx + size * 0.5, cy - size * 0.5),
            (cx + size, cy - size)
        ]
        draw.line(points, fill=color, width=12, joint="curve")
        
        # Arrow head
        arrow_points = [
            (cx + size, cy - size),
            (cx + size - 40, cy - size + 30),
            (cx + size - 30, cy - size + 40)
        ]
        draw.polygon(arrow_points, fill=color)
    
    def _draw_secure_lock(self, draw, cx, cy, size, color):
        """Draw a security lock"""
        # Lock body
        body_width = size * 0.7
        body_height = size * 0.6
        draw.rounded_rectangle(
            [cx - body_width, cy, cx + body_width, cy + body_height * 2],
            radius=20,
            fill=color
        )
        
        # Lock shackle
        draw.arc(
            [cx - body_width * 0.6, cy - size, cx + body_width * 0.6, cy + 20],
            start=180,
            end=0,
            fill=color,
            width=15
        )
        
        # Keyhole
        keyhole_color = self._blend_colors((0, 0, 0, 255), color, 0.3)
        draw.ellipse([cx - 15, cy + body_height * 0.8, cx + 15, cy + body_height * 0.8 + 30], fill=keyhole_color)
    
    def _draw_fortress_shield(self, draw, cx, cy, size, primary, secondary):
        """Draw a fortress-style shield"""
        # Pentagon shield
        points = []
        for i in range(5):
            angle = math.radians(i * 72 - 90)
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append((x, y))
        
        for layer in range(35):
            progress = layer / 35
            color = self._blend_colors(primary, secondary, progress)
            scale = 1 - (layer * 0.018)
            scaled_points = [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in points]
            draw.polygon(scaled_points, fill=color)
    
    def _draw_encryption_layers(self, draw, cx, cy, radius, color, alpha=120):
        """Draw encryption layers"""
        num_layers = 6
        for i in range(num_layers):
            current_radius = radius - (i * 40)
            layer_color = color[:3] + (alpha - i * 15,)
            draw.ellipse(
                [cx - current_radius, cy - current_radius, cx + current_radius, cy + current_radius],
                outline=layer_color,
                width=8
            )
    
    def _draw_blockchain_cubes(self, draw, cx, cy, size, primary, secondary):
        """Draw interconnected blockchain cubes"""
        cube_positions = [
            (cx - size * 0.6, cy - size * 0.6),
            (cx + size * 0.6, cy - size * 0.6),
            (cx - size * 0.6, cy + size * 0.6),
            (cx + size * 0.6, cy + size * 0.6),
            (cx, cy)
        ]
        
        for idx, (cube_cx, cube_cy) in enumerate(cube_positions):
            color = self._blend_colors(primary, secondary, idx / len(cube_positions))
            cube_size = 80
            
            # Draw 3D cube
            # Front face
            draw.rectangle(
                [cube_cx - cube_size, cube_cy - cube_size, cube_cx + cube_size, cube_cy + cube_size],
                fill=color
            )
            
            # Top face
            top_points = [
                (cube_cx - cube_size, cube_cy - cube_size),
                (cube_cx, cube_cy - cube_size - 40),
                (cube_cx + cube_size + 40, cube_cy - cube_size - 40),
                (cube_cx + cube_size, cube_cy - cube_size)
            ]
            top_color = self._lighten_color_rgba(color, 0.3)
            draw.polygon(top_points, fill=top_color)
            
            # Right face
            right_points = [
                (cube_cx + cube_size, cube_cy - cube_size),
                (cube_cx + cube_size + 40, cube_cy - cube_size - 40),
                (cube_cx + cube_size + 40, cube_cy + cube_size - 40),
                (cube_cx + cube_size, cube_cy + cube_size)
            ]
            right_color = self._darken_color_rgba(color, 0.2)
            draw.polygon(right_points, fill=right_color)
    
    def _draw_chain_links(self, draw, cx, cy, radius, color):
        """Draw chain link connections"""
        num_links = 8
        for i in range(num_links):
            angle1 = math.radians(i * (360 / num_links))
            angle2 = math.radians((i + 1) * (360 / num_links))
            
            x1 = cx + radius * math.cos(angle1)
            y1 = cy + radius * math.sin(angle1)
            x2 = cx + radius * math.cos(angle2)
            y2 = cy + radius * math.sin(angle2)
            
            # Draw link
            draw.line([(x1, y1), (x2, y2)], fill=color, width=10)
            
            # Link ends
            draw.ellipse([x1 - 15, y1 - 15, x1 + 15, y1 + 15], fill=color)
    
    def _draw_shopping_bag(self, draw, cx, cy, size, primary, secondary):
        """Draw shopping bag shape"""
        # Bag body - trapezoid
        bag_top = size * 0.6
        bag_bottom = size
        bag_height = size * 1.2
        
        points = [
            (cx - bag_top, cy - bag_height * 0.3),
            (cx + bag_top, cy - bag_height * 0.3),
            (cx + bag_bottom, cy + bag_height * 0.7),
            (cx - bag_bottom, cy + bag_height * 0.7)
        ]
        
        for layer in range(30):
            progress = layer / 30
            color = self._blend_colors(primary, secondary, progress)
            scale = 1 - (layer * 0.02)
            scaled_points = [(cx + (x - cx) * scale, cy + (y - cy) * scale) for x, y in points]
            draw.polygon(scaled_points, fill=color)
        
        # Bag handle
        handle_color = (255, 255, 255, 200)
        handle_width = size * 0.4
        handle_y = cy - bag_height * 0.3
        draw.arc(
            [cx - handle_width, handle_y - 80, cx + handle_width, handle_y + 20],
            start=180,
            end=0,
            fill=handle_color,
            width=12
        )
    
    def _draw_price_tag(self, draw, cx, cy, size, color):
        """Draw a price tag"""
        # Tag shape
        points = [
            (cx - size, cy),
            (cx + size * 0.5, cy),
            (cx + size, cy + size * 0.5),
            (cx + size * 0.5, cy + size),
            (cx - size, cy + size)
        ]
        draw.polygon(points, fill=color)
        
        # Tag hole
        draw.ellipse([cx - size * 0.7, cy + size * 0.3, cx - size * 0.3, cy + size * 0.7], fill=(255, 255, 255, 255))
    
    def _draw_cloud_layers(self, draw, cx, cy, size, primary, secondary):
        """Draw cloud layers for SaaS"""
        layer_offsets = [0, 40, 80]
        
        for idx, offset in enumerate(layer_offsets):
            color = self._blend_colors(primary, secondary, idx / len(layer_offsets))
            layer_y = cy + offset
            
            # Cloud shape (multiple circles)
            circles = [
                (cx - size * 0.5, layer_y, size * 0.4),
                (cx, layer_y - 30, size * 0.5),
                (cx + size * 0.5, layer_y, size * 0.4),
                (cx - size * 0.2, layer_y + 20, size * 0.35),
                (cx + size * 0.2, layer_y + 20, size * 0.35)
            ]
            
            for circle_x, circle_y, circle_size in circles:
                draw.ellipse(
                    [circle_x - circle_size, circle_y - circle_size, circle_x + circle_size, circle_y + circle_size],
                    fill=color
                )
    
    def _draw_infinity_symbol(self, draw, cx, cy, size, color):
        """Draw infinity symbol"""
        points = []
        for i in range(360):
            t = math.radians(i * 2)
            # Infinity curve parametric equation
            x = size * math.cos(t) / (1 + math.sin(t) ** 2)
            y = size * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2)
            points.append((cx + x, cy + y))
        
        if len(points) > 1:
            draw.line(points, fill=color, width=25, joint="curve")
    
    # ==================== UTILITY METHODS ====================
    
    def _get_initials(self, name: str) -> str:
        """Get company initials"""
        words = name.split()
        if len(words) >= 2:
            return (words[0][0] + words[1][0]).upper()
        elif len(words) == 1 and len(words[0]) >= 2:
            return words[0][:2].upper()
        return name[:2].upper()
    
    def _draw_centered_text(self, draw, text: str, cx: int, cy: int, font_size: int, color: Tuple):
        """Draw centered text"""
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        draw.text((cx - text_width // 2, cy - text_height // 2), text, font=font, fill=color)
    
    def _parse_color(self, color_val: Any) -> Tuple[int, int, int, int]:
        """Parse hex string or RGB(A) tuple into RGBA tuple."""
        try:
            # If tuple-like
            if isinstance(color_val, (tuple, list)):
                r, g, b = int(color_val[0]), int(color_val[1]), int(color_val[2])
                a = int(color_val[3]) if len(color_val) > 3 else 255
                return (r, g, b, a)

            if not isinstance(color_val, str):
                return (99, 102, 241, 255)

            s = color_val.strip().lstrip('#')
            if len(s) == 3:  # short hex
                r = int(s[0] * 2, 16)
                g = int(s[1] * 2, 16)
                b = int(s[2] * 2, 16)
                return (r, g, b, 255)
            if len(s) == 6:
                r = int(s[0:2], 16)
                g = int(s[2:4], 16)
                b = int(s[4:6], 16)
                return (r, g, b, 255)
        except Exception:
            pass
        # Fallback indigo
        return (99, 102, 241, 255)
    
    def _blend_colors(self, color1: Tuple, color2: Tuple, ratio: float) -> Tuple:
        """Blend two colors"""
        return tuple(int(color1[i] + (color2[i] - color1[i]) * ratio) for i in range(4))
    
    def _lighten_color_rgba(self, color: Tuple, factor: float) -> Tuple:
        """Lighten a color"""
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color[:3]) + (color[3],)
    
    def _darken_color_rgba(self, color: Tuple, factor: float) -> Tuple:
        """Darken a color"""
        return tuple(max(0, int(c * (1 - factor))) for c in color[:3]) + (color[3],)
    
    def _image_to_base64(self, img: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffered = BytesIO()
        img.save(buffered, format="PNG", optimize=True)
        return base64.b64encode(buffered.getvalue()).decode()


# Global instance
industry_logo_generator = IndustryLogoGenerator()

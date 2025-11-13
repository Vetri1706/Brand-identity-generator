"""
Professional Logo Generation System V4 - Journal Publication Quality
Creates genuinely diverse, professional logos using established design principles
Each logo uses different approaches: wordmarks, lettermarks, pictorials, abstracts, combinations
"""
import logging
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import random
import math
import hashlib
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class ProfessionalLogoGenerator:
    """Professional logo generator with genuine design diversity"""

    def __init__(self):
        """Initialize with professional design standards and multiple approaches"""
        self.cache = {}
        self.width = 1000
        self.height = 1000
        
        # Professional logo categories - each fundamentally different
        self.logo_categories = {
            "wordmark": "Typography-focused design emphasizing the company name",
            "lettermark": "Initials/monogram-based design with custom lettering",
            "pictorial": "Icon-based design with symbolic imagery", 
            "abstract": "Abstract geometric design with artistic elements",
            "combination": "Text + icon combination in balanced composition",
            "emblem": "Badge/crest style with enclosed design elements"
        }
        
        # Design principles for professional quality
        self.design_principles = {
            "contrast": "Strong contrast between elements",
            "balance": "Visual weight distribution",
            "hierarchy": "Clear information hierarchy",
            "unity": "Cohesive design elements",
            "simplicity": "Clean, uncluttered approach"
        }
        
        logger.info("🎨 Professional Logo Generator V4 initialized - Journal Quality")

    def generate_diverse_professional_logos(
        self,
        company_name: str,
        industry: str,
        colors: List[str],
        num_variations: int = 3
    ) -> List[str]:
        """
        Generate truly diverse professional logos using different design approaches
        Each variation uses a fundamentally different design category
        """
        logos = []
        
        # Ensure we have different categories for each variation
        categories = list(self.logo_categories.keys())
        random.shuffle(categories)
        
        # Parse colors
        color_palette = self._create_professional_palette(colors, industry)
        
        for i in range(num_variations):
            # Use different category for each logo to ensure diversity
            category = categories[i % len(categories)]
            
            # Generate cache key with category to ensure different designs
            cache_key = hashlib.md5(
                f"{company_name}_{industry}_{category}_v{i}_{colors}".encode()
            ).hexdigest()
            
            if cache_key in self.cache:
                logos.append(self.cache[cache_key])
                continue
            
            try:
                # Generate logo based on specific category
                logo_b64 = self._generate_logo_by_category(
                    company_name, industry, color_palette, category, i
                )
                
                self.cache[cache_key] = logo_b64
                logos.append(logo_b64)
                
                logger.info(f"Generated {category} logo for {company_name}")
                
            except Exception as e:
                logger.error(f"Failed to generate {category} logo: {e}")
                # Generate fallback
                fallback = self._generate_category_fallback(company_name, category, color_palette)
                logos.append(fallback)
        
        return logos

    def _generate_logo_by_category(
        self, company_name: str, industry: str, colors: Dict, category: str, variation: int
    ) -> str:
        """Generate logo based on specific design category"""
        
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        if category == "wordmark":
            return self._create_wordmark_logo(img, draw, company_name, colors, variation)
        elif category == "lettermark":
            return self._create_lettermark_logo(img, draw, company_name, colors, variation)
        elif category == "pictorial":
            return self._create_pictorial_logo(img, draw, company_name, industry, colors, variation)
        elif category == "abstract":
            return self._create_abstract_logo(img, draw, company_name, colors, variation)
        elif category == "combination":
            return self._create_combination_logo(img, draw, company_name, industry, colors, variation)
        elif category == "emblem":
            return self._create_emblem_logo(img, draw, company_name, colors, variation)
        else:
            return self._create_wordmark_logo(img, draw, company_name, colors, variation)

    def _create_wordmark_logo(self, img, draw, company_name, colors, variation):
        """Create typography-focused wordmark logo"""
        
        # Different typography styles for each variation
        font_styles = [
            {"size": 120, "style": "bold", "spacing": 0.1},
            {"size": 100, "style": "light", "spacing": 0.2}, 
            {"size": 140, "style": "condensed", "spacing": -0.05}
        ]
        
        style = font_styles[variation % len(font_styles)]
        
        # Get font
        font = self._get_best_font(style["size"])
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Adjust for letter spacing
        adjusted_width = text_width * (1 + style["spacing"])
        
        x = (self.width - adjusted_width) // 2
        y = (self.height - text_height) // 2
        
        # Apply different styling approaches
        if variation == 0:
            # Bold modern approach
            self._draw_text_with_shadow(draw, company_name, x, y, font, colors["primary"], colors["shadow"])
        elif variation == 1:
            # Elegant light approach with underline
            draw.text((x, y), company_name, fill=colors["primary"], font=font)
            # Add elegant underline
            underline_y = y + text_height + 20
            draw.rectangle([
                x, underline_y,
                x + text_width, underline_y + 4
            ], fill=colors["accent"])
        else:
            # Condensed modern with background element
            # Background rectangle
            bg_padding = 40
            draw.rectangle([
                x - bg_padding, y - 20,
                x + text_width + bg_padding, y + text_height + 20
            ], fill=colors["secondary"])
            # Text on top
            draw.text((x, y), company_name, fill=colors["neutral"], font=font)
        
        return self._encode_image(img)

    def _create_lettermark_logo(self, img, draw, company_name, colors, variation):
        """Create monogram/initials-based logo"""
        
        # Extract initials
        words = company_name.split()
        if len(words) >= 2:
            initials = words[0][0].upper() + words[1][0].upper()
        else:
            initials = company_name[:2].upper()
        
        center_x, center_y = self.width // 2, self.height // 2
        
        if variation == 0:
            # Classic circular monogram
            self._draw_circular_monogram(draw, initials, center_x, center_y, colors)
        elif variation == 1:
            # Modern stacked lettermark
            self._draw_stacked_lettermark(draw, initials, center_x, center_y, colors)
        else:
            # Interlocked letters design
            self._draw_interlocked_letters(draw, initials, center_x, center_y, colors)
        
        return self._encode_image(img)

    def _create_pictorial_logo(self, img, draw, company_name, industry, colors, variation):
        """Create icon-based pictorial logo"""
        
        center_x, center_y = self.width // 2, self.height // 2
        
        # Industry-specific icons with different styles
        if "tech" in industry.lower() or "ai" in industry.lower():
            if variation == 0:
                self._draw_tech_circuit_icon(draw, center_x, center_y, colors)
            elif variation == 1:
                self._draw_digital_cube_icon(draw, center_x, center_y, colors)
            else:
                self._draw_network_nodes_icon(draw, center_x, center_y, colors)
        elif "health" in industry.lower():
            if variation == 0:
                self._draw_medical_cross_icon(draw, center_x, center_y, colors)
            elif variation == 1:
                self._draw_heartbeat_icon(draw, center_x, center_y, colors)
            else:
                self._draw_wellness_leaf_icon(draw, center_x, center_y, colors)
        elif "finance" in industry.lower() or "fin" in industry.lower():
            if variation == 0:
                self._draw_growth_chart_icon(draw, center_x, center_y, colors)
            elif variation == 1:
                self._draw_secure_vault_icon(draw, center_x, center_y, colors)
            else:
                self._draw_currency_flow_icon(draw, center_x, center_y, colors)
        else:
            # Generic professional icons
            if variation == 0:
                self._draw_professional_diamond(draw, center_x, center_y, colors)
            elif variation == 1:
                self._draw_building_icon(draw, center_x, center_y, colors)
            else:
                self._draw_arrow_growth_icon(draw, center_x, center_y, colors)
        
        # Add company name below icon (smaller text)
        font = self._get_best_font(60)
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (self.width - text_width) // 2
        text_y = center_y + 200
        draw.text((text_x, text_y), company_name, fill=colors["primary"], font=font)
        
        return self._encode_image(img)

    def _create_abstract_logo(self, img, draw, company_name, colors, variation):
        """Create abstract artistic logo"""
        
        center_x, center_y = self.width // 2, self.height // 2
        
        if variation == 0:
            # Flowing wave abstract
            self._draw_flowing_waves(draw, center_x, center_y, colors)
        elif variation == 1:
            # Geometric spiral
            self._draw_geometric_spiral(draw, center_x, center_y, colors)
        else:
            # Angular crystalline structure
            self._draw_crystal_structure(draw, center_x, center_y, colors)
        
        # Add minimalist company name
        font = self._get_best_font(50)
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (self.width - text_width) // 2
        text_y = center_y + 250
        draw.text((text_x, text_y), company_name, fill=colors["primary"], font=font)
        
        return self._encode_image(img)

    def _create_combination_logo(self, img, draw, company_name, industry, colors, variation):
        """Create combination of icon + text"""
        
        center_x, center_y = self.width // 2, self.height // 2
        
        if variation == 0:
            # Icon above text layout
            icon_y = center_y - 100
            self._draw_simple_industry_icon(draw, center_x, icon_y, industry, colors)
            
            font = self._get_best_font(80)
            bbox = draw.textbbox((0, 0), company_name, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (self.width - text_width) // 2
            text_y = center_y + 50
            draw.text((text_x, text_y), company_name, fill=colors["primary"], font=font)
            
        elif variation == 1:
            # Icon left, text right layout
            icon_x = center_x - 150
            self._draw_simple_industry_icon(draw, icon_x, center_y, industry, colors)
            
            font = self._get_best_font(90)
            text_x = center_x + 20
            bbox = draw.textbbox((0, 0), company_name, font=font)
            text_height = bbox[3] - bbox[1]
            text_y = center_y - text_height // 2
            draw.text((text_x, text_y), company_name, fill=colors["primary"], font=font)
            
        else:
            # Integrated icon within text
            font = self._get_best_font(100)
            bbox = draw.textbbox((0, 0), company_name, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = (self.width - text_width) // 2
            text_y = (self.height - text_height) // 2
            
            draw.text((text_x, text_y), company_name, fill=colors["primary"], font=font)
            
            # Small icon integrated above first letter
            icon_x = text_x + 20
            icon_y = text_y - 40
            self._draw_mini_icon(draw, icon_x, icon_y, industry, colors)
        
        return self._encode_image(img)

    def _draw_mini_icon(self, draw, x, y, industry, colors):
        """Draw small icon for combination logos"""
        size = 30
        if industry in ['tech', 'fintech', 'technology']:
            # Mini circuit
            draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], outline=colors["accent"], width=2)
            draw.line([x-10, y, x+10, y], fill=colors["secondary"], width=2)
        elif industry in ['health', 'healthcare', 'medical']:
            # Mini cross
            draw.rectangle([x-15, y-5, x+15, y+5], fill=colors["accent"])
            draw.rectangle([x-5, y-15, x+5, y+15], fill=colors["accent"])
        else:
            # Mini star
            points = []
            for i in range(10):
                angle = (i * 36) * math.pi / 180
                radius = size//2 if i % 2 == 0 else size//4
                px = x + radius * math.cos(angle)
                py = y + radius * math.sin(angle)
                points.append((px, py))
            draw.polygon(points, fill=colors["accent"])

    def _create_emblem_logo(self, img, draw, company_name, colors, variation):
        """Create badge/emblem style logo"""
        
        center_x, center_y = self.width // 2, self.height // 2
        
        if variation == 0:
            # Classic shield emblem
            self._draw_shield_emblem(draw, center_x, center_y, company_name, colors)
        elif variation == 1:
            # Circular badge
            self._draw_circular_badge(draw, center_x, center_y, company_name, colors)
        else:
            # Hexagonal modern emblem
            self._draw_hexagonal_emblem(draw, center_x, center_y, company_name, colors)
        
        return self._encode_image(img)

    def _draw_hexagonal_emblem(self, draw, x, y, company_name, colors):
        """Draw hexagonal emblem with company name"""
        # Hexagon points
        radius = 150
        hex_points = []
        for i in range(6):
            angle = math.radians(i * 60)
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            hex_points.append((px, py))
        
        # Draw hexagon with gradient effect
        draw.polygon(hex_points, fill=colors["primary"], outline=colors["secondary"], width=6)
        
        # Inner hexagon
        inner_radius = 120
        inner_hex_points = []
        for i in range(6):
            angle = math.radians(i * 60)
            px = x + inner_radius * math.cos(angle)
            py = y + inner_radius * math.sin(angle)
            inner_hex_points.append((px, py))
        
        draw.polygon(inner_hex_points, outline=colors["accent"], width=3)
        
        # Company name in center
        font = self._get_best_font(60)
        if len(company_name) > 12:
            # Split into lines for long names
            words = company_name.split()
            if len(words) > 1:
                mid = len(words) // 2
                line1 = " ".join(words[:mid])
                line2 = " ".join(words[mid:])
                
                bbox1 = draw.textbbox((0, 0), line1, font=font)
                bbox2 = draw.textbbox((0, 0), line2, font=font)
                
                line1_x = x - (bbox1[2] - bbox1[0]) // 2
                line1_y = y - 20
                line2_x = x - (bbox2[2] - bbox2[0]) // 2
                line2_y = y + 20
                
                draw.text((line1_x, line1_y), line1, fill=colors["neutral"], font=font)
                draw.text((line2_x, line2_y), line2, fill=colors["neutral"], font=font)
            else:
                bbox = draw.textbbox((0, 0), company_name, font=font)
                text_x = x - (bbox[2] - bbox[0]) // 2
                text_y = y - (bbox[3] - bbox[1]) // 2
                draw.text((text_x, text_y), company_name, fill=colors["neutral"], font=font)
        else:
            bbox = draw.textbbox((0, 0), company_name, font=font)
            text_x = x - (bbox[2] - bbox[0]) // 2
            text_y = y - (bbox[3] - bbox[1]) // 2
            draw.text((text_x, text_y), company_name, fill=colors["neutral"], font=font)

    def _draw_shield_emblem(self, draw, x, y, company_name, colors):
        """Draw shield-style emblem"""
        # Shield shape
        shield_points = [
            (x, y - 120),  # Top
            (x - 80, y - 100),  # Upper left
            (x - 90, y - 20),   # Left
            (x - 70, y + 60),   # Lower left
            (x, y + 120),       # Bottom point
            (x + 70, y + 60),   # Lower right
            (x + 90, y - 20),   # Right
            (x + 80, y - 100),  # Upper right
        ]
        
        # Draw shield
        draw.polygon(shield_points, fill=colors["primary"], outline=colors["secondary"], width=4)
        
        # Inner shield decoration
        inner_shield_points = []
        for px, py in shield_points:
            # Shrink towards center
            inner_px = x + (px - x) * 0.8
            inner_py = y + (py - y) * 0.8
            inner_shield_points.append((inner_px, inner_py))
        
        draw.polygon(inner_shield_points, outline=colors["accent"], width=2)
        
        # Company name
        font = self._get_best_font(50)
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_x = x - (bbox[2] - bbox[0]) // 2
        text_y = y - (bbox[3] - bbox[1]) // 2
        draw.text((text_x, text_y), company_name, fill=colors["neutral"], font=font)
        
        # Decorative elements
        # Top banner
        banner_points = [
            (x - 60, y - 80), (x + 60, y - 80),
            (x + 50, y - 60), (x - 50, y - 60)
        ]
        draw.polygon(banner_points, fill=colors["accent"])

    # Professional icon drawing methods
    def _draw_circular_monogram(self, draw, initials, x, y, colors):
        """Draw professional circular monogram"""
        radius = 180
        
        # Outer circle with gradient effect
        for i in range(20):
            r = radius - i * 4
            alpha = int(255 * (1 - i * 0.03))
            color = (*colors["primary"][:3], alpha)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
        
        # Inner circle
        inner_radius = radius - 80
        draw.ellipse([
            x - inner_radius, y - inner_radius,
            x + inner_radius, y + inner_radius
        ], fill=colors["neutral"])
        
        # Initials
        font = self._get_best_font(120)
        bbox = draw.textbbox((0, 0), initials, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x - text_width // 2
        text_y = y - text_height // 2
        draw.text((text_x, text_y), initials, fill=colors["primary"], font=font)

    def _draw_stacked_lettermark(self, draw, initials, x, y, colors):
        """Draw modern stacked lettermark"""
        if len(initials) >= 2:
            font = self._get_best_font(200)
            
            # First letter
            bbox1 = draw.textbbox((0, 0), initials[0], font=font)
            w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
            x1 = x - w1 // 2
            y1 = y - h1 - 20
            
            draw.text((x1, y1), initials[0], fill=colors["primary"], font=font)
            
            # Second letter
            bbox2 = draw.textbbox((0, 0), initials[1], font=font)
            w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
            x2 = x - w2 // 2
            y2 = y + 20
            
            draw.text((x2, y2), initials[1], fill=colors["secondary"], font=font)
            
            # Connecting line
            line_x1 = min(x1, x2)
            line_x2 = max(x1 + w1, x2 + w2)
            line_y = y - 10
            draw.rectangle([line_x1, line_y, line_x2, line_y + 8], fill=colors["accent"])

    def _draw_interlocked_letters(self, draw, initials, x, y, colors):
        """Draw interlocked letters design"""
        if len(initials) >= 2:
            font = self._get_best_font(180)
            
            # First letter - left position
            bbox1 = draw.textbbox((0, 0), initials[0], font=font)
            w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
            x1 = x - w1 // 3  # Overlap position
            y1 = y - h1 // 2
            
            # Second letter - right position  
            bbox2 = draw.textbbox((0, 0), initials[1], font=font)
            w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
            x2 = x - w2 // 3  # Overlap position
            y2 = y - h2 // 2
            
            # Draw with overlap effect
            draw.text((x1, y1), initials[0], fill=colors["primary"], font=font)
            draw.text((x2, y2), initials[1], fill=colors["secondary"], font=font)

    def _draw_tech_circuit_icon(self, draw, x, y, colors):
        """Draw technology circuit icon with enhanced complexity"""
        # Main circuit board with more detail
        board_size = 160
        
        # Background board
        draw.rectangle([
            x - board_size, y - board_size,
            x + board_size, y + board_size
        ], fill=colors["secondary"])
        
        # Circuit traces - horizontal
        for i in range(-3, 4):
            trace_y = y + i * 25
            draw.rectangle([
                x - board_size + 20, trace_y - 2,
                x + board_size - 20, trace_y + 2
            ], fill=colors["accent"])
        
        # Circuit traces - vertical  
        for i in range(-3, 4):
            trace_x = x + i * 25
            draw.rectangle([
                trace_x - 2, y - board_size + 20,
                trace_x + 2, y + board_size - 20
            ], fill=colors["accent"])
        
        # Components - resistors and capacitors
        for i in range(-2, 3):
            for j in range(-2, 3):
                comp_x = x + i * 50
                comp_y = y + j * 50
                
                if (i + j) % 2 == 0:
                    # Resistor
                    draw.rectangle([
                        comp_x - 12, comp_y - 6,
                        comp_x + 12, comp_y + 6
                    ], fill=colors["primary"])
                else:
                    # Capacitor
                    draw.ellipse([
                        comp_x - 8, comp_y - 8,
                        comp_x + 8, comp_y + 8
                    ], fill=colors["primary"])
        
        # Central processor chip
        chip_size = 40
        draw.rectangle([
            x - chip_size, y - chip_size,
            x + chip_size, y + chip_size
        ], fill=colors["primary"])
        
        # Chip pins
        for i in range(-3, 4):
            pin_x = x - chip_size - 8
            pin_y = y + i * 8
            draw.rectangle([pin_x, pin_y - 2, pin_x + 8, pin_y + 2], fill=colors["accent"])
            
            pin_x = x + chip_size
            draw.rectangle([pin_x, pin_y - 2, pin_x + 8, pin_y + 2], fill=colors["accent"])

    def _draw_medical_cross_icon(self, draw, x, y, colors):
        """Draw enhanced medical cross icon"""
        cross_size = 100
        cross_thickness = 30
        
        # Shadow effect
        shadow_offset = 6
        draw.rectangle([
            x - cross_size + shadow_offset, y - cross_thickness//2 + shadow_offset,
            x + cross_size + shadow_offset, y + cross_thickness//2 + shadow_offset
        ], fill=colors["shadow"])
        draw.rectangle([
            x - cross_thickness//2 + shadow_offset, y - cross_size + shadow_offset,
            x + cross_thickness//2 + shadow_offset, y + cross_size + shadow_offset
        ], fill=colors["shadow"])
        
        # Main cross - horizontal
        draw.rectangle([
            x - cross_size, y - cross_thickness//2,
            x + cross_size, y + cross_thickness//2
        ], fill=colors["primary"])
        
        # Main cross - vertical
        draw.rectangle([
            x - cross_thickness//2, y - cross_size,
            x + cross_thickness//2, y + cross_size
        ], fill=colors["primary"])
        
        # Center highlight
        center_size = 20
        draw.ellipse([
            x - center_size, y - center_size,
            x + center_size, y + center_size
        ], fill=colors["neutral"])
        
        # Corner decorative elements
        corner_size = 15
        corners = [
            (x - cross_size + corner_size, y - cross_size + corner_size),
            (x + cross_size - corner_size, y - cross_size + corner_size),
            (x - cross_size + corner_size, y + cross_size - corner_size),
            (x + cross_size - corner_size, y + cross_size - corner_size)
        ]
        
        for corner in corners:
            draw.ellipse([
                corner[0] - 8, corner[1] - 8,
                corner[0] + 8, corner[1] + 8
            ], fill=colors["accent"])

    def _draw_growth_chart_icon(self, draw, x, y, colors):
        """Draw financial growth chart icon"""
        chart_width = 140
        chart_height = 100
        
        # Chart background
        draw.rectangle([
            x - chart_width//2, y - chart_height//2,
            x + chart_width//2, y + chart_height//2
        ], fill=colors["neutral"], outline=colors["primary"], width=3)
        
        # Growth bars
        bar_width = 20
        bars = [40, 60, 80, 120, 100]  # Heights showing growth trend
        
        for i, height in enumerate(bars):
            bar_x = x - chart_width//2 + 20 + i * 25
            bar_y = y + chart_height//2 - height//2
            
            # Gradient effect for bars
            for layer in range(height//2):
                color_intensity = 1 - (layer / (height//2))
                bar_color = tuple(int(c * color_intensity) for c in colors["primary"][:3]) + (255,)
                draw.rectangle([
                    bar_x, bar_y + layer,
                    bar_x + bar_width, bar_y + layer + 1
                ], fill=bar_color)
        
        # Trend line
        trend_points = []
        for i, height in enumerate(bars):
            point_x = x - chart_width//2 + 30 + i * 25
            point_y = y + chart_height//2 - height//2
            trend_points.append((point_x, point_y))
        
        # Draw trend line segments
        for i in range(len(trend_points) - 1):
            draw.line([trend_points[i], trend_points[i+1]], fill=colors["accent"], width=4)
            
        # Data points
        for point in trend_points:
            draw.ellipse([
                point[0] - 6, point[1] - 6,
                point[0] + 6, point[1] + 6
            ], fill=colors["accent"])

    def _draw_heartbeat_icon(self, draw, x, y, colors):
        """Draw heartbeat/pulse icon"""
        # Heartbeat line path
        heartbeat_points = [
            (x - 120, y),
            (x - 80, y),
            (x - 60, y - 40),
            (x - 40, y + 60),
            (x - 20, y - 80),
            (x, y + 20),
            (x + 20, y),
            (x + 40, y),
            (x + 60, y - 30),
            (x + 80, y + 40),
            (x + 100, y),
            (x + 120, y)
        ]
        
        # Draw heartbeat line with thickness
        for i in range(len(heartbeat_points) - 1):
            draw.line([
                heartbeat_points[i], 
                heartbeat_points[i+1]
            ], fill=colors["primary"], width=6)
        
        # Add pulse dots
        pulse_points = [heartbeat_points[2], heartbeat_points[4], heartbeat_points[7], heartbeat_points[9]]
        for point in pulse_points:
            draw.ellipse([
                point[0] - 8, point[1] - 8,
                point[0] + 8, point[1] + 8
            ], fill=colors["accent"])
        
        # Background pulse rings
        for ring_radius in [60, 80, 100]:
            draw.ellipse([
                x - ring_radius, y - ring_radius,
                x + ring_radius, y + ring_radius
            ], outline=(*colors["secondary"][:3], 80), width=2)

    def _draw_circular_badge(self, draw, x, y, company_name, colors):
        """Draw enhanced circular badge"""
        radius = 200
        
        # Multiple ring layers
        ring_widths = [20, 15, 10, 5]
        ring_colors = [colors["primary"], colors["secondary"], colors["accent"], colors["primary"]]
        
        current_radius = radius
        for width, color in zip(ring_widths, ring_colors):
            draw.ellipse([
                x - current_radius, y - current_radius,
                x + current_radius, y + current_radius
            ], outline=color, width=width)
            current_radius -= width + 5
        
        # Inner circle background
        inner_radius = current_radius
        draw.ellipse([
            x - inner_radius, y - inner_radius,
            x + inner_radius, y + inner_radius
        ], fill=colors["neutral"])
        
        # Company name in center
        font = self._get_best_font(50)
        
        # Split long company names
        if len(company_name) > 12:
            words = company_name.split()
            if len(words) >= 2:
                line1 = words[0]
                line2 = ' '.join(words[1:])
                
                bbox1 = draw.textbbox((0, 0), line1, font=font)
                bbox2 = draw.textbbox((0, 0), line2, font=font)
                
                text1_width = bbox1[2] - bbox1[0]
                text2_width = bbox2[2] - bbox2[0]
                text_height = bbox1[3] - bbox1[1]
                
                text1_x = x - text1_width // 2
                text1_y = y - text_height - 10
                text2_x = x - text2_width // 2
                text2_y = y + 10
                
                draw.text((text1_x, text1_y), line1, fill=colors["primary"], font=font)
                draw.text((text2_x, text2_y), line2, fill=colors["primary"], font=font)
            else:
                # Single long word - use smaller font
                small_font = self._get_best_font(35)
                bbox = draw.textbbox((0, 0), company_name, font=small_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = x - text_width // 2
                text_y = y - text_height // 2
                draw.text((text_x, text_y), company_name, fill=colors["primary"], font=small_font)
        else:
            # Regular single line
            bbox = draw.textbbox((0, 0), company_name, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x - text_width // 2
            text_y = y - text_height // 2
            draw.text((text_x, text_y), company_name, fill=colors["primary"], font=font)
        
        # Decorative stars around the badge
        star_positions = []
        for angle in range(0, 360, 45):
            star_radius = radius + 30
            star_x = x + star_radius * math.cos(math.radians(angle))
            star_y = y + star_radius * math.sin(math.radians(angle))
            star_positions.append((star_x, star_y))
        
        for star_pos in star_positions:
            self._draw_decorative_star(draw, star_pos[0], star_pos[1], 12, colors["accent"])

    def _draw_decorative_star(self, draw, x, y, size, color):
        """Draw decorative star"""
        points = []
        for i in range(10):  # 5-pointed star with 10 points total
            angle = (i * 36) * math.pi / 180  # 36 degrees per step
            radius = size if i % 2 == 0 else size * 0.4
            point_x = x + radius * math.cos(angle)
            point_y = y + radius * math.sin(angle)
            points.append((point_x, point_y))
        
        draw.polygon(points, fill=color)

    def _draw_digital_cube_icon(self, draw, x, y, colors):
        """Draw 3D digital cube icon"""
        size = 120
        
        # 3D cube effect
        # Front face
        draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], fill=colors["primary"])
        
        # Top face (parallelogram)
        top_points = [
            (x-size//2, y-size//2),
            (x+size//2, y-size//2),
            (x+size//2+30, y-size//2-30),
            (x-size//2+30, y-size//2-30)
        ]
        draw.polygon(top_points, fill=colors["secondary"])
        
        # Right face (parallelogram)
        right_points = [
            (x+size//2, y-size//2),
            (x+size//2, y+size//2),
            (x+size//2+30, y+size//2-30),
            (x+size//2+30, y-size//2-30)
        ]
        draw.polygon(right_points, fill=colors["accent"])

    def _draw_network_nodes_icon(self, draw, x, y, colors):
        """Draw network nodes icon"""
        # Node positions
        nodes = [
            (x, y-100), (x-80, y-40), (x+80, y-40),
            (x-50, y+60), (x+50, y+60), (x, y+100)
        ]
        
        # Draw connections
        connections = [(0,1), (0,2), (1,3), (2,4), (3,5), (4,5), (1,4), (2,3)]
        for start_idx, end_idx in connections:
            start = nodes[start_idx]
            end = nodes[end_idx]
            draw.line([start[0], start[1], end[0], end[1]], fill=colors["secondary"], width=3)
        
        # Draw nodes
        for node in nodes:
            draw.ellipse([node[0]-12, node[1]-12, node[0]+12, node[1]+12], fill=colors["primary"])

    def _draw_flowing_waves(self, draw, x, y, colors):
        """Draw enhanced flowing wave pattern with more complexity"""
        # Create multiple wave layers with different frequencies
        wave_layers = [
            {"amplitude": 60, "frequency": 0.05, "offset": 0},
            {"amplitude": 40, "frequency": 0.08, "offset": 30},
            {"amplitude": 80, "frequency": 0.03, "offset": -20}
        ]
        
        for layer_idx, wave in enumerate(wave_layers):
            wave_points = []
            for i in range(-180, 181, 5):  # Wider range for more detail
                angle = i * wave["frequency"]
                wave_x = x + i * 1.2
                wave_y = y + math.sin(angle) * wave["amplitude"] + wave["offset"]
                wave_points.append((wave_x, wave_y))
            
            # Draw wave with gradient effect
            color = [colors["primary"], colors["secondary"], colors["accent"]][layer_idx]
            
            # Create filled wave shape
            if len(wave_points) > 2:
                # Add baseline points to create filled shape
                filled_points = wave_points + [(wave_points[-1][0], y + 100), (wave_points[0][0], y + 100)]
                
                # Draw with transparency
                alpha_color = (*color[:3], 150)
                draw.polygon(filled_points, fill=alpha_color)
                
                # Draw wave outline
                for i in range(len(wave_points) - 1):
                    draw.line([wave_points[i], wave_points[i+1]], fill=color, width=4)
        
        # Add decorative flow particles
        for i in range(15):
            particle_x = x + random.randint(-200, 200)
            particle_y = y + random.randint(-100, 100)
            particle_size = random.randint(3, 8)
            draw.ellipse([
                particle_x - particle_size, particle_y - particle_size,
                particle_x + particle_size, particle_y + particle_size
            ], fill=colors["accent"])

    def _draw_geometric_spiral(self, draw, x, y, colors):
        """Draw enhanced geometric spiral with mathematical precision"""
        angle = 0
        radius = 5
        points = []
        
        # Golden ratio spiral
        golden_ratio = 1.618
        
        while radius < 180:
            spiral_x = x + radius * math.cos(math.radians(angle))
            spiral_y = y + radius * math.sin(math.radians(angle))
            points.append((spiral_x, spiral_y))
            
            angle += 12  # Finer steps for smoother curve
            radius *= 1.05  # Growth factor
        
        # Draw spiral segments with varying properties
        for i in range(len(points) - 1):
            # Varying thickness and color intensity
            progress = i / len(points)
            thickness = max(2, int(8 * (1 - progress)))
            
            # Color transition
            if progress < 0.33:
                color = colors["primary"]
            elif progress < 0.66:
                color = colors["secondary"] 
            else:
                color = colors["accent"]
            
            draw.line([points[i], points[i+1]], fill=color, width=thickness)
        
        # Add geometric construction lines
        construction_points = points[::len(points)//6]  # Select key points
        for i, point in enumerate(construction_points):
            # Draw lines to center with decreasing opacity
            alpha = max(50, 200 - i * 30)
            construction_color = (*colors["secondary"][:3], alpha)
            draw.line([point, (x, y)], fill=construction_color, width=1)
            
            # Mark key points
            draw.ellipse([
                point[0] - 4, point[1] - 4,
                point[0] + 4, point[1] + 4
            ], fill=colors["accent"])
        
        # Central focal point
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=colors["primary"])

    def _draw_crystal_structure(self, draw, x, y, colors):
        """Draw enhanced angular crystal structure"""
        # Create multiple crystal layers for depth
        crystal_layers = [
            {"scale": 1.0, "rotation": 0, "color": colors["primary"]},
            {"scale": 0.7, "rotation": 30, "color": colors["secondary"]},
            {"scale": 0.4, "rotation": 60, "color": colors["accent"]}
        ]
        
        base_points = [
            (0, -120), (100, -60), (80, 40), (0, 120), (-80, 40), (-100, -60)
        ]
        
        for layer in crystal_layers:
            # Apply transformations
            layer_points = []
            for px, py in base_points:
                # Scale
                px *= layer["scale"]
                py *= layer["scale"]
                
                # Rotate
                angle = math.radians(layer["rotation"])
                rotated_x = px * math.cos(angle) - py * math.sin(angle)
                rotated_y = px * math.sin(angle) + py * math.cos(angle)
                
                # Translate to position
                layer_points.append((x + rotated_x, y + rotated_y))
            
            # Draw crystal outline with thickness
            for i in range(len(layer_points)):
                next_i = (i + 1) % len(layer_points)
                draw.line([
                    layer_points[i], 
                    layer_points[next_i]
                ], fill=layer["color"], width=6)
            
            # Fill alternate facets
            center = (x, y)
            for i in range(0, len(layer_points), 2):
                if i + 1 < len(layer_points):
                    triangle = [layer_points[i], center, layer_points[i+1]]
                    alpha_color = (*layer["color"][:3], 100)
                    draw.polygon(triangle, fill=alpha_color)
            
            # Add internal structure lines
            for point in layer_points:
                draw.line([point, center], fill=layer["color"], width=2)
        
        # Add crystalline reflections
        reflection_points = [
            (x - 40, y - 60), (x + 30, y - 40), (x - 20, y + 50), (x + 60, y + 20)
        ]
        for point in reflection_points:
            draw.ellipse([
                point[0] - 6, point[1] - 6,
                point[0] + 6, point[1] + 6
            ], fill=colors["neutral"])

    def _draw_simple_industry_icon(self, draw, x, y, industry, colors):
        """Draw simple industry-appropriate icon"""
        size = 60
        
        if "tech" in industry.lower():
            # Simple gear
            self._draw_simple_gear(draw, x, y, size, colors["accent"])
        elif "health" in industry.lower():
            # Simple cross
            draw.rectangle([x-size//4, y-size, x+size//4, y+size], fill=colors["accent"])
            draw.rectangle([x-size, y-size//4, x+size, y+size//4], fill=colors["accent"])
        elif "finance" in industry.lower():
            # Simple arrow up
            arrow_points = [(x, y-size), (x+size//2, y), (x-size//2, y)]
            draw.polygon(arrow_points, fill=colors["accent"])
        else:
            # Generic diamond
            diamond_points = [(x, y-size), (x+size, y), (x, y+size), (x-size, y)]
            draw.polygon(diamond_points, fill=colors["accent"])

    def _draw_simple_gear(self, draw, x, y, size, color):
        """Draw simple gear icon"""
        # Outer gear teeth
        teeth = 8
        outer_radius = size
        inner_radius = size * 0.7
        
        points = []
        for i in range(teeth * 2):
            angle = (i * 180 / teeth) * math.pi / 180
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((px, py))
        
        draw.polygon(points, fill=color)
        
        # Center hole
        center_radius = size * 0.3
        draw.ellipse([
            x - center_radius, y - center_radius,
            x + center_radius, y + center_radius
        ], fill=(255, 255, 255, 0))

    def _draw_shield_emblem(self, draw, x, y, company_name, colors):
        """Draw shield emblem with company name"""
        # Shield shape
        shield_height = 280
        shield_width = 200
        
        shield_points = [
            (x, y - shield_height//2),
            (x + shield_width//2, y - shield_height//3),
            (x + shield_width//2, y + shield_height//4),
            (x, y + shield_height//2),
            (x - shield_width//2, y + shield_height//4),
            (x - shield_width//2, y - shield_height//3)
        ]
        
        draw.polygon(shield_points, fill=colors["primary"])
        
        # Inner shield
        inner_points = [(px + (x-px)*0.15, py + (y-py)*0.15) for px, py in shield_points]
        draw.polygon(inner_points, fill=colors["secondary"])
        
        # Company name in center
        font = self._get_best_font(40)
        bbox = draw.textbbox((0, 0), company_name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x - text_width // 2
        text_y = y - text_height // 2
        draw.text((text_x, text_y), company_name, fill=colors["neutral"], font=font)

    def _create_professional_palette(self, input_colors: List[str], industry: str) -> Dict:
        """Create professional color palette with proper contrast"""
        
        # Parse input colors
        parsed = [self._parse_color(color) for color in input_colors[:3]]
        
        # Ensure we have at least 3 colors
        while len(parsed) < 3:
            default_colors = [
                "#2563EB",  # Professional blue
                "#10B981",  # Success green  
                "#F59E0B"   # Accent orange
            ]
            parsed.append(self._parse_color(default_colors[len(parsed)]))
        
        primary, secondary, accent = parsed[:3]
        
        return {
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
            "neutral": (248, 250, 252, 255),  # Light gray
            "shadow": (15, 23, 42, 180),      # Dark shadow
            "text": (30, 41, 59, 255)         # Dark text
        }

    def _parse_color(self, hex_color: str) -> Tuple[int, int, int, int]:
        """Parse hex color to RGBA"""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b, 255)
        except:
            return (37, 99, 235, 255)  # Default blue

    def _get_best_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get best available font"""
        font_names = ["arial.ttf", "calibri.ttf", "tahoma.ttf"]
        
        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue
        
        return ImageFont.load_default()

    def _draw_text_with_shadow(self, draw, text, x, y, font, text_color, shadow_color):
        """Draw text with professional shadow effect"""
        # Shadow
        for offset in range(6, 0, -1):
            alpha = int(shadow_color[3] * (offset / 6))
            shadow = (*shadow_color[:3], alpha)
            draw.text((x + offset, y + offset), text, fill=shadow, font=font)
        
        # Main text
        draw.text((x, y), text, fill=text_color, font=font)

    def _encode_image(self, img: Image.Image) -> str:
        """Encode image to base64"""
        buffered = BytesIO()
        img.save(buffered, format="PNG", optimize=True)
        return base64.b64encode(buffered.getvalue()).decode()

    def _generate_category_fallback(self, company_name: str, category: str, colors: Dict) -> str:
        """Generate fallback for specific category"""
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Simple fallback based on category
        if category == "wordmark":
            return self._create_wordmark_logo(img, draw, company_name, colors, 0)
        else:
            # Simple text fallback
            font = self._get_best_font(80)
            bbox = draw.textbbox((0, 0), company_name, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (self.width - text_width) // 2
            y = (self.height - text_height) // 2
            draw.text((x, y), company_name, fill=colors["primary"], font=font)
            return self._encode_image(img)


# Global professional generator instance
professional_logo_generator = ProfessionalLogoGenerator()
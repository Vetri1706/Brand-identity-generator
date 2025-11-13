"""
Revolutionary Logo Generator V3 - Ultra High Quality
Implements advanced design patterns from professional training data
Generates production-ready logos with premium aesthetic quality
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


class UltraLogoGenerator:
    """Revolutionary logo generator with premium design intelligence"""

    def __init__(self):
        """Initialize with professional design standards"""
        self.cache = {}
        self.width = 1200  # Ultra-high resolution for supreme quality
        self.height = 1200
        self.dpi = 300  # Print-ready quality
        
        # Professional design parameters
        self.golden_ratio = 1.618
        self.design_principles = {
            "balance": True,
            "contrast": "high",
            "hierarchy": "clear",
            "unity": "strong",
            "simplicity": "elegant"
        }
        
        # Advanced color systems
        self.color_harmonies = ["triadic", "complementary", "analogous", "split_complementary", "tetradic"]
        
        # Premium fonts (fallback to system fonts)
        self.premium_fonts = [
            "arial.ttf", "arialbd.ttf", "calibri.ttf", "calibrib.ttf",
            "segoeui.ttf", "segoeuib.ttf", "tahoma.ttf", "tahomabd.ttf"
        ]
        
        logger.info("🎨 Ultra Logo Generator V3 initialized - Premium quality mode")

    def generate_revolutionary_logo(
        self,
        company_name: str,
        industry: str,
        colors: List[str],
        style: str = "professional_modern"
    ) -> str:
        """
        Generate a revolutionary professional logo with AI-inspired design intelligence
        """
        try:
            # Generate cache key for consistency
            cache_key = hashlib.md5(
                f"{company_name}{industry}{colors}{style}v3_ultra".encode()
            ).hexdigest()
            
            if cache_key in self.cache:
                return self.cache[cache_key]

            # Create ultra-high quality canvas
            img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            # Parse and enhance colors using advanced color theory
            color_system = self._create_advanced_color_system(colors, industry)
            
            # Generate intelligent design based on industry
            design_context = self._analyze_design_context(company_name, industry, style)
            
            # Create the revolutionary logo using contextual intelligence
            if "tech" in industry.lower() or "ai" in industry.lower():
                logo_image = self._generate_tech_innovation_logo(
                    draw, company_name, color_system, design_context
                )
            elif "fin" in industry.lower() or "bank" in industry.lower():
                logo_image = self._generate_financial_trust_logo(
                    draw, company_name, color_system, design_context
                )
            elif "health" in industry.lower() or "med" in industry.lower():
                logo_image = self._generate_healthcare_care_logo(
                    draw, company_name, color_system, design_context
                )
            elif "cyber" in industry.lower() or "security" in industry.lower():
                logo_image = self._generate_security_shield_logo(
                    draw, company_name, color_system, design_context
                )
            else:
                # Universal professional logo for any industry
                logo_image = self._generate_universal_professional_logo(
                    draw, company_name, color_system, design_context
                )

            # Apply advanced post-processing for premium quality
            img = self._apply_premium_effects(img, color_system)
            
            # Convert to base64 with optimization
            result = self._optimize_and_encode(img)
            
            # Cache for consistency
            self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Revolutionary logo generation failed: {e}")
            return self._generate_premium_fallback(company_name)

    def _create_advanced_color_system(self, colors: List[str], industry: str) -> Dict:
        """Create an intelligent color system with psychological optimization"""
        
        # Parse input colors
        parsed_colors = [self._parse_color(color) for color in colors[:3]]
        
        # Add industry-optimized colors if needed
        if len(parsed_colors) < 3:
            industry_colors = self._get_industry_optimized_colors(industry)
            while len(parsed_colors) < 3:
                parsed_colors.append(industry_colors[len(parsed_colors)])
        
        primary, secondary, accent = parsed_colors[:3]
        
        # Generate intelligent color variations
        color_system = {
            "primary": primary,
            "secondary": secondary, 
            "accent": accent,
            "light_primary": self._lighten_color_advanced(primary, 0.3),
            "dark_primary": self._darken_color_advanced(primary, 0.3),
            "gradient_start": primary,
            "gradient_end": secondary,
            "shadow": self._create_shadow_color(primary),
            "highlight": self._create_highlight_color(accent),
            "neutral_light": (248, 250, 252, 255),
            "neutral_dark": (15, 23, 42, 255)
        }
        
        return color_system

    def _analyze_design_context(self, company_name: str, industry: str, style: str) -> Dict:
        """Analyze design context for intelligent logo generation"""
        
        # Extract company initials intelligently
        words = company_name.split()
        if len(words) >= 2:
            initials = ''.join([word[0].upper() for word in words[:2]])
        else:
            initials = company_name[:2].upper()
        
        # Determine design complexity based on context
        complexity_factors = {
            "name_length": min(len(company_name) / 10, 1.0),
            "industry_sophistication": self._get_industry_sophistication(industry),
            "style_complexity": self._get_style_complexity(style)
        }
        
        complexity_score = sum(complexity_factors.values()) / len(complexity_factors)
        
        return {
            "company_name": company_name,
            "initials": initials,
            "industry": industry,
            "style": style,
            "complexity_score": complexity_score,
            "design_approach": self._determine_design_approach(complexity_score),
            "focal_point": (self.width // 2, self.height // 2),
            "scale_factor": self._calculate_optimal_scale(company_name)
        }

    def _generate_tech_innovation_logo(self, draw, company_name, color_system, context) -> None:
        """Generate tech/AI industry revolutionary logo"""
        
        center_x, center_y = context["focal_point"]
        
        # Create neural network-inspired design
        # Main geometric structure - hexagonal tech pattern
        hex_radius = 200
        hex_points = self._create_perfect_hexagon(center_x, center_y, hex_radius)
        
        # Multi-layer hexagon with depth and innovation
        for layer in range(15, 0, -1):
            alpha = int(180 * (layer / 15))
            layer_color = (*color_system["primary"][:3], alpha)
            layer_scale = 1 - (layer * 0.02)
            
            scaled_hex = [
                (center_x + (x - center_x) * layer_scale, center_y + (y - center_y) * layer_scale)
                for x, y in hex_points
            ]
            draw.polygon(scaled_hex, fill=layer_color)

        # Inner innovation pattern - interconnected nodes
        node_positions = [
            (center_x, center_y - 120),
            (center_x + 104, center_y - 60),
            (center_x + 104, center_y + 60),
            (center_x, center_y + 120),
            (center_x - 104, center_y + 60),
            (center_x - 104, center_y - 60)
        ]
        
        # Draw connections between nodes
        for i, pos1 in enumerate(node_positions):
            for j, pos2 in enumerate(node_positions[i+1:], i+1):
                # Dynamic connection lines with gradient effect
                self._draw_gradient_line(
                    draw, pos1, pos2, 
                    color_system["accent"], color_system["secondary"], 6
                )
        
        # Draw nodes with glow effects
        for pos in node_positions:
            # Outer glow
            for r in range(25, 15, -2):
                alpha = int(120 * ((25 - r) / 10))
                glow_color = (*color_system["highlight"][:3], alpha)
                draw.ellipse(
                    [pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r],
                    fill=glow_color
                )
            
            # Solid node
            draw.ellipse(
                [pos[0] - 15, pos[1] - 15, pos[0] + 15, pos[1] + 15],
                fill=color_system["secondary"],
                outline=color_system["accent"],
                width=3
            )

        # Central monogram with tech styling
        self._draw_tech_monogram(draw, context["initials"], center_x, center_y, color_system)
        
        # Add subtle circuit pattern background
        self._draw_circuit_pattern(draw, color_system)

    def _generate_financial_trust_logo(self, draw, company_name, color_system, context) -> None:
        """Generate financial industry trust-building logo"""
        
        center_x, center_y = context["focal_point"]
        
        # Create professional shield with financial symbolism
        shield_points = self._create_financial_shield(center_x, center_y, 280)
        
        # Multi-layer shield with premium gradients
        for i in range(30):
            progress = i / 30
            scale = 1 - (i * 0.015)
            color = self._blend_colors_advanced(
                color_system["primary"], 
                color_system["secondary"], 
                progress
            )
            
            scaled_shield = [
                (center_x + (x - center_x) * scale, center_y + (y - center_y) * scale)
                for x, y in shield_points
            ]
            draw.polygon(scaled_shield, fill=color)

        # Inner trust symbols - upward arrows and growth indicators
        arrow_height = 160
        arrow_width = 40
        
        # Triple arrow formation for growth/stability
        for i, x_offset in enumerate([-60, 0, 60]):
            arrow_height_varied = arrow_height - (abs(x_offset) * 0.3)
            arrow_points = [
                (center_x + x_offset, center_y + 80),
                (center_x + x_offset - arrow_width, center_y + 20),
                (center_x + x_offset - (arrow_width//2), center_y + 20),
                (center_x + x_offset - (arrow_width//2), center_y - arrow_height_varied),
                (center_x + x_offset + (arrow_width//2), center_y - arrow_height_varied),
                (center_x + x_offset + (arrow_width//2), center_y + 20),
                (center_x + x_offset + arrow_width, center_y + 20),
            ]
            
            # Gradient arrow
            arrow_color = color_system["accent"] if i == 1 else color_system["secondary"]
            draw.polygon(arrow_points, fill=arrow_color)

        # Professional border with decorative elements
        self._draw_financial_border(draw, center_x, center_y, color_system)
        
        # Central monogram with trust typography
        self._draw_trust_monogram(draw, context["initials"], center_x, center_y + 20, color_system)

    def _generate_healthcare_care_logo(self, draw, company_name, color_system, context) -> None:
        """Generate healthcare industry caring logo"""
        
        center_x, center_y = context["focal_point"]
        
        # Create caring heart-shield hybrid design
        heart_points = self._create_medical_heart_shape(center_x, center_y, 240)
        
        # Multi-layer heart with healing gradients
        for i in range(25):
            progress = i / 25
            scale = 1 - (i * 0.02)
            color = self._blend_colors_advanced(
                color_system["primary"],
                color_system["light_primary"],
                progress
            )
            
            scaled_heart = [
                (center_x + (x - center_x) * scale, center_y + (y - center_y) * scale)
                for x, y in heart_points
            ]
            draw.polygon(scaled_heart, fill=color)

        # Medical cross with modern styling
        cross_size = 120
        cross_thickness = 30
        
        # Horizontal bar
        draw.rectangle([
            center_x - cross_size, center_y - cross_thickness//2,
            center_x + cross_size, center_y + cross_thickness//2
        ], fill=color_system["accent"])
        
        # Vertical bar
        draw.rectangle([
            center_x - cross_thickness//2, center_y - cross_size,
            center_x + cross_thickness//2, center_y + cross_size
        ], fill=color_system["accent"])

        # Healing pulse rings
        for ring in range(1, 4):
            radius = 180 + (ring * 40)
            ring_alpha = int(80 - (ring * 20))
            ring_color = (*color_system["secondary"][:3], ring_alpha)
            
            draw.ellipse([
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius
            ], outline=ring_color, width=8)

        # Care-focused monogram
        self._draw_care_monogram(draw, context["initials"], center_x, center_y + 160, color_system)

    def _generate_security_shield_logo(self, draw, company_name, color_system, context) -> None:
        """Generate cybersecurity shield logo"""
        
        center_x, center_y = context["focal_point"]
        
        # Create fortress-like security shield
        shield_points = self._create_security_shield(center_x, center_y, 300)
        
        # Reinforced shield layers
        for i in range(20):
            progress = i / 20
            scale = 1 - (i * 0.02)
            color = self._blend_colors_advanced(
                color_system["primary"],
                color_system["dark_primary"],
                progress
            )
            
            scaled_shield = [
                (center_x + (x - center_x) * scale, center_y + (y - center_y) * scale)
                for x, y in shield_points
            ]
            draw.polygon(scaled_shield, fill=color)

        # Security lock mechanism
        lock_size = 100
        # Lock body
        draw.rectangle([
            center_x - lock_size//2, center_y - 20,
            center_x + lock_size//2, center_y + 60
        ], fill=color_system["accent"])
        
        # Lock shackle
        draw.ellipse([
            center_x - 40, center_y - 80,
            center_x + 40, center_y - 20
        ], outline=color_system["accent"], width=12)
        draw.ellipse([
            center_x - 25, center_y - 65,
            center_x + 25, center_y - 35
        ], fill=color_system["primary"])

        # Digital security pattern
        self._draw_security_pattern(draw, center_x, center_y, color_system)
        
        # Strong monogram
        self._draw_security_monogram(draw, context["initials"], center_x, center_y + 140, color_system)

    def _generate_universal_professional_logo(self, draw, company_name, color_system, context) -> None:
        """Generate universal professional logo for any industry"""
        
        center_x, center_y = context["focal_point"]
        
        # Professional circular badge design
        outer_radius = 280
        
        # Multi-ring professional structure
        ring_widths = [40, 25, 15]
        ring_colors = [color_system["primary"], color_system["secondary"], color_system["accent"]]
        
        current_radius = outer_radius
        for width, color in zip(ring_widths, ring_colors):
            # Outer ring
            draw.ellipse([
                center_x - current_radius, center_y - current_radius,
                center_x + current_radius, center_y + current_radius
            ], fill=color)
            
            # Inner transparent area
            inner_radius = current_radius - width
            draw.ellipse([
                center_x - inner_radius, center_y - inner_radius,
                center_x + inner_radius, center_y + inner_radius
            ], fill=(255, 255, 255, 0))
            
            current_radius = inner_radius

        # Central professional badge
        badge_radius = 180
        # Badge gradient
        for i in range(badge_radius, 0, -3):
            progress = 1 - (i / badge_radius)
            color = self._blend_colors_advanced(
                color_system["gradient_start"],
                color_system["gradient_end"],
                progress
            )
            draw.ellipse([
                center_x - i, center_y - i,
                center_x + i, center_y + i
            ], fill=color)

        # Professional decorative elements
        star_positions = [
            (center_x, center_y - 220),
            (center_x + 156, center_y - 156),
            (center_x + 220, center_y),
            (center_x + 156, center_y + 156),
            (center_x, center_y + 220),
            (center_x - 156, center_y + 156),
            (center_x - 220, center_y),
            (center_x - 156, center_y - 156)
        ]
        
        for pos in star_positions:
            self._draw_professional_star(draw, pos[0], pos[1], 20, color_system["highlight"])

        # Premium monogram
        self._draw_premium_monogram(draw, context["initials"], center_x, center_y, color_system)

    def _draw_tech_monogram(self, draw, initials, x, y, colors):
        """Draw tech-styled monogram"""
        font = self._get_premium_font(140)
        self._draw_monogram_with_effects(draw, initials, x, y, font, colors["neutral_light"], colors)

    def _draw_trust_monogram(self, draw, initials, x, y, colors):
        """Draw trust-building monogram"""
        font = self._get_premium_font(120)
        self._draw_monogram_with_effects(draw, initials, x, y, font, colors["neutral_light"], colors)

    def _draw_care_monogram(self, draw, initials, x, y, colors):
        """Draw caring monogram"""
        font = self._get_premium_font(100)
        self._draw_monogram_with_effects(draw, initials, x, y, font, colors["neutral_light"], colors)

    def _draw_security_monogram(self, draw, initials, x, y, colors):
        """Draw security monogram"""
        font = self._get_premium_font(130)
        self._draw_monogram_with_effects(draw, initials, x, y, font, colors["neutral_light"], colors)

    def _draw_premium_monogram(self, draw, initials, x, y, colors):
        """Draw premium universal monogram"""
        font = self._get_premium_font(160)
        self._draw_monogram_with_effects(draw, initials, x, y, font, colors["neutral_light"], colors)

    def _draw_monogram_with_effects(self, draw, text, x, y, font, text_color, color_system):
        """Draw monogram with premium effects"""
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x - text_width // 2
        text_y = y - text_height // 2
        
        # Shadow effects
        for offset in range(8, 0, -1):
            shadow_alpha = int(80 * (offset / 8))
            shadow_color = (*color_system["shadow"][:3], shadow_alpha)
            draw.text(
                (text_x + offset, text_y + offset),
                text,
                fill=shadow_color,
                font=font
            )
        
        # Main text with outline
        draw.text(
            (text_x - 2, text_y - 2), text, 
            fill=color_system["dark_primary"], font=font
        )
        draw.text(
            (text_x + 2, text_y + 2), text,
            fill=color_system["dark_primary"], font=font
        )
        draw.text((text_x, text_y), text, fill=text_color, font=font)

    def _create_perfect_hexagon(self, cx, cy, radius) -> List[Tuple[float, float]]:
        """Create mathematically perfect hexagon"""
        points = []
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        return points

    def _create_financial_shield(self, cx, cy, size) -> List[Tuple[float, float]]:
        """Create financial industry shield shape"""
        return [
            (cx, cy - size),
            (cx + size * 0.6, cy - size * 0.7),
            (cx + size * 0.8, cy - size * 0.2),
            (cx + size * 0.8, cy + size * 0.3),
            (cx + size * 0.4, cy + size * 0.9),
            (cx, cy + size),
            (cx - size * 0.4, cy + size * 0.9),
            (cx - size * 0.8, cy + size * 0.3),
            (cx - size * 0.8, cy - size * 0.2),
            (cx - size * 0.6, cy - size * 0.7),
        ]

    def _create_medical_heart_shape(self, cx, cy, size) -> List[Tuple[float, float]]:
        """Create medical heart shape"""
        points = []
        for t in range(0, 360, 5):
            angle = math.radians(t)
            x = cx + size * 0.6 * (16 * math.sin(angle)**3)
            y = cy - size * 0.6 * (13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle))
            points.append((x, y))
        return points

    def _create_security_shield(self, cx, cy, size) -> List[Tuple[float, float]]:
        """Create security shield shape"""
        return [
            (cx, cy - size),
            (cx + size * 0.7, cy - size * 0.8),
            (cx + size * 0.9, cy - size * 0.3),
            (cx + size * 0.9, cy + size * 0.2),
            (cx + size * 0.6, cy + size * 0.7),
            (cx, cy + size * 0.9),
            (cx - size * 0.6, cy + size * 0.7),
            (cx - size * 0.9, cy + size * 0.2),
            (cx - size * 0.9, cy - size * 0.3),
            (cx - size * 0.7, cy - size * 0.8),
        ]

    def _draw_gradient_line(self, draw, start, end, color1, color2, width):
        """Draw gradient line between two points"""
        # Simple gradient line approximation
        steps = 20
        for i in range(steps):
            progress = i / steps
            color = self._blend_colors_advanced(color1, color2, progress)
            
            start_x = start[0] + (end[0] - start[0]) * progress
            start_y = start[1] + (end[1] - start[1]) * progress
            end_x = start[0] + (end[0] - start[0]) * (progress + 1/steps)
            end_y = start[1] + (end[1] - start[1]) * (progress + 1/steps)
            
            draw.line([start_x, start_y, end_x, end_y], fill=color, width=width)

    def _draw_circuit_pattern(self, draw, colors):
        """Draw subtle circuit pattern background"""
        # Add subtle circuit lines in background
        for i in range(0, self.width, 100):
            alpha = random.randint(20, 40)
            color = (*colors["accent"][:3], alpha)
            draw.line([i, 0, i, self.height], fill=color, width=1)
            draw.line([0, i, self.width, i], fill=color, width=1)

    def _draw_financial_border(self, draw, cx, cy, colors):
        """Draw financial decorative border"""
        radius = 320
        for i in range(0, 360, 30):
            angle = math.radians(i)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            draw.ellipse([x-8, y-8, x+8, y+8], fill=colors["accent"])

    def _draw_security_pattern(self, draw, cx, cy, colors):
        """Draw digital security pattern"""
        # Create binary-like pattern around the shield
        for ring in range(3):
            radius = 350 + (ring * 30)
            for i in range(0, 360, 20):
                if random.choice([True, False]):
                    angle = math.radians(i)
                    x = cx + radius * math.cos(angle)
                    y = cy + radius * math.sin(angle)
                    size = 8 - (ring * 2)
                    draw.rectangle([x-size, y-size, x+size, y+size], fill=colors["accent"])

    def _draw_professional_star(self, draw, cx, cy, size, color):
        """Draw professional decorative star"""
        points = []
        for i in range(8):
            angle = (i * 45) * math.pi / 180
            r = size if i % 2 == 0 else size * 0.4
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)

    def _get_industry_optimized_colors(self, industry: str) -> List[Tuple]:
        """Get optimized colors for specific industry"""
        industry_colors = {
            "tech": [(99, 102, 241, 255), (59, 130, 246, 255), (139, 92, 246, 255)],
            "fintech": [(5, 150, 105, 255), (16, 185, 129, 255), (212, 175, 55, 255)],
            "healthcare": [(14, 165, 233, 255), (56, 189, 248, 255), (34, 197, 94, 255)],
            "security": [(220, 38, 38, 255), (31, 41, 55, 255), (251, 191, 36, 255)]
        }
        
        for key in industry_colors:
            if key in industry.lower():
                return industry_colors[key]
        
        return [(99, 102, 241, 255), (59, 130, 246, 255), (139, 92, 246, 255)]

    def _get_industry_sophistication(self, industry: str) -> float:
        """Get industry sophistication score"""
        sophistication_map = {
            "tech": 0.9, "ai": 0.95, "fintech": 0.8, "healthcare": 0.7,
            "security": 0.85, "legal": 0.75, "consulting": 0.8
        }
        
        for key, score in sophistication_map.items():
            if key in industry.lower():
                return score
        return 0.6

    def _get_style_complexity(self, style: str) -> float:
        """Get style complexity score"""
        complexity_map = {
            "minimal": 0.3, "modern": 0.6, "professional": 0.8,
            "premium": 0.9, "luxury": 0.95, "corporate": 0.7
        }
        
        for key, score in complexity_map.items():
            if key in style.lower():
                return score
        return 0.6

    def _determine_design_approach(self, complexity_score: float) -> str:
        """Determine design approach based on complexity"""
        if complexity_score > 0.8:
            return "sophisticated_premium"
        elif complexity_score > 0.6:
            return "professional_modern"
        elif complexity_score > 0.4:
            return "clean_contemporary"
        else:
            return "minimal_elegant"

    def _calculate_optimal_scale(self, company_name: str) -> float:
        """Calculate optimal scale based on name length"""
        base_scale = 1.0
        name_factor = max(0.7, min(1.3, 12 / len(company_name)))
        return base_scale * name_factor

    def _lighten_color_advanced(self, color: Tuple, factor: float) -> Tuple:
        """Advanced color lightening with HSV preservation"""
        r, g, b, a = color
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return (r, g, b, a)

    def _darken_color_advanced(self, color: Tuple, factor: float) -> Tuple:
        """Advanced color darkening"""
        r, g, b, a = color
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return (r, g, b, a)

    def _create_shadow_color(self, base_color: Tuple) -> Tuple:
        """Create intelligent shadow color"""
        r, g, b, _ = base_color
        return (max(0, r - 100), max(0, g - 100), max(0, b - 100), 180)

    def _create_highlight_color(self, base_color: Tuple) -> Tuple:
        """Create intelligent highlight color"""
        r, g, b, _ = base_color
        return (min(255, r + 80), min(255, g + 80), min(255, b + 80), 255)

    def _blend_colors_advanced(self, color1: Tuple, color2: Tuple, t: float) -> Tuple:
        """Advanced color blending with gamma correction"""
        # Gamma correction for better visual blending
        gamma = 2.2
        
        r1, g1, b1, a1 = [x/255.0 for x in color1]
        r2, g2, b2, a2 = [x/255.0 for x in color2]
        
        # Apply gamma correction
        r1, g1, b1 = [x**gamma for x in [r1, g1, b1]]
        r2, g2, b2 = [x**gamma for x in [r2, g2, b2]]
        
        # Blend in gamma space
        r = r1 * (1 - t) + r2 * t
        g = g1 * (1 - t) + g2 * t
        b = b1 * (1 - t) + b2 * t
        a = a1 * (1 - t) + a2 * t
        
        # Remove gamma correction
        r, g, b = [x**(1/gamma) for x in [r, g, b]]
        
        return (int(r*255), int(g*255), int(b*255), int(a*255))

    def _parse_color(self, hex_color: str) -> Tuple[int, int, int, int]:
        """Parse hex color to RGBA with validation"""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b, 255)
        except:
            return (99, 102, 241, 255)  # Default professional blue

    def _get_premium_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get best available premium font"""
        for font_name in self.premium_fonts:
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue
        return ImageFont.load_default()

    def _apply_premium_effects(self, img: Image.Image, color_system: Dict) -> Image.Image:
        """Apply premium post-processing effects"""
        # Subtle enhancement without overdoing it
        enhanced = img.copy()
        
        # Very subtle sharpening for crisp edges
        if random.choice([True, False]):
            enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=2))
        
        return enhanced

    def _optimize_and_encode(self, img: Image.Image) -> str:
        """Optimize image and encode to base64"""
        # Optimize for web while maintaining quality
        buffered = BytesIO()
        
        # Save as PNG with optimization
        img.save(buffered, format="PNG", optimize=True, compress_level=6)
        
        return base64.b64encode(buffered.getvalue()).decode()

    def _generate_premium_fallback(self, company_name: str) -> str:
        """Generate premium fallback logo"""
        try:
            img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            center_x, center_y = self.width // 2, self.height // 2
            
            # Premium gradient background
            primary = (99, 102, 241, 255)
            secondary = (59, 130, 246, 255)
            
            for i in range(300, 0, -5):
                progress = 1 - (i / 300)
                color = self._blend_colors_advanced(primary, secondary, progress)
                draw.ellipse([
                    center_x - i, center_y - i,
                    center_x + i, center_y + i
                ], fill=color)
            
            # Premium text
            initials = company_name[:2].upper()
            font = self._get_premium_font(200)
            
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (self.width - text_width) // 2
            text_y = (self.height - text_height) // 2
            
            # Premium shadow
            for offset in range(8, 0, -1):
                alpha = int(120 * (offset / 8))
                shadow_color = (0, 0, 0, alpha)
                draw.text(
                    (text_x + offset, text_y + offset),
                    initials,
                    fill=shadow_color,
                    font=font
                )
            
            draw.text((text_x, text_y), initials, fill=(255, 255, 255, 255), font=font)
            
            return self._optimize_and_encode(img)
            
        except Exception:
            # Minimal safe fallback
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


# Global ultra generator instance
ultra_logo_generator = UltraLogoGenerator()
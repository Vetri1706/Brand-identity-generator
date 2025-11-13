"""
Logo Image Generation Service
Generates professional logo images with advanced design techniques
"""
import logging
import requests
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
from typing import Dict, List, Tuple
import hashlib
import math

logger = logging.getLogger(__name__)


class LogoImageGenerator:
    """Service for generating professional logo images"""

    def __init__(self):
        """Initialize logo generator with professional design settings"""
        self.cache = {}
        self.width = 800  # Higher resolution for professional quality
        self.height = 800
        self.premium_fonts = ["arial.ttf", "arialbd.ttf", "calibri.ttf", "calibrib.ttf"]
        logger.info("✅ Professional Logo Generator initialized")

    def generate_simple_logo(
        self, 
        company_name: str, 
        colors: List[str], 
        style: str = "modern"
    ) -> str:
        """
        Generate a professional emblem/badge logo with iconic elements
        Returns base64 encoded PNG image string
        """
        try:
            cache_key = hashlib.md5(f"{company_name}{colors}{style}v3".encode()).hexdigest()
            if cache_key in self.cache:
                return self.cache[cache_key]

            img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            initials = ''.join([word[0].upper() for word in company_name.split()[:2]])
            if not initials:
                initials = company_name[:2].upper()

            primary = self._parse_color(colors[0] if colors else '#6366F1')
            secondary = self._parse_color(colors[1] if len(colors) > 1 else self._lighten_color(colors[0]))
            accent = self._parse_color(colors[2] if len(colors) > 2 else self._complement_color(colors[0]))

            center_x, center_y = self.width // 2, self.height // 2

            # Create professional shield/badge emblem
            # Outer shield shape with gradient
            shield_points = [
                (center_x, center_y - 280),
                (center_x + 200, center_y - 240),
                (center_x + 240, center_y - 80),
                (center_x + 240, center_y + 120),
                (center_x + 100, center_y + 280),
                (center_x, center_y + 320),
                (center_x - 100, center_y + 280),
                (center_x - 240, center_y + 120),
                (center_x - 240, center_y - 80),
                (center_x - 200, center_y - 240),
            ]

            # Multi-layer shield with depth
            for layer in range(20, 0, -1):
                alpha = int(255 * (layer / 20))
                shadow_offset = 20 - layer
                shadow_points = [(x, y + shadow_offset * 2) for x, y in shield_points]
                shadow_color = (0, 0, 0, int(alpha * 0.3))
                draw.polygon(shadow_points, fill=shadow_color)

            # Main shield gradient layers
            for i in range(40):
                progress = i / 40
                scale = 1 - (i * 0.008)
                color = self._blend_colors(primary, secondary, progress)
                scaled_points = [
                    (center_x + (x - center_x) * scale, center_y + (y - center_y) * scale)
                    for x, y in shield_points
                ]
                draw.polygon(scaled_points, fill=color)

            # Inner decorative elements - geometric pattern
            # Central diamond/rhombus
            diamond_size = 160
            diamond_points = [
                (center_x, center_y - diamond_size),
                (center_x + diamond_size, center_y),
                (center_x, center_y + diamond_size),
                (center_x - diamond_size, center_y),
            ]
            
            # Diamond with gradient
            for i in range(30):
                progress = i / 30
                scale = 1 - (i * 0.025)
                color = self._blend_colors(accent, secondary, progress)
                scaled_diamond = [
                    (center_x + (x - center_x) * scale, center_y + (y - center_y) * scale)
                    for x, y in diamond_points
                ]
                draw.polygon(scaled_diamond, fill=color)

            # Decorative circles at corners
            circle_positions = [
                (center_x, center_y - 220),
                (center_x + 180, center_y + 80),
                (center_x - 180, center_y + 80),
            ]
            
            for pos in circle_positions:
                # Outer glow
                for r in range(35, 20, -1):
                    alpha = int(150 * ((35 - r) / 15))
                    glow_color = (*accent[:3], alpha)
                    draw.ellipse(
                        [pos[0] - r, pos[1] - r, pos[0] + r, pos[1] + r],
                        fill=glow_color
                    )
                # Solid circle
                draw.ellipse(
                    [pos[0] - 20, pos[1] - 20, pos[0] + 20, pos[1] + 20],
                    fill=(*secondary[:3], 255),
                    outline=(*primary[:3], 255),
                    width=4
                )

            # Central circular badge for initials
            badge_radius = 90
            # Badge shadow
            for i in range(15, 0, -1):
                shadow_alpha = int(120 * (i / 15))
                shadow_color = (0, 0, 0, shadow_alpha)
                draw.ellipse(
                    [center_x - badge_radius - i, center_y - badge_radius + i,
                     center_x + badge_radius - i, center_y + badge_radius + i],
                    fill=shadow_color
                )
            
            # Badge gradient
            for i in range(badge_radius, 0, -3):
                progress = 1 - (i / badge_radius)
                color = self._blend_colors(primary, accent, progress)
                draw.ellipse(
                    [center_x - i, center_y - i, center_x + i, center_y + i],
                    fill=color
                )

            # Decorative ring around badge
            ring_width = 8
            draw.ellipse(
                [center_x - badge_radius - ring_width, center_y - badge_radius - ring_width,
                 center_x + badge_radius + ring_width, center_y + badge_radius + ring_width],
                outline=(*accent[:3], 255),
                width=ring_width
            )

            # Professional typography for initials
            font = self._get_best_font(140)
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (self.width - text_width) // 2
            text_y = (self.height - text_height) // 2 - 10

            # Multi-layer text shadow for depth
            for offset in range(10, 0, -2):
                shadow_alpha = int(180 * (offset / 10))
                draw.text(
                    (text_x + offset, text_y + offset),
                    initials,
                    fill=(0, 0, 0, shadow_alpha),
                    font=font
                )

            # Main text with outline effect
            text_color = (255, 255, 255, 255)
            draw.text((text_x, text_y), initials, fill=text_color, font=font)

            # Decorative stars/sparkles
            star_positions = [
                (center_x - 220, center_y - 180),
                (center_x + 220, center_y - 180),
                (center_x - 200, center_y + 200),
                (center_x + 200, center_y + 200),
            ]
            
            for sx, sy in star_positions:
                self._draw_star(draw, sx, sy, 15, (*accent[:3], 200))

            img = img.filter(ImageFilter.SMOOTH)

            buffered = BytesIO()
            img.save(buffered, format="PNG", optimize=True)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            self.cache[cache_key] = img_str
            return img_str

        except Exception as e:
            logger.error(f"Error generating emblem logo: {e}")
            return self._generate_fallback_logo(company_name)

    def generate_geometric_logo(
        self,
        company_name: str,
        colors: List[str],
        shape: str = "hexagon"
    ) -> str:
        """Generate a professional tech/modern logo with complex geometry"""
        try:
            img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            center_x, center_y = self.width // 2, self.height // 2
            primary = self._parse_color(colors[0] if colors else '#6366F1')
            secondary = self._parse_color(colors[1] if len(colors) > 1 else self._lighten_color(colors[0]))
            accent = self._parse_color(colors[2] if len(colors) > 2 else self._complement_color(colors[0]))

            # Create complex interlocking shapes design
            if shape == "hexagon":
                # Multiple layered hexagons creating a 3D effect
                sizes = [280, 240, 200, 160, 120]
                offsets = [0, 15, 30, 45, 60]
                
                for i, (size, offset) in enumerate(zip(sizes, offsets)):
                    progress = i / len(sizes)
                    color = self._blend_colors(primary, secondary, progress)
                    
                    # Shadow layer
                    shadow_points = self._hexagon_points(center_x + offset//2, center_y + offset, size)
                    shadow_color = (0, 0, 0, int(100 * (1 - progress)))
                    draw.polygon(shadow_points, fill=shadow_color)
                    
                    # Main hexagon
                    points = self._hexagon_points(center_x, center_y, size)
                    draw.polygon(points, fill=color, outline=(*accent[:3], 255), width=6)
                    
                    # Inner geometric pattern
                    if i < len(sizes) - 1:
                        inner_size = size - 30
                        inner_points = self._hexagon_points(center_x, center_y, inner_size)
                        for j in range(6):
                            p1 = inner_points[j]
                            p2 = (center_x, center_y)
                            draw.line([p1, p2], fill=(*accent[:3], 150), width=3)

                # Central star burst pattern
                for angle in range(0, 360, 30):
                    rad = math.radians(angle)
                    x1 = center_x + 60 * math.cos(rad)
                    y1 = center_y + 60 * math.sin(rad)
                    x2 = center_x + 100 * math.cos(rad)
                    y2 = center_y + 100 * math.sin(rad)
                    draw.line([(x1, y1), (x2, y2)], fill=(*accent[:3], 200), width=4)

            elif shape == "triangle":
                # Modern triangular tech logo with interconnected elements
                main_size = 280
                
                # Create three interlocking triangles
                angles = [0, 120, 240]
                for i, base_angle in enumerate(angles):
                    progress = i / 3
                    color = self._blend_colors(primary if i % 2 == 0 else secondary, accent, 0.5)
                    
                    for offset in range(4):
                        rad = math.radians(base_angle + offset * 10)
                        tri_center_x = center_x + (offset * 30) * math.cos(rad)
                        tri_center_y = center_y + (offset * 30) * math.sin(rad)
                        size = main_size - (offset * 40)
                        
                        alpha = 255 - (offset * 50)
                        tri_color = (*color[:3], alpha)
                        
                        points = [
                            (tri_center_x, tri_center_y - size),
                            (tri_center_x - size * 0.866, tri_center_y + size * 0.5),
                            (tri_center_x + size * 0.866, tri_center_y + size * 0.5)
                        ]
                        draw.polygon(points, fill=tri_color)

                # Central connecting nodes
                node_size = 25
                for angle in [0, 120, 240]:
                    rad = math.radians(angle)
                    nx = center_x + 100 * math.cos(rad)
                    ny = center_y + 100 * math.sin(rad)
                    draw.ellipse(
                        [nx - node_size, ny - node_size, nx + node_size, ny + node_size],
                        fill=accent,
                        outline=(*primary[:3], 255),
                        width=5
                    )

            else:  # Modern overlapping squares - cube/box effect
                # Create 3D cube illusion
                cube_size = 200
                
                # Back face
                back_offset = 80
                back_points = [
                    (center_x - cube_size + back_offset, center_y - cube_size - back_offset),
                    (center_x + cube_size + back_offset, center_y - cube_size - back_offset),
                    (center_x + cube_size + back_offset, center_y + cube_size - back_offset),
                    (center_x - cube_size + back_offset, center_y + cube_size - back_offset),
                ]
                draw.polygon(back_points, fill=(*secondary[:3], 180), outline=(*accent[:3], 255), width=6)
                
                # Front face
                front_points = [
                    (center_x - cube_size, center_y - cube_size),
                    (center_x + cube_size, center_y - cube_size),
                    (center_x + cube_size, center_y + cube_size),
                    (center_x - cube_size, center_y + cube_size),
                ]
                draw.polygon(front_points, fill=primary, outline=(*accent[:3], 255), width=6)
                
                # Connecting edges for 3D effect
                for i in range(4):
                    draw.line([front_points[i], back_points[i]], fill=(*accent[:3], 200), width=4)
                
                # Central accent square
                accent_size = 80
                accent_points = [
                    (center_x - accent_size, center_y - accent_size),
                    (center_x + accent_size, center_y - accent_size),
                    (center_x + accent_size, center_y + accent_size),
                    (center_x - accent_size, center_y + accent_size),
                ]
                draw.polygon(accent_points, fill=accent, outline=(255, 255, 255, 255), width=4)

            # Professional typography for initials
            initials = ''.join([word[0].upper() for word in company_name.split()[:2]])
            if not initials:
                initials = company_name[:2].upper()

            font = self._get_best_font(120)
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (self.width - text_width) // 2
            text_y = (self.height - text_height) // 2

            # Strong text shadow for visibility
            for offset in range(8, 0, -1):
                shadow_alpha = int(200 * (offset / 8))
                draw.text(
                    (text_x + offset, text_y + offset),
                    initials,
                    fill=(0, 0, 0, shadow_alpha),
                    font=font
                )

            # Main text with glow
            draw.text((text_x, text_y), initials, fill=(255, 255, 255, 255), font=font)

            img = img.filter(ImageFilter.SMOOTH)

            buffered = BytesIO()
            img.save(buffered, format="PNG", optimize=True)
            return base64.b64encode(buffered.getvalue()).decode()

        except Exception as e:
            logger.error(f"Error generating geometric logo: {e}")
            return self._generate_fallback_logo(company_name)

    def generate_minimal_logo(
        self,
        company_name: str,
        colors: List[str]
    ) -> str:
        """Generate a professional abstract/iconic logo with symbolic elements"""
        try:
            img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)

            primary = self._parse_color(colors[0] if colors else '#6366F1')
            secondary = self._parse_color(colors[1] if len(colors) > 1 else self._lighten_color(colors[0]))
            accent = self._parse_color(colors[2] if len(colors) > 2 else self._complement_color(colors[0]))

            center_x, center_y = self.width // 2, self.height // 2

            # Create abstract flowing ribbon/wave design
            # Main wave shape - multiple curved ribbons
            ribbon_paths = []
            for wave_num in range(3):
                wave_offset = (wave_num - 1) * 80
                amplitude = 120
                frequency = 3
                points = []
                
                for x in range(-300, 301, 20):
                    y_wave = amplitude * math.sin((x / 300) * math.pi * frequency)
                    points.append((center_x + x, center_y + y_wave + wave_offset))
                
                # Create closed ribbon shape
                points_bottom = [(px, py + 40) for px, py in reversed(points)]
                ribbon_path = points + points_bottom
                
                # Draw ribbon with gradient effect
                progress = wave_num / 3
                ribbon_color = self._blend_colors(primary, secondary, progress)
                
                # Shadow
                shadow_path = [(px, py + 10) for px, py in ribbon_path]
                draw.polygon(shadow_path, fill=(0, 0, 0, 80))
                
                # Main ribbon
                draw.polygon(ribbon_path, fill=ribbon_color, outline=(*accent[:3], 255), width=5)

            # Overlapping circles creating infinity/connection symbol
            circle_configs = [
                # (x_offset, y_offset, size, color_blend)
                (-100, -50, 140, 0.0),
                (100, -50, 140, 0.5),
                (0, 80, 100, 1.0),
            ]
            
            for x_off, y_off, size, blend_ratio in circle_configs:
                cx = center_x + x_off
                cy = center_y + y_off
                
                # Gradient fill for each circle
                for r in range(size, 0, -4):
                    progress = 1 - (r / size)
                    if blend_ratio < 0.5:
                        color = self._blend_colors(primary, accent, progress)
                    else:
                        color = self._blend_colors(secondary, accent, progress)
                    
                    alpha = int(255 * (0.7 + 0.3 * (1 - progress)))
                    color_with_alpha = (*color[:3], alpha)
                    
                    draw.ellipse(
                        [cx - r, cy - r, cx + r, cy + r],
                        fill=color_with_alpha
                    )
                
                # Outer ring for definition
                draw.ellipse(
                    [cx - size, cy - size, cx + size, cy + size],
                    outline=(*accent[:3], 255),
                    width=6
                )

            # Central iconic element - star/compass rose
            compass_size = 80
            num_points = 8
            for i in range(num_points):
                angle1 = (i * 360 / num_points) * math.pi / 180
                angle2 = ((i + 0.5) * 360 / num_points) * math.pi / 180
                
                x1 = center_x + compass_size * math.cos(angle1)
                y1 = center_y + compass_size * math.sin(angle1)
                x2 = center_x + (compass_size * 1.5) * math.cos(angle2)
                y2 = center_y + (compass_size * 1.5) * math.sin(angle2)
                
                # Create triangular ray
                ray_points = [
                    (center_x, center_y),
                    (x1, y1),
                    (x2, y2),
                ]
                
                ray_color = self._blend_colors(accent, secondary, i / num_points)
                draw.polygon(ray_points, fill=ray_color, outline=(*primary[:3], 200), width=3)

            # Central glowing core
            core_size = 40
            for r in range(core_size, 0, -2):
                alpha = int(255 * (r / core_size))
                core_color = (*accent[:3], alpha)
                draw.ellipse(
                    [center_x - r, center_y - r, center_x + r, center_y + r],
                    fill=core_color
                )
            
            # Outer glow ring
            draw.ellipse(
                [center_x - core_size, center_y - core_size, 
                 center_x + core_size, center_y + core_size],
                outline=(255, 255, 255, 255),
                width=4
            )

            # Decorative connecting arcs between elements
            for angle_start in range(0, 360, 60):
                start_angle = angle_start
                end_angle = angle_start + 40
                arc_radius = 200
                
                # Calculate arc points
                arc_points = []
                for angle in range(start_angle, end_angle, 2):
                    rad = angle * math.pi / 180
                    x = center_x + arc_radius * math.cos(rad)
                    y = center_y + arc_radius * math.sin(rad)
                    arc_points.append((x, y))
                
                if len(arc_points) > 1:
                    for i in range(len(arc_points) - 1):
                        draw.line([arc_points[i], arc_points[i+1]], 
                                fill=(*accent[:3], 150), width=5)

            # Professional company name typography
            font_large = self._get_best_font(64)
            name_upper = company_name.upper()
            bbox = draw.textbbox((0, 0), name_upper, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_x = (self.width - text_width) // 2
            text_y = self.height - 150

            # Text with strong shadow
            for offset in range(6, 0, -1):
                shadow_alpha = int(180 * (offset / 6))
                draw.text(
                    (text_x + offset, text_y + offset),
                    name_upper,
                    fill=(0, 0, 0, shadow_alpha),
                    font=font_large
                )

            # Main text
            draw.text((text_x, text_y), name_upper, fill=primary, font=font_large)

            img = img.filter(ImageFilter.SMOOTH)

            buffered = BytesIO()
            img.save(buffered, format="PNG", optimize=True)
            return base64.b64encode(buffered.getvalue()).decode()

        except Exception as e:
            logger.error(f"Error generating minimal logo: {e}")
            return self._generate_fallback_logo(company_name)

    def _hexagon_points(self, center_x: int, center_y: int, size: int) -> List[tuple]:
        """Calculate hexagon points"""
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            x = center_x + size * math.cos(angle)
            y = center_y + size * math.sin(angle)
            points.append((x, y))
        return points

    def _parse_color(self, hex_color: str) -> Tuple[int, int, int, int]:
        """Convert hex color to RGBA tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b, 255)

    def _blend_colors(self, color1: Tuple, color2: Tuple, t: float) -> Tuple[int, int, int, int]:
        """Blend two colors with given ratio (0-1)"""
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        a = int(color1[3] * (1 - t) + color2[3] * t) if len(color1) > 3 and len(color2) > 3 else 255
        return (r, g, b, a)

    def _get_best_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get the best available font"""
        for font_name in self.premium_fonts:
            try:
                return ImageFont.truetype(font_name, size)
            except:
                continue
        # Fallback
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

    def _get_contrast_color(self, bg_color: Tuple) -> Tuple[int, int, int, int]:
        """Get contrasting text color (black or white) based on background"""
        luminance = (0.299 * bg_color[0] + 0.587 * bg_color[1] + 0.114 * bg_color[2])
        return (255, 255, 255, 255) if luminance < 140 else (0, 0, 0, 255)

    def _draw_rotated_square(self, draw: ImageDraw, cx: int, cy: int, 
                            size: int, angle: float, color: Tuple):
        """Draw a rotated square"""
        half = size / 2
        corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
        rotated = []
        for x, y in corners:
            rx = x * math.cos(angle) - y * math.sin(angle) + cx
            ry = x * math.sin(angle) + y * math.cos(angle) + cy
            rotated.append((rx, ry))
        draw.polygon(rotated, fill=color)

    def _draw_star(self, draw: ImageDraw, cx: int, cy: int, size: int, color: Tuple):
        """Draw a decorative star/sparkle"""
        points = []
        for i in range(8):
            angle = (i * 45) * math.pi / 180
            r = size if i % 2 == 0 else size * 0.4
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)

    def _lighten_color(self, hex_color: str) -> str:
        """Lighten a color by 30%"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, int(r + (255 - r) * 0.3))
        g = min(255, int(g + (255 - g) * 0.3))
        b = min(255, int(b + (255 - b) * 0.3))
        return f'#{r:02x}{g:02x}{b:02x}'

    def _complement_color(self, hex_color: str) -> str:
        """Get a harmonious complementary color using color theory"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        # Use triadic harmony (120 degree shift) for better aesthetics
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        if r == max_val:
            return f'#{b:02x}{r:02x}{g:02x}'
        elif g == max_val:
            return f'#{g:02x}{b:02x}{r:02x}'
        else:
            return f'#{r:02x}{g:02x}{b:02x}'

    def _generate_fallback_logo(self, company_name: str) -> str:
        """Generate a professional fallback logo"""
        try:
            img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Professional gradient background
            primary = (99, 102, 241, 255)  # Indigo
            secondary = (59, 130, 246, 255)  # Blue
            
            center_x, center_y = self.width // 2, self.height // 2
            
            # Gradient circle
            for i in range(300, 0, -5):
                progress = 1 - (i / 300)
                color = self._blend_colors(primary, secondary, progress)
                draw.ellipse(
                    [center_x - i, center_y - i, center_x + i, center_y + i],
                    fill=color
                )
            
            initials = company_name[:2].upper()
            font = self._get_best_font(180)
            
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (self.width - text_width) // 2
            text_y = (self.height - text_height) // 2
            
            # Shadow
            for offset in range(6, 0, -1):
                draw.text(
                    (text_x + offset, text_y + offset),
                    initials,
                    fill=(0, 0, 0, int(100 * (offset / 6))),
                    font=font
                )
            
            draw.text((text_x, text_y), initials, fill=(255, 255, 255, 255), font=font)
            
            buffered = BytesIO()
            img.save(buffered, format="PNG", optimize=True)
            return base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            logger.error(f"Fallback logo generation failed: {e}")
            # Return a minimal base64 image
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


# Global instance
logo_generator = LogoImageGenerator()

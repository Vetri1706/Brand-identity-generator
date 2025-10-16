"""
Utility functions for Brand Identity Generator
Helper functions for color manipulation, image processing, etc.
"""

import colorsys
import math


def hex_to_rgb(hex_color):
    """
    Convert hex color to RGB tuple.
    
    Args:
        hex_color (str): Hex color code (e.g., '#FF5733')
    
    Returns:
        tuple: RGB values (0-255)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """
    Convert RGB tuple to hex color.
    
    Args:
        rgb (tuple): RGB values (0-255)
    
    Returns:
        str: Hex color code
    """
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def rgb_to_hsv(rgb):
    """
    Convert RGB to HSV color space.
    
    Args:
        rgb (tuple): RGB values (0-255)
    
    Returns:
        tuple: HSV values (H: 0-360, S: 0-1, V: 0-1)
    """
    r, g, b = [x / 255.0 for x in rgb]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h * 360, s, v)


def hsv_to_rgb(hsv):
    """
    Convert HSV to RGB color space.
    
    Args:
        hsv (tuple): HSV values (H: 0-360, S: 0-1, V: 0-1)
    
    Returns:
        tuple: RGB values (0-255)
    """
    h, s, v = hsv
    r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return tuple(int(x * 255) for x in (r, g, b))


def adjust_brightness(hex_color, factor):
    """
    Adjust the brightness of a color.
    
    Args:
        hex_color (str): Hex color code
        factor (float): Brightness factor (>1 = lighter, <1 = darker)
    
    Returns:
        str: Adjusted hex color code
    """
    rgb = hex_to_rgb(hex_color)
    adjusted = tuple(max(0, min(255, int(c * factor))) for c in rgb)
    return rgb_to_hex(adjusted)


def adjust_saturation(hex_color, factor):
    """
    Adjust the saturation of a color.
    
    Args:
        hex_color (str): Hex color code
        factor (float): Saturation factor (>1 = more saturated, <1 = less saturated)
    
    Returns:
        str: Adjusted hex color code
    """
    rgb = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(rgb)
    s = max(0, min(1, s * factor))
    adjusted_rgb = hsv_to_rgb((h, s, v))
    return rgb_to_hex(adjusted_rgb)


def get_complementary_color(hex_color):
    """
    Get the complementary color (opposite on color wheel).
    
    Args:
        hex_color (str): Hex color code
    
    Returns:
        str: Complementary hex color code
    """
    rgb = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(rgb)
    h = (h + 180) % 360
    complementary_rgb = hsv_to_rgb((h, s, v))
    return rgb_to_hex(complementary_rgb)


def get_analogous_colors(hex_color, angle=30):
    """
    Get analogous colors (adjacent on color wheel).
    
    Args:
        hex_color (str): Hex color code
        angle (int): Angle offset in degrees (default: 30)
    
    Returns:
        tuple: Two analogous hex color codes
    """
    rgb = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(rgb)
    
    h1 = (h + angle) % 360
    h2 = (h - angle) % 360
    
    color1_rgb = hsv_to_rgb((h1, s, v))
    color2_rgb = hsv_to_rgb((h2, s, v))
    
    return (rgb_to_hex(color1_rgb), rgb_to_hex(color2_rgb))


def get_triadic_colors(hex_color):
    """
    Get triadic colors (120 degrees apart on color wheel).
    
    Args:
        hex_color (str): Hex color code
    
    Returns:
        tuple: Two triadic hex color codes
    """
    rgb = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(rgb)
    
    h1 = (h + 120) % 360
    h2 = (h + 240) % 360
    
    color1_rgb = hsv_to_rgb((h1, s, v))
    color2_rgb = hsv_to_rgb((h2, s, v))
    
    return (rgb_to_hex(color1_rgb), rgb_to_hex(color2_rgb))


def get_tetradic_colors(hex_color):
    """
    Get tetradic colors (90 degrees apart on color wheel).
    
    Args:
        hex_color (str): Hex color code
    
    Returns:
        tuple: Three tetradic hex color codes
    """
    rgb = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(rgb)
    
    h1 = (h + 90) % 360
    h2 = (h + 180) % 360
    h3 = (h + 270) % 360
    
    color1_rgb = hsv_to_rgb((h1, s, v))
    color2_rgb = hsv_to_rgb((h2, s, v))
    color3_rgb = hsv_to_rgb((h3, s, v))
    
    return (rgb_to_hex(color1_rgb), rgb_to_hex(color2_rgb), rgb_to_hex(color3_rgb))


def get_monochromatic_palette(hex_color, steps=5):
    """
    Generate a monochromatic color palette.
    
    Args:
        hex_color (str): Base hex color code
        steps (int): Number of color variations
    
    Returns:
        list: List of hex color codes
    """
    rgb = hex_to_rgb(hex_color)
    h, s, v = rgb_to_hsv(rgb)
    
    palette = []
    for i in range(steps):
        factor = 0.3 + (i / (steps - 1)) * 0.7
        adjusted_v = v * factor
        color_rgb = hsv_to_rgb((h, s, adjusted_v))
        palette.append(rgb_to_hex(color_rgb))
    
    return palette


def color_contrast_ratio(hex_color1, hex_color2):
    """
    Calculate the contrast ratio between two colors (WCAG standard).
    
    Args:
        hex_color1 (str): First hex color code
        hex_color2 (str): Second hex color code
    
    Returns:
        float: Contrast ratio (1-21)
    """
    def get_luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        
        def adjust(channel):
            if channel <= 0.03928:
                return channel / 12.92
            return ((channel + 0.055) / 1.055) ** 2.4
        
        r = adjust(r)
        g = adjust(g)
        b = adjust(b)
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    rgb1 = hex_to_rgb(hex_color1)
    rgb2 = hex_to_rgb(hex_color2)
    
    l1 = get_luminance(rgb1)
    l2 = get_luminance(rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def is_color_light(hex_color):
    """
    Determine if a color is light or dark.
    
    Args:
        hex_color (str): Hex color code
    
    Returns:
        bool: True if light, False if dark
    """
    rgb = hex_to_rgb(hex_color)
    # Calculate perceived brightness
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    return brightness > 128


def get_text_color_for_background(hex_color):
    """
    Get the optimal text color (black or white) for a given background.
    
    Args:
        hex_color (str): Background hex color code
    
    Returns:
        str: '#000000' or '#FFFFFF'
    """
    return '#000000' if is_color_light(hex_color) else '#FFFFFF'


def blend_colors(hex_color1, hex_color2, ratio=0.5):
    """
    Blend two colors together.
    
    Args:
        hex_color1 (str): First hex color code
        hex_color2 (str): Second hex color code
        ratio (float): Blend ratio (0-1, 0=color1, 1=color2)
    
    Returns:
        str: Blended hex color code
    """
    rgb1 = hex_to_rgb(hex_color1)
    rgb2 = hex_to_rgb(hex_color2)
    
    blended = tuple(
        int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio)
        for i in range(3)
    )
    
    return rgb_to_hex(blended)


def validate_hex_color(hex_color):
    """
    Validate if a string is a valid hex color code.
    
    Args:
        hex_color (str): Potential hex color code
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not hex_color:
        return False
    
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) not in [3, 6]:
        return False
    
    try:
        int(hex_color, 16)
        return True
    except ValueError:
        return False


def normalize_hex_color(hex_color):
    """
    Normalize a hex color code to 6-digit format with #.
    
    Args:
        hex_color (str): Hex color code (3 or 6 digits, with or without #)
    
    Returns:
        str: Normalized 6-digit hex color code with #
    """
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    
    return f'#{hex_color.upper()}'

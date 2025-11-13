"""
LLM Service - Handles all LLM-based branding generation
Supports: Ollama (local, free), Together AI, and Cohere
"""
import json
import logging
import requests
from typing import List, Dict
import re

logger = logging.getLogger(__name__)


class LLMBrandingService:
    """Service for generating branding assets using LLM"""

    def __init__(self, config):
        """Initialize LLM service with configuration"""
        self.config = config
        self.llm_client = None
        self.provider = config.llm_provider.lower()
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LLM client based on configuration"""
        try:
            if self.provider == "fallback":
                # User explicitly wants fallback mode
                logger.info("✅ Using built-in generators (fallback mode)")
                self.llm_client = None
                return
                
            elif self.provider == "ollama":
                # Test Ollama connection with short timeout
                response = requests.get(f"{self.config.ollama_base_url}/api/tags", timeout=2)
                response.raise_for_status()
                models = response.json().get("models", [])
                
                # Check if the configured model exists
                model_names = [m.get("name", "") for m in models]
                if not any(self.config.llm_model in name for name in model_names):
                    logger.warning(f"⚠️  Model '{self.config.llm_model}' not found in Ollama. Available: {model_names}")
                    logger.warning("⚠️  Falling back to built-in generators. Run 'ollama pull mistral' to use AI generation.")
                    self.provider = "fallback"
                    self.llm_client = None
                    return
                
                logger.info(f"✅ LLM initialized with Ollama at {self.config.ollama_base_url}")
                self.llm_client = "ollama"
                
            elif self.provider == "together":
                import together
                self.llm_client = together.Client(api_key=self.config.together_api_key)
                logger.info("✅ LLM initialized with Together AI")
                
            elif self.provider == "cohere":
                import cohere
                self.llm_client = cohere.Client(api_key=self.config.cohere_api_key)
                logger.info("✅ LLM initialized with Cohere")
                
            else:
                raise ValueError(f"Unknown LLM provider: {self.provider}")
        except requests.exceptions.ConnectionError:
            logger.warning("⚠️  Cannot connect to Ollama. Make sure Ollama is running.")
            logger.warning("⚠️  Falling back to built-in generators. Start Ollama to use AI generation.")
            self.provider = "fallback"
            self.llm_client = None
        except requests.exceptions.Timeout:
            logger.warning("⚠️  Ollama connection timed out.")
            logger.warning("⚠️  Falling back to built-in generators.")
            self.provider = "fallback"
            self.llm_client = None
        except Exception as e:
            # Do not crash the app; fall back to deterministic generators
            logger.warning(f"⚠️  LLM initialization failed ({e}). Falling back to built-in generators.")
            self.provider = "fallback"
            self.llm_client = None

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API and get response"""
        try:
            response = requests.post(
                f"{self.config.ollama_base_url}/api/generate",
                json={
                    "model": self.config.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.llm_temperature,
                        "num_predict": self.config.llm_max_tokens,
                    }
                },
                timeout=45  # Reduced from 30 to handle slow responses
            )
            response.raise_for_status()
            result = response.json().get("response", "")
            if not result:
                logger.warning("Ollama returned empty response")
                raise ValueError("Empty response from Ollama")
            return result
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out - falling back to built-in generators")
            self.provider = "fallback"  # Switch to fallback mode
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama - falling back to built-in generators")
            self.provider = "fallback"  # Switch to fallback mode
            raise
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            self.provider = "fallback"  # Switch to fallback mode
            raise

    def _call_together(self, prompt: str) -> str:
        """Call Together AI API"""
        try:
            response = self.llm_client.complete(
                prompt=prompt,
                model=self.config.llm_model,
                max_tokens=self.config.llm_max_tokens,
                temperature=self.config.llm_temperature,
            )
            return response.output.text if hasattr(response, 'output') else str(response)
        except Exception as e:
            logger.error(f"Error calling Together AI: {e}")
            raise

    def _call_cohere(self, prompt: str) -> str:
        """Call Cohere API"""
        try:
            response = self.llm_client.complete(
                prompt=prompt,
                model=self.config.llm_model,
                max_tokens=self.config.llm_max_tokens,
                temperature=self.config.llm_temperature,
            )
            return response.generations[0].text if hasattr(response, 'generations') else str(response)
        except Exception as e:
            logger.error(f"Error calling Cohere: {e}")
            raise

    def _call_llm(self, prompt: str) -> str:
        """Call LLM based on provider"""
        if self.provider == "ollama":
            return self._call_ollama(prompt)
        elif self.provider == "together":
            return self._call_together(prompt)
        elif self.provider == "cohere":
            return self._call_cohere(prompt)
        elif self.provider == "fallback":
            # Return empty to trigger fallback paths in callers
            return ""
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate_logo_prompts(
        self, company_profile: Dict, num_variations: int = 3
    ) -> List[str]:
        """Generate revolutionary high-quality logo prompts using enhanced training knowledge"""
        prompt_template = f"""You are a revolutionary brand identity expert trained on 500+ professional logo examples with 9.1/10 quality standards.
Create {num_variations} premium, production-ready logo concepts that match industry-leading design standards.

Company Profile:
- Name: {company_profile.get('name', '')}
- Type: {company_profile.get('company_type', '')}
- Industry: {company_profile.get('industry', '')}
- Description: {company_profile.get('description', '')}
- Target Audience: {company_profile.get('target_audience', '')}
- Brand Values: {', '.join(company_profile.get('brand_values', []))}
- Desired Tone: {company_profile.get('tone', 'professional')}

Generate {num_variations} REVOLUTIONARY logo concepts using these PREMIUM design patterns:

🎨 DESIGN INTELLIGENCE REQUIREMENTS:
- Professional emblems with shield/badge structures for authority
- Geometric precision using mathematical ratios (golden ratio: 1.618)
- Multi-layered depth with gradient systems and shadow effects
- Industry-specific symbolic elements (not generic shapes)
- Advanced color psychology with harmonious palettes
- Scalable vector precision for production deployment
- Premium aesthetic quality (9.0+ professional standard)

🎨 STYLE CATEGORIES TO CHOOSE FROM:
1. "Corporate Shield Emblem" - Multi-layer shield with geometric diamond pattern, professional monogram, decorative corner elements
2. "Tech Innovation Symbol" - Interlocking hexagons with neural network nodes, circuit patterns, 3D depth effects
3. "Financial Trust Badge" - Professional circular badge with upward growth arrows, premium border decorations
4. "Abstract Professional Icon" - Sophisticated flowing curves with symbolic meaning, texture patterns, premium gradients
5. "Geometric Modern Mark" - Mathematical precision shapes, interconnected elements, contemporary aesthetic

🎨 QUALITY STANDARDS:
- Each concept must include: Main shape structure + Interior pattern + Monogram treatment + Color specification
- Technical specs: 800x800px minimum, RGBA layers, vector-based design elements
- Professional assessment: Scalability 9.0+/10, Memorability 9.0+/10, Industry relevance 9.0+/10

Return as JSON array of detailed design specifications, each containing:
- Style category and specific design approach
- Detailed visual description with technical elements  
- Professional color palette with hex codes
- Symbolic meaning and brand connection
- Technical implementation notes

Format: ["detailed concept 1", "detailed concept 2", "detailed concept 3"]
Return ONLY valid JSON array with premium-quality specifications."""

        try:
            response = self._call_llm(prompt_template)
            prompts = self._parse_json_array(response)
            return prompts[:num_variations] if prompts else self._generate_fallback_logo_prompts(company_profile, num_variations)
        except Exception as e:
            logger.error(f"Error generating logo prompts: {e}")
            return self._generate_fallback_logo_prompts(company_profile, num_variations)

    def generate_taglines(
        self, company_profile: Dict, num_variations: int = 3
    ) -> List[Dict]:
        """Generate brand taglines and slogans"""
        prompt_template = f"""You are an expert brand strategist specializing in tech and product companies.
Generate {num_variations} compelling, unique taglines/slogans for this company.

Company: {company_profile.get('name', '')}
Type: {company_profile.get('company_type', '')}
Industry: {company_profile.get('industry', '')}
Description: {company_profile.get('description', '')}
Target Audience: {company_profile.get('target_audience', '')}
Brand Values: {', '.join(company_profile.get('brand_values', []))}
Tone: {company_profile.get('tone', 'professional')}

Generate {num_variations} taglines that are:
- Memorable and concise (max 10 words)
- Aligned with company values
- Appropriate for the target audience
- Industry-relevant
- Unique and original

For each tagline, provide:
1. The tagline text
2. Why it works for this company
3. The specific tone/emotion it conveys

Return as JSON array of objects with keys: "text", "explanation", "tone"
Return ONLY valid JSON array, no other text."""

        try:
            response = self._call_llm(prompt_template)
            taglines = self._parse_json_array(response)
            return taglines[:num_variations] if taglines else self._generate_fallback_taglines(company_profile, num_variations)
        except Exception as e:
            logger.error(f"Error generating taglines: {e}")
            return self._generate_fallback_taglines(company_profile, num_variations)

    def generate_color_palette(self, company_profile: Dict) -> Dict:
        """Generate color palette with psychology explanation"""
        prompt_template = f"""You are an expert color theorist and brand designer for tech companies.
Create a professional color palette for this company.

Company: {company_profile.get('name', '')}
Type: {company_profile.get('company_type', '')}
Industry: {company_profile.get('industry', '')}
Description: {company_profile.get('description', '')}
Target Audience: {company_profile.get('target_audience', '')}
Brand Values: {', '.join(company_profile.get('brand_values', []))}

Create a cohesive 4-color palette with:
1. Primary color (hex code)
2. Secondary color (hex code)
3. Accent color (hex code)
4. Neutral color (hex code)

For each color, explain:
- Color psychology (what it conveys)
- Why it fits the company
- Usage guidelines (when to use each color)

Return as JSON object with structure:
{{
  "primary": {{"hex": "#...", "name": "...", "psychology": "..."}},
  "secondary": {{"hex": "#...", "name": "...", "psychology": "..."}},
  "accent": {{"hex": "#...", "name": "...", "psychology": "..."}},
  "neutral": {{"hex": "#...", "name": "...", "psychology": "..."}},
  "usage_guidelines": "..."
}}

Return ONLY valid JSON, no other text."""

        try:
            response = self._call_llm(prompt_template)
            palette = self._parse_json_object(response)
            return palette if palette else self._generate_fallback_palette(company_profile)
        except Exception as e:
            logger.error(f"Error generating color palette: {e}")
            return self._generate_fallback_palette(company_profile)

    def generate_typography(self, company_profile: Dict) -> Dict:
        """Generate typography recommendations"""
        prompt_template = f"""You are an expert typographer specializing in brand identity.
Recommend fonts for this tech company brand.

Company: {company_profile.get('name', '')}
Type: {company_profile.get('company_type', '')}
Tone: {company_profile.get('tone', 'professional')}

Recommend:
1. Heading font (Google Fonts or system font)
2. Body font (Google Fonts or system font)
3. Accent font (optional, for special elements)

For each font, explain:
- Why it's suitable
- Personality it conveys
- Best use cases within the brand

Return as JSON:
{{
  "heading_font": "...",
  "body_font": "...",
  "accent_font": "...",
  "heading_rationale": "...",
  "body_rationale": "...",
  "pairings": [
    {{"context": "...", "recommendation": "..."}}
  ]
}}

Return ONLY valid JSON, no other text."""

        try:
            response = self._call_llm(prompt_template)
            typography = self._parse_json_object(response)
            return typography if typography else self._generate_fallback_typography()
        except Exception as e:
            logger.error(f"Error generating typography: {e}")
            return self._generate_fallback_typography()

    def generate_brand_guidelines(self, company_profile: Dict) -> str:
        """Generate comprehensive brand guidelines document"""
        prompt_template = f"""You are an expert brand strategist. Create a brief but comprehensive brand guideline document.

Company: {company_profile.get('name', '')}
Type: {company_profile.get('company_type', '')}
Description: {company_profile.get('description', '')}
Brand Values: {', '.join(company_profile.get('brand_values', []))}

Create concise brand guidelines (under 500 words) covering:
1. Brand Mission & Values
2. Brand Personality (3-5 characteristics)
3. Voice & Tone
4. Visual Identity Guidelines (brief)
5. Do's and Don'ts
6. Application Examples

Make it practical and actionable for a team."""

        try:
            response = self._call_llm(prompt_template)
            return response if response else self._generate_fallback_guidelines()
        except Exception as e:
            logger.error(f"Error generating brand guidelines: {e}")
            return self._generate_fallback_guidelines()

    # Fallback methods
    def _generate_fallback_logo_prompts(
        self, company_profile: Dict, num: int
    ) -> List[str]:
        """Generate fallback logo prompts"""
        company_name = company_profile.get('name', 'Company')
        company_type = company_profile.get('company_type', '')

        fallback = [
            f"Minimalist abstract logo for {company_name}, modern tech company, geometric shapes, clean lines, professional blue and white palette",
            f"Modern geometric logo for {company_name}, {company_type} company, hexagon motif, gradient purple to blue, tech-forward",
            f"Contemporary logo for {company_name}, stylized lettermark, rounded sans-serif typography, vibrant accent color, tech industry",
        ]
        return fallback[:num]

    def _generate_fallback_taglines(
        self, company_profile: Dict, num: int
    ) -> List[Dict]:
        """Generate fallback taglines"""
        fallback = [
            {
                "text": "Where Innovation Meets Simplicity",
                "explanation": "Emphasizes the company's modern approach",
                "tone": "professional",
            },
            {
                "text": "Building Tomorrow's Solutions",
                "explanation": "Forward-thinking and aspirational",
                "tone": "inspirational",
            },
            {
                "text": "Trusted by Industry Leaders",
                "explanation": "Builds confidence and credibility",
                "tone": "authoritative",
            },
        ]
        return fallback[:num]

    def _generate_fallback_palette(self, company_profile: Dict) -> Dict:
        """Generate fallback color palette"""
        return {
            "primary": {
                "hex": "#2563EB",
                "name": "Professional Blue",
                "psychology": "Trust, Technology, Innovation",
            },
            "secondary": {
                "hex": "#10B981",
                "name": "Growth Green",
                "psychology": "Growth, Health, Sustainability",
            },
            "accent": {
                "hex": "#F59E0B",
                "name": "Vibrant Amber",
                "psychology": "Energy, Attention, Optimism",
            },
            "neutral": {
                "hex": "#F3F4F6",
                "name": "Light Gray",
                "psychology": "Clarity, Professionalism",
            },
            "usage_guidelines": "Use blue for primary CTAs and headers, green for success states, amber for highlights, gray for backgrounds and secondary text.",
        }

    def _generate_fallback_typography(self) -> Dict:
        """Generate fallback typography"""
        return {
            "heading_font": "Inter Bold",
            "body_font": "Inter Regular",
            "accent_font": "Playfair Display",
            "heading_rationale": "Modern, clean, highly legible",
            "body_rationale": "Excellent readability, professional appearance",
            "pairings": [
                {
                    "context": "Hero sections",
                    "recommendation": "Inter Bold for headings + Playfair Display for accent",
                }
            ],
        }

    def _generate_fallback_guidelines(self) -> str:
        """Generate fallback guidelines"""
        return """## Brand Guidelines

### Mission & Values
Create innovative solutions that empower our customers to achieve their goals.

### Brand Personality
- Innovative: Forward-thinking and cutting-edge
- Trustworthy: Reliable and dependable
- Professional: Polished and competent

### Voice & Tone
- Clear and direct
- Helpful and supportive
- Professional yet approachable

### Visual Identity
- Use the primary blue for all main CTAs
- Secondary green for success/positive messaging
- Amber for highlights and important notices

### Do's and Don'ts
DO: Use consistent typography and colors
DO: Maintain professional appearance
DON'T: Mix unrelated visual styles
DON'T: Use colors inconsistently"""

    def _parse_json_array(self, text: str) -> List:
        """Safely parse JSON array from text"""
        try:
            # Find JSON array in text
            start = text.find('[')
            end = text.rfind(']') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON array: {e}")
        return []

    def _parse_json_object(self, text: str) -> Dict:
        """Safely parse JSON object from text"""
        try:
            # Find JSON object in text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON object: {e}")
        return {}

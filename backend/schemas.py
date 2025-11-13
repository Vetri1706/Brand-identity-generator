"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class CompanyType(str, Enum):
    """Supported company types"""
    SAAS = "saas"
    FINTECH = "fintech"
    HEALTHTECH = "healthtech"
    ECOMMERCE = "ecommerce"
    AI_ML = "ai_ml"
    BLOCKCHAIN = "blockchain"
    CYBERSECURITY = "cybersecurity"
    DEVTOOLS = "devtools"


class CompanyProfileCreate(BaseModel):
    """Create company profile"""
    name: str = Field(..., min_length=1, max_length=100)
    company_type: CompanyType
    industry: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    target_audience: str = Field(..., min_length=1, max_length=500)
    brand_values: List[str] = Field(...)
    tone: str = Field(default="professional", max_length=50)
    additional_context: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "TechStartup AI",
                "company_type": "ai_ml",
                "industry": "Artificial Intelligence",
                "description": "Building AI tools for businesses",
                "target_audience": "Enterprise B2B companies",
                "brand_values": ["Innovation", "Trust", "Simplicity"],
                "tone": "professional",
            }
        }


class CompanyProfile(CompanyProfileCreate):
    """Company profile response"""
    id: str
    created_at: datetime
    updated_at: datetime


class GodModeOptions(BaseModel):
    """Advanced user-driven guidance to supercharge generation"""
    prompt: Optional[str] = None
    industry_override: Optional[str] = None
    color_overrides: Optional[List[str]] = None  # up to 3 hex colors
    style_preference: Optional[str] = None       # e.g., minimal, 3d, geometric
    symbols: Optional[List[str]] = None          # e.g., ["flower","leaf","shield"]
    negative: Optional[List[str]] = None         # e.g., ["no letters","no gradients"]
    seed: Optional[str] = None


class BrandingRequest(BaseModel):
    """Request brand assets generation"""
    company_id: str
    company_profile: Optional[CompanyProfileCreate] = None
    num_variations: int = Field(default=3, ge=1, le=10)
    focus: str = Field(
        default="logo",
        pattern="^(logo|tagline|palette|typography|all)$"
    )
    god_mode: Optional[GodModeOptions] = None

    class Config:
        json_schema_extra = {
            "example": {
                "company_id": "company_123",
                "num_variations": 3,
                "focus": "all",
                "god_mode": {
                    "prompt": "Make it minimal, nature-forward, no letters",
                    "industry_override": "Floral boutique",
                    "color_overrides": ["#16A34A", "#EC4899", "#A855F7"],
                    "style_preference": "minimal",
                    "symbols": ["flower", "leaf"],
                    "negative": ["no text", "no serif"],
                    "seed": "1234"
                }
            }
        }


class LogoVariation(BaseModel):
    """Single logo variation"""
    id: str
    description: str
    color_scheme: List[str]
    style: str
    image_url: Optional[str] = None
    prompt_used: str


class TaglineVariation(BaseModel):
    """Single tagline variation"""
    id: str
    text: str
    tone: str
    explanation: str


class ColorPalette(BaseModel):
    """Color palette for brand"""
    primary: str
    secondary: str
    accent: str
    neutral: str
    psychology: Dict[str, str]
    usage_guidelines: str


class TypographyRecommendation(BaseModel):
    """Typography recommendations"""
    heading_font: str
    body_font: str
    accent_font: Optional[str] = None
    rationale: str
    pairings: List[Dict[str, str]]


class BrandingResponse(BaseModel):
    """Complete branding response"""
    id: str
    company_id: str
    logos: List[LogoVariation]
    taglines: List[TaglineVariation]
    color_palette: ColorPalette
    typography: TypographyRecommendation
    brand_guidelines: str
    generated_at: datetime
    generation_time_seconds: float


class GenerationHistory(BaseModel):
    """Past generation history"""
    id: str
    company_id: str
    branding_id: str
    created_at: datetime
    status: str


class ModelMetrics(BaseModel):
    """Model performance metrics"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time: float
    num_samples: int

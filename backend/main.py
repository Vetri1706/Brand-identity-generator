"""
FastAPI Backend for Brand Identity Generator MVP
Handles LLM-based branding asset generation for tech companies
"""
import logging
import time
import uuid
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from schemas import (
    CompanyProfileCreate,
    CompanyProfile,
    BrandingRequest,
    BrandingResponse,
    LogoVariation,
    TaglineVariation,
    ColorPalette,
    TypographyRecommendation,
)
from llm_service import LLMBrandingService
from logo_generator import logo_generator
from ultra_logo_generator import ultra_logo_generator
from professional_logo_generator import professional_logo_generator
from industry_logo_generator import industry_logo_generator

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global LLM service instance
llm_service: LLMBrandingService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global llm_service
    
    # Startup
    logger.info("🚀 Starting Brand Identity Generator Backend")
    try:
        llm_service = LLMBrandingService(settings)
        logger.info("✅ LLM service initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize LLM service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Brand Identity Generator Backend")


# Create FastAPI app
app = FastAPI(
    title="Brand Identity Generator API",
    description="AI-powered brand identity generation for tech companies",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
cors_origins = settings.cors_origins if settings.environment == "production" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# ==================== Routes ====================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "llm_model": settings.llm_model,
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Brand Identity Generator API",
        "version": "1.0.0",
        "description": "AI-powered brand identity generation for tech companies",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "health": "/health",
            "generate_branding": "/api/v1/generate-branding",
            "company_profiles": "/api/v1/company-profiles",
        },
    }


@app.options("/api/v1/generate-branding", tags=["CORS"])
async def generate_branding_options():
    """Handle CORS preflight for generate-branding endpoint"""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, Accept",
            "Access-Control-Max-Age": "86400",
        }
    )


@app.post(
    "/api/v1/generate-branding",
    response_model=BrandingResponse,
    tags=["Branding Generation"],
    summary="Generate complete brand identity",
)
async def generate_branding(request: BrandingRequest):
    """
    Generate comprehensive brand identity assets for a company.
    
    Generates:
    - Multiple logo variations with descriptions
    - Tagline/slogan options
    - Color palette with psychology
    - Typography recommendations
    - Brand guidelines document
    
    Returns complete branding package in ~30-60 seconds.
    """
    if not llm_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service not initialized",
        )
    
    try:
        start_time = time.time()
        generation_id = str(uuid.uuid4())
        
        logger.info(f"[{generation_id}] Starting branding generation for company {request.company_id}")
        
        # Prepare company profile
        if request.company_profile:
            company_data = request.company_profile.model_dump()
        else:
            company_data = {
                "name": f"Company {request.company_id}",
                "company_type": "saas",
                "industry": "Technology",
                "description": "Tech company",
                "target_audience": "Enterprise",
                "brand_values": ["Innovation", "Quality"],
            }
        
        # Generate branding assets based on focus
        logos = []
        taglines = []
        color_palette = None
        typography = None
        brand_guidelines = ""
        
        if request.focus in ["logo", "all"]:
            logger.info(f"[{generation_id}] Generating industry-aware logos with VARIATIONS")
            logo_prompts = llm_service.generate_logo_prompts(
                company_data, request.num_variations
            )
            
            # Get industry and company type from company data
            industry = company_data.get("industry", "Technology")
            company_type = company_data.get("company_type", "saas")
            company_name = company_data.get("name", "Company")

            # God Mode overrides
            gm = getattr(request, 'god_mode', None)
            if gm and gm.prompt:
                # Add god mode prompt into additional_context for downstream LLM-based pieces
                company_data["additional_context"] = f"{company_data.get('additional_context','')} GOD_MODE: {gm.prompt}".strip()

            # Combine industry and company_type, allow override and keyword bias (symbols/negative)
            industry_context = f"{gm.industry_override if gm and gm.industry_override else industry} {company_type}"
            if gm and (gm.symbols or gm.negative):
                bias = []
                if gm.symbols:
                    bias.append("symbols:" + ",".join(gm.symbols))
                if gm.negative:
                    bias.append("avoid:" + ",".join(gm.negative))
                industry_context = industry_context + " " + " ".join(bias)
            
            logger.info(f"[{generation_id}] Using PROFESSIONAL diverse logo generator for: {industry_context}")
            
            # Create DIFFERENT color schemes for each variation
            color_variations = [
                ["#2563EB", "#10B981", "#F59E0B"],  # Blue-Green-Orange
                ["#8B5CF6", "#EC4899", "#06B6D4"],  # Purple-Pink-Cyan
                ["#EF4444", "#F59E0B", "#10B981"],  # Red-Orange-Green
            ]

            # Apply color overrides if provided
            if gm and gm.color_overrides and len(gm.color_overrides) >= 3:
                ov = gm.color_overrides[:3]
                color_variations = [ov, ov, ov]
            
            # Generate truly diverse professional logos
            professional_logos = professional_logo_generator.generate_diverse_professional_logos(
                company_name,
                industry,
                [color_variations[0][0], color_variations[1][0], color_variations[2][0]],  # Use first color from each palette
                request.num_variations
            )
            
            # Create logo variations with proper descriptions
            style_descriptions = [
                "Professional Wordmark - Typography-focused design emphasizing brand name",
                "Custom Lettermark - Monogram-based design with distinctive lettering", 
                "Pictorial Symbol - Icon-based design with industry-relevant imagery",
                "Abstract Mark - Artistic geometric design with unique visual elements",
                "Combination Logo - Balanced integration of text and symbolic elements",
                "Professional Emblem - Badge-style design with authoritative presence"
            ]
            
            for idx, logo_image in enumerate(professional_logos, 1):
                # Get appropriate description for this logo type
                logo_desc = style_descriptions[(idx - 1) % len(style_descriptions)]
                
                # Use different color scheme for each
                variation_colors = color_variations[(idx - 1) % len(color_variations)]
                
                logos.append(
                    LogoVariation(
                        id=f"logo_{idx}",
                        description=logo_desc,
                        color_scheme=variation_colors,
                        style=f"Professional {['Wordmark', 'Lettermark', 'Pictorial', 'Abstract', 'Combination', 'Emblem'][idx-1]}",
                        prompt_used=f"Professional {logo_desc} for {company_name} in {industry}",
                        image_url=f"data:image/png;base64,{logo_image}"
                    )
                )
        
        if request.focus in ["tagline", "all"]:
            logger.info(f"[{generation_id}] Generating taglines")
            tagline_data = llm_service.generate_taglines(
                company_data, request.num_variations
            )
            
            for idx, tagline in enumerate(tagline_data, 1):
                taglines.append(
                    TaglineVariation(
                        id=f"tagline_{idx}",
                        text=tagline.get("text", f"Tagline {idx}"),
                        tone=tagline.get("tone", "professional"),
                        explanation=tagline.get("explanation", ""),
                    )
                )
        
        if request.focus in ["palette", "all"]:
            logger.info(f"[{generation_id}] Generating color palette")
            palette_data = llm_service.generate_color_palette(company_data)
            
            primary = palette_data.get("primary", {})
            secondary = palette_data.get("secondary", {})
            accent = palette_data.get("accent", {})
            neutral = palette_data.get("neutral", {})
            
            color_palette = ColorPalette(
                primary=primary.get("hex", "#2563EB"),
                secondary=secondary.get("hex", "#10B981"),
                accent=accent.get("hex", "#F59E0B"),
                neutral=neutral.get("hex", "#F3F4F6"),
                psychology={
                    "primary": primary.get("psychology", "Trust"),
                    "secondary": secondary.get("psychology", "Growth"),
                    "accent": accent.get("psychology", "Energy"),
                    "neutral": neutral.get("psychology", "Clarity"),
                },
                usage_guidelines=palette_data.get("usage_guidelines", ""),
            )
        
        if request.focus in ["typography", "all"]:
            logger.info(f"[{generation_id}] Generating typography")
            typo_data = llm_service.generate_typography(company_data)
            
            typography = TypographyRecommendation(
                heading_font=typo_data.get("heading_font", "Inter Bold"),
                body_font=typo_data.get("body_font", "Inter Regular"),
                accent_font=typo_data.get("accent_font"),
                rationale=typo_data.get("heading_rationale", ""),
                pairings=typo_data.get("pairings", []),
            )
        
        if request.focus == "all":
            logger.info(f"[{generation_id}] Generating brand guidelines")
            brand_guidelines = llm_service.generate_brand_guidelines(company_data)
        
        generation_time = time.time() - start_time
        
        logger.info(
            f"[{generation_id}] ✅ Branding generation completed in {generation_time:.2f}s"
        )
        
        return BrandingResponse(
            id=generation_id,
            company_id=request.company_id,
            logos=logos,
            taglines=taglines,
            color_palette=color_palette or ColorPalette(
                primary="#2563EB",
                secondary="#10B981",
                accent="#F59E0B",
                neutral="#F3F4F6",
                psychology={},
                usage_guidelines="",
            ),
            typography=typography or TypographyRecommendation(
                heading_font="Inter Bold",
                body_font="Inter Regular",
                rationale="",
                pairings=[],
            ),
            brand_guidelines=brand_guidelines,
            generated_at=datetime.utcnow(),
            generation_time_seconds=generation_time,
        )
    
    except Exception as e:
        logger.error(f"Error generating branding: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Branding generation failed: {str(e)}",
        )


@app.get(
    "/api/v1/company-types",
    tags=["Reference Data"],
    summary="Get supported company types",
)
async def get_company_types():
    """Get list of supported company types for branding generation"""
    return {
        "company_types": [
            {
                "id": "saas",
                "name": "SaaS",
                "description": "Software as a Service",
            },
            {
                "id": "fintech",
                "name": "FinTech",
                "description": "Financial Technology",
            },
            {
                "id": "healthtech",
                "name": "HealthTech",
                "description": "Health Technology",
            },
            {
                "id": "ecommerce",
                "name": "E-Commerce",
                "description": "E-Commerce Platform",
            },
            {
                "id": "ai_ml",
                "name": "AI/ML",
                "description": "Artificial Intelligence & Machine Learning",
            },
            {
                "id": "blockchain",
                "name": "Blockchain",
                "description": "Blockchain/Web3",
            },
            {
                "id": "cybersecurity",
                "name": "Cybersecurity",
                "description": "Cybersecurity",
            },
            {
                "id": "devtools",
                "name": "DevTools",
                "description": "Developer Tools",
            },
        ]
    }


@app.get(
    "/api/v1/example-company-profile",
    response_model=CompanyProfileCreate,
    tags=["Reference Data"],
    summary="Get example company profile",
)
async def get_example_profile():
    """Get example company profile for reference"""
    return CompanyProfileCreate(
        name="TechFlow AI",
        company_type="ai_ml",
        industry="Artificial Intelligence",
        description="Building AI-powered automation tools for enterprises",
        target_audience="Fortune 500 companies and mid-market enterprises",
        brand_values=["Innovation", "Reliability", "Transparency", "Excellence"],
        tone="professional",
    )


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Generic exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )

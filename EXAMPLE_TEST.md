# Example Test Cases for Brand Identity Generator

## Test Case 1: Tech Startup (Recommended First Test)

### Company Information

- **Company Name**: CloudSync
- **Industry**: Cloud Computing / SaaS
- **Target Audience**: Small to medium businesses, tech-savvy professionals
- **Values**: Innovation, Reliability, Simplicity, Security
- **Description**: A cloud storage and collaboration platform that helps remote teams work seamlessly. We focus on making file sharing fast, secure, and intuitive for modern businesses.

### Expected Results

- Logo prompts featuring cloud, sync, or connection themes
- Taglines emphasizing speed, security, and collaboration
- Color palette: Blues (trust), whites (clean), possibly accent colors (energy)
- Modern, clean typography
- Professional brand guidelines

---

## Test Case 2: E-commerce Platform

### Company Information

- **Company Name**: ShopLocal
- **Industry**: E-commerce / Retail Technology
- **Target Audience**: Local businesses, conscious consumers, millennials
- **Values**: Community, Sustainability, Authenticity, Support Local
- **Description**: An online marketplace connecting local artisans and small businesses with customers who want to shop sustainably and support their community.

### Expected Results

- Logo prompts with community, handshake, or local themes
- Taglines about community support and authentic products
- Color palette: Greens (sustainability), warm tones (community)
- Friendly, approachable typography
- Brand guidelines emphasizing warmth and trust

---

## Test Case 3: AI/ML Company

### Company Information

- **Company Name**: NeuralEdge
- **Industry**: Artificial Intelligence / Machine Learning
- **Target Audience**: Enterprise clients, data scientists, CTO/CTOs
- **Values**: Intelligence, Precision, Innovation, Cutting-edge
- **Description**: We build enterprise-grade AI models that help companies make data-driven decisions faster. Our platform automates complex data analysis and provides actionable insights.

### Expected Results

- Logo prompts with neural networks, brain, or geometric patterns
- Taglines about intelligence, automation, and insights
- Color palette: Deep blues/purples (intelligence), metallics (tech)
- Modern, bold typography
- Sophisticated brand guidelines

---

## Quick Test Steps

1. **Open the application**: http://localhost:3000

2. **Fill in the form** with one of the examples above

3. **Click "Generate Brand Identity"**

4. **Wait 30-60 seconds** (Ollama needs time to generate with Mistral model)

5. **Review the results**:
   - 3 logo prompt variations
   - 3 tagline variations
   - Color palette (5-6 colors)
   - Typography recommendations
   - Brand usage guidelines

---

## What to Check

### ✅ Good Results Should Include:

- Logo prompts that match the company's industry and values
- Taglines that are catchy and relevant
- Colors appropriate for the brand personality
- Typography that fits the brand style
- Clear, actionable brand guidelines

### ❌ If Results Are Generic:

- Make your company description more detailed
- Add more specific values
- Be clear about what makes the company unique
- Try running again (AI generates different results each time)

---

## Troubleshooting

### If Generation Fails:

1. Check backend terminal - is Ollama running?
2. Test Ollama: `ollama list` (should show mistral)
3. Try: `ollama run mistral "Hello"` (test if model works)
4. Check backend logs for errors

### If It Takes Too Long (>2 minutes):

- First generation is slower (model loads)
- Subsequent generations should be faster
- Ollama might be using CPU (slower than GPU)

### If Results Are in Fallback Mode:

- You'll see very simple, template-based results
- This means Ollama isn't responding
- Check if Ollama service is running: `ollama list`

---

## Advanced Testing

### Test Different Industries:

- Healthcare (MedTech startup)
- Finance (Fintech app)
- Education (EdTech platform)
- Gaming (Game development studio)
- Food & Beverage (Restaurant chain)

### Test Different Brand Personalities:

- **Playful**: Gaming, children's products, entertainment
- **Professional**: Banking, legal, consulting
- **Innovative**: Tech startups, AI, blockchain
- **Sustainable**: Eco-friendly, organic, green tech
- **Luxury**: High-end retail, premium services

---

## Expected Response Time

- **First generation**: 45-90 seconds (model loading)
- **Subsequent generations**: 20-40 seconds
- **Fallback mode**: 2-5 seconds (instant)

---

## Sample Output Format

```json
{
  "company_id": "company_1730678400000",
  "brand_name": "CloudSync",
  "logo_prompts": [
    "Modern cloud icon with synchronized arrows...",
    "Abstract geometric shape representing connectivity...",
    "Minimalist cloud symbol with data stream..."
  ],
  "taglines": [
    "Sync Beyond Boundaries",
    "Your Files, Everywhere",
    "Cloud Computing, Simplified"
  ],
  "color_palette": {
    "primary": "#0066CC",
    "secondary": "#00A3E0",
    "accent": "#FF6B35",
    "neutral": "#F5F5F5",
    "text": "#2C3E50"
  },
  "typography": {
    "heading": "Inter",
    "body": "Open Sans",
    "accent": "Poppins"
  },
  "brand_guidelines": "..."
}
```

---

## Next Steps After Testing

1. **Try different company profiles** to see variety
2. **Compare Ollama vs Fallback results** (quality difference)
3. **Experiment with different values and descriptions**
4. **Generate multiple times** for the same company (see variations)
5. **Check what works best** for your use case

---

**Need help?** Check the backend terminal logs for detailed generation information!

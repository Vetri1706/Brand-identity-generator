"""
LLM Fine-tuning Pipeline for Brand Generation
Prepares data and trains models for company-specific branding
"""
import json
import os
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrainingDataPreparator:
    """Prepares training data for LLM fine-tuning"""

    def __init__(self, data_dir: str = "./data/training"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def create_sample_dataset(self) -> None:
        """Create sample training dataset for SaaS and Tech companies"""
        
        logger.info("📊 Creating sample training dataset...")

        sample_data = {
            "tech_companies": [
                {
                    "company": "CloudSync AI",
                    "industry": "AI/ML",
                    "description": "Real-time cloud synchronization with AI",
                    "target_audience": "Enterprise developers",
                    "brand_values": ["Innovation", "Reliability", "Speed"],
                    "generated_logos": [
                        "Minimalist cloud with AI circuit overlay, blue and purple gradient",
                        "Geometric hexagon with synchronized nodes, modern tech aesthetic",
                        "Abstract flowing sync icon with AI particles, sleek design"
                    ],
                    "generated_taglines": [
                        "Sync in Real-Time, Think Ahead",
                        "AI-Powered Synchronization for Modern Teams",
                        "Where Cloud Meets Intelligence"
                    ],
                    "color_palette": {
                        "primary": "#0E63FF",
                        "secondary": "#6C5CE7",
                        "accent": "#00D4FF",
                        "neutral": "#F5F6F7"
                    }
                },
                {
                    "company": "DataVault Security",
                    "industry": "Cybersecurity",
                    "description": "Enterprise data protection and encryption",
                    "target_audience": "Fortune 500 CIOs",
                    "brand_values": ["Security", "Trust", "Compliance"],
                    "generated_logos": [
                        "Locked vault with data streams, dark blue and gold",
                        "Shield with encrypted data patterns, professional look",
                        "Fortress architecture with secure access points"
                    ],
                    "generated_taglines": [
                        "Your Data, Secured by Vault",
                        "Enterprise Security Redefined",
                        "Protect What Matters Most"
                    ],
                    "color_palette": {
                        "primary": "#1E3A5F",
                        "secondary": "#2E5090",
                        "accent": "#FFB800",
                        "neutral": "#FFFFFF"
                    }
                },
                {
                    "company": "PayFlow Pro",
                    "industry": "FinTech",
                    "description": "Payments platform for global transactions",
                    "target_audience": "SMB and Enterprise merchants",
                    "brand_values": ["Simplicity", "Speed", "Global"],
                    "generated_logos": [
                        "Flowing payment wave with upward arrow, vibrant green",
                        "Connected nodes forming payment path, modern geometric",
                        "Minimalist cash flow symbol, clean and professional"
                    ],
                    "generated_taglines": [
                        "Payments That Flow",
                        "Global Transactions Made Simple",
                        "Fast, Secure, Everywhere"
                    ],
                    "color_palette": {
                        "primary": "#00A854",
                        "secondary": "#52C41A",
                        "accent": "#FAAD14",
                        "neutral": "#F5F5F5"
                    }
                }
            ],
            "branding_patterns": {
                "tech_startups": {
                    "common_values": ["Innovation", "Speed", "Reliability"],
                    "color_preferences": ["Blues", "Purples", "Cyan"],
                    "style_preferences": ["Minimalist", "Geometric", "Modern"],
                    "tone": "Professional with modern edge"
                },
                "saas": {
                    "common_values": ["Simplicity", "Scalability", "Integration"],
                    "color_preferences": ["Blues", "Greens", "Grays"],
                    "style_preferences": ["Clean", "Approachable", "Trustworthy"],
                    "tone": "Friendly professional"
                },
                "fintech": {
                    "common_values": ["Security", "Speed", "Trust"],
                    "color_preferences": ["Blues", "Golds", "Greens"],
                    "style_preferences": ["Professional", "Secure", "Modern"],
                    "tone": "Confident and authoritative"
                }
            }
        }

        # Save sample data
        output_file = self.data_dir / "sample_companies.json"
        with open(output_file, "w") as f:
            json.dump(sample_data, f, indent=2)
        
        logger.info(f"✅ Sample dataset created at {output_file}")
        return sample_data

    def create_training_prompts(self, company_data: Dict) -> List[Dict]:
        """Create training prompts from company data"""
        
        prompts = []
        
        for company in company_data.get("tech_companies", []):
            prompt = {
                "input": f"""
Generate a brand identity for this company:
Name: {company['company']}
Industry: {company['industry']}
Description: {company['description']}
Target Audience: {company['target_audience']}
Brand Values: {', '.join(company['brand_values'])}

Provide:
1. 3 logo description variations
2. 3 tagline options
3. Recommended color palette
4. Typography recommendations
""",
                "expected_output": {
                    "logos": company["generated_logos"],
                    "taglines": company["generated_taglines"],
                    "colors": company["color_palette"]
                }
            }
            prompts.append(prompt)
        
        return prompts

    def save_training_data(self, prompts: List[Dict]) -> None:
        """Save training data in JSONL format (one JSON per line)"""
        
        output_file = self.data_dir / "training_prompts.jsonl"
        
        with open(output_file, "w") as f:
            for prompt in prompts:
                f.write(json.dumps(prompt) + "\n")
        
        logger.info(f"✅ Training data saved to {output_file}")

    def create_evaluation_set(self, num_samples: int = 5) -> List[Dict]:
        """Create evaluation dataset"""
        
        evaluation_data = [
            {
                "company_name": "TechStart Innovations",
                "industry": "AI/ML",
                "expected_style": "Modern, geometric, tech-forward"
            },
            {
                "company_name": "SecureFlow Systems",
                "industry": "Cybersecurity",
                "expected_style": "Professional, trustworthy, secure"
            },
            {
                "company_name": "GrowthScale",
                "industry": "SaaS",
                "expected_style": "Clean, friendly, scalable"
            },
            {
                "company_name": "PaymentHub",
                "industry": "FinTech",
                "expected_style": "Modern, trustworthy, global"
            },
            {
                "company_name": "HealthAI Pro",
                "industry": "HealthTech",
                "expected_style": "Professional, caring, modern"
            }
        ]
        
        output_file = self.data_dir / "evaluation_set.json"
        with open(output_file, "w") as f:
            json.dump(evaluation_data, f, indent=2)
        
        logger.info(f"✅ Evaluation set saved to {output_file}")
        return evaluation_data


class LLMFineTuner:
    """Fine-tunes LLM for specific company types and branding"""

    def __init__(self, model_name: str = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"):
        self.model_name = model_name
        logger.info(f"🤖 Initialized fine-tuner with model: {model_name}")

    def prepare_for_finetuning(self, training_data_path: str) -> Dict:
        """Prepare data for fine-tuning with Together AI or similar service"""
        
        logger.info("📋 Preparing data for fine-tuning...")
        
        with open(training_data_path, "r") as f:
            lines = f.readlines()
        
        total_examples = len(lines)
        logger.info(f"✅ Found {total_examples} training examples")
        
        return {
            "model": self.model_name,
            "training_examples": total_examples,
            "data_file": training_data_path,
            "prepared_at": datetime.now().isoformat(),
            "recommended_params": {
                "learning_rate": 2e-5,
                "epochs": 3,
                "batch_size": 8,
                "warmup_steps": 500,
                "weight_decay": 0.01,
            }
        }

    def get_finetuning_guide(self) -> str:
        """Get instructions for fine-tuning via Together AI"""
        
        guide = """
# Together AI Fine-tuning Guide

## Step 1: Prepare Your Data
- Data should be in JSONL format (one JSON per line)
- Each line should contain: {"prompt": "...", "completion": "..."}

## Step 2: Upload to Together AI
```bash
curl -X POST https://api.together.xyz/v1/fine-tunes \\
  -H "Authorization: Bearer $TOGETHER_API_KEY" \\
  -F "training_file=@training_prompts.jsonl" \\
  -F "model=NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
```

## Step 3: Monitor Training
```bash
curl https://api.together.xyz/v1/fine-tunes/{job_id} \\
  -H "Authorization: Bearer $TOGETHER_API_KEY"
```

## Step 4: Use Fine-tuned Model
Your fine-tuned model will be available as:
`together-ft-{job_id}`

## Estimated Costs:
- Training: ~$10-50 depending on data size
- Inference: Similar to base model pricing

## Expected Improvements:
- 15-30% better accuracy on company branding
- More consistent style recommendations
- Faster generation for familiar company types
"""
        return guide


class TrainingOrchestrator:
    """Orchestrates the complete training pipeline"""

    def __init__(self):
        self.preparator = TrainingDataPreparator()
        self.finetuner = LLMFineTuner()

    def run_full_pipeline(self) -> Dict:
        """Run complete training pipeline"""
        
        logger.info("🚀 Starting full training pipeline...")
        
        # Step 1: Create sample dataset
        sample_data = self.preparator.create_sample_dataset()
        
        # Step 2: Create training prompts
        prompts = self.preparator.create_training_prompts(sample_data)
        
        # Step 3: Save training data
        self.preparator.save_training_data(prompts)
        
        # Step 4: Create evaluation set
        self.preparator.create_evaluation_set()
        
        # Step 5: Prepare for fine-tuning
        prep_result = self.finetuner.prepare_for_finetuning(
            "./data/training/training_prompts.jsonl"
        )
        
        # Step 6: Get fine-tuning guide
        guide = self.finetuner.get_finetuning_guide()
        
        logger.info("✅ Training pipeline completed successfully!")
        logger.info("\n" + guide)
        
        return {
            "status": "completed",
            "sample_data_created": True,
            "training_prompts_created": len(prompts),
            "fine_tuning_preparation": prep_result,
            "guide": guide
        }


def main():
    """Main entry point"""
    orchestrator = TrainingOrchestrator()
    result = orchestrator.run_full_pipeline()
    
    print("\n" + "="*60)
    print("TRAINING PIPELINE SUMMARY")
    print("="*60)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()

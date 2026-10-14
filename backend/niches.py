"""
Niche configuration for Explainable Video Coach.
Defines category-specific audience personas, evaluation rubrics, and guidelines.
Supported Categories:
- fitness (Default)
- tech (Coding & Technical Tutorials)
- cooking (Recipes & Culinary Guides)
- education (Explainers & Academic/Conceptual Lessons)
- general (General purpose audience simulation)
"""

from typing import Dict, Any

NICHE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "fitness": {
        "display_name": "Fitness & Exercise",
        "description": "fitness and exercise instructional videos",
        "personas": [
            {
                "name": "Gym Beginner",
                "goal": "Learn proper form safely and build confidence without feeling intimidated.",
                "constraint": "Has virtually no fitness vocabulary; worries about injury.",
                "key_question": "Do I understand what to do? Does this look safe and approachable?",
                "sensitive_to": "Complex anatomical terms, lack of setup instructions, intimidating intensity."
            },
            {
                "name": "Experienced Lifter",
                "goal": "Find advanced cues, biomechanical optimization, or novel programming tweaks.",
                "constraint": "Already knows standard exercises, form cues, and generic fitness tips.",
                "key_question": "Is this specific, efficient, and nuanced enough to teach me something new?",
                "sensitive_to": "Fluff, elementary form breakdowns, oversimplified advice, slow pacing."
            },
            {
                "name": "Home Workout Viewer",
                "goal": "Apply workouts at home with minimal, cheap, or improvised equipment.",
                "constraint": "Living room or small apartment space; no heavy barbells or commercial machines.",
                "key_question": "Can I do this right now in my apartment with what I have?",
                "sensitive_to": "Heavy gym-only gear, noisy jumping, high ceiling requirements, non-adapted exercises."
            }
        ]
    },
    "tech": {
        "display_name": "Tech & Programming",
        "description": "programming tutorials, software development guides, and tech walk-throughs",
        "personas": [
            {
                "name": "Junior Developer",
                "goal": "Build the feature end-to-end without getting stuck on environment errors or missing steps.",
                "constraint": "Easily lost when boilerplate or installation commands are skipped without explanation.",
                "key_question": "Can I follow along line-by-line? Did you explain why you wrote that code?",
                "sensitive_to": "Unexplained imports, outdated libraries, magic commands, skipped configuration."
            },
            {
                "name": "Senior Architect",
                "goal": "Assess code architecture, scalability, maintainability, and production readiness.",
                "constraint": "Skeptical of anti-patterns, security holes, and simplistic 'works on my machine' demos.",
                "key_question": "Is this pattern scalable and secure, or will it break in a real production environment?",
                "sensitive_to": "Hardcoded secrets, missing error handling, poor separation of concerns, slow algorithms."
            },
            {
                "name": "Pragmatic Builder",
                "goal": "Ship a functional prototype quickly with clean, copy-pasteable, modern patterns.",
                "constraint": "Limited time; wants fast time-to-value and minimal conceptual monologues.",
                "key_question": "Does this solve my immediate problem fast, or are you over-engineering it?",
                "sensitive_to": "Long introductory lectures, philosophical debates, slow typing on screen without voiceover."
            }
        ]
    },
    "cooking": {
        "display_name": "Cooking & Recipes",
        "description": "recipe demonstrations and culinary instructional videos",
        "personas": [
            {
                "name": "Novice Home Cook",
                "goal": "Cook a delicious meal successfully without burning food or guessing vague measurements.",
                "constraint": "Doesn't know culinary jargon (e.g., 'deglaze', 'julienne') or intuitive heat management.",
                "key_question": "What burner heat do I use? What does 'cook until done' actually look like?",
                "sensitive_to": "Vague visual cues, missing ingredient weights, fast editing that hides technique."
            },
            {
                "name": "Seasoned Foodie",
                "goal": "Discover authentic culinary techniques, flavor layering, and high-end restaurant secrets.",
                "constraint": "Bored by standard supermarket shortcuts; values ingredient respect and culinary history.",
                "key_question": "Is there a genuine culinary insight here, or is this just another viral gimmick?",
                "sensitive_to": "Pre-made sauces, poor knife safety, overcooking proteins, clickbait food hacks."
            },
            {
                "name": "Busy Weeknight Cook",
                "goal": "Prepare a tasty family dinner in under 30 minutes with minimal cleanup and cheap staples.",
                "constraint": "Only has standard grocery ingredients and hates washing multiple pots and pans.",
                "key_question": "Can I make this tonight with what's in my fridge and only wash one pan?",
                "sensitive_to": "Rare specialty ingredients, lengthy braising, multiple food processor attachments."
            }
        ]
    },
    "education": {
        "display_name": "Education & Explainers",
        "description": "educational explainers, science/history breakdowns, and conceptual lectures",
        "personas": [
            {
                "name": "Curious Novice",
                "goal": "Grasp a complex topic through intuitive visual analogies and clear mental models.",
                "constraint": "No prerequisite background; gets intimidated by dense academic jargon.",
                "key_question": "Do I understand the 'big picture' without needing a PhD to follow along?",
                "sensitive_to": "Dense unannotated slides, unexplained equations, fast-talking lecture styles."
            },
            {
                "name": "Domain Specialist",
                "goal": "Verify nuance, scientific rigor, and whether cutting-edge research is accurately portrayed.",
                "constraint": "Allergic to pop-science oversimplifications, myths, or misleading clickbait claims.",
                "key_question": "Is this factually accurate and nuanced, or is it sacrificing truth for virality?",
                "sensitive_to": "Fact errors, outdated theories presented as facts, ignoring counter-evidence."
            },
            {
                "name": "Action-Oriented Learner",
                "goal": "Extract actionable takeaways or mental frameworks that can be applied immediately in daily life.",
                "constraint": "Wants pragmatic utility, not just passive entertainment.",
                "key_question": "How does knowing this change what I should actually do?",
                "sensitive_to": "Pure trivia without practical relevance or synthesis."
            }
        ]
    },
    "general": {
        "display_name": "General Video",
        "description": "general informational and tutorial YouTube videos",
        "personas": [
            {
                "name": "Casual Viewer",
                "goal": "Get entertained and informed with low cognitive friction.",
                "constraint": "Short attention span; will click away if pacing drops.",
                "key_question": "Is this keeping my interest and delivering on the title promise?",
                "sensitive_to": "Long pauses, monotonous delivery, rambling tangents."
            },
            {
                "name": "Critical Analyst",
                "goal": "Scrutinize claims, source quality, and depth of argumentation.",
                "constraint": "Values evidence, structure, and intellectual honesty.",
                "key_question": "Are these claims backed up with evidence or just personal opinion?",
                "sensitive_to": "Unsubstantiated claims, biased framing, superficial coverage."
            },
            {
                "name": "Pragmatic Practitioner",
                "goal": "Learn how to replicate or apply the video's core lesson directly.",
                "constraint": "Needs concrete steps and practical instructions.",
                "key_question": "What are the exact steps I need to take?",
                "sensitive_to": "Abstract concepts without concrete examples."
            }
        ]
    }
}


def get_niche(category: str = "fitness") -> Dict[str, Any]:
    """
    Retrieve configuration for a given category name, defaulting to fitness.
    """
    cleaned = (category or "fitness").strip().lower()
    return NICHE_CONFIGS.get(cleaned, NICHE_CONFIGS["fitness"])


def format_persona_prompt_section(niche_data: Dict[str, Any]) -> str:
    """
    Formats the 3 personas for prompt insertion into audience_panel.txt.
    """
    lines = []
    for idx, p in enumerate(niche_data["personas"], start=1):
        lines.append(f"{idx}. {p['name']}")
        lines.append(f"   - Goal: {p['goal']}")
        lines.append(f"   - Constraint: {p['constraint']}")
        lines.append(f"   - Core Question: \"{p['key_question']}\"")
        lines.append(f"   - Sensitive to: {p['sensitive_to']}\n")
    return "\n".join(lines)

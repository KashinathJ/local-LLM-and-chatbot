"""
Recipe Intelligence Chatbot - Utilities.
Few-shot prompting dataset and LLM invocation helpers.
"""

from src.models import Recipe

# High-quality few-shot recipe examples to guide LLM style (simulated fine-tuning via prompting)
FEW_SHOT_RECIPES: list[dict] = [
    {
        "name": "Classic French Omelette",
        "ingredients": ["3 large eggs", "1 tbsp butter", "Salt and pepper to taste", "1 tbsp fresh chives"],
        "steps": [
            "Beat eggs with salt and pepper until just combined.",
            "Melt butter in non-stick pan over medium-low heat.",
            "Pour in eggs and let set slightly, then gently push cooked edges toward center.",
            "When mostly set but still glossy, fold one third over, then roll onto plate. Garnish with chives.",
        ],
        "prep_time_minutes": 8,
        "calories": 220,
    },
    {
        "name": "Caramelized Onion and Egg Scramble",
        "ingredients": ["4 eggs", "2 medium onions, sliced", "2 tbsp olive oil", "Salt", "Black pepper", "Fresh parsley"],
        "steps": [
            "Heat olive oil in a skillet. Add onions and cook over medium-low heat, stirring occasionally, until golden and caramelized (about 20 minutes).",
            "In a bowl, whisk eggs with salt and pepper.",
            "Push onions to one side, add a little more oil if needed, and pour in eggs.",
            "Scramble gently until set but still soft. Fold in onions, garnish with parsley, and serve.",
        ],
        "prep_time_minutes": 28,
        "calories": 320,
    },
    {
        "name": "Tomato Basil Pasta",
        "ingredients": ["400g spaghetti", "4 ripe tomatoes", "3 cloves garlic", "Fresh basil", "Olive oil", "Parmesan", "Salt and pepper"],
        "steps": [
            "Boil salted water and cook pasta until al dente. Reserve 1/2 cup pasta water.",
            "Dice tomatoes and mince garlic. Tear basil leaves.",
            "Sauté garlic in olive oil until fragrant. Add tomatoes, salt, and pepper; cook 5 minutes.",
            "Toss drained pasta with sauce, adding pasta water as needed. Top with basil and Parmesan.",
        ],
        "prep_time_minutes": 25,
        "calories": 450,
    },
    {
        "name": "Garlic Butter Shrimp",
        "ingredients": ["500g shrimp", "4 tbsp butter", "4 cloves garlic", "Lemon juice", "Parsley", "Salt and pepper"],
        "steps": [
            "Pat shrimp dry and season with salt and pepper.",
            "Melt butter in a large skillet over medium-high. Add minced garlic; cook 30 seconds.",
            "Add shrimp in a single layer; cook 2 minutes per side until pink.",
            "Remove from heat. Add lemon juice and parsley. Serve immediately.",
        ],
        "prep_time_minutes": 15,
        "calories": 280,
    },
    {
        "name": "Chicken Stir-Fry with Vegetables",
        "ingredients": ["400g chicken breast", "2 cups mixed vegetables", "2 tbsp soy sauce", "1 tbsp sesame oil", "Ginger", "Garlic", "Rice"],
        "steps": [
            "Slice chicken and vegetables. Mince ginger and garlic.",
            "Heat sesame oil in a wok. Stir-fry chicken until cooked; set aside.",
            "Stir-fry vegetables and ginger-garlic until tender-crisp.",
            "Return chicken, add soy sauce, toss. Serve over rice.",
        ],
        "prep_time_minutes": 30,
        "calories": 380,
    },
    {
        "name": "Creamy Avocado Toast",
        "ingredients": ["2 slices sourdough", "1 ripe avocado", "Lime juice", "Salt", "Red pepper flakes", "2 poached eggs"],
        "steps": [
            "Toast bread until golden.",
            "Mash avocado with lime juice and salt. Spread on toast.",
            "Top with poached eggs, red pepper flakes, and extra salt if desired.",
        ],
        "prep_time_minutes": 12,
        "calories": 350,
    },
    {
        "name": "Lentil Soup",
        "ingredients": ["1 cup red lentils", "1 onion", "2 carrots", "3 cups vegetable broth", "Cumin", "Turmeric", "Lemon"],
        "steps": [
            "Dice onion and carrots. Rinse lentils.",
            "Sauté onion and carrots in oil. Add cumin and turmeric; cook 1 minute.",
            "Add lentils and broth. Simmer 20 minutes until lentils are tender.",
            "Blend partially if desired. Season with salt and lemon juice.",
        ],
        "prep_time_minutes": 35,
        "calories": 220,
    },
    {
        "name": "Greek Salad",
        "ingredients": ["Cucumber", "Tomatoes", "Red onion", "Kalamata olives", "Feta cheese", "Olive oil", "Oregano", "Lemon"],
        "steps": [
            "Chop cucumber and tomatoes. Thinly slice red onion.",
            "Combine vegetables with olives and cubed feta in a bowl.",
            "Dress with olive oil, lemon juice, oregano, salt, and pepper. Toss and serve.",
        ],
        "prep_time_minutes": 15,
        "calories": 250,
    },
    {
        "name": "Honey Garlic Salmon",
        "ingredients": ["2 salmon fillets", "3 tbsp honey", "3 cloves garlic", "Soy sauce", "Rice vinegar", "Sesame seeds", "Green onions"],
        "steps": [
            "Mix honey, minced garlic, soy sauce, and rice vinegar for the glaze.",
            "Season salmon. Pan-sear skin-side down until crisp; flip and cook until done.",
            "Pour glaze over salmon; let it bubble 1–2 minutes. Garnish with sesame seeds and green onions.",
        ],
        "prep_time_minutes": 22,
        "calories": 420,
    },
    {
        "name": "Mushroom Risotto",
        "ingredients": ["1.5 cups Arborio rice", "300g mushrooms", "1 onion", "White wine", "Vegetable broth", "Parmesan", "Butter"],
        "steps": [
            "Slice mushrooms. Dice onion. Heat broth in a separate pot.",
            "Sauté onion in butter; add rice and toast 2 minutes. Add wine; stir until absorbed.",
            "Add broth one ladle at a time, stirring until absorbed. Halfway through, add mushrooms.",
            "When rice is creamy and tender, stir in Parmesan and butter. Season and serve.",
        ],
        "prep_time_minutes": 45,
        "calories": 480,
    },
    {
        "name": "Spicy Egg and Potato Hash",
        "ingredients": ["4 eggs", "2 medium potatoes", "1 onion", "Bell pepper", "Paprika", "Cumin", "Salt", "Oil"],
        "steps": [
            "Dice potatoes and onion. Dice bell pepper.",
            "Pan-fry potatoes in oil until golden and tender. Add onion and pepper; cook until soft.",
            "Season with paprika, cumin, and salt. Make wells in the hash and crack in eggs.",
            "Cover and cook until eggs are set. Serve with hot sauce if desired.",
        ],
        "prep_time_minutes": 35,
        "calories": 340,
    },
]


def get_few_shot_examples_text() -> str:
    """Format few-shot examples as text for the system or user prompt."""
    lines = []
    for i, r in enumerate(FEW_SHOT_RECIPES[:5], 1):  # Use 5 for prompt length
        lines.append(f"Example {i}: {r['name']}")
        lines.append(f"  Ingredients: {', '.join(r['ingredients'])}")
        lines.append(f"  Steps: {' | '.join(r['steps'])}")
        lines.append(f"  Prep: {r['prep_time_minutes']} min, Calories: {r['calories']}")
        lines.append("")
    return "\n".join(lines).strip()


def get_chef_system_prompt() -> str:
    """Chef Persona system prompt that enforces valid JSON recipe output."""
    examples = get_few_shot_examples_text()
    return f"""You are an expert Chef and Recipe Intelligence Assistant. Your role is to generate a single, complete recipe based ONLY on the ingredients the user provides. You must be creative and professional.

Rules:
- Use ONLY the ingredients given by the user. You may add minimal pantry staples (salt, pepper, oil, water) only if necessary.
- Output MUST be a valid JSON object with exactly these fields: name (string), ingredients (list of strings with quantities), steps (list of strings, clear and ordered), prep_time_minutes (integer, 1-480), calories (integer, 0-5000).
- Recipe name should be descriptive and appetizing.
- Steps must be clear, numbered in logic order, and actionable.
- Estimate prep_time_minutes and calories realistically.

Style examples (for format and quality only):
{examples}

Respond with ONLY the recipe as a single valid JSON object. No markdown, no extra text.
Example shape: {"name": "Dish Name", "ingredients": ["1 cup flour", "2 eggs"], "steps": ["Step 1.", "Step 2."], "prep_time_minutes": 25, "calories": 300}"""

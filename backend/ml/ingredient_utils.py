import re


# ==========================================
# INGREDIENT SYNONYMS
# ==========================================

SYNONYMS = {

    # Potato
    "aloo": "potato",
    "alu": "potato",
    "potatoes": "potato",

    # Onion
    "pyaz": "onion",
    "pyaaz": "onion",
    "onions": "onion",

    # Tomato
    "tamatar": "tomato",
    "tomatoes": "tomato",

    # Peas
    "matar": "peas",
    "green peas": "peas",

    # Carrot
    "gajar": "carrot",
    "carrots": "carrot",

    # Bell Pepper
    "shimla mirch": "bell pepper",
    "capsicum": "bell pepper",
    "bell peppers": "bell pepper",

    # Milk
    "doodh": "milk",

    # Butter
    "makhan": "butter",

    # Garlic
    "lahsun": "garlic",
    "garlic clove": "garlic",
    "garlic cloves": "garlic",

    # Ginger
    "adrak": "ginger",
    "gingerroot": "ginger",
    "ginger root": "ginger",

    # Coriander
    "cilantro": "coriander",
    "coriander leaves": "coriander",
    "fresh coriander": "coriander",

    # Paneer
    "paneer": "paneer"
}


# ==========================================
# NORMALIZE INGREDIENT
# ==========================================

def normalize_ingredient(ingredient):

    if not isinstance(ingredient, str):
        return ""

    ingredient = ingredient.lower().strip()

    # Remove extra spaces
    ingredient = re.sub(
        r"\s+",
        " ",
        ingredient
    )

    # Direct synonym replacement
    if ingredient in SYNONYMS:

        return SYNONYMS[ingredient]

    return ingredient


# ==========================================
# PARSE RECIPE INGREDIENTS
# ==========================================

def parse_ingredients(ingredient_text):

    if not isinstance(
        ingredient_text,
        str
    ):
        return []

    ingredient_text = (
        ingredient_text.strip()
    )

    # Remove c(...)
    if ingredient_text.startswith("c("):

        ingredient_text = (
            ingredient_text[2:-1]
        )

    # Split ingredients
    ingredients = (
        ingredient_text.split(",")
    )

    # Normalize every ingredient
    ingredients = [

        normalize_ingredient(
            ingredient
        )

        for ingredient in ingredients

        if ingredient.strip()
    ]

    return ingredients


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    test_ingredients = [

        "aloo",
        "pyaz",
        "tamatar",
        "matar",
        "garlic cloves",
        "garlic clove",
        "gingerroot",
        "cilantro",
        "capsicum"
    ]

    print("\nOriginal:")
    print(test_ingredients)

    normalized = [

        normalize_ingredient(
            ingredient
        )

        for ingredient in test_ingredients
    ]

    print("\nNormalized:")
    print(normalized)


    # Test recipe
    test_recipe = (
        "c("
        "potato, "
        "onion, "
        "tomato, "
        "green peas, "
        "garlic cloves, "
        "gingerroot, "
        "cilantro, "
        "salt"
        ")"
    )

    print("\nRecipe ingredients:")

    print(
        parse_ingredients(
            test_recipe
        )
    )
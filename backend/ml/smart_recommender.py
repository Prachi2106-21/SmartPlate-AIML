import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ml.ingredient_utils import normalize_ingredient, parse_ingredients

DATA_PATH = "../dataset/cleaned_recipes.csv"

MAX_FEATURES = 2000
TFIDF_TRAIN_SIZE = 100000
TFIDF_BATCH_SIZE = 5000
DEFAULT_TOP_N = 5

LOW_CALORIE_LIMIT = 174.2
HIGH_PROTEIN_MINIMUM = 25.0
HIGH_PROTEIN_TARGET = 50.0
LOW_CARB_LIMIT = 12.8

PANTRY_INGREDIENTS = {
    "salt", "black pepper", "pepper", "water", "oil",
    "vegetable oil", "canola oil", "olive oil",
    "extra virgin olive oil", "cooking oil",
    "sugar", "brown sugar", "cumin", "cumin seed",
    "cumin seeds", "ground cumin", "turmeric",
    "turmeric powder", "ground turmeric", "coriander",
    "coriander powder", "ground coriander", "chili powder",
    "red chili powder", "cayenne pepper", "garam masala",
    "garam masala powder", "ginger", "ginger paste",
    "garlic", "garlic flakes", "garlic powder",
    "green chili", "green chilies", "green chili peppers",
    "bay leaf", "bay leaves", "cinnamon", "cardamom",
    "cardamoms", "lemon juice"
}

NON_VEGETARIAN = [
    "chicken", "beef", "pork", "lamb", "mutton", "veal",
    "turkey", "goat", "venison", "duck", "rabbit",
    "buffalo", "bison", "fish", "salmon", "tuna", "cod",
    "tilapia", "trout", "haddock", "sardine", "anchovy",
    "mackerel", "catfish", "halibut", "bass", "herring",
    "pollock", "mahi mahi", "sea bass", "white fish",
    "shrimp", "prawn", "crab", "lobster", "clam", "oyster",
    "mussel", "squid", "octopus", "shellfish", "seafood",
    "bacon", "ham", "sausage", "pepperoni", "salami",
    "prosciutto", "pastrami", "meat", "steak", "mince",
    "minced meat", "ground beef", "ground turkey",
    "ground chicken", "egg", "eggs", "egg white",
    "egg whites", "egg yolk", "egg yolks", "boiled egg",
    "fried egg", "scrambled egg", "hard boiled egg",
    "poached egg", "omelette", "omelet"
]

NON_VEGAN = NON_VEGETARIAN + [
    "milk", "whole milk", "skim milk", "cream", "heavy cream",
    "half and half", "cheese", "cheddar", "parmesan",
    "mozzarella", "swiss cheese", "cream cheese", "butter",
    "ghee", "yogurt", "yoghurt", "curd", "paneer",
    "cottage cheese", "whey", "casein", "mayonnaise",
    "condensed milk", "evaporated milk", "buttermilk"
]

CUISINE_ALIASES = {
    "Indian": [
        "indian", "india", "punjabi", "south indian",
        "north indian", "mughlai", "bengali", "gujarati",
        "rajasthani", "maharashtrian", "hyderabadi",
        "kashmiri", "kerala", "tamil", "andhra", "goan",
        "sindhi"
    ],
    "Italian": [
        "italian", "italy", "sicilian", "tuscan", "roman"
    ],
    "Mexican": [
        "mexican", "mexico", "tex mex"
    ],
    "Chinese": [
        "chinese", "china", "szechuan", "sichuan", "cantonese"
    ],
    "Thai": [
        "thai", "thailand"
    ],
    "Mediterranean": [
        "mediterranean", "greek", "lebanese", "turkish"
    ],
    "American": [
        "american", "usa", "southern"
    ]
}

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded!")
print("Total recipes:", len(df))

TEXT_COLUMNS = [
    "Name",
    "RecipeIngredientParts",
    "Keywords",
    "RecipeCategory"
]

for column in TEXT_COLUMNS:
    if column not in df.columns:
        df[column] = ""

    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
    )

NUTRITION_COLUMNS = [
    "Calories",
    "ProteinContent",
    "CarbohydrateContent",
    "FatContent"
]

for column in NUTRITION_COLUMNS:
    if column not in df.columns:
        df[column] = 0

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)

print("Processing ingredients...")

df["parsed_ingredients"] = (
    df["RecipeIngredientParts"]
    .apply(parse_ingredients)
)

def normalize_recipe_ingredients(items):
    result = []

    for item in items:
        item = str(item).strip().lower()

        if not item:
            continue

        value = normalize_ingredient(item)

        if value:
            result.append(value)

    return list(dict.fromkeys(result))

df["parsed_ingredients"] = (
    df["parsed_ingredients"]
    .apply(normalize_recipe_ingredients)
)

df["ingredient_text"] = (
    df["parsed_ingredients"]
    .apply(lambda x: " ".join(x))
)

df["search_text"] = (
    df["Name"]
    + " "
    + df["RecipeCategory"]
    + " "
    + df["Keywords"]
    + " "
    + df["ingredient_text"]
)

print("Creating memory-safe TF-IDF model...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=MAX_FEATURES,
    ngram_range=(1, 1),
    min_df=2,
    dtype=np.float32,
    sublinear_tf=True
)

if len(df) > TFIDF_TRAIN_SIZE:
    tfidf_training_data = (
        df["search_text"]
        .sample(
            n=TFIDF_TRAIN_SIZE,
            random_state=42
        )
    )
else:
    tfidf_training_data = df["search_text"]

print(
    "TF-IDF training documents:",
    len(tfidf_training_data)
)

vectorizer.fit(tfidf_training_data)

print("TF-IDF model created!")

print(
    "Vocabulary size:",
    len(vectorizer.vocabulary_)
)

def clean_text(value):
    if pd.isna(value):
        return ""

    return str(value).lower().strip()

def build_recipe_text(row):
    return " ".join([
        clean_text(row.get("Name", "")),
        clean_text(row.get("RecipeIngredientParts", "")),
        clean_text(row.get("Keywords", "")),
        clean_text(row.get("RecipeCategory", "")),
        clean_text(row.get("ingredient_text", ""))
    ])

def contains_forbidden_term(
    text,
    forbidden_terms
):
    text = clean_text(text)

    for term in forbidden_terms:
        term = clean_text(term)

        if not term:
            continue

        if " " in term:
            if term in text:
                return True

        else:
            pattern = rf"\b{re.escape(term)}\b"

            if re.search(pattern, text):
                return True

    return False

def is_recipe_allowed(row, diet):
    if not diet:
        return True

    diet = diet.lower().strip()

    if diet == "all":
        return True

    recipe_text = build_recipe_text(row)

    if diet == "vegetarian":
        return not contains_forbidden_term(
            recipe_text,
            NON_VEGETARIAN
        )

    if diet == "vegan":
        return not contains_forbidden_term(
            recipe_text,
            NON_VEGAN
        )

    return True

def normalize_user_ingredients(
    user_ingredients
):
    result = []

    for ingredient in user_ingredients:
        if not ingredient:
            continue

        value = (
            str(ingredient)
            .strip()
            .lower()
        )

        value = normalize_ingredient(value)

        if value:
            result.append(value)

    return list(dict.fromkeys(result))

def ingredient_matches(
    user_ingredient,
    recipe_ingredient
):
    user = clean_text(user_ingredient)
    recipe = clean_text(recipe_ingredient)

    if not user or not recipe:
        return False

    if user == recipe:
        return True

    if user in recipe:
        return True

    if recipe in user:
        return True

    if user.rstrip("s") == recipe.rstrip("s"):
        return True

    return False

def calculate_ingredient_details(
    user_ingredients,
    recipe_ingredients
):
    matched = []
    missing = []
    used_indexes = set()

    for user_ingredient in user_ingredients:

        for index, recipe_ingredient in enumerate(
            recipe_ingredients
        ):

            if index in used_indexes:
                continue

            if ingredient_matches(
                user_ingredient,
                recipe_ingredient
            ):
                matched.append(
                    user_ingredient
                )

                used_indexes.add(index)

                break

    for index, recipe_ingredient in enumerate(
        recipe_ingredients
    ):

        if index not in used_indexes:
            missing.append(
                recipe_ingredient
            )

    matched_count = len(matched)
    user_count = len(user_ingredients)
    recipe_count = len(recipe_ingredients)

    if user_count:
        user_coverage = (
            matched_count
            / user_count
        ) * 100
    else:
        user_coverage = 0

    if recipe_count:
        recipe_coverage = (
            matched_count
            / recipe_count
        ) * 100
    else:
        recipe_coverage = 0

    return (
        matched,
        missing,
        user_coverage,
        recipe_coverage
    )

def get_core_missing_ingredients(
    missing
):
    result = []

    for ingredient in missing:

        ingredient = clean_text(
            ingredient
        )

        if ingredient not in PANTRY_INGREDIENTS:
            result.append(
                ingredient
            )

    return result

def calculate_practicality_score(
    matched_count,
    user_count,
    recipe_count,
    core_missing_count
):
    if user_count == 0:
        return 0

    user_coverage = (
        matched_count
        / user_count
    ) * 100

    effective_recipe_count = min(
        recipe_count,
        12
    )

    if effective_recipe_count:
        recipe_coverage = (
            matched_count
            / effective_recipe_count
        ) * 100
    else:
        recipe_coverage = 0

    recipe_coverage = min(
        recipe_coverage,
        100
    )

    if core_missing_count == 0:
        missing_score = 100

    elif core_missing_count == 1:
        missing_score = 85

    elif core_missing_count == 2:
        missing_score = 70

    elif core_missing_count == 3:
        missing_score = 55

    elif core_missing_count == 4:
        missing_score = 40

    elif core_missing_count == 5:
        missing_score = 25

    elif core_missing_count == 6:
        missing_score = 15

    else:
        missing_score = 0

    return (
        user_coverage * 0.55
        + recipe_coverage * 0.20
        + missing_score * 0.25
    )

def calculate_cuisine_score(
    row,
    cuisine
):
    if not cuisine:
        return 100

    cuisine = cuisine.strip()

    if cuisine.lower() == "all":
        return 100

    aliases = CUISINE_ALIASES.get(
        cuisine,
        [cuisine.lower()]
    )

    metadata_text = " ".join([
        clean_text(
            row.get("Keywords", "")
        ),
        clean_text(
            row.get("RecipeCategory", "")
        ),
        clean_text(
            row.get("Name", "")
        )
    ])

    for alias in aliases:

        if alias.lower() in metadata_text:
            return 100

    return 0

def calculate_nutrition_score(
    row,
    nutrition
):
    if not nutrition:
        return 100

    nutrition = (
        nutrition
        .lower()
        .strip()
    )

    if nutrition == "all":
        return 100

    calories = float(
        row.get("Calories", 0)
    )

    protein = float(
        row.get("ProteinContent", 0)
    )

    carbs = float(
        row.get(
            "CarbohydrateContent",
            0
        )
    )

    if nutrition == "high protein":

        if protein <= 0:
            return 0

        return min(
            100,
            (
                protein
                / HIGH_PROTEIN_TARGET
            ) * 100
        )

    if nutrition == "low calorie":

        if calories <= 0:
            return 0

        if calories <= LOW_CALORIE_LIMIT:
            return 100

        return max(
            0,
            min(
                100,
                (
                    LOW_CALORIE_LIMIT
                    / calories
                ) * 100
            )
        )

    if nutrition == "low carb":

        if carbs <= 0:
            return 0

        if carbs <= LOW_CARB_LIMIT:
            return 100

        return max(
            0,
            min(
                100,
                (
                    LOW_CARB_LIMIT
                    / carbs
                ) * 100
            )
        )

    return 100

def calculate_batch_similarities(
    user_vector,
    candidate_text
):
    similarities = []

    for start in range(
        0,
        len(candidate_text),
        TFIDF_BATCH_SIZE
    ):

        end = (
            start
            + TFIDF_BATCH_SIZE
        )

        batch = candidate_text[
            start:end
        ]

        batch_matrix = (
            vectorizer.transform(batch)
        )

        batch_similarity = (
            cosine_similarity(
                user_vector,
                batch_matrix
            ).flatten()
        )

        similarities.extend(
            batch_similarity.tolist()
        )

        del batch_matrix
        del batch_similarity

    return np.array(
        similarities,
        dtype=np.float32
    )

def recommend_recipes(
    user_ingredients,
    top_n=DEFAULT_TOP_N,
    cuisine="All",
    diet="All",
    nutrition="All"
):
    normalized_user_ingredients = (
        normalize_user_ingredients(
            user_ingredients
        )
    )

    if not normalized_user_ingredients:
        return pd.DataFrame()

    print()
    print("User ingredients:")
    print(user_ingredients)

    print(
        "Normalized ingredients:",
        normalized_user_ingredients
    )

    candidates = df

    if (
        cuisine
        and cuisine.lower() != "all"
    ):

        cuisine = cuisine.strip()

        aliases = CUISINE_ALIASES.get(
            cuisine,
            [cuisine.lower()]
        )

        pattern = "|".join(
            re.escape(alias)
            for alias in aliases
        )

        keyword_mask = (
            candidates["Keywords"]
            .str.contains(
                pattern,
                case=False,
                na=False,
                regex=True
            )
        )

        category_mask = (
            candidates["RecipeCategory"]
            .str.contains(
                pattern,
                case=False,
                na=False,
                regex=True
            )
        )

        name_mask = (
            candidates["Name"]
            .str.contains(
                pattern,
                case=False,
                na=False,
                regex=True
            )
        )

        candidates = candidates[
            keyword_mask
            | category_mask
            | name_mask
        ]

    if (
        diet
        and diet.lower() != "all"
    ):

        allowed_mask = candidates.apply(
            lambda row:
            is_recipe_allowed(
                row,
                diet
            ),
            axis=1
        )

        candidates = candidates[
            allowed_mask
        ]

    nutrition_lower = (
        nutrition.lower().strip()
        if nutrition
        else "all"
    )

    if nutrition_lower == "high protein":

        candidates = candidates[
            candidates[
                "ProteinContent"
            ] >= HIGH_PROTEIN_MINIMUM
        ]

    elif nutrition_lower == "low calorie":

        candidates = candidates[
            (
                candidates["Calories"] > 0
            )
            &
            (
                candidates["Calories"]
                <= LOW_CALORIE_LIMIT
            )
        ]

    elif nutrition_lower == "low carb":

        candidates = candidates[
            (
                candidates[
                    "CarbohydrateContent"
                ] > 0
            )
            &
            (
                candidates[
                    "CarbohydrateContent"
                ] <= LOW_CARB_LIMIT
            )
        ]

    print(
        "Recipes after filters:",
        len(candidates)
    )

    if candidates.empty:
        return pd.DataFrame()

    user_text = " ".join(
        normalized_user_ingredients
    )

    user_vector = vectorizer.transform(
        [user_text]
    )

    candidate_text = (
        candidates["search_text"]
        .tolist()
    )

    similarities = (
        calculate_batch_similarities(
            user_vector,
            candidate_text
        )
    )

    candidates = candidates.copy()

    candidates["similarity_raw"] = (
        similarities
    )

    candidates = (
        candidates
        .sort_values(
            "similarity_raw",
            ascending=False
        )
        .head(1500)
    )

    results = []

    for index, row in candidates.iterrows():

        recipe_ingredients = list(
            row["parsed_ingredients"]
        )

        if not recipe_ingredients:
            continue

        (
            matched,
            missing,
            user_coverage,
            recipe_coverage
        ) = calculate_ingredient_details(
            normalized_user_ingredients,
            recipe_ingredients
        )

        matched_count = len(matched)

        total_recipe_ingredients = len(
            recipe_ingredients
        )

        missing_count = len(missing)

        if user_coverage < 50:
            continue

        core_missing = (
            get_core_missing_ingredients(
                missing
            )
        )

        core_missing_count = len(
            core_missing
        )

        practicality_score = (
            calculate_practicality_score(
                matched_count,
                len(
                    normalized_user_ingredients
                ),
                total_recipe_ingredients,
                core_missing_count
            )
        )

        ingredient_match_score = (
            user_coverage * 0.70
            + recipe_coverage * 0.30
        )

        similarity_score = (
            float(
                row["similarity_raw"]
            ) * 100
        )

        cuisine_score = (
            calculate_cuisine_score(
                row,
                cuisine
            )
        )

        nutrition_score = (
            calculate_nutrition_score(
                row,
                nutrition
            )
        )

        exact_match_bonus = (
            8
            if matched_count
            == len(
                normalized_user_ingredients
            )
            else 0
        )

        coverage_bonus = (
            8
            if user_coverage >= 100
            else 4
            if user_coverage >= 75
            else 0
        )

        smart_score = (
            ingredient_match_score * 0.30
            + practicality_score * 0.35
            + similarity_score * 0.10
            + cuisine_score * 0.10
            + nutrition_score * 0.05
            + exact_match_bonus
            + coverage_bonus
        )

        results.append({
            "RecipeId": row.get(
                "RecipeId",
                index
            ),
            "Name": row["Name"],
            "Category": row[
                "RecipeCategory"
            ],
            "Calories": row[
                "Calories"
            ],
            "Protein": row[
                "ProteinContent"
            ],
            "Carbs": row[
                "CarbohydrateContent"
            ],
            "Fat": row[
                "FatContent"
            ],
            "AvailableIngredients": (
                ", ".join(matched)
            ),
            "MissingIngredients": (
                ", ".join(missing)
            ),
            "CoreMissingIngredients": (
                ", ".join(core_missing)
            ),
            "MatchedCount": matched_count,
            "TotalRecipeIngredients": (
                total_recipe_ingredients
            ),
            "UserCoverage": round(
                user_coverage,
                2
            ),
            "RecipeCoverage": round(
                recipe_coverage,
                2
            ),
            "MissingCount": missing_count,
            "CoreMissingCount": (
                core_missing_count
            ),
            "PracticalityScore": round(
                practicality_score,
                2
            ),
            "Similarity": round(
                similarity_score,
                2
            ),
            "IngredientMatchScore": round(
                ingredient_match_score,
                2
            ),
            "CuisineScore": round(
                cuisine_score,
                2
            ),
            "NutritionScore": round(
                nutrition_score,
                2
            ),
            "SmartScore": round(
                smart_score,
                2
            )
        })

    result_df = pd.DataFrame(
        results
    )

    if result_df.empty:
        return result_df

    result_df = (
        result_df
        .sort_values(
            by=[
                "SmartScore",
                "MatchedCount",
                "UserCoverage",
                "PracticalityScore",
                "Similarity"
            ],
            ascending=False
        )
    )

    return result_df.head(top_n)


if __name__ == "__main__":

    print()
    print("=" * 50)
    print("          SMARTPLATE AI")
    print("=" * 50)

    user_ingredients = [
        "aloo",
        "pyaz",
        "tamatar",
        "matar"
    ]

    recommendations = recommend_recipes(
        user_ingredients=user_ingredients,
        top_n=5,
        cuisine="Indian",
        diet="Vegetarian",
        nutrition="High Protein"
    )

    print()

    if recommendations.empty:

        print(
            "No suitable recipes found."
        )

    else:

        for _, recipe in recommendations.iterrows():

            print()
            print(
                f"Recipe: {recipe['Name']}"
            )

            print(
                f"Category: {recipe['Category']}"
            )

            print(
                f"Smart Score: "
                f"{recipe['SmartScore']} %"
            )

            print(
                f"AI Similarity: "
                f"{recipe['Similarity']} %"
            )

            print(
                f"Ingredient Match: "
                f"{recipe['IngredientMatchScore']} %"
            )

            print(
                f"Practicality: "
                f"{recipe['PracticalityScore']} %"
            )

            print(
                f"Cuisine Score: "
                f"{recipe['CuisineScore']} %"
            )

            print(
                f"Nutrition Score: "
                f"{recipe['NutritionScore']} %"
            )

            print(
                f"User Coverage: "
                f"{recipe['UserCoverage']} %"
            )

            print(
                f"Recipe Coverage: "
                f"{recipe['RecipeCoverage']} %"
            )

            print(
                f"Matched: "
                f"{recipe['MatchedCount']} / "
                f"{len(user_ingredients)}"
            )

            print(
                f"Total Ingredients: "
                f"{recipe['TotalRecipeIngredients']}"
            )

            print(
                f"Available: "
                f"{recipe['AvailableIngredients']}"
            )

            print(
                f"Missing: "
                f"{recipe['MissingIngredients']}"
            )

            print(
                f"Core Missing: "
                f"{recipe['CoreMissingIngredients']}"
            )

            print(
                f"Calories: "
                f"{recipe['Calories']}"
            )

            print(
                f"Protein: "
                f"{recipe['Protein']}"
            )

            print(
                f"Carbs: "
                f"{recipe['Carbs']}"
            )

            print(
                f"Fat: "
                f"{recipe['Fat']}"
            )

            print("-" * 50)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ingredient_utils import normalize_ingredient, parse_ingredients


# =========================================================
# 1. LOAD DATASET
# =========================================================

DATA_PATH = "../dataset/cleaned_recipes.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded!")
print("Total recipes:", len(df))


# =========================================================
# 2. BASIC CLEANING
# =========================================================

for col in [
    "RecipeIngredientParts",
    "Keywords",
    "RecipeCategory",
    "Name"
]:
    df[col] = df[col].fillna("").astype(str)


# Nutrition columns
nutrition_columns = [
    "Calories",
    "ProteinContent",
    "CarbohydrateContent",
    "FatContent"
]

for col in nutrition_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)


# =========================================================
# 3. INGREDIENT PROCESSING
# =========================================================

print("Processing ingredients...")

df["parsed_ingredients"] = df["RecipeIngredientParts"].apply(
    parse_ingredients
)

df["ingredient_text"] = df["parsed_ingredients"].apply(
    lambda x: " ".join(x)
)


# =========================================================
# 4. CREATE SEARCH TEXT
# =========================================================

# Combine multiple recipe fields.
# This improves semantic matching.

df["search_text"] = (
    df["Name"]
    + " "
    + df["RecipeCategory"]
    + " "
    + df["Keywords"]
    + " "
    + df["ingredient_text"]
)


# =========================================================
# 5. TF-IDF MODEL
# =========================================================

print("Creating TF-IDF model...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(
    df["search_text"]
)

print("TF-IDF model created!")
print("Matrix shape:", tfidf_matrix.shape)


# =========================================================
# 6. NON-VEGETARIAN INGREDIENTS / TERMS
# =========================================================

NON_VEGETARIAN = [
    "chicken",
    "beef",
    "pork",
    "lamb",
    "mutton",
    "veal",
    "turkey",

    "fish",
    "salmon",
    "tuna",
    "cod",
    "tilapia",
    "trout",
    "haddock",

    "shrimp",
    "prawn",
    "crab",
    "lobster",

    "bacon",
    "ham",
    "sausage",
    "pepperoni",

    "anchovy",
    "sardine",

    "meat",
    "steak",
    "mince",
    "minced meat",
    "ground beef",
    "ground turkey",
    "ground chicken",

    "gelatin"
]


# =========================================================
# 7. VEGAN EXCLUSIONS
# =========================================================

NON_VEGAN = NON_VEGETARIAN + [
    "egg",
    "eggs",
    "milk",
    "cream",
    "cheese",
    "butter",
    "yogurt",
    "yoghurt",
    "ghee",
    "whey",
    "casein",
    "mayonnaise"
]


# =========================================================
# 8. THRESHOLDS
# =========================================================

LOW_CALORIE_LIMIT = 174.2
HIGH_PROTEIN_LIMIT = 25.0
LOW_CARB_LIMIT = 12.8


# =========================================================
# 9. HELPER FUNCTIONS
# =========================================================

def contains_forbidden_term(text, forbidden_terms):
    """
    Checks whether text contains any forbidden food term.
    """
    text = str(text).lower()

    for term in forbidden_terms:

        # For multi-word terms
        if " " in term:
            if term in text:
                return True

        else:
            words = text.split()

            if term in words:
                return True

    return False


def build_recipe_filter_text(row):
    """
    Combines all important recipe fields.
    """

    return " ".join([
        str(row["Name"]),
        str(row["RecipeIngredientParts"]),
        str(row["Keywords"]),
        str(row["RecipeCategory"]),
        str(row["ingredient_text"])
    ]).lower()


# =========================================================
# 10. RECOMMENDATION FUNCTION
# =========================================================

def recommend_recipes(
    user_ingredients,
    top_n=5,
    cuisine="All",
    diet="All",
    nutrition="All"
):

    # -----------------------------------------------------
    # Normalize user ingredients
    # -----------------------------------------------------

    normalized_user_ingredients = [
        normalize_ingredient(x)
        for x in user_ingredients
    ]

    normalized_user_ingredients = [
        x for x in normalized_user_ingredients
        if x
    ]

    user_set = set(normalized_user_ingredients)

    print("\nUser ingredients:")
    print(normalized_user_ingredients)

    print("Cuisine:", cuisine)
    print("Diet:", diet)
    print("Nutrition:", nutrition)


    # -----------------------------------------------------
    # Start with all recipes
    # -----------------------------------------------------

    filtered_df = df.copy()


    # =====================================================
    # CUISINE FILTER
    # =====================================================

    if cuisine.lower() != "all":

        cuisine_mask = (
            filtered_df["Keywords"]
            .str.contains(
                cuisine,
                case=False,
                na=False,
                regex=False
            )
        )

        filtered_df = filtered_df[cuisine_mask]


    # =====================================================
    # DIET FILTER
    # =====================================================

    if diet.lower() == "vegetarian":

        # Build comprehensive recipe text
        filtered_df = filtered_df[
            ~filtered_df.apply(
                lambda row: contains_forbidden_term(
                    build_recipe_filter_text(row),
                    NON_VEGETARIAN
                ),
                axis=1
            )
        ]


    elif diet.lower() == "vegan":

        filtered_df = filtered_df[
            ~filtered_df.apply(
                lambda row: contains_forbidden_term(
                    build_recipe_filter_text(row),
                    NON_VEGAN
                ),
                axis=1
            )
        ]


    # =====================================================
    # NUTRITION FILTER
    # =====================================================

    if nutrition.lower() == "low calorie":

        filtered_df = filtered_df[
            (filtered_df["Calories"] > 0)
            &
            (filtered_df["Calories"] <= LOW_CALORIE_LIMIT)
        ]


    elif nutrition.lower() == "high protein":

        filtered_df = filtered_df[
            (filtered_df["ProteinContent"] > 0)
            &
            (filtered_df["ProteinContent"] >= HIGH_PROTEIN_LIMIT)
        ]


    elif nutrition.lower() == "low carb":

        filtered_df = filtered_df[
            (filtered_df["CarbohydrateContent"] > 0)
            &
            (filtered_df["CarbohydrateContent"] <= LOW_CARB_LIMIT)
        ]


    print(
        "Recipes after filters:",
        len(filtered_df)
    )


    if len(filtered_df) == 0:

        print("\nNo recipes found with these filters.")

        return pd.DataFrame()


    # =====================================================
    # TF-IDF USER VECTOR
    # =====================================================

    user_text = " ".join(normalized_user_ingredients)

    user_vector = vectorizer.transform([user_text])


    # =====================================================
    # SIMILARITY
    # =====================================================

    candidate_indices = filtered_df.index

    similarities = cosine_similarity(
        user_vector,
        tfidf_matrix[candidate_indices]
    )[0]


    filtered_df = filtered_df.copy()

    filtered_df["similarity"] = similarities


    # =====================================================
    # TAKE TOP AI CANDIDATES
    # =====================================================

    candidates = filtered_df.nlargest(
        min(200, len(filtered_df)),
        "similarity"
    )


    results = []


    # =====================================================
    # SMART SCORING
    # =====================================================

    for idx, row in candidates.iterrows():

        recipe_ingredients = set(
            row["parsed_ingredients"]
        )

        # -------------------------------------------------
        # Ingredient matching
        # -------------------------------------------------

        matched = user_set.intersection(
            recipe_ingredients
        )

        missing = recipe_ingredients - user_set


        # -------------------------------------------------
        # Coverage
        # -------------------------------------------------

        user_coverage = (
            len(matched)
            / len(user_set)
            * 100
            if user_set
            else 0
        )


        recipe_coverage = (
            len(matched)
            / len(recipe_ingredients)
            * 100
            if recipe_ingredients
            else 0
        )


        # -------------------------------------------------
        # Missing ingredients
        # -------------------------------------------------

        missing_count = len(missing)


        missing_penalty = max(
            0,
            100 - missing_count * 10
        )


        # -------------------------------------------------
        # Feasibility
        # -------------------------------------------------

        feasibility_score = (
            recipe_coverage * 0.70
            +
            missing_penalty * 0.30
        )


        # -------------------------------------------------
        # AI similarity
        # -------------------------------------------------

        similarity_score = (
            row["similarity"] * 100
        )


        # -------------------------------------------------
        # Smart Score
        # -------------------------------------------------

        smart_score = (
            similarity_score * 0.25
            +
            user_coverage * 0.15
            +
            recipe_coverage * 0.25
            +
            missing_penalty * 0.10
            +
            feasibility_score * 0.25
        )


        # -------------------------------------------------
        # Store result
        # -------------------------------------------------

        results.append({

            "RecipeId": row["RecipeId"],

            "Name": row["Name"],

            "Category": row["RecipeCategory"],

            "Calories": row["Calories"],

            "Protein": row["ProteinContent"],

            "Carbs": row["CarbohydrateContent"],

            "Fat": row["FatContent"],

            "AvailableIngredients": ", ".join(
                sorted(matched)
            ),

            "MissingIngredients": ", ".join(
                sorted(missing)
            ),

            "MatchedCount": len(matched),

            "TotalRecipeIngredients": len(
                recipe_ingredients
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

            "Similarity": round(
                similarity_score,
                2
            ),

            "MissingPenalty": round(
                missing_penalty,
                2
            ),

            "Feasibility": round(
                feasibility_score,
                2
            ),

            "SmartScore": round(
                smart_score,
                2
            )
        })


    # =====================================================
    # FINAL SORTING
    # =====================================================

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        by="SmartScore",
        ascending=False
    ).head(top_n)


    return results_df


# =========================================================
# 11. TEST
# =========================================================

if __name__ == "__main__":

    user_ingredients = [
        "aloo",
        "pyaz",
        "tamatar",
        "matar"
    ]


    recommendations = recommend_recipes(

        user_ingredients,

        top_n=5,

        cuisine="Indian",

        diet="Vegetarian",

        nutrition="High Protein"
    )


    print("\n")
    print("=" * 42)
    print("          🍽️ SMARTPLATE AI")
    print("=" * 42)


    if recommendations.empty:

        print("\nNo suitable recipes found.")

    else:

        for _, recipe in recommendations.iterrows():

            print(
                f"\n🍴 {recipe['Name']}"
            )

            print(
                f"Category: {recipe['Category']}"
            )

            print(
                f"Smart Score: {recipe['SmartScore']} %"
            )

            print(
                f"AI Similarity: {recipe['Similarity']} %"
            )

            print(
                f"User Ingredient Coverage: "
                f"{recipe['UserCoverage']} %"
            )

            print(
                f"Recipe Coverage: "
                f"{recipe['RecipeCoverage']} %"
            )

            print(
                f"Matched: "
                f"{recipe['MatchedCount']} / 4"
            )

            print(
                f"Total Recipe Ingredients: "
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
                f"Missing Count: "
                f"{recipe['MissingCount']}"
            )

            print(
                f"Missing Penalty: "
                f"{recipe['MissingPenalty']} %"
            )

            print(
                f"Feasibility Score: "
                f"{recipe['Feasibility']} %"
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

            print("-" * 42)
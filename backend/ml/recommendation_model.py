import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. LOAD CLEANED DATASET
# ==========================================

df = pd.read_csv("../dataset/cleaned_recipes.csv")

print("Dataset loaded!")
print("Total recipes:", len(df))


# ==========================================
# 2. HANDLE MISSING INGREDIENTS
# ==========================================

df["RecipeIngredientParts"] = (
    df["RecipeIngredientParts"]
    .fillna("")
    .astype(str)
)


# ==========================================
# 3. CREATE TF-IDF MODEL
# ==========================================

vectorizer = TfidfVectorizer(
    stop_words="english"
)

ingredient_matrix = vectorizer.fit_transform(
    df["RecipeIngredientParts"]
)

print("TF-IDF matrix created!")
print("Matrix shape:", ingredient_matrix.shape)


# ==========================================
# 4. RECOMMENDATION FUNCTION
# ==========================================

def recommend_recipes(user_ingredients, top_n=5):

    # Convert list into text
    user_text = " ".join(user_ingredients)

    # Convert user ingredients into TF-IDF vector
    user_vector = vectorizer.transform([user_text])

    # Calculate similarity
    similarity_scores = cosine_similarity(
        user_vector,
        ingredient_matrix
    ).flatten()

    # Get top recipe indexes
    top_indices = similarity_scores.argsort()[-top_n:][::-1]

    # Create results
    results = df.iloc[top_indices].copy()

    # Add similarity score
    results["match_score"] = (
        similarity_scores[top_indices] * 100
    ).round(2)

    return results[
        [
            "RecipeId",
            "Name",
            "RecipeIngredientParts",
            "Calories",
            "ProteinContent",
            "CarbohydrateContent",
            "FatContent",
            "match_score"
        ]
    ]


# ==========================================
# 5. TEST THE MODEL
# ==========================================

user_ingredients = [
    "potato",
    "onion",
    "tomato",
    "peas"
]

recommendations = recommend_recipes(
    user_ingredients,
    top_n=5
)


print("\n================================")
print("SMARTPLATE AI RECOMMENDATIONS")
print("================================")

for _, recipe in recommendations.iterrows():

    print(
        f"\n{recipe['Name']}"
        f" | Match: {recipe['match_score']}%"
        f" | Calories: {recipe['Calories']}"
    )
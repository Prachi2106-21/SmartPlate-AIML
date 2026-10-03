import pandas as pd


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "../dataset/cleaned_recipes.csv"
)

print("Dataset loaded!")
print("Total recipes:", len(df))


# ==========================================
# CLEAN KEYWORDS
# ==========================================

df["Keywords"] = (
    df["Keywords"]
    .fillna("")
    .astype(str)
    .str.lower()
)


# ==========================================
# DIET KEYWORDS TO CHECK
# ==========================================

diet_keywords = [
    "vegetarian",
    "vegan",
    "vegetarianism",
    "plant based",
    "plant-based",
    "meatless"
]


# ==========================================
# CHECK EACH KEYWORD
# ==========================================

print("\n==========================================")
print("       DIET KEYWORD ANALYSIS")
print("==========================================")

for keyword in diet_keywords:

    count = df["Keywords"].str.contains(
        keyword,
        case=False,
        na=False
    ).sum()

    print(
        f"{keyword:20} : {count} recipes"
    )


# ==========================================
# SHOW VEGETARIAN EXAMPLES
# ==========================================

vegetarian = df[
    df["Keywords"].str.contains(
        "vegetarian",
        case=False,
        na=False
    )
]

print("\n==========================================")
print("       VEGETARIAN EXAMPLES")
print("==========================================")

print(
    vegetarian[
        [
            "RecipeId",
            "Name",
            "Keywords",
            "Calories",
            "ProteinContent"
        ]
    ].head(10).to_string(index=False)
)


# ==========================================
# SHOW VEGAN EXAMPLES
# ==========================================

vegan = df[
    df["Keywords"].str.contains(
        "vegan",
        case=False,
        na=False
    )
]

print("\n==========================================")
print("          VEGAN EXAMPLES")
print("==========================================")

print(
    vegan[
        [
            "RecipeId",
            "Name",
            "Keywords",
            "Calories",
            "ProteinContent"
        ]
    ].head(10).to_string(index=False)
)
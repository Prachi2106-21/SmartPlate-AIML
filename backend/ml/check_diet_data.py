import pandas as pd


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "../dataset/cleaned_recipes.csv"
)


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
# CHECK NUTRITION DATA
# ==========================================

print("\n==========================================")
print("        NUTRITION DATA CHECK")
print("==========================================")


print(
    "\nCalories:"
)

print(
    df["Calories"].describe()
)


print(
    "\nProtein:"
)

print(
    df["ProteinContent"].describe()
)


print(
    "\nCarbohydrates:"
)

print(
    df["CarbohydrateContent"].describe()
)


# ==========================================
# SHOW VEGAN RECIPES
# ==========================================

vegan = df[
    df["Keywords"].str.contains(
        '"vegan"',
        case=False,
        na=False
    )
]


print("\n==========================================")
print("           VEGAN COUNT")
print("==========================================")

print(
    "Vegan recipes:",
    len(vegan)
)


# ==========================================
# CHECK COMMON NON-VEGETARIAN INGREDIENTS
# ==========================================

meat_keywords = [
    "chicken",
    "beef",
    "pork",
    "lamb",
    "mutton",
    "turkey",
    "fish",
    "salmon",
    "tuna",
    "shrimp",
    "prawn",
    "bacon",
    "ham",
    "sausage",
    "anchovy",
    "crab",
    "lobster"
]


print("\n==========================================")
print("     NON-VEGETARIAN INGREDIENT CHECK")
print("==========================================")


for keyword in meat_keywords:

    count = (
        df["RecipeIngredientParts"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(
            keyword,
            case=False,
            na=False
        )
        .sum()
    )

    print(
        f"{keyword:15} : {count}"
    )
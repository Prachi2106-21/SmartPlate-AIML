import pandas as pd
import os

# --------------------------------
# 1. Load original dataset
# --------------------------------

file_path = "../dataset/recipes.csv"

df = pd.read_csv(file_path)

print("Original dataset shape:")
print(df.shape)

print("\nOriginal columns:")
print(df.columns.tolist())


# --------------------------------
# 2. Select useful columns
# --------------------------------

columns = [
    "RecipeId",
    "Name",
    "Description",
    "Images",
    "RecipeCategory",
    "Keywords",
    "RecipeIngredientParts",
    "RecipeInstructions",
    "PrepTime",
    "CookTime",
    "TotalTime",
    "Calories",
    "FatContent",
    "SaturatedFatContent",
    "CholesterolContent",
    "SodiumContent",
    "CarbohydrateContent",
    "FiberContent",
    "SugarContent",
    "ProteinContent",
    "RecipeServings"
]

df = df[columns]


# --------------------------------
# 3. Remove duplicate recipes
# --------------------------------

df = df.drop_duplicates(subset=["RecipeId"])


# --------------------------------
# 4. Remove recipes without ingredients
# --------------------------------

df = df.dropna(subset=["RecipeIngredientParts"])


# --------------------------------
# 5. Remove recipes without name
# --------------------------------

df = df.dropna(subset=["Name"])


# --------------------------------
# 6. Clean ingredient text
# --------------------------------

df["RecipeIngredientParts"] = (
    df["RecipeIngredientParts"]
    .astype(str)
    .str.lower()
    .str.replace("[", "", regex=False)
    .str.replace("]", "", regex=False)
    .str.replace('"', "", regex=False)
)


# --------------------------------
# 7. Clean recipe names
# --------------------------------

df["Name"] = (
    df["Name"]
    .astype(str)
    .str.strip()
)


# --------------------------------
# 8. Reset index
# --------------------------------

df = df.reset_index(drop=True)


# --------------------------------
# 9. Save cleaned dataset
# --------------------------------

output_path = "../dataset/cleaned_recipes.csv"

df.to_csv(output_path, index=False)


# --------------------------------
# 10. Final information
# --------------------------------

print("\nCleaning completed successfully!")

print("\nCleaned dataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 recipes:")
print(df[["RecipeId", "Name", "RecipeIngredientParts"]].head())
# 🍽️ SmartPlate AI — Meal Planning Assistant

SmartPlate AI is an AI-powered meal planning and recipe recommendation system developed using Machine Learning and modern web technologies.

The system recommends recipes based on:
- Available ingredients
- Cuisine preference
- Diet preference
- Nutrition preference

It helps users discover suitable meals and plan their food choices more intelligently.

---

## 🚀 Features

- 🤖 AI/ML-based recipe recommendation
- 🥗 Ingredient-based meal suggestions
- 🌍 Multiple cuisine preferences
- 🌱 Vegetarian / Vegan diet filtering
- 💪 Nutrition-based recommendations
- 📊 Recipe matching using TF-IDF and cosine similarity
- 📅 Meal planning interface
- 🔐 Login and Signup functionality
- 🎨 Modern responsive React frontend
- ⚡ FastAPI backend

---

## 🧠 Machine Learning

SmartPlate AI uses:

- **TF-IDF (Term Frequency-Inverse Document Frequency)** for recipe text representation
- **Cosine Similarity** for finding recipes similar to user-provided ingredients
- Ingredient normalization for common Indian/Hindi ingredient names

Example:

`aloo → potato`  
`pyaz → onion`  
`tamatar → tomato`  
`matar → peas`

The recommendation system also considers cuisine, diet, nutrition and ingredient matching while generating results.

---

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- JavaScript
- Axios
- React Router
- Lucide React
- CSS

### Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- TF-IDF
- Cosine Similarity

---

## 📁 Project Structure

```text
SmartPlate-AIML/
│
├── backend/
│   ├── api/
│   │   └── recommendation_routes.py
│   │
│   ├── ml/
│   │   ├── ingredient_utils.py
│   │   ├── recommendation_model.py
│   │   ├── smart_recommender.py
│   │   └── ...
│   │
│   ├── dataset/
│   │   └── README.md
│   │
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md

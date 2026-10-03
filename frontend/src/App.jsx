import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  NavLink,
  Navigate,
  Outlet,
  useNavigate
} from "react-router-dom";

import {
  useEffect,
  useMemo,
  useState
} from "react";

import { getRecommendations } from "./api";

import {
  ArrowRight,
  BarChart3,
  CalendarDays,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Heart,
  Home,
  Leaf,
  LogIn,
  LogOut,
  Menu,
  Search,
  Settings,
  Sparkles,
  User,
  Users,
  Utensils,
  X,
  Zap,
  Coffee,
  Sun,
  Moon,
  Apple,
  RefreshCw,
  ChefHat
} from "lucide-react";


// ======================================================
// FOOD IMAGES
// ======================================================

const FOOD_IMAGES = {
  curry:
    "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=85",

  soup:
    "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=85",

  salad:
    "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=85",

  rice:
    "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1200&q=85",

  vegetables:
    "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=1200&q=85",

  breakfast:
    "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?auto=format&fit=crop&w=1200&q=85",

  snack:
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=1200&q=85",

  default:
    "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=85"
};


function getRecipeImage(recipe) {
  const text = `
    ${recipe?.Name || ""}
    ${recipe?.Category || ""}
  `.toLowerCase();

  if (
    text.includes("soup") ||
    text.includes("dal")
  ) {
    return FOOD_IMAGES.soup;
  }

  if (
    text.includes("curry") ||
    text.includes("masala") ||
    text.includes("bhaji") ||
    text.includes("beans")
  ) {
    return FOOD_IMAGES.curry;
  }

  if (
    text.includes("salad") ||
    text.includes("green")
  ) {
    return FOOD_IMAGES.salad;
  }

  if (
    text.includes("rice") ||
    text.includes("biryani")
  ) {
    return FOOD_IMAGES.rice;
  }

  if (
    text.includes("vegetable") ||
    text.includes("veggie")
  ) {
    return FOOD_IMAGES.vegetables;
  }

  return FOOD_IMAGES.default;
}


// ======================================================
// MOCK FALLBACK RECIPES
// ======================================================

const fallbackRecipes = [
  {
    RecipeId: 1,
    Name: "Lentil, Pea and Potato Curry",
    Category: "Curries",
    Calories: 420,
    Protein: 18,
    Carbs: 55,
    Fat: 12,
    AvailableIngredients: "potato, onion, tomato, peas",
    MissingIngredients: "lentils, spices",
    MatchedCount: 4,
    TotalRecipeIngredients: 6,
    UserCoverage: 100,
    SmartScore: 77.6,
    IngredientMatchScore: 85
  },
  {
    RecipeId: 2,
    Name: "Indian Spiced Chickpea Soup",
    Category: "Soups",
    Calories: 350,
    Protein: 16,
    Carbs: 48,
    Fat: 8,
    AvailableIngredients: "onion, tomato",
    MissingIngredients: "chickpeas, spices",
    MatchedCount: 2,
    TotalRecipeIngredients: 5,
    UserCoverage: 70,
    SmartScore: 74,
    IngredientMatchScore: 72
  },
  {
    RecipeId: 3,
    Name: "Green Vegetable Bhaji",
    Category: "Vegetables",
    Calories: 280,
    Protein: 12,
    Carbs: 32,
    Fat: 10,
    AvailableIngredients: "peas, onion",
    MissingIngredients: "green beans, spices",
    MatchedCount: 2,
    TotalRecipeIngredients: 5,
    UserCoverage: 65,
    SmartScore: 70,
    IngredientMatchScore: 68
  },
  {
    RecipeId: 4,
    Name: "Malaysian-Indian Dalcha",
    Category: "Curries",
    Calories: 390,
    Protein: 20,
    Carbs: 46,
    Fat: 9,
    AvailableIngredients: "potato, tomato, onion",
    MissingIngredients: "lentils, spices",
    MatchedCount: 3,
    TotalRecipeIngredients: 6,
    UserCoverage: 80,
    SmartScore: 72,
    IngredientMatchScore: 75
  },
  {
    RecipeId: 5,
    Name: "French Beans Aalu",
    Category: "Vegetables",
    Calories: 310,
    Protein: 9,
    Carbs: 40,
    Fat: 11,
    AvailableIngredients: "potato, onion",
    MissingIngredients: "beans, spices",
    MatchedCount: 2,
    TotalRecipeIngredients: 5,
    UserCoverage: 70,
    SmartScore: 69,
    IngredientMatchScore: 70
  }
];


// ======================================================
// NAVIGATION
// ======================================================

const navItems = [
  {
    label: "Overview",
    path: "/dashboard",
    icon: Home
  },
  {
    label: "AI Recommendations",
    path: "/recommendations",
    icon: Sparkles
  },
  {
    label: "Meal Planner",
    path: "/meal-planner",
    icon: CalendarDays
  },
  {
    label: "History",
    path: "/history",
    icon: Clock3
  },
  {
    label: "Profile",
    path: "/profile",
    icon: User
  },
  {
    label: "Settings",
    path: "/settings",
    icon: Settings
  }
];


// ======================================================
// LOGO
// ======================================================

function Logo() {
  return (
    <Link
      to="/"
      className="brand"
      style={{
        textDecoration: "none",
        color: "inherit"
      }}
    >
      <div className="brand-mark">
        <Leaf size={20} />
      </div>

      <div>
        <div className="brand-name">
          SmartPlate
        </div>

        <div className="brand-subtitle">
          AI Meal Planning
        </div>
      </div>
    </Link>
  );
}


// ======================================================
// LANDING
// ======================================================

function Landing() {
  return (
    <div className="landing-page">

      <header className="landing-header">
        <Logo />

        <div className="landing-actions">
          <Link
            to="/login"
            className="btn btn-secondary"
          >
            Log in
          </Link>

          <Link
            to="/signup"
            className="btn btn-primary"
          >
            Get Started
            <ArrowRight size={17} />
          </Link>
        </div>
      </header>


      <main className="hero-section">

        <div className="hero-content">

          <div className="eyebrow">
            <Sparkles size={16} />
            AI-Powered Nutrition Assistant
          </div>

          <h1>
            Turn your ingredients
            <span> into smarter meals.</span>
          </h1>

          <p>
            SmartPlate AI recommends recipes based on
            your ingredients, diet preferences, cuisine
            and nutrition goals.
          </p>

          <div className="hero-actions">

            <Link
              to="/signup"
              className="btn btn-primary btn-large"
            >
              Start Planning
              <ArrowRight size={18} />
            </Link>

            <Link
              to="/login"
              className="btn btn-secondary btn-large"
            >
              <LogIn size={18} />
              Log in
            </Link>

          </div>

          <div className="hero-trust">
            <CheckCircle2 size={17} />
            Personalized recommendations
          </div>

        </div>


        <div className="hero-card">

          <div className="hero-card-header">
            <div>
              <span>Today's AI Suggestion</span>
              <strong>Smart Meal Match</strong>
            </div>

            <Sparkles size={24} />
          </div>

          <div className="hero-food-image">
            <img
              src={FOOD_IMAGES.curry}
              alt="Healthy meal"
            />
          </div>

          <div className="hero-meal-info">
            <h3>
              Lentil, Pea and Potato Curry
            </h3>

            <p>
              High protein · Indian cuisine
            </p>

            <div className="hero-score">
              <Zap size={16} />
              77.6% Smart Match
            </div>
          </div>

        </div>

      </main>


      <section className="feature-section">

        <div className="section-heading">
          <span className="eyebrow">
            Why SmartPlate
          </span>

          <h2>
            One smart assistant for your meals.
          </h2>
        </div>

        <div className="feature-grid">

          <FeatureCard
            icon={<Sparkles />}
            title="AI Recommendations"
            description="Get recipe suggestions using ingredient matching and machine learning."
          />

          <FeatureCard
            icon={<BarChart3 />}
            title="Nutrition Insights"
            description="Understand calories, protein, carbs and fats for every recommendation."
          />

          <FeatureCard
            icon={<CalendarDays />}
            title="Smart Meal Planner"
            description="Automatically organize breakfast, lunch, snacks and dinner."
          />

        </div>

      </section>

    </div>
  );
}


function FeatureCard({
  icon,
  title,
  description
}) {
  return (
    <div className="feature-card">

      <div className="feature-icon">
        {icon}
      </div>

      <h3>{title}</h3>

      <p>{description}</p>

    </div>
  );
}


// ======================================================
// AUTH
// ======================================================

function AuthLayout({
  title,
  subtitle,
  children
}) {
  return (
    <div className="auth-page">

      <div className="auth-left">

        <Logo />

        <div className="auth-hero">

          <span className="eyebrow">
            SmartPlate AI
          </span>

          <h1>
            Smarter meals.
            <br />
            Better planning.
          </h1>

          <p>
            Build personalized meal plans
            using AI-powered recipe recommendations.
          </p>

        </div>

      </div>


      <div className="auth-right">

        <div className="auth-card">

          <h2>{title}</h2>

          <p className="auth-subtitle">
            {subtitle}
          </p>

          {children}

        </div>

      </div>

    </div>
  );
}


function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleLogin(e) {
    e.preventDefault();

    localStorage.setItem(
      "smartplate_logged_in",
      "true"
    );

    localStorage.setItem(
      "smartplate_user",
      JSON.stringify({
        name: email.split("@")[0] || "User",
        email
      })
    );

    navigate("/dashboard");
  }

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Log in to continue planning smarter meals."
    >

      <form
        className="auth-form"
        onSubmit={handleLogin}
      >

        <label>
          Email

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
          />

        </label>


        <label>
          Password

          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
          />

        </label>


        <button
          className="btn btn-primary btn-full"
          type="submit"
        >
          <LogIn size={17} />
          Log in
        </button>

      </form>


      <p className="auth-footer">
        Don't have an account?

        <Link to="/signup">
          Create account
        </Link>
      </p>

    </AuthLayout>
  );
}


function Signup() {

  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSignup(e) {
    e.preventDefault();

    localStorage.setItem(
      "smartplate_logged_in",
      "true"
    );

    localStorage.setItem(
      "smartplate_user",
      JSON.stringify({
        name,
        email
      })
    );

    navigate("/dashboard");
  }

  return (
    <AuthLayout
      title="Create your account"
      subtitle="Start building smarter meals with AI."
    >

      <form
        className="auth-form"
        onSubmit={handleSignup}
      >

        <label>
          Full name

          <input
            type="text"
            placeholder="Your name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            required
          />

        </label>


        <label>
          Email

          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) =>
              setEmail(e.target.value)
            }
            required
          />

        </label>


        <label>
          Password

          <input
            type="password"
            placeholder="Create a password"
            value={password}
            onChange={(e) =>
              setPassword(e.target.value)
            }
            required
          />

        </label>


        <button
          className="btn btn-primary btn-full"
          type="submit"
        >
          Create Account
          <ArrowRight size={17} />
        </button>

      </form>


      <p className="auth-footer">
        Already have an account?

        <Link to="/login">
          Log in
        </Link>
      </p>

    </AuthLayout>
  );
}


// ======================================================
// PROTECTED ROUTE
// ======================================================

function ProtectedRoute() {

  const loggedIn =
    localStorage.getItem(
      "smartplate_logged_in"
    ) === "true";

  if (!loggedIn) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  return <Outlet />;
}


// ======================================================
// DASHBOARD LAYOUT
// ======================================================

function DashboardLayout() {

  const navigate = useNavigate();

  const [mobileMenu, setMobileMenu] =
    useState(false);

  const user =
    JSON.parse(
      localStorage.getItem(
        "smartplate_user"
      ) || "{}"
    );

  function logout() {

    localStorage.removeItem(
      "smartplate_logged_in"
    );

    navigate("/login");
  }

  return (
    <div className="dashboard-shell">

      <aside
        className={
          mobileMenu
            ? "sidebar open"
            : "sidebar"
        }
      >

        <div className="sidebar-top">

          <Logo />

          <button
            className="mobile-close"
            onClick={() =>
              setMobileMenu(false)
            }
          >
            <X size={20} />
          </button>

        </div>


        <nav className="sidebar-nav">

          {navItems.map((item) => {

            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={
                  item.path === "/dashboard"
                }
                onClick={() =>
                  setMobileMenu(false)
                }
                className={({ isActive }) =>
                  isActive
                    ? "nav-link active"
                    : "nav-link"
                }
              >
                <Icon size={19} />
                {item.label}
              </NavLink>
            );

          })}

        </nav>


        <div className="sidebar-bottom">

          <button
            className="nav-link logout-button"
            onClick={logout}
          >
            <LogOut size={19} />
            Sign out
          </button>

        </div>

      </aside>


      <div className="dashboard-main">

        <header className="topbar">

          <button
            className="mobile-menu-button"
            onClick={() =>
              setMobileMenu(true)
            }
          >
            <Menu size={22} />
          </button>


          <div className="topbar-title">
            SmartPlate AI
          </div>


          <div className="topbar-user">

            <div className="avatar">
              {(user.name || "U")
                .charAt(0)
                .toUpperCase()}
            </div>

            <span>
              {user.name || "User"}
            </span>

          </div>

        </header>


        <main className="dashboard-content">
          <Outlet />
        </main>

      </div>

    </div>
  );
}


// ======================================================
// DASHBOARD
// ======================================================

function Dashboard() {

  const navigate = useNavigate();

  const [ingredients, setIngredients] =
    useState([
      "Potato",
      "Onion",
      "Tomato",
      "Peas"
    ]);

  const [ingredientInput, setIngredientInput] =
    useState("");

  const [cuisine, setCuisine] =
    useState("Indian");

  const [diet, setDiet] =
    useState("Vegetarian");

  const [nutrition, setNutrition] =
    useState("High Protein");


  function addIngredient() {

    const value =
      ingredientInput.trim();

    if (!value) return;

    if (
      ingredients.some(
        (item) =>
          item.toLowerCase() ===
          value.toLowerCase()
      )
    ) {
      setIngredientInput("");
      return;
    }

    setIngredients([
      ...ingredients,
      value
    ]);

    setIngredientInput("");
  }


  function removeIngredient(item) {

    setIngredients(
      ingredients.filter(
        (ingredient) =>
          ingredient !== item
      )
    );
  }


  function findRecipes() {

    localStorage.setItem(
      "smartplate_preferences",
      JSON.stringify({
        ingredients,
        cuisine,
        diet,
        nutrition
      })
    );

    navigate("/recommendations");
  }


  return (
    <div className="dashboard-page">

      <div className="page-heading">

        <div>
          <span className="eyebrow">
            AI Kitchen Assistant
          </span>

          <h1>
            What are we cooking today?
          </h1>

          <p>
            Tell SmartPlate what you have,
            and AI will find matching recipes.
          </p>
        </div>

      </div>


      <div className="dashboard-grid">

        <section className="planner-input-card">

          <div className="card-heading">
            <div>
              <h2>Your ingredients</h2>
              <p>
                Add what is available in your kitchen.
              </p>
            </div>

            <Utensils size={22} />
          </div>


          <div className="ingredient-input">

            <input
              value={ingredientInput}
              onChange={(e) =>
                setIngredientInput(
                  e.target.value
                )
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  addIngredient();
                }
              }}
              placeholder="e.g. paneer, rice..."
            />

            <button
              className="btn btn-primary"
              onClick={addIngredient}
            >
              Add
            </button>

          </div>


          <div className="ingredient-list">

            {ingredients.map((item) => (

              <span
                className="ingredient-chip"
                key={item}
              >
                {item}

                <button
                  onClick={() =>
                    removeIngredient(item)
                  }
                >
                  <X size={13} />
                </button>

              </span>

            ))}

          </div>


          <div className="preference-grid">

            <label>
              Cuisine

              <select
                value={cuisine}
                onChange={(e) =>
                  setCuisine(e.target.value)
                }
              >
                <option>All</option>
                <option>Indian</option>
                <option>Italian</option>
                <option>Mexican</option>
                <option>Chinese</option>
                <option>Thai</option>
                <option>Mediterranean</option>
                <option>American</option>
              </select>

            </label>


            <label>
              Diet

              <select
                value={diet}
                onChange={(e) =>
                  setDiet(e.target.value)
                }
              >
                <option>All</option>
                <option>Vegetarian</option>
                <option>Vegan</option>
                <option>Non-Vegetarian</option>
              </select>

            </label>


            <label>
              Nutrition

              <select
                value={nutrition}
                onChange={(e) =>
                  setNutrition(e.target.value)
                }
              >
                <option>All</option>
                <option>High Protein</option>
                <option>Low Calorie</option>
                <option>Low Carb</option>
              </select>

            </label>

          </div>


          <button
            className="btn btn-primary btn-large btn-full"
            onClick={findRecipes}
          >
            <Sparkles size={18} />
            Find AI Recipes
          </button>

        </section>


        <section className="dashboard-side-card">

          <div className="side-card-icon">
            <Zap size={22} />
          </div>

          <h2>
            Smart meal planning
          </h2>

          <p>
            After finding recipes, SmartPlate can
            automatically create a complete daily
            plan with breakfast, lunch, snacks and dinner.
          </p>

          <button
            className="text-button"
            onClick={() =>
              navigate("/meal-planner")
            }
          >
            Open Meal Planner
            <ArrowRight size={16} />
          </button>

        </section>

      </div>


      <div className="stats-grid">

        <StatCard
          icon={<Sparkles />}
          value="AI"
          label="Recommendation Engine"
        />

        <StatCard
          icon={<BarChart3 />}
          value="4+"
          label="Nutrition Metrics"
        />

        <StatCard
          icon={<CalendarDays />}
          value="4"
          label="Daily Meal Slots"
        />

      </div>

    </div>
  );
}


function StatCard({
  icon,
  value,
  label
}) {
  return (
    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>

    </div>
  );
}


// ======================================================
// RECOMMENDATIONS
// ======================================================

function Recommendations() {

  const [recommendations, setRecommendations] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [selectedRecipe, setSelectedRecipe] =
    useState(null);


  const preferences =
    useMemo(() => {

      return JSON.parse(
        localStorage.getItem(
          "smartplate_preferences"
        ) || "{}"
      );

    }, []);


  async function fetchRecipes() {

    setLoading(true);
    setError("");

    try {

      const response =
        await getRecommendations({

          ingredients:
            preferences.ingredients ||
            [
              "Potato",
              "Onion",
              "Tomato",
              "Peas"
            ],

          cuisine:
            preferences.cuisine ||
            "Indian",

          diet:
            preferences.diet ||
            "Vegetarian",

          nutrition:
            preferences.nutrition ||
            "High Protein",

          top_n: 6

        });


      const data =
        response?.recommendations || [];


      // ==============================================
      // IMPORTANT:
      // REAL BACKEND DATA SET
      // + LOCAL STORAGE FOR MEAL PLANNER
      // ==============================================

      setRecommendations(data);

      localStorage.setItem(
        "smartplate_recommendations",
        JSON.stringify(data)
      );


      // Save search history
      const history =
        JSON.parse(
          localStorage.getItem(
            "smartplate_history"
          ) || "[]"
        );

      const historyItem = {
        id: Date.now(),
        date: new Date().toLocaleDateString(),
        ingredients:
          preferences.ingredients || [],
        cuisine:
          preferences.cuisine || "All",
        diet:
          preferences.diet || "All",
        nutrition:
          preferences.nutrition || "All",
        count: data.length
      };

      localStorage.setItem(
        "smartplate_history",
        JSON.stringify([
          historyItem,
          ...history.slice(0, 9)
        ])
      );

    } catch (err) {

      console.error(err);

      setError(
        "Unable to connect to SmartPlate AI backend."
      );

      // Don't destroy previously saved results
      const saved =
        JSON.parse(
          localStorage.getItem(
            "smartplate_recommendations"
          ) || "[]"
        );

      if (saved.length) {
        setRecommendations(saved);
      }

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    fetchRecipes();

  }, []);


  return (
    <div className="dashboard-page">

      <div className="page-heading page-heading-row">

        <div>

          <span className="eyebrow">
            <Sparkles size={15} />
            AI Recipe Engine
          </span>

          <h1>
            Your Smart Recommendations
          </h1>

          <p>
            Recipes selected using your ingredients,
            preferences and nutrition goals.
          </p>

        </div>


        <button
          className="btn btn-secondary"
          onClick={fetchRecipes}
          disabled={loading}
        >
          <RefreshCw
            size={17}
            className={
              loading
                ? "spin"
                : ""
            }
          />

          Refresh

        </button>

      </div>


      {error && (
        <div className="error-banner">

          <span>{error}</span>

          <button
            onClick={fetchRecipes}
          >
            Retry
          </button>

        </div>
      )}


      {loading ? (

        <div className="loading-state">

          <div className="loading-spinner" />

          <h3>
            AI is finding recipes...
          </h3>

          <p>
            Matching ingredients, cuisine and nutrition.
          </p>

        </div>

      ) : recommendations.length === 0 ? (

        <div className="empty-state">

          <ChefHat size={42} />

          <h3>
            No recipes found
          </h3>

          <p>
            Try adding more ingredients or changing
            your preferences.
          </p>

        </div>

      ) : (

        <>
          <div className="results-bar">

            <strong>
              {recommendations.length}
              {" "}
              recipes found
            </strong>

            <span>
              Based on your current preferences
            </span>

          </div>


          <div className="recommendation-grid">

            {recommendations.map(
              (recipe, index) => (

                <RecipeCard
                  key={
                    recipe.RecipeId ||
                    `${recipe.Name}-${index}`
                  }
                  recipe={recipe}
                  onView={() =>
                    setSelectedRecipe(recipe)
                  }
                />

              )
            )}

          </div>
        </>

      )}


      {selectedRecipe && (

        <RecipeDetailsModal
          recipe={selectedRecipe}
          onClose={() =>
            setSelectedRecipe(null)
          }
        />

      )}

    </div>
  );
}


// ======================================================
// RECIPE CARD
// ======================================================

function RecipeCard({
  recipe,
  onView
}) {

  const image =
    getRecipeImage(recipe);


  const available =
    String(
      recipe.AvailableIngredients || ""
    )
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean);


  const missing =
    String(
      recipe.MissingIngredients || ""
    )
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean);


  const smartScore =
    Number(
      recipe.SmartScore || 0
    );


  const matchScore =
    Number(
      recipe.IngredientMatchScore || 0
    );


  return (
    <article className="recipe-card">

      <div className="recipe-image-wrapper">

        <img
          src={image}
          alt={recipe.Name}
          className="recipe-image"
        />

        <div className="recipe-score-badge">
          <Zap size={14} />
          {smartScore.toFixed(1)}%
        </div>

      </div>


      <div className="recipe-card-body">

        <div className="recipe-category">
          {recipe.Category || "Recipe"}
        </div>

        <h3>
          {recipe.Name}
        </h3>


        <div className="recipe-metrics">

          <div>
            <span>Calories</span>
            <strong>
              {formatNumber(recipe.Calories)}
            </strong>
          </div>

          <div>
            <span>Protein</span>
            <strong>
              {formatNumber(recipe.Protein)}g
            </strong>
          </div>

          <div>
            <span>Carbs</span>
            <strong>
              {formatNumber(recipe.Carbs)}g
            </strong>
          </div>

        </div>


        <div className="match-row">

          <span>
            Ingredient match
          </span>

          <strong>
            {matchScore.toFixed(1)}%
          </strong>

        </div>


        <div className="progress-track">

          <div
            className="progress-fill"
            style={{
              width: `${Math.min(
                100,
                Math.max(
                  0,
                  matchScore
                )
              )}%`
            }}
          />

        </div>


        <div className="ingredient-summary">

          <span className="available-count">
            ✓ {available.length} available
          </span>

          <span className="missing-count">
            + {missing.length} missing
          </span>

        </div>


        <button
          className="recipe-view-button"
          onClick={onView}
        >
          View Recipe
          <ChevronRight size={17} />
        </button>

      </div>

    </article>
  );
}


// ======================================================
// RECIPE DETAILS MODAL
// ======================================================

function RecipeDetailsModal({
  recipe,
  onClose
}) {

  const image =
    getRecipeImage(recipe);


  const available =
    String(
      recipe.AvailableIngredients || ""
    )
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean);


  const missing =
    String(
      recipe.MissingIngredients || ""
    )
      .split(",")
      .map((x) => x.trim())
      .filter(Boolean);


  const saveRecipe = () => {

    const saved =
      JSON.parse(
        localStorage.getItem(
          "smartplate_saved_recipes"
        ) || "[]"
      );

    const exists =
      saved.some(
        (item) =>
          item.Name === recipe.Name
      );

    if (!exists) {

      localStorage.setItem(
        "smartplate_saved_recipes",
        JSON.stringify([
          recipe,
          ...saved
        ])
      );

      alert("Recipe saved!");

    } else {

      alert("Recipe already saved!");

    }
  };


  return (
    <div
      className="modal-overlay"
      onClick={onClose}
    >

      <div
        className="recipe-modal"
        onClick={(e) =>
          e.stopPropagation()
        }
      >

        <button
          className="modal-close"
          onClick={onClose}
        >
          <X size={21} />
        </button>


        <div className="modal-image">

          <img
            src={image}
            alt={recipe.Name}
          />

          <div className="modal-score">
            <Sparkles size={15} />
            AI Match{" "}
            {Number(
              recipe.SmartScore || 0
            ).toFixed(1)}
            %
          </div>

        </div>


        <div className="modal-content">

          <div className="recipe-category">
            {recipe.Category || "Recipe"}
          </div>

          <h2>
            {recipe.Name}
          </h2>


          <div className="nutrition-grid">

            <NutritionItem
              label="Calories"
              value={`${formatNumber(
                recipe.Calories
              )} kcal`}
            />

            <NutritionItem
              label="Protein"
              value={`${formatNumber(
                recipe.Protein
              )} g`}
            />

            <NutritionItem
              label="Carbs"
              value={`${formatNumber(
                recipe.Carbs
              )} g`}
            />

            <NutritionItem
              label="Fat"
              value={`${formatNumber(
                recipe.Fat
              )} g`}
            />

          </div>


          <div className="modal-section">

            <h3>
              <CheckCircle2 size={18} />
              Ingredients you have
            </h3>

            {available.length ? (

              <div className="modal-chip-list">

                {available.map(
                  (item) => (
                    <span
                      className="modal-chip available-chip"
                      key={item}
                    >
                      ✓ {item}
                    </span>
                  )
                )}

              </div>

            ) : (

              <p className="muted">
                No matched ingredients listed.
              </p>

            )}

          </div>


          <div className="modal-section">

            <h3>
              <Search size={18} />
              Ingredients you may need
            </h3>

            {missing.length ? (

              <div className="modal-chip-list">

                {missing.map(
                  (item) => (
                    <span
                      className="modal-chip missing-chip"
                      key={item}
                    >
                      + {item}
                    </span>
                  )
                )}

              </div>

            ) : (

              <p className="muted">
                You have all listed ingredients.
              </p>

            )}

          </div>


          <div className="modal-section">

            <h3>
              <BarChart3 size={18} />
              AI Recipe Analysis
            </h3>

            <div className="analysis-grid">

              <AnalysisItem
                label="Ingredient Match"
                value={
                  recipe.IngredientMatchScore
                }
              />

              <AnalysisItem
                label="User Coverage"
                value={
                  recipe.UserCoverage
                }
              />

              <AnalysisItem
                label="Recipe Coverage"
                value={
                  recipe.RecipeCoverage
                }
              />

              <AnalysisItem
                label="Practicality"
                value={
                  recipe.PracticalityScore
                }
              />

            </div>

          </div>


          <div className="modal-note">

            <ChefHat size={18} />

            <div>

              <strong>
                Preparation note
              </strong>

              <p>
                The current AI backend provides
                recipe matching, ingredients and
                nutrition data. Exact cooking
                instructions are not currently
                returned by the API, so SmartPlate
                does not invent recipe instructions.
              </p>

            </div>

          </div>


          <button
            className="btn btn-primary btn-full"
            onClick={saveRecipe}
          >
            <Heart size={17} />
            Save Recipe
          </button>

        </div>

      </div>

    </div>
  );
}


function NutritionItem({
  label,
  value
}) {
  return (
    <div className="nutrition-item">

      <span>{label}</span>

      <strong>{value}</strong>

    </div>
  );
}


function AnalysisItem({
  label,
  value
}) {

  const number =
    Number(value || 0);

  return (
    <div className="analysis-item">

      <div>
        <span>{label}</span>

        <strong>
          {number.toFixed(1)}%
        </strong>
      </div>

      <div className="progress-track">

        <div
          className="progress-fill"
          style={{
            width: `${Math.min(
              100,
              Math.max(
                0,
                number
              )
            )}%`
          }}
        />

      </div>

    </div>
  );
}


// ======================================================
// MEAL PLANNER
// ======================================================

const MEAL_SLOTS = [
  {
    key: "Breakfast",
    icon: Coffee,
    description: "Start your day"
  },
  {
    key: "Lunch",
    icon: Sun,
    description: "Main meal"
  },
  {
    key: "Snack",
    icon: Apple,
    description: "Light snack"
  },
  {
    key: "Dinner",
    icon: Moon,
    description: "End your day"
  }
];


const DAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday"
];


function MealPlanner() {

  const [recommendations, setRecommendations] =
    useState([]);


  const [selectedDay, setSelectedDay] =
    useState("Monday");


  const [mealPlan, setMealPlan] =
    useState(() => {

      return JSON.parse(
        localStorage.getItem(
          "smartplate_meal_plan"
        ) || "{}"
      );

    });


  useEffect(() => {

    const saved =
      JSON.parse(
        localStorage.getItem(
          "smartplate_recommendations"
        ) || "[]"
      );

    setRecommendations(saved);

  }, []);


  function getRecipeForSlot(
    dayIndex,
    slotIndex
  ) {

    if (!recommendations.length) {
      return null;
    }

    const index =
      (
        dayIndex * MEAL_SLOTS.length +
        slotIndex
      ) % recommendations.length;

    return recommendations[index];
  }


  function generateMealPlan() {

    if (!recommendations.length) {

      alert(
        "First generate AI recommendations from the Recommendations page."
      );

      return;
    }


    const newPlan = {};


    DAYS.forEach(
      (day, dayIndex) => {

        newPlan[day] = {};

        MEAL_SLOTS.forEach(
          (slot, slotIndex) => {

            newPlan[day][slot.key] =
              getRecipeForSlot(
                dayIndex,
                slotIndex
              );

          }
        );

      }
    );


    setMealPlan(newPlan);

    localStorage.setItem(
      "smartplate_meal_plan",
      JSON.stringify(newPlan)
    );

  }


  function changeMeal(
    day,
    slot,
    recipeId
  ) {

    const recipe =
      recommendations.find(
        (item) =>
          String(
            item.RecipeId
          ) === String(recipeId)
      );


    const newPlan = {
      ...mealPlan,
      [day]: {
        ...(mealPlan[day] || {}),
        [slot]: recipe || null
      }
    };


    setMealPlan(newPlan);

    localStorage.setItem(
      "smartplate_meal_plan",
      JSON.stringify(newPlan)
    );

  }


  const currentDayPlan =
    mealPlan[selectedDay] || {};


  return (
    <div className="dashboard-page">

      <div className="page-heading page-heading-row">

        <div>

          <span className="eyebrow">
            <CalendarDays size={15} />
            Weekly Meal Planner
          </span>

          <h1>
            Build your smart meal plan
          </h1>

          <p>
            Use your real AI recommendations for
            breakfast, lunch, snacks and dinner.
          </p>

        </div>


        <button
          className="btn btn-primary"
          onClick={generateMealPlan}
        >
          <Sparkles size={17} />
          Generate Smart Plan
        </button>

      </div>


      {recommendations.length === 0 && (

        <div className="planner-warning">

          <Sparkles size={19} />

          <div>

            <strong>
              No AI recommendations available yet.
            </strong>

            <p>
              Open AI Recommendations first,
              generate recipes, then return here.
            </p>

          </div>

        </div>

      )}


      <div className="day-tabs">

        {DAYS.map((day) => (

          <button
            key={day}
            className={
              selectedDay === day
                ? "day-tab active"
                : "day-tab"
            }
            onClick={() =>
              setSelectedDay(day)
            }
          >
            {day}
          </button>

        ))}

      </div>


      <div className="meal-plan-grid">

        {MEAL_SLOTS.map(
          (slot, slotIndex) => {

            const Icon = slot.icon;

            const recipe =
              currentDayPlan[
                slot.key
              ];


            return (
              <div
                className="meal-slot-card"
                key={slot.key}
              >

                <div className="meal-slot-header">

                  <div className="meal-slot-icon">
                    <Icon size={20} />
                  </div>

                  <div>
                    <strong>
                      {slot.key}
                    </strong>

                    <span>
                      {slot.description}
                    </span>
                  </div>

                </div>


                {recipe ? (

                  <>

                    <img
                      className="meal-slot-image"
                      src={getRecipeImage(recipe)}
                      alt={recipe.Name}
                    />


                    <div className="meal-slot-body">

                      <h3>
                        {recipe.Name}
                      </h3>

                      <div className="meal-slot-nutrition">

                        <span>
                          {formatNumber(
                            recipe.Calories
                          )} kcal
                        </span>

                        <span>
                          {formatNumber(
                            recipe.Protein
                          )}g protein
                        </span>

                      </div>


                      <select
                        value={
                          recipe.RecipeId
                        }
                        onChange={(e) =>
                          changeMeal(
                            selectedDay,
                            slot.key,
                            e.target.value
                          )
                        }
                      >

                        {recommendations.map(
                          (item) => (

                            <option
                              key={
                                item.RecipeId
                              }
                              value={
                                item.RecipeId
                              }
                            >
                              {item.Name}
                            </option>

                          )
                        )}

                      </select>

                    </div>

                  </>

                ) : (

                  <div className="empty-meal-slot">

                    <ChefHat size={30} />

                    <p>
                      No meal selected
                    </p>

                    <span>
                      Click Generate Smart Plan
                    </span>

                  </div>

                )}

              </div>
            );

          }
        )}

      </div>


      <div className="weekly-overview">

        <div className="card-heading">

          <div>
            <h2>
              Weekly overview
            </h2>

            <p>
              Your saved meal plan
            </p>
          </div>

          <CalendarDays size={21} />

        </div>


        <div className="weekly-list">

          {DAYS.map((day) => {

            const plan =
              mealPlan[day] || {};


            const count =
              MEAL_SLOTS.filter(
                (slot) =>
                  plan[slot.key]
              ).length;


            return (
              <button
                key={day}
                className="weekly-day-row"
                onClick={() =>
                  setSelectedDay(day)
                }
              >

                <strong>
                  {day}
                </strong>

                <span>
                  {count}/4 meals planned
                </span>

                <ChevronRight size={17} />

              </button>
            );

          })}

        </div>

      </div>

    </div>
  );
}


// ======================================================
// HISTORY
// ======================================================

function History() {

  const history =
    JSON.parse(
      localStorage.getItem(
        "smartplate_history"
      ) || "[]"
    );


  return (
    <div className="dashboard-page">

      <div className="page-heading">

        <span className="eyebrow">
          Search History
        </span>

        <h1>
          Recommendation History
        </h1>

        <p>
          Your previous AI recipe searches.
        </p>

      </div>


      <div className="history-card">

        {history.length === 0 ? (

          <div className="empty-state">
            <Clock3 size={40} />

            <h3>
              No history yet
            </h3>

            <p>
              Your recommendation searches will
              appear here.
            </p>
          </div>

        ) : (

          history.map((item) => (

            <div
              className="history-row"
              key={item.id}
            >

              <div className="history-icon">
                <Sparkles size={18} />
              </div>

              <div className="history-info">

                <strong>
                  {item.count} recipes found
                </strong>

                <span>
                  {item.ingredients.join(", ")}
                </span>

              </div>

              <div className="history-meta">

                <span>
                  {item.cuisine}
                </span>

                <small>
                  {item.date}
                </small>

              </div>

            </div>

          ))

        )}

      </div>

    </div>
  );
}


// ======================================================
// PROFILE
// ======================================================

function Profile() {

  const user =
    JSON.parse(
      localStorage.getItem(
        "smartplate_user"
      ) || "{}"
    );


  return (
    <div className="dashboard-page">

      <div className="page-heading">

        <span className="eyebrow">
          Account
        </span>

        <h1>
          Your Profile
        </h1>

        <p>
          Manage your SmartPlate account.
        </p>

      </div>


      <div className="profile-card">

        <div className="profile-avatar">

          {(user.name || "U")
            .charAt(0)
            .toUpperCase()}

        </div>


        <div>

          <h2>
            {user.name || "SmartPlate User"}
          </h2>

          <p>
            {user.email || "No email available"}
          </p>

        </div>

      </div>

    </div>
  );
}


// ======================================================
// SETTINGS
// ======================================================

function SettingsPage() {

  const [saved, setSaved] =
    useState(false);


  function clearData() {

    localStorage.removeItem(
      "smartplate_recommendations"
    );

    localStorage.removeItem(
      "smartplate_meal_plan"
    );

    localStorage.removeItem(
      "smartplate_history"
    );

    setSaved(true);

    setTimeout(
      () => setSaved(false),
      2000
    );

  }


  return (
    <div className="dashboard-page">

      <div className="page-heading">

        <span className="eyebrow">
          Preferences
        </span>

        <h1>
          Settings
        </h1>

        <p>
          Manage your SmartPlate data.
        </p>

      </div>


      <div className="settings-card">

        <div className="settings-row">

          <div>
            <h3>
              Local recommendation data
            </h3>

            <p>
              Clear saved recommendations and meal plans
              from this browser.
            </p>
          </div>

          <button
            className="btn btn-secondary"
            onClick={clearData}
          >
            Clear Data
          </button>

        </div>


        {saved && (

          <div className="success-message">
            Data cleared successfully.
          </div>

        )}

      </div>

    </div>
  );
}


// ======================================================
// HELPERS
// ======================================================

function formatNumber(value) {

  const number =
    Number(value);

  if (
    Number.isNaN(number)
  ) {
    return "0";
  }

  return number % 1 === 0
    ? number.toString()
    : number.toFixed(1);
}


// ======================================================
// APP
// ======================================================

function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Landing />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/signup"
          element={<Signup />}
        />


        <Route element={<ProtectedRoute />}>

          <Route
            element={<DashboardLayout />}
          >

            <Route
              path="/dashboard"
              element={<Dashboard />}
            />

            <Route
              path="/recommendations"
              element={<Recommendations />}
            />

            <Route
              path="/meal-planner"
              element={<MealPlanner />}
            />

            <Route
              path="/history"
              element={<History />}
            />

            <Route
              path="/profile"
              element={<Profile />}
            />

            <Route
              path="/settings"
              element={<SettingsPage />}
            />

          </Route>

        </Route>


        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>

    </BrowserRouter>
  );
}


export default App;
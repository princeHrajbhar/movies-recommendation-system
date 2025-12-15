import pickle
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.recommend-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    color: #ffffff;
    padding: 16px;
    margin-bottom: 12px;
    border-radius: 12px;
    font-size: 18px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25);
}

div.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    font-size: 16px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
movies = pickle.load(open('movies.pkl', 'rb'))

# ---------------- BUILD SIMILARITY (RUNTIME) ----------------
@st.cache_data(show_spinner=True)
def build_similarity(data):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(data['tags']).toarray()
    similarity_matrix = cosine_similarity(vectors)
    return similarity_matrix

similarity = build_similarity(movies)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎥 Movie Recommender")
st.sidebar.markdown("""
**Recommendation Type:**  
Content-Based Filtering  

**Tech Used:**  
- Python  
- Scikit-learn  
- Streamlit  

**Algorithm:**  
- Bag of Words  
- Cosine Similarity  

👨‍💻 *By Prince Rajbhar*
""")

# ---------------- MAIN TITLE ----------------
st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommendation System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "Select a movie to get similar movie recommendations based on content similarity."
    "</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):
    if movie not in movies['title'].values:
        return []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    return [movies.iloc[i[0]].title for i in distances[1:6]]

# ---------------- MOVIE SELECT ----------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_movie = st.selectbox(
        "🎞️ Select a Movie",
        movies['title'].values
    )

    recommend_btn = st.button("✨ Get Recommendations")

# ---------------- OUTPUT ----------------
if recommend_btn:
    results = recommend(selected_movie)

    st.subheader("📌 Recommended Movies")

    if results:
        for movie in results:
            st.markdown(
                f"""
                <div class="recommend-card">
                    🎬 {movie}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("No recommendations found.")

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "Content-Based Movie Recommendation System | Streamlit App"
    "</p>",
    unsafe_allow_html=True
)

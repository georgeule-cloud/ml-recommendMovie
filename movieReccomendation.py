import pickle
import streamlit as st
import requests
from streamlit_star_rating import st_star_rating

st.set_page_config(layout="wide")

st.markdown("""
<style>
.overview-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def fetch_overview(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    overview = data['overview']
    return overview


def fetch_rating(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    rating = round(((data['vote_average']*10)/20), 1)
    return rating


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    recommended_movie_overviews = []
    recommended_movie_ratings = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_ids.append(movie_id)
        overview = fetch_overview(
            movie_id)[:200] + (fetch_overview(movie_id)[200:] and '..')
        rating = fetch_rating(movie_id)
        recommended_movie_overviews.append(overview)
        recommended_movie_ratings.append(rating)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids, recommended_movie_overviews, recommended_movie_ratings


st.title('F★Movies')
st.header('Lista de películas')
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Busca o selecciona una película",
    movie_list
)

if st.button('Muestrame las recomendaciones'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ids, recommended_movie_overviews, recommended_movie_ratings = recommend(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
        st.write(str(recommended_movie_ratings[0]), "/5 ★")
        st.write(
            '<p class="overview-font">' + recommended_movie_overviews[0]+'</p>', unsafe_allow_html=True)
        # st.write(recommended_movie_overviews[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
        st.write(str(recommended_movie_ratings[1]), "/5 ★")
        st.write(
            '<p class="overview-font">' + recommended_movie_overviews[1]+'</p>', unsafe_allow_html=True)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        st.write(str(recommended_movie_ratings[2]), "/5 ★")
        st.write(
            '<p class="overview-font">' + recommended_movie_overviews[2]+'</p>', unsafe_allow_html=True)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
        st.write(str(recommended_movie_ratings[3]), "/5 ★")
        st.write(
            '<p class="overview-font">' + recommended_movie_overviews[3]+'</p>', unsafe_allow_html=True)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
        st.write(str(recommended_movie_ratings[4]), "/5 ★")
        st.write(
            '<p class="overview-font">' + recommended_movie_overviews[4]+'</p>', unsafe_allow_html=True)

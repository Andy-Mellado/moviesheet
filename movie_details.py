import requests

def get_movie_details(title, api_key):
    """
    Retrieves director and actors of a movie (if found) by its title. 

    Args:
        title (str): The title of the movie to search for.
        api_key (str): TMDb API key.

    Returns:
        dict (or None): A dictionary containing title, director and actors (if found),
                         otherwise None on error or no results.
    """
    # Busco en el apartado de la API search/movie 
    base_url = 'https://api.themoviedb.org/3'
    search_url = f'{base_url}/search/movie?query={title}&api_key={api_key}'

    try:
        data = requests.get(search_url).json()

        if not data.get('results'):
            print(f"'{title}', no retorna resultados.")
            return None

        for movie in data['results']: # data devuelve una lista con las películas que coinciden con el título
            if movie['title'] == title: # Con el título rescato especificamente la que quiero
                movie_id = movie['id']

                credits_url = f'{base_url}/movie/{movie_id}/credits?api_key={api_key}'
                credits_response = requests.get(credits_url) # Rescato los créditos mediante el id de la película
                credits_data = credits_response.json()

                director = None
                actors = [] # Lista para guardar los actores
                # Busco el id del director dentro del atributo crew
                for crew in credits_data['crew']: #crew puede devolver más de 1 dato
                    if crew['job'] == 'Director': 
                        director = crew['id']
                        break
                # Busco los actores
                for cast in credits_data['cast']:
                    if len(actors) < 5: # Tomo los primeros 5 actores
                        actors.append(cast['name'])
                    else:
                        break
                # Busco las 5 películas más populares del director
                directors_movies = get_top_director_movies(director, api_key)
                # Retorno con toda la información
                return {
                    'overview': movie['overview'],
                    'director': directors_movies,
                    'dir_name': credits_data['crew'][0]['name'],
                    'poster': movie['poster_path'],
                    'actors': actors,
                    'languaje': movie['original_language'],
                    'rating': movie['vote_average']
                }
            else:
                print(f"\nLo siento, '{title}' no se encontró en los resultados.")
                print("\nQuizá te referías a:\n")
                data['results'].sort(key=lambda x: x['vote_average'], reverse=True) # Ordeno las películas por rating
                for i, movie in enumerate(data['results'], 1):
                    print(f"{i}. {movie['title']} - {movie['release_date']}, Voto: {movie['vote_average']}")
                print("\nPor favor, intenta de nuevo con uno de los títulos de arriba.\n")
                return None
            
    except Exception as e:
        print(f"Error retrieving details for '{title}': {e}")
        return None

def get_top_director_movies(director_id, api_key):
    """
    Devuelve las 5 películas más populares de un director.

    Args:
        director (str): Nombre del director.
        api_key (str): Tmdb key.

    Returns:
        list (or None): A list of dictionaries containing movie details (if found),
                        otherwise None on error or no results.
                        (Debe compartir una lista con las 5 peliculas más populares del director, ordenadas de mayor a menor popularidad.)
    """

    try:
        director_movies_url = f'https://api.themoviedb.org/3/person/{director_id}/movie_credits?api_key={api_key}'
        director_movies_response = requests.get(director_movies_url).json()
        movies = director_movies_response.get('crew', []) # Devuelve una lista con las peliculas del mismo director
        director_movies = [
            {
                'title': movie['title'],
                'popularity': movie['popularity'],
                'rating': movie['vote_average'],
                'release_date': movie['release_date']
            }
            for movie in movies if movie['job'] == 'Director' # Rescato las películas donde el director es el mismo
        ]
        # Ordenar las películas por popularidad de mayor a menor
        director_movies.sort(key=lambda x: x['rating'], reverse=True)
        # Tomar las 10 películas más populares
        top_director_movies = director_movies[:5]
        return top_director_movies

    except Exception as e:
        print(f"Error retrieving movies for '{director_id}': {e}")
        return None

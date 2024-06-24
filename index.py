from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Lista para almacenar los animes agregados por el usuario
my_anime_list = []

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '')

    if query:
        response = requests.get('https://api.jikan.moe/v4/anime', params={'q': query, 'page': page})
    else:
        response = requests.get(f'https://api.jikan.moe/v4/anime?page={page}')
    
    data = response.json()
    animes = data.get('data', [])

    pagination = data.get('pagination', {})
    current_page = pagination.get('current_page', 1)
    has_next_page = pagination.get('has_next_page', False)

    prev_page = current_page - 1 if current_page > 1 else None
    next_page = current_page + 1 if has_next_page else None

    return render_template('home.html', animes=animes, prev_page=prev_page, next_page=next_page, query=query)

@app.route('/add-to-list', methods=['POST'])
def add_to_list():
    anime_id = request.form['anime_id']
    # Aquí deberías obtener el anime de la API con el ID si es necesario
    response = requests.get(f'https://api.jikan.moe/v4/anime/{anime_id}')
    anime_data = response.json()

    # Añadir el anime completo a la lista personal
    my_anime_list.append({
        'id': anime_id,
        'title': anime_data.get('title', ''),
        'synopsis': anime_data.get('synopsis', ''),
        'image_url': anime_data.get('images', {}).get('jpg', {}).get('image_url', '')
    })
    return redirect(url_for('home'))

@app.route('/my-anime-list')
def my_anime_list_page():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de elementos por página

    # Implementar paginación para la lista personal de animes
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_list = my_anime_list[start_idx:end_idx]

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if end_idx < len(my_anime_list) else None

    return render_template('added.html', my_anime_list=paginated_list, prev_page=prev_page, next_page=next_page)

if __name__ == '__main__':
    app.run(debug=True)

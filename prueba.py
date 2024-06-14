import requests
import flet as ft

# Función para obtener datos de la API de Pokémon
def fetch_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Función para mostrar los datos del Pokémon en una aplicación Flet
def main(page: ft.Page):
    page.title = "Pokémon Data Fetcher"

    def search_pokemon(e):
        pokemon_name = name_input.value
        data = fetch_pokemon_data(pokemon_name)
        if data:
            name_label.value = f"Name: {data['name'].capitalize()}"
            index_label.value = f"Index: {data['id']}"
            height_label.value = f"Height: {data['height']}"
            weight_label.value = f"Weight: {data['weight']}"
            abilities = ", ".join([ability['ability']['name'] for ability in data['abilities']])
            abilities_label.value = f"Abilities: {abilities}"
            sprite.src = data['sprites']['front_default']
        else:
            name_label.value = "Pokémon not found!"
            index_label.value = ""
            height_label.value = ""
            weight_label.value = ""
            abilities_label.value = ""
            sprite.src = ""

        page.update()

    name_input = ft.TextField(label="Enter Pokémon name")
    search_button = ft.ElevatedButton(text="Search", on_click=search_pokemon)
    name_label = ft.Text()
    index_label = ft.Text()
    height_label = ft.Text()
    weight_label = ft.Text()
    abilities_label = ft.Text()
    sprite = ft.Image()

    page.add(
        name_input,
        search_button,
        name_label,
        index_label,
        height_label,
        weight_label,
        abilities_label,
        sprite
    )

ft.app(target=main)

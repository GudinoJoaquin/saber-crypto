from flask import Flask, jsonify, render_template_string
from pycoingecko import CoinGeckoAPI

app = Flask(__name__)

# Crea una instancia del cliente de CoinGecko
cg = CoinGeckoAPI()

# Plantilla HTML como string
html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Criptomonedas</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #282A36; /* Fondo oscuro */
            color: #F8F8F2; /* Texto claro */
        }
    </style>
</head>
<body>
    <div class="container mx-auto py-10">
        <h1 class="text-3xl font-bold text-center mb-5">Lista de Criptomonedas</h1>
        <div id="crypto-table" class="overflow-x-auto">
            <!-- La tabla de criptomonedas se llenará aquí -->
        </div>
    </div>

    <script>
        // Función para cargar criptomonedas
        async function loadCryptos() {
            const response = await fetch('/cryptos');
            const data = await response.json();
            const table = document.createElement('table');
            table.className = 'min-w-full bg-gray-800 text-white';
            table.innerHTML = `
                <thead>
                    <tr>
                        <th class="px-4 py-2">#</th>
                        <th class="px-4 py-2">Nombre</th>
                        <th class="px-4 py-2">Precio USD</th>
                        <th class="px-4 py-2">Cambio 24h</th>
                        <th class="px-4 py-2">Cap. de Mercado</th>
                        <th class="px-4 py-2">Volumen 24h</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(coin => `
                        <tr class="hover:bg-gray-700">
                            <td class="border px-4 py-2">${coin.rank}</td>
                            <td class="border px-4 py-2">${coin.name} (${coin.symbol})</td>
                            <td class="border px-4 py-2">$${coin.price_usd}</td>
                            <td class="border px-4 py-2">${coin.change_24h.toFixed(2)}%</td>
                            <td class="border px-4 py-2">$${coin.market_cap.toFixed(2)}</td>
                            <td class="border px-4 py-2">$${coin.volume_24h.toFixed(2)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;
            document.getElementById('crypto-table').appendChild(table);
        }

        // Cargar criptomonedas al cargar la página
        window.onload = loadCryptos;
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Renderiza la plantilla HTML desde el string
    return render_template_string(html_template)

@app.route('/cryptos', methods=['GET'])
def cryptos():
    # Utiliza el cliente de CoinGecko para obtener los datos de criptomonedas
    cryptos = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=250, page=1, sparkline=False)

    # Selecciona solo los campos relevantes para enviarlos en formato JSON
    simplified_data = [
        {
            'rank': crypto['market_cap_rank'],
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'price_usd': crypto['current_price'],
            'change_24h': crypto['price_change_percentage_24h'],
            'market_cap': crypto['market_cap'],
            'volume_24h': crypto['total_volume']
        }
        for crypto in cryptos
    ]
    
    return jsonify(simplified_data)

if __name__ == '__main__':
    app.run(debug=True)

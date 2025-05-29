from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Données d'exemple
df = pd.DataFrame({
    "Fruit": ["Pommes", "Oranges", "Bananes"],
    "Quantité": [4, 1, 2]
})

# Créer un graphique à barres
fig = px.bar(df, x="Fruit", y="Quantité", title="Quantité de fruits")

# Initialiser l'application Dash
app = Dash(__name__)

# Définir le layout
app.layout = html.Div([
    html.H1("Mon premier dashboard Dash"),
    dcc.Graph(id="graphique-fruits", figure=fig)
])

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
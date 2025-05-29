from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Données d'exemple
df = pd.DataFrame({
    "Produit": ["Pommes", "Pommes", "Oranges", "Oranges", "Bananes", "Bananes"],
    "Région": ["Nord", "Sud", "Nord", "Sud", "Nord", "Sud"],
    "Ventes": [100, 150, 80, 120, 200, 180]
})

# Initialiser l'application Dash
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dashboard des Ventes de Fruits"),
    dcc.Dropdown(
        id="dropdown-region",
        options=[{"label": region, "value": region} for region in df["Région"].unique()],
        value="Nord",
        style={"width": "50%"}
    ),
    dcc.Graph(id="graphique-ventes")
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output("graphique-ventes", "figure"),
    Input("dropdown-region", "value")
)
def update_graph(selected_region):
    filtered_df = df[df["Région"] == selected_region]
    fig = px.bar(filtered_df, x="Produit", y="Ventes", title=f"Ventes dans la région {selected_region}")
    return fig

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
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
        options=[{"label": "Toutes", "value": "Toutes"}] + [{"label": region, "value": region} for region in df["Région"].unique()],
        value="Nord",  # Valeur par défaut
        style={"width": "50%", "margin-bottom": "10px"},
        placeholder="Sélectionner une région"
    ),
    dcc.Dropdown(
        id="dropdown-produit",
        options=[{"label": produit, "value": produit} for produit in df["Produit"].unique()],
        value="Oranges",  # Valeur par défaut
        style={"width": "50%"},
        placeholder="Sélectionner un produit"
    ),
    dcc.Graph(id="graphique-ventes")
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output("graphique-ventes", "figure"),
    Input("dropdown-region", "value"),
    Input("dropdown-produit", "value")
)
def update_graph(selected_region, selected_product):
    # Vérifier si les dropdowns ont des valeurs
    if selected_region is None or selected_product is None:
        return {
            "data": [],
            "layout": {
                "title": "Veuillez sélectionner une région et un produit",
                "xaxis": {"title": "Produit"},
                "yaxis": {"title": "Ventes"}
            }
        }
    
    # Filtrer selon la région et le produit
    if selected_region == "Toutes":
        filtered_df = df[df["Produit"] == selected_product]
    else:
        filtered_df = df[(df["Région"] == selected_region) & (df["Produit"] == selected_product)]
    
    # Gérer les cas où le DataFrame est vide
    if filtered_df.empty:
        return {
            "data": [],
            "layout": {
                "title": f"Aucune donnée pour {selected_product} dans la région {selected_region}",
                "xaxis": {"title": "Produit"},
                "yaxis": {"title": "Ventes"}
            }
        }
    
    # Créer le graphique
    fig = px.bar(
        filtered_df,
        x="Région" if selected_region == "Toutes" else "Produit",
        y="Ventes",
        title=f"Ventes de {selected_product} {'dans toutes les régions' if selected_region == 'Toutes' else 'dans la région ' + selected_region}"
    )
    return fig

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
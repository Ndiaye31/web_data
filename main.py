from dash import Dash, html, dcc, Input, Output, callback_context
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
    html.Label("Sélectionner une région :"),
    dcc.Dropdown(
        id="dropdown-region",
        options=[{"label": "Toutes", "value": "Toutes"}] + [{"label": region, "value": region} for region in df["Région"].unique()],
        value="Nord",
        style={"width": "50%", "margin-bottom": "10px"},
        clearable=False,
        placeholder="Sélectionner une région"
    ),
    html.Label("Sélectionner un produit :"),
    dcc.Dropdown(
        id="dropdown-produit",
        options=[{"label": "Toutes", "value": "Toutes"}] + [{"label": produit, "value": produit} for produit in df["Produit"].unique()],
        value="Oranges",
        style={"width": "50%", "margin-bottom": "10px"},
        clearable=False,
        placeholder="Sélectionner un produit"
    ),
    html.Button("Réinitialiser", id="reset-button", n_clicks=0, style={"margin-top": "10px"}),
    html.Div(id="reset-message", style={"color": "green", "margin-top": "10px"}),
    dcc.Interval(id="reset-timer", interval=3000, n_intervals=0, disabled=True),
    dcc.Graph(id="graphique-ventes")
])

# Callback pour mettre à jour le graphique, les dropdowns et le message
@app.callback(
    Output("graphique-ventes", "figure"),
    Output("dropdown-region", "value"),
    Output("dropdown-produit", "value"),
    Output("reset-message", "children"),
    Output("reset-timer", "disabled"),
    Input("dropdown-region", "value"),
    Input("dropdown-produit", "value"),
    Input("reset-button", "n_clicks"),
    Input("reset-timer", "n_intervals")
)
def update_graph(selected_region, selected_product, n_clicks, n_intervals):
    ctx = callback_context
    reset_message = ""
    timer_disabled = True
    
    # Réinitialiser si le bouton est cliqué
    if ctx.triggered_id == "reset-button":
        selected_region = "Toutes"
        selected_product = "Toutes"
        reset_message = "Filtres réinitialisés !"
        timer_disabled = False
    elif ctx.triggered_id == "reset-timer":
        reset_message = ""
        timer_disabled = True
    
    # Vérifier si les dropdowns ont des valeurs
    if selected_region is None or selected_product is None:
        return {
            "data": [],
            "layout": {
                "title": "Veuillez sélectionner une région et un produit",
                "xaxis": {"title": "Produit"},
                "yaxis": {"title": "Ventes"}
            }
        }, selected_region, selected_product, reset_message, timer_disabled
    
    # Filtrer selon la région et le produit
    if selected_region == "Toutes" and selected_product == "Toutes":
        filtered_df = df
    elif selected_region == "Toutes":
        filtered_df = df[df["Produit"] == selected_product]
    elif selected_product == "Toutes":
        filtered_df = df[df["Région"] == selected_region]
    else:
        filtered_df = df[(df["Région"] == selected_region) & (df["Produit"] == selected_product)]
    
    # Gérer les cas où le DataFrame est vide
    if filtered_df.empty:
        return {
            "data": [],
            "layout": {
                "title": f"Aucune vente enregistrée pour {selected_product} dans la région {selected_region}",
                "xaxis": {"title": "Produit"},
                "yaxis": {"title": "Ventes"}
            }
        }, selected_region, selected_product, reset_message, timer_disabled
    
    # Créer le graphique
    fig = px.bar(
        filtered_df,
        x="Produit" if selected_product == "Toutes" else "Région",
        y="Ventes",
        title=f"Ventes de {'tous les produits' if selected_product == 'Toutes' else selected_product} "
              f"{'dans toutes les régions' if selected_region == 'Toutes' else 'dans la région ' + selected_region}"
    )
    return fig, selected_region, selected_product, reset_message, timer_disabled

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
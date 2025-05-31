from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Données d'exemple (commerce international)
df = pd.DataFrame({
    "Pays": ["France", "France", "Allemagne", "Allemagne", "Italie", "Italie"],
    "Catégorie": ["Voitures", "Vins", "Voitures", "Machines", "Vins", "Machines"],
    "Exportations": [500, 300, 800, 600, 200, 400]
})

# Initialiser l'application Dash
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Dashboard du Commerce International"),
    html.Label("Sélectionner un pays :"),
    dcc.Dropdown(
        id="dropdown-pays",
        options=[{"label": "Toutes", "value": "Toutes"}] + [{"label": pays, "value": pays} for pays in df["Pays"].unique()],
        value="Toutes",
        style={"width": "50%", "margin-bottom": "10px"},
        clearable=False,
        placeholder="Sélectionner un pays"
    ),
    dcc.Graph(id="graphique-barres"),
    html.Label("Détails des exportations par catégorie :"),
    dcc.Graph(id="graphique-scatter")
])

# Callback pour mettre à jour les graphiques
@app.callback(
    Output("graphique-barres", "figure"),
    Output("graphique-scatter", "figure"),
    Input("graphique-barres", "clickData"),
    Input("dropdown-pays", "value")
)
def update_graphs(click_data, selected_pays):
    # Graphique à barres (exportations totales par pays)
    if selected_pays == "Toutes":
        df_bar = df.groupby("Pays")["Exportations"].sum().reset_index()
    else:
        df_bar = df[df["Pays"] == selected_pays].groupby("Pays")["Exportations"].sum().reset_index()
    fig_bar = px.bar(df_bar, x="Pays", y="Exportations", title="Exportations totales par pays")
    
    # Graphique scatter (détails par catégorie pour le pays sélectionné)
    if click_data is None and selected_pays == "Toutes":
        return fig_bar, {
            "data": [],
            "layout": {
                "title": "Cliquez sur un pays ou sélectionnez un pays dans le dropdown",
                "xaxis": {"title": "Catégorie"},
                "yaxis": {"title": "Exportations"}
            }
        }
    
    # Déterminer le pays à afficher dans le scatter
    if click_data is not None:
        pays = click_data["points"][0]["x"]
    elif selected_pays != "Toutes":
        pays = selected_pays
    else:
        return fig_bar, {
            "data": [],
            "layout": {
                "title": "Cliquez sur un pays ou sélectionnez un pays dans le dropdown",
                "xaxis": {"title": "Catégorie"},
                "yaxis": {"title": "Exportations"}
            }
        }
    
    filtered_df = df[df["Pays"] == pays]
    fig_scatter = px.scatter(filtered_df, x="Catégorie", y="Exportations", 
                            title=f"Exportations de {pays} par catégorie",
                            size="Exportations", color="Catégorie")
    
    return fig_bar, fig_scatter

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
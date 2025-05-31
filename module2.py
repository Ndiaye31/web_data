from dash import Dash, html, dcc, Input, Output, callback_context
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
    html.Button("Réinitialiser", id="reset-button", n_clicks=0, style={"margin-top": "10px"}),
    html.Div("Filtres réinitialisés !", id="reset-message", style={
        "color": "green",
        "margin-top": "10px",
        "transition": "opacity 0.5s ease-out",
        "opacity": 0
    }),
    dcc.Interval(id="reset-timer", interval=3000, n_intervals=0, disabled=True),
    dcc.Graph(id="graphique-barres"),
    html.Label("Détails des exportations par catégorie :"),
    dcc.Graph(id="graphique-scatter")
])

# Callback pour mettre à jour les graphiques
@app.callback(
    Output("graphique-barres", "figure"),
    Output("graphique-scatter", "figure"),
    Output("dropdown-pays", "value"),
    Output("reset-message", "style"),
    Output("reset-timer", "disabled"),
    Output("reset-timer", "interval"),
    Input("graphique-barres", "clickData"),
    Input("dropdown-pays", "value"),
    Input("reset-button", "n_clicks"),
    Input("reset-timer", "n_intervals")
)
def update_graphs(click_data, selected_pays, n_clicks, n_intervals):
    ctx = callback_context
    message_style = {"color": "green", "margin-top": "10px", "transition": "opacity 0.5s ease-out", "opacity": 0}
    timer_disabled = True
    duree = 3000  # Durée par défaut (en ms)
    
    # Réinitialiser si le bouton est cliqué
    if ctx.triggered_id == "reset-button":
        selected_pays = "Toutes"
        message_style["opacity"] = 1
        timer_disabled = False
    elif ctx.triggered_id == "reset-timer":
        message_style["opacity"] = 0
        timer_disabled = True
    
    # Graphique à barres (exportations totales par pays)
    if selected_pays == "Toutes":
        df_bar = df.groupby("Pays")["Exportations"].sum().reset_index()
    else:
        df_bar = df[df["Pays"] == selected_pays].groupby("Pays")["Exportations"].sum().reset_index()
    fig_bar = px.bar(df_bar, x="Pays", y="Exportations", title="Exportations totales par pays")
    
    # Graphique scatter (détails par catégorie pour le pays sélectionné)
    if click_data is None and selected_pays == "Toutes":
        fig_scatter = {
            "data": [],
            "layout": {
                "title": "Cliquez sur un pays ou sélectionnez un pays dans le dropdown",
                "xaxis": {"title": "Catégorie"},
                "yaxis": {"title": "Exportations"}
            }
        }
    else:
        # Déterminer le pays à afficher dans le scatter
        if click_data is not None:
            pays = click_data["points"][0]["x"]
        else:
            pays = selected_pays
        
        filtered_df = df[df["Pays"] == pays]
        fig_scatter = px.scatter(filtered_df, x="Catégorie", y="Exportations", 
                                title=f"Exportations de {pays} par catégorie",
                                size="Exportations", color="Catégorie")
    
    return fig_bar, fig_scatter, selected_pays, message_style, timer_disabled, duree

# Lancer l'application
if __name__ == "__main__":
    app.run(debug=True)
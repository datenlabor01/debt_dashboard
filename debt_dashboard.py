import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd

df_22 = pd.read_excel("https://github.com/datenlabor01/debt_dashboard/raw/main/debt_data_2022.xlsx")
df_22["Year"] = "2022"
df_23 = pd.read_excel("https://github.com/datenlabor01/debt_dashboard/raw/main/debt_data_2023.xlsx")
df_23["Year"] = "2023"
df_24 = pd.read_excel("https://github.com/datenlabor01/debt_dashboard/raw/main/debt_data_2024.xlsx")
df_24["Year"] = "2024"

df_debt = pd.concat([df_22, df_23, df_24])
df_debt = df_debt[["Classification Name", "Country Name", "Data", "Year"]]
df_debt = df_debt.rename(columns={'Classification Name': 'CreditorName', 'Country Name': 'country'})
#df_debt.to_excel("wb_debtdata.xlsx")

debt_africa = pd.read_excel("https://github.com/datenlabor01/debt_dashboard/raw/main/Africa_Debt_Database_2023_NEU.xlsx", sheet_name=1)

app = Dash(external_stylesheets = [dbc.themes.ZEPHYR])

creditor_dropdown = dcc.Dropdown(id = "creditor", options = sorted(df_debt["CreditorName"].unique()), value = "All", style = {"textAlign": "center"},
                               clearable=True, multi=True, searchable=True, placeholder='Land auswählen')

#Dropdown for Africa-tab:
color_dropdown = dcc.Dropdown(id = "yaxis", options = ["CreditorAgency", "country", "CreditorGroup"],
                                value="country", style = {"textAlign": "center"}, clearable=False, multi=False,
                                searchable= True, placeholder='Dimension für y-Achse auswählen')

value_dropdown = dcc.Dropdown(id = "dimension", options = ["Amount_musd", "interest", "maturity", "grace"],
                                value="Amount_musd", style = {"textAlign": "center"}, clearable=False, multi=False,
                                searchable= True, placeholder='Dimension für y-Achse auswählen')

borrower_dropdown = dcc.Dropdown(id = "borrower", options = sorted(debt_africa["CreditorName"].unique()), value = "All", style = {"textAlign": "center"},
                               clearable=True, multi=True, searchable=True, placeholder='Land auswählen')

map_view = dcc.RadioItems(id = "map_view", options=['Schuldner-Ansicht', 'Gläubiger-Ansicht'], value='Gläubiger-Ansicht', inline=True,
                          className="btn-group d-flex", labelClassName="btn btn-outline-info")

text2 = "Diese Anwendung wird als Prototyp vom BMZ Datenlabor angeboten. Sie kann Fehler enthalten und ist als alleinige Entscheidungsgrundlage nicht geeignet. Außerdem können Prototypen ausfallen oder kurzfristig von uns verändert werden. Sichern Sie daher wichtige Ergebnisse per Screenshot oder Export. Die Anwendung ist vorerst intern und sollte daher nicht ohne Freigabe geteilt werden. Wenden Sie sich bei Fragen gerne an datenlabor@bmz.bund.de"

app.layout = html.Div([
     dbc.Row([
         html.Div(html.Img(src="https://github.com/datenlabor01/LS/raw/main/logo.png", style={'height':'80%', 'width':'20%'})),
         html.H1(children='Prototyp Schulden-Dashboard'),
         html.P(children = "Dies ist ein Prototyp, der Fehler enthalten kann. Es zeigt die Daten der Debt Suspension Initiative von IMF/Weltbank an sowie des Africa Debt Database vom IFW-Kiel.\
          Über die Buttons kann zwischen Gläubiger und Schuldner Ansicht gewechselt werden: Unter Gläubiger werden bei Auswahl eines Landes Staaten angezeigt, an die das Land Darlehen vergeben hat.\
           Bei Schuldner zeigt es die Länder an, von denen das Land Darlehen erhalten hat.")],
         style={'textAlign': 'center'}),

    #App button:
     dbc.Row([
       dbc.Button(children = "Über diese App", id = "textbutton", color = "light", className = "me-1",
                    n_clicks=0, style={'textAlign': 'center', "width": "30rem"})
      ], justify = "center"),
     dbc.Row([
       dbc.Collapse(dbc.Card(dbc.CardBody([
         dbc.Badge(text2, className="text-wrap")])),
         id="collapse", style={'textAlign': 'center', "width": "60rem"}, is_open=False),
      ], justify = "center"),

     dbc.Row([
       dbc.Col([html.Br(), map_view], width=6)], justify = "center"),

    dcc.Tabs([
        dcc.Tab(label='Global', children=[

            dbc.Row([
              html.P("Diesen Datensatz unterhalten IMF und Weltbank. Es schlüsselt öffentliche Schulden nach Gläubiger-Ländern auf\
                     und erlaubt so eine Übersicht zu Darlehen von Staaten an andere Staaten. Es umfasst nur Staaten, die an der Debt Service Suspension Initiative teilnehmen\
                      und ihre Darlehen an IMF melden. Auf dieser Basis errechnen Weltbank und IMF Prognosen für zukünftige Jahre. \
                      Mehr Informationen und den Datensatz gibt es unter https://www.worldbank.org/en/programs/debt-statistics/dssi."),
                dbc.Col([html.Br(), creditor_dropdown], width=6)], justify = "center"),

            dbc.Row([
                dcc.Graph(id='line', style={'textAlign': 'center'}),
                ]),

            dbc.Row([
                dcc.Graph(id='tree', style={'textAlign': 'center'}),
                ]),
            ]),

        dcc.Tab(label="Schuldenanalyse in Afrika", children = [

            dbc.Row([
              html.P(dcc.Markdown('''Diesen Datensatz hat das Kieler Institut für Weltwirtschaftsforschung im April 2023 aus diversen Quellen zusammengestellt. Es enthält Informationen zu\
                     Darlehen, die afrikanische Länder aufgenommen haben, teils mit Details zu den Darlehenskonditionen. Mehr Informationen dazu sind auf der [Projektwebseite](https://www.ifw-kiel.de/publications/kiel-working-papers/2022/who-lends-to-africa-and-how-introducing-the-africa-debt-database-17146)\
                     Mit dem ersten Dropdown-Menü lässt sich das Schuldner oder Gläubiger auswählen (je nach Button-Auswahl), mit dem zweiten Dropdown-Menü lässt sich die dargestellte Kategorie einstellen. Das dritte Dropdown-Menü passt die Dimension nach verliehener Betrag (Summe), Zinssatz, zahlungsfreie Zeit und Laufzeit (alle Durchschnitt) an.''')),
                dbc.Col([html.Br(), borrower_dropdown,
                         html.Br(), color_dropdown], width=6)], justify = "center"),

            dbc.Row([
                dcc.Graph(id = "africa_line", style={'textAlign': 'center'}),
            ]),

            dbc.Row([
                dbc.Col([html.Br(), value_dropdown], width=6)], justify = "center"),

            dbc.Row([
                dcc.Graph(id = "africa_map", style={'textAlign': 'center'}),
                ]),
            ]),
    ]),
])

#Button to display text:
@app.callback(
    Output("collapse", "is_open"),
    [Input("textbutton", "n_clicks")],
    [State("collapse", "is_open")],
)

def collapse(n, is_open):
   if n:
      return not is_open
   return is_open

#Callback for dropdown:
@app.callback(
    [Output('borrower', 'options'), Output('creditor', 'options')],
    Input("map_view", "value"),
)

def update_dropdown(view):
  if view == "Gläubiger-Ansicht":
      col = "CreditorName"
  else:
      col = "country"
  return sorted(debt_africa[col].unique()), sorted(df_debt[col].unique())

@app.callback(
    [Output('line', 'figure'), Output('tree', 'figure')],
    [Input("creditor", "value"), Input("map_view", "value")],
)

def update_graph_1(creditor, view):

  if view == "Gläubiger-Ansicht":
      col = "CreditorName"
  else:
      col = "country"

  if (creditor != "All") & (creditor != []):
    dat = df_debt[df_debt[col].isin(creditor)]
    log_bol = False
    if col == "CreditorName":
      col = "country"
    else:
      col = "CreditorName"
  else:
    dat = df_debt
    log_bol = True

  df_tree = dat.groupby([col])[["Data"]].sum().reset_index()
  figTree = px.treemap(df_tree, path=[px.Constant("All"), col], values = "Data", template = "simple_white")

  #Line graphs:
  df_line = dat.groupby(["Year", col])["Data"].sum().reset_index()
  figLine = px.line(df_line, x="Year", y= "Data", color = col, log_y = log_bol, template = "simple_white")

  return figLine, figTree

#callback for Africa tab:
@app.callback(
    [Output('africa_line', 'figure'), Output('africa_map', 'figure')],
    [Input("borrower", "value"), Input("yaxis", "value"),
     Input("dimension", "value"), Input("map_view", "value")],
)

def update_africa(borrower, yaxis, value, view):

  if view == "Gläubiger-Ansicht":
      col = "CreditorName"
  else:
      col = "country"

  if (borrower != "All") & (borrower != []):
    dat_afr = debt_africa[debt_africa[col].isin(borrower)]
    if col == "CreditorName":
      col = "country"
    else:
      col = "CreditorName"
  else:
    dat_afr = debt_africa

  if value == "Amount_musd":
    dfafr_map = dat_afr.groupby([col])[value].sum().reset_index()
    dfafr_line = dat_afr.groupby(["year", yaxis])[value].sum().reset_index()
  else:
    dfafr_map = dat_afr.groupby([col])[value].mean().reset_index()
    dfafr_line = dat_afr.groupby(["year", yaxis])[value].mean().reset_index()

  figLine_Afr = px.line(dfafr_line, x="year", y= value, color = yaxis, template = "simple_white")
  figLine_Afr.update_traces(connectgaps=False)
  fig_map_Afr = px.choropleth(dfafr_map, locations = col, locationmode="country names",
                        color_continuous_scale="Fall", color = value, projection="natural earth")

  return figLine_Afr, fig_map_Afr

if __name__ == '__main__':
    app.run_server(debug=True)

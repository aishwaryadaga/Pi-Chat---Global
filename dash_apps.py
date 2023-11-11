import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np

def create_dash_app1(server):

    app =dash.Dash(server=server, url_base_pathname="/dash1/")

    app.layout = html.Div(children=[
    html.H1("Hello Dash!"),
    html.A("Main Page", href="/main", style={"color": "blue", "textDecoration": "underline"}),
    html.Div("Dash: Web Dashboards with Python"),
    dcc.Graph(id="example",
            figure={"data":[
            {"x":[1,2,3],"y":[4,1,2],"type":"bar","name":"SF"},
            {"x":[1,2,3],"y":[2,4,5],"type":"bar","name":"NYC"}
            ],
                "layout":{
                    "title":"BAR PLOTS!"
                }})
    ])
    return app

def create_dash_app2(server):

    app =dash.Dash(server=server, url_base_pathname="/dash2/")

    colors = {"background" : "#111111","text":"#7FDBFF"}



    app.layout = html.Div(children=[
        html.H1("Hello Dash!",style={"textAlign":"centre",
                                    "color":colors["text"]}),
        html.A("Main Page", href="/main", style={"color": "blue", "textDecoration": "underline"}),
        dcc.Graph(id="example",
                figure={"data":[
                {"x":[1,2,3],"y":[4,1,2],"type":"bar","name":"SF"},
                {"x":[1,2,3],"y":[2,4,5],"type":"bar","name":"NYC"}
                ],
                    "layout":{
                        "plot_bgcolor":colors["background"],
                        "paper_bgcolor":colors["background"],
                        "font":{"color":colors["text"]},
                        "title":"BAR PLOTS!"
                    }})
    ],style={"backgrounColor":colors["background"]}

    )
    return app

def create_dash_app3(server):
    app =dash.Dash(server=server, url_base_pathname="/dash3/")

    np.random.seed(42)
    random_x = np.random.randint(1,101,100)
    random_y = np.random.randint(1,101,100)

    app.layout = html.Div([
                        html.A("Main Page", href="/main", style={"color": "blue", "textDecoration": "underline"}),
                        dcc.Graph(id="scatterplot",
                            figure={"data":[
                                go.Scatter(
                                    x=random_x,
                                    y=random_y,
                                    mode="markers",
                                    marker = {
                                        "size":12,
                                        "color":"rgb(51,204,153)",
                                        "symbol":"pentagon",
                                        "line":{"width":2}
                                    }
                                )],
                                    "layout":go.Layout(title="My Scatterplot",
                                        xaxis = {"title":"Some x title"})}
                        ),
                        dcc.Graph(id="scatterplot2",
                        figure={"data":[
                            go.Scatter(
                                x=random_x,
                                y=random_y,
                                mode="markers",
                                marker = {
                                    "size":12,
                                    "color":"rgb(200,204,53)",
                                    "symbol":"pentagon",
                                    "line":{"width":2}
                                }
                            )],
                        "layout":go.Layout(title="Second plot",
                                            xaxis = {"title":"Some x title"})}
                        )])
    return app

# def create_dash_app4(server):

#     app =dash.Dash(server=server, url_base_pathname="/dash4/")

#     app.layout = html.Div(["This is the outermost div!",
#                             html.Div(["This is an inner div!"],
#                             style={"color":"red","border":"2px red solid"}),
#                             html.Div(["Another inner div!"],
#                             style={"color":"blue","border":"3px blue solid"}),
#                             html.A("Main Page", href="/main", style={"color": "blue", "textDecoration": "underline"}),],
                            
#                         style={"color":"green","border":"2px green solid"})
#     return app

# def create_dash_app5(server):

#     app =dash.Dash(server=server, url_base_pathname="/dash5/")

#     app.layout = html.Div([
#                 html.A("Main Page", href="/main", style={"color": "blue", "textDecoration": "underline"}),
#                 html.Label("Dropdown"),
#                 dcc.Dropdown(options=[{"label":"New York City",
#                                         "value":"NYC"},
#                                         {"label":"San Francisco",
#                                         "value":"SF"}],
#                             value="SF"),
                
#                 html.Label("Slider"),
#                 dcc.Slider(min=-10,max=10,step=0.5,value=0,
#                             marks={i: i for i in range(-10,10)}),
                
#                 html.P(html.Label("Some Radio Items")),
#                 dcc.RadioItems(options=[{"label":"New York City",
#                                         "value":"NYC"},
#                                         {"label":"San Francisco",
#                                         "value":"SF"}],
#                             value="SF")
#     ])
#     return app
# if __name__ == "__main__":
#     app = create_dash_app1()
#     app.run_server(debug=True, port=5802)



import numpy as np
import plotly.graph_objects as go

def plot_swings(results):
    buyMarkers = [x for x in results['markers'] if x['score'] == 1]
    sellMarkers = [x for x in results['markers'] if x['score'] == -1]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=results['dataset']['date'],
     open=results['dataset']['open'],
     high=results['dataset']['high'],
     low=results['dataset']['low'],
     close=results['dataset']['close'],
     name="Price"))

    fig.add_trace(go.Scatter(
            x=[x['date'] for x in buyMarkers],
            y=[x['price'] for x in buyMarkers],
            mode='markers',
            name='Scores',
            text = "BUY",
            line_color='yellow'))

    fig.add_trace(go.Scatter(
            x=[x['date'] for x in sellMarkers],
            y=[x['price'] for x in sellMarkers],
            mode='markers',
            name='Scores',
            text = "SELL",
            line_color='purple'))

    fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False)

    return fig

def plot_structure(results):
    fig = plot_swings(results)
    for obj in results['structures']:
        fig.add_shape(type="rect",
            x0=obj['start'], y0=obj['top'], x1=obj['end'], y1=obj['bottom'],
            line=dict(color="rgba(189, 0, 189, 1)"),
            fillcolor="rgba(189, 0, 189, 0.1)"
        )

    fig.show()
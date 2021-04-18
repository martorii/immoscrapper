import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def plot_true_vs_pred(y_test, y_pred):
    line_x0 = 0
    line_y0 = 0
    line_xn = max(np.max(y_pred), np.max(y_pred))
    line_yn = line_xn
    x_line = [line_x0, line_xn]
    y_line = [line_y0, line_yn]

    fig = go.Figure()

    y_test_flatten = np.asarray(y_test).flatten()
    y_pred_flatten = np.asarray(y_pred).flatten()
    # Add traces
    fig.add_trace(go.Scatter(x=y_pred_flatten, y=y_test_flatten,
                             mode='markers',
                             name='property'))
    fig.add_trace(go.Scatter(x=x_line, y=y_line,
                             mode='lines',
                             name='baseline'))
    fig.update_yaxes(title='real')
    fig.update_xaxes(title='prediction')

    fig.show()
    return

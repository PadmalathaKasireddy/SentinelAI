"""Plotly charts for dashboard analytics."""

import plotly.express as px
import plotly.graph_objects as go


def pie_threat_distribution(counts: dict) -> go.Figure:
    if not counts:
        counts = {"Safe": 1, "Suspicious": 0, "Dangerous": 0}
    fig = px.pie(
        names=list(counts.keys()),
        values=list(counts.values()),
        color_discrete_sequence=["#2ed573", "#ffa502", "#ff4757"],
        hole=0.45,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        margin=dict(t=30, b=20, l=20, r=20),
        showlegend=True,
    )
    return fig


def bar_module_usage(by_module: dict) -> go.Figure:
    if not by_module:
        by_module = {"demo": 0}
    fig = px.bar(
        x=list(by_module.keys()),
        y=list(by_module.values()),
        labels={"x": "Module", "y": "Scans"},
        color=list(by_module.values()),
        color_continuous_scale=["#00d4aa", "#00b894"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        coloraxis_showscale=False,
        margin=dict(t=30, b=20, l=20, r=20),
    )
    return fig


def gauge_confidence(value: float, title: str = "Confidence") -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value * 100,
            title={"text": title, "font": {"color": "#e6edf3"}},
            number={"suffix": "%", "font": {"color": "#00d4aa"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00d4aa"},
                "bgcolor": "#161b22",
                "steps": [
                    {"range": [0, 33], "color": "rgba(46, 213, 115, 0.35)"},
                    {"range": [33, 66], "color": "rgba(255, 165, 2, 0.35)"},
                    {"range": [66, 100], "color": "rgba(255, 71, 87, 0.35)"},
                ],
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e6edf3",
        height=220,
        margin=dict(t=40, b=10, l=30, r=30),
    )
    return fig

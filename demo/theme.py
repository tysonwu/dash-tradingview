"""Console tokens and layout primitives for the hosted demo.

Mirrors `assets/stylesheet.css`. The chart canvas is drawn by JavaScript and
cannot read CSS custom properties, so the values the charts need are repeated
here as Python constants. Keep the two files in step.

Structure is monochrome; colour is reserved for meaning. Chart series therefore
draw from the semantic palette (up/down, classification), never from decorative
hues.
"""
from dash import html

# Structural tokens, dark console layer.
BACKGROUND = '#121316'
CARD = '#1b1e24'
SECONDARY = '#252a32'
ACCENT = '#0f1115'
BORDER = '#4a5162'
FOREGROUND = '#eef0f7'
MUTED_FOREGROUND = '#9aa1b1'

# Hairline grid, a low-alpha border rather than a separate hue.
GRID_LINE = 'rgba(74, 81, 98, 0.32)'

# Semantic and data palette.
RED = '#ff453a'
GREEN = '#30d158'
BLUE = '#0a84ff'
ORANGE = '#ff9f0a'
YELLOW = '#ffd60a'
PURPLE = '#bf5af2'
INDIGO = '#5e5ce6'
TEAL = '#40cbe0'
CYAN = '#64d2ff'
MINT = '#63e6e2'
PINK = '#ff375f'

FONT_MONO = "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace"

# Loaded so the charts render in IBM Plex rather than the canvas default.
FONTS = ('https://fonts.googleapis.com/css2'
         '?family=IBM+Plex+Mono:wght@400;500;600'
         '&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap')

# Base chart options every panel starts from. Individual panels override only
# the option they exist to demonstrate.
CHART_OPTIONS = {
    'layout': {
        'background': {'type': 'solid', 'color': CARD},
        'textColor': MUTED_FOREGROUND,
        'fontSize': 10,
        'fontFamily': FONT_MONO,
    },
    'grid': {
        'vertLines': {'visible': True, 'color': GRID_LINE},
        'horzLines': {'visible': True, 'color': GRID_LINE},
    },
    'rightPriceScale': {'borderColor': BORDER},
    'timeScale': {'borderColor': BORDER},
    'crosshair': {
        'vertLine': {'color': BORDER, 'labelBackgroundColor': SECONDARY},
        'horzLine': {'color': BORDER, 'labelBackgroundColor': SECONDARY},
    },
    'localization': {'locale': 'en-US'},
}


def merge(*layers):
    """Shallow-merge option layers one key deep, so a panel can override
    `layout.textColor` without restating the rest of `layout`."""
    out = {}
    for layer in layers:
        for key, value in layer.items():
            if isinstance(value, dict) and isinstance(out.get(key), dict):
                out[key] = {**out[key], **value}
            else:
                out[key] = value
    return out


def topbar(title, context):
    """Fixed thin utility bar carrying the app name and system context."""
    return html.Header(className='topbar', children=[
        html.Div(className='topbar-inner', children=[
            html.Span(title, className='topbar-title'),
            html.Span(context, className='topbar-context'),
        ]),
    ])


def panel(title, meta, *children):
    """Flat bordered panel with a tonal header strip. No shadow, no radius."""
    return html.Section(className='panel', children=[
        html.Div(className='panel-head', children=[
            html.Span(title, className='panel-title'),
            html.Span(meta, className='panel-meta'),
        ]),
        html.Div(className='panel-body', children=list(children)),
    ])


def prose(*children):
    return html.Div(className='prose', children=list(children))


def toolbar(*buttons):
    return html.Div(className='toolbar', children=list(buttons))


def button(label, component_id):
    return html.Button(label, id=component_id, className='btn', n_clicks=0)

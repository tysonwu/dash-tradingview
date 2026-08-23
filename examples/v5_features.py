"""What lightweight-charts v5 makes possible from Dash.

Two halves. The first needs no component support at all: `chartOptions` and
`series[].options` are handed straight to `applyOptions`, so any option the
installed library understands is already reachable from Python. The second
exercises the props added to the component for v5: panes, streaming appends,
two-way range control, history paging and the pointer events.

Run from the repository root:

    PYTHONPATH=. python examples/v5_features.py
"""
import copy
from datetime import date, timedelta

from dash import (MATCH, Dash, Input, Output, State, callback, ctx, dcc, html,
                  no_update)

import dash_tvlwc
import theme
from data_generator import (generate_intraday_series, generate_random_ohlc,
                            generate_random_series)
from dash_tvlwc.types import MismatchDirection
from theme import CHART_OPTIONS, merge

LINE = generate_random_series(v0=100, n=40)
OHLC = generate_random_ohlc(v0=100, n=60)
TICKS = generate_random_series(v0=2500, n=90)
# Conflation merges points that would occupy under half a pixel. Two things have
# to be true before it can engage at all, and both are easy to miss:
#
#   1. There must be more points on screen than half-pixels of width.
#   2. `minBarSpacing` must be below 0.5, because it defaults to exactly 0.5 and
#      so pins the chart at the conflation threshold no matter how far you zoom.
#
# The panel therefore opens already zoomed out, via a small `barSpacing`, instead
# of asking anyone to scroll several hundred wheel steps to get there.
DENSE_POINTS = 50_000
DENSE = generate_intraday_series(v0=100, n=DENSE_POINTS)

# Each entry builds one panel. `states` are cycled by the panel's button; the
# button label always names the option value currently applied.
FEATURES = {
    'linetype': {
        'title': 'Curved lines',
        'meta': 'series[].options.lineType',
        'note': 'LineType.Curved is new in v5. 0 = Simple, 1 = WithSteps, 2 = Curved.',
        'series': {'id': 'price', 'type': 'line', 'data': LINE,
                   'options': {'color': theme.CYAN, 'lineWidth': 2}},
        'states': [
            {'label': 'lineType: Simple', 'series_options': {'lineType': 0}},
            {'label': 'lineType: Curved', 'series_options': {'lineType': 2}},
            {'label': 'lineType: WithSteps', 'series_options': {'lineType': 1}},
        ],
    },
    'magnet': {
        'title': 'Crosshair magnet',
        'meta': 'chartOptions.crosshair.mode',
        'note': 'Hover a candle. MagnetOHLC snaps to any of the four values; '
                'Magnet only ever snaps to close.',
        'series': {'id': 'price', 'type': 'candlestick', 'data': OHLC,
                   'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                               'borderVisible': False,
                               'wickUpColor': theme.GREEN,
                               'wickDownColor': theme.RED}},
        'states': [
            {'label': 'mode: Magnet', 'chart': {'crosshair': {'mode': 1}}},
            {'label': 'mode: MagnetOHLC', 'chart': {'crosshair': {'mode': 3}}},
            {'label': 'mode: Normal', 'chart': {'crosshair': {'mode': 0}}},
        ],
    },
    'pricescale': {
        'title': 'Price scale ticks',
        'meta': 'tickMarkDensity, ensureEdgeTickMarksVisible',
        'note': 'The name is back to front: a higher value means more spacing '
                'and so fewer tick marks. Default is 2.5. Edge ticks force '
                'labels at the very top and bottom of the scale.',
        'series': {'id': 'price', 'type': 'area', 'data': TICKS,
                   'options': {'lineColor': theme.BLUE, 'lineWidth': 2,
                               'topColor': 'rgba(10, 132, 255, 0.30)',
                               'bottomColor': 'rgba(10, 132, 255, 0.02)'}},
        'states': [
            {'label': 'tickMarkDensity: 2.5 (default)',
             'chart': {'rightPriceScale': {'tickMarkDensity': 2.5}}},
            {'label': 'tickMarkDensity: 1 (more ticks)',
             'chart': {'rightPriceScale': {'tickMarkDensity': 1}}},
            {'label': 'tickMarkDensity: 5 (fewer ticks)',
             'chart': {'rightPriceScale': {'tickMarkDensity': 5}}},
            {'label': '+ ensureEdgeTickMarksVisible',
             'chart': {'rightPriceScale': {
                 'tickMarkDensity': 5, 'ensureEdgeTickMarksVisible': True,
                 'minimumWidth': 90}}},
        ],
    },
    'timescale': {
        'title': 'Time scale labels',
        'meta': 'allowBoldLabels, uniformDistribution',
        'note': 'Bold labels mark period boundaries. Uniform distribution spaces '
                'tick marks evenly instead of by significance.',
        'series': {'id': 'price', 'type': 'line', 'data': TICKS,
                   'options': {'color': theme.MINT, 'lineWidth': 2}},
        'states': [
            {'label': 'bold labels on', 'chart': {'timeScale': {
                'allowBoldLabels': True, 'uniformDistribution': False}}},
            {'label': 'bold off, uniform on', 'chart': {'timeScale': {
                'allowBoldLabels': False, 'uniformDistribution': True}}},
        ],
    },
    'conflation': {
        'title': 'Conflation',
        'meta': f'timeScale.enableConflation, {DENSE_POINTS:,} points',
        'note': 'Needs minBarSpacing under its 0.5 default, or the chart cannot '
                'zoom past the threshold and the option does nothing. Factor 1 '
                'is performance-focused; factor 8 conflates eight times earlier '
                'and visibly smooths the line.',
        'chart_base': {'timeScale': {
            'timeVisible': True, 'secondsVisible': False,
            # Open zoomed out, and allow zooming past the conflation threshold.
            'barSpacing': 0.01, 'minBarSpacing': 0.005}},
        'series': {'id': 'price', 'type': 'line', 'data': DENSE,
                   'options': {'color': theme.ORANGE, 'lineWidth': 1,
                               'priceLineVisible': False}},
        'states': [
            {'label': 'enableConflation: False',
             'chart': {'timeScale': {'enableConflation': False}}},
            {'label': 'conflation on, factor 1',
             'chart': {'timeScale': {'enableConflation': True,
                                     'conflationThresholdFactor': 1}}},
            {'label': 'conflation on, factor 8',
             'chart': {'timeScale': {'enableConflation': True,
                                     'conflationThresholdFactor': 8}}},
        ],
    },
    'attribution': {
        'title': 'Attribution logo',
        'meta': 'chartOptions.layout.attributionLogo',
        'note': 'A rendering option only. Apache-2.0 requires the NOTICE file to '
                'accompany redistribution, which the wheel ships regardless.',
        'series': {'id': 'price', 'type': 'baseline', 'data': LINE,
                   'options': {'baseValue': {'type': 'price', 'price': 100},
                               'topLineColor': theme.GREEN,
                               'topFillColor1': 'rgba(48, 209, 88, 0.28)',
                               'topFillColor2': 'rgba(48, 209, 88, 0.02)',
                               'bottomLineColor': theme.RED,
                               'bottomFillColor1': 'rgba(255, 69, 58, 0.02)',
                               'bottomFillColor2': 'rgba(255, 69, 58, 0.28)'}},
        'states': [
            {'label': 'attributionLogo: True',
             'chart': {'layout': {'attributionLogo': True}}},
            {'label': 'attributionLogo: False',
             'chart': {'layout': {'attributionLogo': False}}},
        ],
    },
}


# --------------------------------------------------------------------------
# Capability panels. These exercise props that had to be added to the component,
# so unlike the panels above they are not pure option pass-through.
# --------------------------------------------------------------------------

CONSOLE_PANES = {'panes': {'enableResize': True,
                           'separatorColor': theme.BORDER,
                           'separatorHoverColor': theme.CYAN}}


def ohlc_bar(previous_close, when, swing=3.0):
    import math
    import random
    o = previous_close
    c = o + random.uniform(-swing, swing)
    return {'time': when, 'open': o, 'close': c,
            'high': max(o, c) + abs(math.sin(o)) * 0.8,
            'low': min(o, c) - abs(math.cos(o)) * 0.8}


def next_day(iso):
    return (date.fromisoformat(iso) + timedelta(days=1)).isoformat()


# Panes: three series sharing one time scale.
PANE_PRICE = generate_random_ohlc(v0=100, n=220)
PANE_VOLUME = [{'time': p['time'], 'value': 400 + (i % 29) * 30,
                'color': ('rgba(48,209,88,0.6)' if p['close'] >= p['open']
                          else 'rgba(255,69,58,0.6)')}
               for i, p in enumerate(PANE_PRICE)]
PANE_MACD = [{'time': p['time'], 'value': p['close'] - PANE_PRICE[max(0, i - 12)]['close']}
             for i, p in enumerate(PANE_PRICE)]

PANE_SERIES = [
    {'id': 'px', 'type': 'candlestick', 'data': PANE_PRICE, 'pane': 0,
     'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                 'borderVisible': False, 'wickUpColor': theme.GREEN,
                 'wickDownColor': theme.RED}},
    {'id': 'vol', 'type': 'histogram', 'data': PANE_VOLUME, 'pane': 1,
     'options': {'priceFormat': {'type': 'volume'}, 'priceLineVisible': False,
                 'lastValueVisible': False}},
    {'id': 'macd', 'type': 'line', 'data': PANE_MACD, 'pane': 2,
     'options': {'color': theme.PURPLE, 'lineWidth': 2,
                 'priceLineVisible': False}},
]

# Streaming: starts short so appended bars are obvious.
STREAM_SEED = generate_random_ohlc(v0=100, n=60)

# History paging: the full series exists server-side, and only a window of it is
# ever sent. Scrolling left past the edge asks for more.
HISTORY_MASTER = generate_random_ohlc(v0=100, n=1500)
HISTORY_WINDOW = 150

# Line-shaped copies of the pane data, for the panels that want a single series.
PANE_PRICE_LINE = [{'time': p['time'], 'value': p['close']} for p in PANE_PRICE]
PANE_PRICE_LINE_B = [{'time': p['time'], 'value': p['close'] * 0.85 + 12}
                     for p in PANE_PRICE]

# Point queries: short enough that popping five bars off the end is visible.
QUERY_DATA = generate_random_series(v0=80, n=60)

# Markers anchored to a price rather than to a bar.
MARKER_DATA = generate_random_series(v0=50, n=70)
MARKER_MID = sum(p['value'] for p in MARKER_DATA) / len(MARKER_DATA)


def readout(*pairs):
    return html.Div(className='readout', children=[
        html.Div(className='readout-row', children=[
            html.Span(k, className='readout-key'),
            html.Span(v, className='readout-value'),
        ]) for k, v in pairs
    ])


def capability_chart(component_id, series, options=None, height=240, **kwargs):
    return dash_tvlwc.Tvlwc(
        id=component_id, series=series, width='100%', height=height,
        chartOptions=merge(CHART_OPTIONS, options or {}), **kwargs)


panes_panel = html.Div(className='wide', children=[theme.panel(
    'Panes', 'series[].pane, paneOptions',
    capability_chart(
        'panes-chart', PANE_SERIES,
        merge({'layout': CONSOLE_PANES}, {'timeScale': {'borderColor': theme.BORDER}}),
        height=440,
        paneOptions=[{'stretchFactor': 3}, {'stretchFactor': 1}, {'stretchFactor': 1}],
    ),
    html.P('Panes stack vertically and share one time scale, which is the '
           'shared-x-axis subplot people have been asking for. Drag a separator: '
           'layout.panes.enableResize only has something to act on now that a '
           'second pane can exist. Moving a series between panes uses moveToPane, '
           'so its data and markers survive the move.', className='note'),
    theme.toolbar(
        theme.button('move MACD to pane 1', 'panes-move'),
        theme.button('stretch 3:1:1', 'panes-stretch'),
        theme.button('fixed heights', 'panes-fixed'),
    ),
)])


stream_panel = theme.panel(
    'Streaming append', 'tick',
    capability_chart('stream-chart', [
        {'id': 'px', 'type': 'candlestick', 'data': STREAM_SEED,
         'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                     'borderVisible': False, 'wickUpColor': theme.GREEN,
                     'wickDownColor': theme.RED}}],
        subscribeVisibleRange=True, reportThrottle=80),
    html.P('tick appends through series.update, which leaves the visible range '
           'alone. Zoom in, then append: the view does not jump. Rewriting the '
           'whole series prop instead would reset it. A list of ticks costs one '
           'prop write, and historicalUpdate amends a bar that is not the last.',
           className='note'),
    html.Div(id='stream-readout'),
    dcc.Interval(id='stream-timer', interval=700, disabled=True),
    dcc.Store(id='stream-state', data={'last': STREAM_SEED[-1]['time'],
                                       'close': STREAM_SEED[-1]['close'],
                                       'count': len(STREAM_SEED)}),
    theme.toolbar(
        theme.button('append 1', 'stream-one'),
        theme.button('append 5', 'stream-batch'),
        theme.button('amend previous bar', 'stream-amend'),
        theme.button('start live', 'stream-live'),
    ),
)


range_panel = theme.panel(
    'Visible range control', 'visibleRange, visibleLogicalRange',
    capability_chart('range-chart', [
        {'id': 'px', 'type': 'area', 'data': PANE_PRICE,
         'options': {'lineColor': theme.BLUE, 'lineWidth': 2,
                     'topColor': 'rgba(10,132,255,0.30)',
                     'bottomColor': 'rgba(10,132,255,0.02)'}}],
        subscribeVisibleRange=True, reportThrottle=80),
    html.P('Both range props are two-way: read them to follow the user, write '
           'them to drive the chart. The component records what it last emitted '
           'and ignores that value coming back, so writing does not feed itself.',
           className='note'),
    html.Div(id='range-readout'),
    theme.toolbar(
        theme.button('bars 0-40', 'range-first'),
        theme.button('bars 150-200', 'range-last'),
        theme.button('by date', 'range-dates'),
    ),
)


history_panel = theme.panel(
    'History paging', 'barsInLogicalRange',
    capability_chart('history-chart', [
        {'id': 'px', 'type': 'line', 'data': HISTORY_MASTER[-HISTORY_WINDOW:],
         'options': {'color': theme.MINT, 'lineWidth': 2}}],
        subscribeVisibleRange=True, reportThrottle=120),
    html.P('Scroll left. barsInLogicalRange reports how much data lies either '
           'side of the view; when barsBefore runs low the callback prepends '
           'another slice. The payload is a small fixed object, so this works '
           'where shipping the whole dataset back would not.', className='note'),
    html.Div(id='history-readout'),
    dcc.Store(id='history-loaded', data=HISTORY_WINDOW),
    theme.toolbar(theme.button('reset to newest 150', 'history-reset')),
)


pointer_panel = theme.panel(
    'Pointer events', 'subscribeDblClick, click payload',
    capability_chart('pointer-chart', [
        {'id': 'px', 'type': 'candlestick', 'data': PANE_PRICE[-90:],
         'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                     'borderVisible': False, 'wickUpColor': theme.GREEN,
                     'wickDownColor': theme.RED}}],
        subscribeClick=True, subscribeDblClick=True, reportThrottle=0),
    html.P('Double click anywhere to drop a price line at the cursor. The click '
           'payload carries the price under the pointer on each series scale, '
           'not just the bar values, which is what makes annotating from Python '
           'possible at all. paneIndex says which pane was hit.', className='note'),
    html.Div(id='pointer-readout'),
    theme.toolbar(theme.button('clear price lines', 'pointer-clear')),
)


marker_panel = theme.panel(
    'Price-anchored markers', "position: 'atPriceMiddle'",
    capability_chart('marker-chart', [
        {'id': 'px', 'type': 'line', 'data': MARKER_DATA,
         'options': {'color': theme.CYAN, 'lineWidth': 2},
         'markers': []}]),
    html.P('v5 markers can sit at an arbitrary price rather than above or below '
           'a bar, and carry an id that comes back through the click payload. '
           'Both are plain data fields, so they needed no component change.',
           className='note'),
    theme.toolbar(
        theme.button('bar-anchored', 'marker-bar'),
        theme.button('price-anchored', 'marker-price'),
    ),
)


# Up/down markers only work on line and area series.
UPDOWN_SEED = generate_random_series(v0=100, n=50)

scroll_panel = theme.panel(
    'Time scale commands', 'timeScaleAction',
    capability_chart('scroll-chart', [
        {'id': 'px', 'type': 'line', 'data': PANE_PRICE_LINE,
         'options': {'color': theme.BLUE, 'lineWidth': 2}}],
        subscribeVisibleRange=True, reportThrottle=80),
    html.P('These are commands, not state, so a repeat needs a changing nonce: '
           'a prop set to the value it already holds gives the component nothing '
           'to react to. Each button sends its n_clicks as that nonce, which is '
           'why pressing the same one twice still works.', className='note'),
    html.Div(id='scroll-readout'),
    theme.toolbar(
        theme.button('fitContent', 'scroll-fit'),
        theme.button('scrollToRealTime', 'scroll-real'),
        theme.button('resetTimeScale', 'scroll-reset'),
        theme.button('scrollToPosition(-40)', 'scroll-pos'),
    ),
)


query_panel = theme.panel(
    'Point queries', 'dataAction, dataResult',
    capability_chart('query-chart', [
        {'id': 'px', 'type': 'line', 'data': QUERY_DATA,
         'options': {'color': theme.PURPLE, 'lineWidth': 2}}]),
    html.P('Dash cannot call a method and take its return value, so each of '
           'these is a command prop in and a result prop out. All three answers '
           'are O(1), which is the whole reason they are allowed on the wire: a '
           'query proportional to the dataset would just be a slow way to ship '
           'back data Python already has. dataByIndex reads one bar, lastValue '
           'reads the last price and the colour it is drawn in, and pop removes '
           'bars from the end and reports what it removed. pop leaves the chart '
           'holding less than series[].data describes, exactly as tick leaves it '
           'holding more; reset writes series again to make the prop the whole '
           'truth once more.', className='note'),
    html.Div(id='query-readout'),
    theme.toolbar(
        theme.button('dataByIndex(0)', 'query-first'),
        theme.button('dataByIndex(9999)', 'query-past'),
        theme.button('dataByIndex(9999, nearestLeft)', 'query-left'),
        theme.button('lastValue', 'query-last'),
        theme.button('pop(5)', 'query-pop'),
        theme.button('reset data', 'query-reset'),
    ),
)


crosshair_panel = html.Div(className='wide', children=[theme.panel(
    'Crosshair sync', 'crosshairPosition',
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
                    'gap': '8px'}, children=[
        capability_chart('sync-a', [
            {'id': 'px', 'type': 'line', 'data': PANE_PRICE_LINE,
             'options': {'color': theme.CYAN, 'lineWidth': 2}}],
            subscribeCrosshair=True, reportThrottle=0, height=210),
        capability_chart('sync-b', [
            {'id': 'px', 'type': 'line', 'data': PANE_PRICE_LINE_B,
             'options': {'color': theme.ORANGE, 'lineWidth': 2}}],
            subscribeCrosshair=True, reportThrottle=0, height=210),
    ]),
    html.P('Hover either chart and the other follows. Placing the crosshair from '
           'Python routes through a synthetic position that skips the crosshair '
           'event, so two charts pointed at each other do not feed back. This '
           'round trips through the server, which is why it lags; the same wiring '
           'as a clientside callback is instant.', className='note'),
    html.Div(id='sync-readout'),
)])


updown_panel = theme.panel(
    'Streaming markers', 'series[].upDownMarkers',
    capability_chart('updown-chart', [
        {'id': 'px', 'type': 'line', 'data': UPDOWN_SEED,
         'options': {'color': theme.MINT, 'lineWidth': 2},
         'upDownMarkers': {'positiveColor': theme.GREEN,
                           'negativeColor': theme.RED,
                           'updateVisibilityDuration': 2500}}],
        subscribeVisibleRange=False),
    html.P('A plugin that flashes a marker on each tick, coloured by direction. '
           'Line and area series only. Data has to be routed through the plugin '
           'rather than the series, or it never learns which way the value '
           'moved, so the component does that for you.', className='note'),
    html.Div(id='updown-readout'),
    dcc.Interval(id='updown-timer', interval=900, disabled=True),
    dcc.Store(id='updown-state', data={'last': UPDOWN_SEED[-1]['time'],
                                       'value': UPDOWN_SEED[-1]['value'],
                                       'count': 0}),
    theme.toolbar(
        theme.button('tick up', 'updown-up'),
        theme.button('tick down', 'updown-down'),
        theme.button('start live', 'updown-live'),
        theme.button('markers off', 'updown-toggle'),
    ),
)


watermark_panel = theme.panel(
    'Watermarks', 'watermark',
    capability_chart('watermark-chart', [
        {'id': 'px', 'type': 'area', 'data': PANE_PRICE_LINE,
         'options': {'lineColor': theme.PURPLE, 'lineWidth': 2,
                     'topColor': 'rgba(191,90,242,0.30)',
                     'bottomColor': 'rgba(191,90,242,0.02)'}}]),
    html.P('The v5 replacement for the old watermark chart option. Text '
           'watermarks take multiple lines, each with its own size and colour; '
           'image watermarks have no v3 equivalent at all. Give centred text a '
           'lineHeight, because the vertical centring computes a text height '
           'from it and there is no default.', className='note'),
    theme.toolbar(
        theme.button('text, one line', 'wm-one'),
        theme.button('text, two lines', 'wm-two'),
        theme.button('image', 'wm-image'),
        theme.button('none', 'wm-none'),
    ),
)


screenshot_panel = theme.panel(
    'Screenshot', 'screenshotRequest, screenshot',
    capability_chart('shot-chart', [
        {'id': 'px', 'type': 'candlestick', 'data': PANE_PRICE[-70:],
         'options': {'upColor': theme.GREEN, 'downColor': theme.RED,
                     'borderVisible': False, 'wickUpColor': theme.GREEN,
                     'wickDownColor': theme.RED}}]),
    html.P('A command prop answered by a read-back prop, which is the only shape '
           'a method call can take across the Dash boundary. The PNG comes back '
           'as a data URI, so it can be shown, stored, or handed to dcc.Download.',
           className='note'),
    html.Div(id='shot-readout'),
    html.Img(id='shot-preview', style={'width': '100%', 'marginTop': '8px',
                                       'border': f'1px solid {theme.BORDER}'}),
    theme.toolbar(theme.button('capture', 'shot-take')),
)


def initial_options(feature):
    return merge(CHART_OPTIONS,
                 feature.get('chart_base', {}),
                 feature['states'][0].get('chart', {}))


def initial_series(feature):
    series = copy.deepcopy(feature['series'])
    series['options'] = {**series.get('options', {}),
                         **feature['states'][0].get('series_options', {})}
    return [series]


def build_panel(name, feature):
    return theme.panel(
        feature['title'], feature['meta'],
        dash_tvlwc.Tvlwc(
            id={'type': 'chart', 'name': name},
            series=initial_series(feature),
            width='100%',
            height=230,
            chartOptions=initial_options(feature),
        ),
        html.P(feature['note'], className='note'),
        theme.toolbar(
            theme.button(feature['states'][0]['label'], {'type': 'toggle', 'name': name}),
        ),
    )


app = Dash(__name__, external_stylesheets=[theme.FONTS])
app.layout = html.Div([
    theme.topbar('v5 capabilities',
                 'lightweight-charts 5.2.1 · dash-tvlwc 0.2.0-dev'),
    html.Main(className='shell', children=[
        html.H1('What v5 makes possible from Dash', className='page-title'),
        theme.prose(html.P(
            'The first section needs no component support: chartOptions and '
            'series[].options are passed straight to applyOptions, so anything '
            'the installed lightweight-charts understands is already reachable. '
            'The second exercises props added to the component for v5.'
        )),
        html.H2('Options, no component support needed', className='section-title'),
        html.Div(className='panel-grid options-grid',
                 children=[build_panel(name, f) for name, f in FEATURES.items()]),

        html.H2('Capabilities added to the component', className='section-title'),
        html.Div(className='panel-grid capability-grid', children=[
            panes_panel, stream_panel, range_panel,
            history_panel, pointer_panel, marker_panel,
            scroll_panel, query_panel, updown_panel, watermark_panel,
            screenshot_panel, crosshair_panel,
        ]),
        html.H2('Not reachable this way', className='section-title'),
        theme.prose(html.Ul([
            html.Li([
                html.Code('layout.colorParsers'), ' and ',
                html.Code('autoscaleInfoProvider'),
                ' take functions, and a function cannot cross a JSON prop '
                'boundary. Naming one registered on window.dashTvlwcFunctions is '
                'the only route, and then the logic is JavaScript rather than '
                'Python.',
            ]),
            html.Li([
                html.Code('layout.colorSpace'), " set to 'display-p3' is applied, "
                'but the difference only shows on a wide-gamut display, so there '
                'is nothing to demonstrate on most screens.',
            ]),
            html.Li([
                html.Code('series[].options.hitTestTolerance'), ' and ',
                html.Code('crosshair.doNotSnapToHiddenSeriesIndices'),
                ' both work, but only change which series the crosshair reports, '
                'so they need subscribeCrosshair and a readout to see.',
            ]),
            html.Li([
                'Pane and series primitives, and custom series, are classes '
                'implementing canvas render callbacks. Nothing about them '
                'serialises, so the plugin layer stays out of reach.',
            ]),
        ])),
    ]),
])


@callback(
    Output({'type': 'chart', 'name': MATCH}, 'chartOptions'),
    Output({'type': 'chart', 'name': MATCH}, 'series'),
    Output({'type': 'toggle', 'name': MATCH}, 'children'),
    Input({'type': 'toggle', 'name': MATCH}, 'n_clicks'),
    State({'type': 'chart', 'name': MATCH}, 'series'),
    prevent_initial_call=True,
)
def cycle_option(n_clicks, series):
    """One callback serves every panel, matched on the panel name."""
    feature = FEATURES[ctx.triggered_id['name']]
    state = feature['states'][n_clicks % len(feature['states'])]

    chart_options = merge(CHART_OPTIONS,
                          feature.get('chart_base', {}),
                          state.get('chart', {}))

    if 'series_options' not in state:
        # Leave `series` untouched rather than round-tripping it. The conflation
        # panel holds 20k points and there is no reason to copy them.
        return chart_options, no_update, state['label']

    series = copy.deepcopy(series)
    series[0]['options'] = {**series[0]['options'], **state['series_options']}
    return chart_options, series, state['label']



# --------------------------------------------------------------------------
# Capability callbacks. One per panel, because each drives a different prop.
# --------------------------------------------------------------------------

@callback(
    Output('panes-chart', 'series'),
    Output('panes-chart', 'paneOptions'),
    Input('panes-move', 'n_clicks'),
    Input('panes-stretch', 'n_clicks'),
    Input('panes-fixed', 'n_clicks'),
    State('panes-chart', 'series'),
    prevent_initial_call=True,
)
def panes_controls(move, stretch, fixed, series):
    if ctx.triggered_id == 'panes-move':
        out = [dict(spec) for spec in series]
        # Changing `pane` moves the series; it is not recreated, so its data
        # and options survive.
        out[2] = {**out[2], 'pane': 1 if move % 2 else 2}
        return out, no_update
    if ctx.triggered_id == 'panes-stretch':
        ratios = [{'stretchFactor': 1}] * 3 if stretch % 2 else [
            {'stretchFactor': 3}, {'stretchFactor': 1}, {'stretchFactor': 1}]
        return no_update, ratios
    return no_update, [{'height': 240}, {'height': 100}, {'height': 100}]


@callback(
    Output('stream-chart', 'tick'),
    Output('stream-state', 'data'),
    Output('stream-timer', 'disabled'),
    Output('stream-live', 'children'),
    Input('stream-one', 'n_clicks'),
    Input('stream-batch', 'n_clicks'),
    Input('stream-amend', 'n_clicks'),
    Input('stream-live', 'n_clicks'),
    Input('stream-timer', 'n_intervals'),
    State('stream-state', 'data'),
    State('stream-timer', 'disabled'),
    prevent_initial_call=True,
)
def stream_controls(one, batch, amend, live, ticks, state, paused):
    if ctx.triggered_id == 'stream-live':
        running = paused
        return no_update, no_update, not running, ('stop live' if running
                                                   else 'start live')

    if ctx.triggered_id == 'stream-amend':
        # historicalUpdate rewrites a bar that is not the last one. Without it,
        # update() would treat an older timestamp as out of order.
        when = state['last']
        amended = ohlc_bar(state['close'], when, swing=6.0)
        return ({'id': 'px', 'bar': amended, 'historicalUpdate': True},
                state, no_update, no_update)

    count = 5 if ctx.triggered_id == 'stream-batch' else 1
    bars, when, close = [], state['last'], state['close']
    for _ in range(count):
        when = next_day(when)
        bar = ohlc_bar(close, when)
        close = bar['close']
        bars.append(bar)

    payload = ([{'id': 'px', 'bar': b} for b in bars] if count > 1
               else {'id': 'px', 'bar': bars[0]})
    return (payload,
            {'last': when, 'close': close, 'count': state['count'] + count},
            no_update, no_update)


@callback(
    Output('stream-readout', 'children'),
    Input('stream-state', 'data'),
    Input('stream-chart', 'visibleLogicalRange'),
)
def stream_readout(state, logical):
    span = '-' if not logical else f"{logical['from']:.1f} .. {logical['to']:.1f}"
    return readout(('bars sent', str(state['count'])),
                   ('last time', str(state['last'])),
                   ('visible bars', span))


@callback(
    Output('range-chart', 'visibleLogicalRange'),
    Output('range-chart', 'visibleRange'),
    Input('range-first', 'n_clicks'),
    Input('range-last', 'n_clicks'),
    Input('range-dates', 'n_clicks'),
    prevent_initial_call=True,
)
def range_controls(first, last, dates):
    if ctx.triggered_id == 'range-first':
        return {'from': 0, 'to': 40}, no_update
    if ctx.triggered_id == 'range-last':
        return {'from': 150, 'to': 200}, no_update
    # setVisibleRange takes times in whatever form the series data uses.
    return no_update, {'from': PANE_PRICE[20]['time'], 'to': PANE_PRICE[70]['time']}


@callback(
    Output('range-readout', 'children'),
    Input('range-chart', 'visibleLogicalRange'),
    Input('range-chart', 'visibleRange'),
)
def range_readout(logical, times):
    lr = '-' if not logical else f"{logical['from']:.1f} .. {logical['to']:.1f}"
    tr = '-' if not times else f"{times['from']} .. {times['to']}"
    return readout(('visibleLogicalRange', lr), ('visibleRange', tr))


@callback(
    Output('history-chart', 'series'),
    Output('history-loaded', 'data'),
    Output('history-readout', 'children'),
    Output('history-chart', 'visibleLogicalRange'),
    Input('history-chart', 'barsInLogicalRange'),
    Input('history-reset', 'n_clicks'),
    State('history-loaded', 'data'),
    prevent_initial_call=True,
)
def history_controls(bars, reset, loaded):
    if ctx.triggered_id == 'history-reset':
        window = HISTORY_MASTER[-HISTORY_WINDOW:]
        # The view has to be reset along with the data. Shrinking the series
        # while still zoomed out leaves barsBefore deeply negative, and the
        # pager below would immediately load everything back.
        return ([{'id': 'px', 'type': 'line', 'data': window,
                  'options': {'color': theme.MINT, 'lineWidth': 2}}],
                HISTORY_WINDOW,
                readout(('loaded', str(HISTORY_WINDOW)), ('barsBefore', 'reset')),
                {'from': HISTORY_WINDOW - 40, 'to': HISTORY_WINDOW})

    before = (bars or {}).get('barsBefore')
    info = readout(('loaded', str(loaded)),
                   ('barsBefore', str(before)),
                   ('barsAfter', str((bars or {}).get('barsAfter'))))

    # Only fetch when the user has nearly scrolled off the left edge, and stop
    # once the whole series has been sent.
    if before is None or before > 20 or loaded >= len(HISTORY_MASTER):
        return no_update, no_update, info, no_update

    grown = min(loaded + HISTORY_WINDOW, len(HISTORY_MASTER))
    window = HISTORY_MASTER[-grown:]
    return ([{'id': 'px', 'type': 'line', 'data': window,
              'options': {'color': theme.MINT, 'lineWidth': 2}}],
            grown,
            readout(('loaded', f'{grown} (grown)'),
                    ('barsBefore', str(before)),
                    ('barsAfter', str((bars or {}).get('barsAfter')))),
            no_update)


@callback(
    Output('pointer-chart', 'series'),
    Output('pointer-readout', 'children'),
    Input('pointer-chart', 'click'),
    Input('pointer-chart', 'dblClick'),
    Input('pointer-clear', 'n_clicks'),
    State('pointer-chart', 'series'),
    prevent_initial_call=True,
)
def pointer_controls(click, dbl, clear, series):
    out = [dict(spec) for spec in series]

    if ctx.triggered_id == 'pointer-clear':
        out[0]['priceLines'] = []
        return out, readout(('price lines', '0'))

    # `ctx.triggered_id` is only the component id, so it cannot tell `click`
    # from `dblClick` on the same chart. The full prop_id can. A double click
    # fires both props in one batch, so look through the whole triggered list
    # and let the double click win rather than reading only the first entry.
    props = [entry['prop_id'] for entry in ctx.triggered]
    is_double = any(prop.endswith('.dblClick') for prop in props)
    source = dbl if is_double else click

    price = ((source or {}).get('price') or {}).get('px')
    rows = readout(
        ('event', 'dblClick' if is_double else 'click'),
        ('time', str((source or {}).get('time'))),
        ('paneIndex', str((source or {}).get('paneIndex'))),
        ('price at cursor', '-' if price is None else f'{price:.2f}'),
    )

    # A double click drops a price line where the pointer is. This is only
    # expressible because the payload carries the price under the cursor, which
    # is defined between bars where seriesData is not.
    if is_double and price is not None:
        lines = list(out[0].get('priceLines') or [])
        lines.append({'price': price, 'color': theme.ORANGE, 'lineStyle': 2,
                      'title': f'{price:.1f}', 'axisLabelVisible': True})
        out[0]['priceLines'] = lines
        return out, rows
    return no_update, rows


@callback(
    Output('marker-chart', 'series'),
    Input('marker-bar', 'n_clicks'),
    Input('marker-price', 'n_clicks'),
    State('marker-chart', 'series'),
    prevent_initial_call=True,
)
def marker_controls(bar_clicks, price_clicks, series):
    out = [dict(spec) for spec in series]
    if ctx.triggered_id == 'marker-bar':
        out[0]['markers'] = [
            {'id': 'buy', 'time': MARKER_DATA[20]['time'], 'position': 'belowBar',
             'color': theme.GREEN, 'shape': 'arrowUp', 'text': 'Buy'},
            {'id': 'sell', 'time': MARKER_DATA[45]['time'], 'position': 'aboveBar',
             'color': theme.RED, 'shape': 'arrowDown', 'text': 'Sell'},
        ]
    else:
        # `price` places the marker at a value of your choosing; the position
        # keyword only says how it sits relative to that price.
        out[0]['markers'] = [
            {'id': 'mid', 'time': MARKER_DATA[20]['time'],
             'position': 'atPriceMiddle', 'price': MARKER_MID,
             'color': theme.ORANGE, 'shape': 'circle', 'text': 'mean'},
            {'id': 'top', 'time': MARKER_DATA[45]['time'],
             'position': 'atPriceTop', 'price': MARKER_MID * 1.15,
             'color': theme.CYAN, 'shape': 'arrowDown', 'text': 'target'},
        ]
    return out



# A tiny inline SVG, so the image watermark needs no network fetch.
WATERMARK_IMAGE = (
    'data:image/svg+xml;utf8,'
    "<svg xmlns='http://www.w3.org/2000/svg' width='240' height='80'>"
    "<text x='0' y='58' font-family='monospace' font-size='54'"
    " fill='%23bf5af2'>tvlwc</text></svg>"
)


@callback(
    Output('scroll-chart', 'timeScaleAction'),
    Output('scroll-readout', 'children'),
    Input('scroll-fit', 'n_clicks'),
    Input('scroll-real', 'n_clicks'),
    Input('scroll-reset', 'n_clicks'),
    Input('scroll-pos', 'n_clicks'),
    prevent_initial_call=True,
)
def scroll_controls(fit, real, reset, pos):
    which = ctx.triggered_id
    # n_clicks doubles as the nonce, so pressing the same button twice still
    # produces a prop value the component has not seen before.
    if which == 'scroll-fit':
        action = {'action': 'fitContent', 'nonce': fit}
    elif which == 'scroll-real':
        action = {'action': 'scrollToRealTime', 'nonce': real}
    elif which == 'scroll-reset':
        action = {'action': 'resetTimeScale', 'nonce': reset}
    else:
        action = {'action': 'scrollToPosition', 'position': -40,
                  'animated': True, 'nonce': pos}
    return action, readout(('last action', action['action']),
                           ('nonce', str(action['nonce'])))


@callback(
    Output('query-chart', 'dataAction'),
    Output('query-chart', 'series'),
    Input('query-first', 'n_clicks'),
    Input('query-past', 'n_clicks'),
    Input('query-left', 'n_clicks'),
    Input('query-last', 'n_clicks'),
    Input('query-pop', 'n_clicks'),
    Input('query-reset', 'n_clicks'),
    State('query-chart', 'series'),
    prevent_initial_call=True,
)
def query_controls(first, past, left, last, pop, reset, series):
    which = ctx.triggered_id
    if which == 'query-reset':
        # `pop` mutated the chart without touching the prop, so rewriting
        # `series` is what puts the two back in agreement.
        fresh = copy.deepcopy(series)
        fresh[0]['data'] = QUERY_DATA
        return no_update, fresh

    # n_clicks doubles as the nonce, as elsewhere: these are commands, and a
    # prop reset to the value it already holds is not a change.
    if which == 'query-first':
        action = {'action': 'dataByIndex', 'seriesId': 'px',
                  'logicalIndex': 0, 'nonce': first}
    elif which == 'query-past':
        # No bar at 9999, and the default `none` says not to look for one.
        action = {'action': 'dataByIndex', 'seriesId': 'px',
                  'logicalIndex': 9999, 'nonce': past}
    elif which == 'query-left':
        action = {'action': 'dataByIndex', 'seriesId': 'px',
                  'logicalIndex': 9999,
                  'mismatchDirection': MismatchDirection.NearestLeft,
                  'nonce': left}
    elif which == 'query-last':
        action = {'action': 'lastValue', 'seriesId': 'px',
                  'globalLast': True, 'nonce': last}
    else:
        action = {'action': 'pop', 'seriesId': 'px', 'count': 5, 'nonce': pop}
    return action, no_update


@callback(
    Output('query-readout', 'children'),
    Input('query-chart', 'dataResult'),
)
def query_readout(result):
    if not result:
        return readout(('result', 'press a button'))
    rows = [('action', result['action'])]
    if result['action'] == 'dataByIndex':
        point = result['data']
        rows.append(('index', str(result['logicalIndex'])))
        rows.append(('data', 'None (no bar there)' if point is None
                     else f"{point['time']} · {point['value']:.2f}"))
    elif result['action'] == 'lastValue':
        if result['noData']:
            rows.append(('value', 'series is empty'))
        else:
            rows.append(('price', f"{result['price']:.2f}"))
            rows.append(('color', result['color']))
    else:
        removed = result['removed']
        rows.append(('asked for', str(result['count'])))
        # Newest first, so this is the bar that was on the right edge.
        rows.append(('removed', f"{len(removed)} bars, newest "
                                f"{removed[0]['time']}" if removed else 'none'))
    return readout(*rows)


@callback(
    Output('sync-b', 'crosshairPosition'),
    Output('sync-a', 'crosshairPosition'),
    Output('sync-readout', 'children'),
    Input('sync-a', 'crosshair'),
    Input('sync-b', 'crosshair'),
    prevent_initial_call=True,
)
def sync_crosshair(a, b):
    # Whichever chart the pointer is over drives the other one. Dash sees two
    # different props here, so the callback graph has no cycle, and the library
    # does not emit a crosshair event for a position set this way.
    source_is_a = any(entry['prop_id'].startswith('sync-a.')
                      for entry in ctx.triggered)
    event = a if source_is_a else b
    if not event or event.get('time') is None:
        return None, None, readout(('pointer', 'off chart'))

    price = (event.get('price') or {}).get('px')
    if price is None:
        return None, None, readout(('pointer', 'no price'))

    target = {'seriesId': 'px', 'price': price, 'time': event['time']}
    rows = readout(('driven by', 'left' if source_is_a else 'right'),
                   ('time', str(event['time'])),
                   ('price', f'{price:.2f}'))
    return (target, no_update, rows) if source_is_a else (no_update, target, rows)


@callback(
    Output('updown-chart', 'tick'),
    Output('updown-state', 'data'),
    Output('updown-timer', 'disabled'),
    Output('updown-live', 'children'),
    Input('updown-up', 'n_clicks'),
    Input('updown-down', 'n_clicks'),
    Input('updown-live', 'n_clicks'),
    Input('updown-timer', 'n_intervals'),
    State('updown-state', 'data'),
    State('updown-timer', 'disabled'),
    prevent_initial_call=True,
)
def updown_controls(up, down, live, ticks, state, paused):
    import random
    if ctx.triggered_id == 'updown-live':
        running = paused
        return no_update, no_update, not running, ('stop live' if running
                                                   else 'start live')

    if ctx.triggered_id == 'updown-up':
        step = abs(random.uniform(1, 4))
    elif ctx.triggered_id == 'updown-down':
        step = -abs(random.uniform(1, 4))
    else:
        step = random.uniform(-4, 4)

    when = next_day(state['last'])
    value = round(state['value'] + step, 2)
    return ({'id': 'px', 'bar': {'time': when, 'value': value}},
            {'last': when, 'value': value, 'count': state['count'] + 1},
            no_update, no_update)


@callback(
    Output('updown-chart', 'series'),
    Output('updown-toggle', 'children'),
    Input('updown-toggle', 'n_clicks'),
    State('updown-chart', 'series'),
    prevent_initial_call=True,
)
def updown_toggle(n, series):
    out = [dict(spec) for spec in series]
    if n % 2:
        out[0].pop('upDownMarkers', None)
        return out, 'markers on'
    out[0]['upDownMarkers'] = {'positiveColor': theme.GREEN,
                               'negativeColor': theme.RED,
                               'updateVisibilityDuration': 2500}
    return out, 'markers off'


@callback(
    Output('updown-readout', 'children'),
    Input('updown-state', 'data'),
)
def updown_readout(state):
    return readout(('ticks sent', str(state['count'])),
                   ('last value', str(state['value'])))


@callback(
    Output('watermark-chart', 'watermark'),
    Input('wm-one', 'n_clicks'),
    Input('wm-two', 'n_clicks'),
    Input('wm-image', 'n_clicks'),
    Input('wm-none', 'n_clicks'),
    prevent_initial_call=True,
)
def watermark_controls(one, two, image, none):
    which = ctx.triggered_id
    if which == 'wm-none':
        return None
    if which == 'wm-image':
        return {'imageUrl': WATERMARK_IMAGE, 'alpha': 0.35, 'padding': 20,
                'maxHeight': 90}
    if which == 'wm-one':
        return {'horzAlign': 'center', 'vertAlign': 'center',
                'lines': [{'text': 'DEMO', 'color': 'rgba(238,240,247,0.35)',
                           'fontSize': 64, 'lineHeight': 72,
                           'fontFamily': 'IBM Plex Mono'}]}
    return {'horzAlign': 'left', 'vertAlign': 'top',
            'lines': [
                {'text': 'dash-tvlwc', 'color': 'rgba(64,203,224,0.35)',
                 'fontSize': 34, 'fontFamily': 'IBM Plex Mono'},
                {'text': 'multi-line watermarks are new in v5',
                 'color': 'rgba(238,240,247,0.20)', 'fontSize': 15,
                 'fontFamily': 'IBM Plex Sans'},
            ]}


@callback(
    Output('shot-chart', 'screenshotRequest'),
    Input('shot-take', 'n_clicks'),
    prevent_initial_call=True,
)
def request_shot(n):
    return n


@callback(
    Output('shot-preview', 'src'),
    Output('shot-readout', 'children'),
    Input('shot-chart', 'screenshot'),
    prevent_initial_call=True,
)
def show_shot(data_uri):
    if not data_uri:
        return no_update, readout(('screenshot', 'none yet'))
    return data_uri, readout(('format', data_uri.split(';')[0].split(':')[1]),
                             ('bytes', f'{len(data_uri):,}'))


if __name__ == '__main__':
    app.run(debug=True, port=8051)

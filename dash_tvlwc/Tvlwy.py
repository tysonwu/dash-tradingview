# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.types import NumberType  # noqa: F401
except ImportError:
    # Backwards compatibility for dash<=4.1.0
    if typing.TYPE_CHECKING:
        raise
    NumberType = typing.Union[  # noqa: F401
        typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
    ]

ComponentSingleType = typing.Union[str, int, float, Component, None]
ComponentType = typing.Union[
    ComponentSingleType,
    typing.Sequence[ComponentSingleType],
]


class Tvlwy(Component):
    """A Tvlwy component.
Tradingview Lightweight Chart on a maturity axis, for yield curves. Points
carry `time` as a number of `chartOptions.yieldCurve.baseResolution` units
from `startTimeRange`, which defaults to months from zero, so a ten-year
point is written `{'time': 120, 'value': 4.3}`. The chart spaces maturities
by that value rather than evenly, which is what makes the short end of a
curve read correctly. Points must be unique and ascending in `time`.

Keyword arguments:

- id (string; optional):
    The ID of this component.

- barsInLogicalRange (boolean | number | string | dict | list; optional):
    Bars available around the visible range, as `{barsBefore,
    barsAfter, from, to, seriesId}`; read-only. Describes the first
    entry in `series`, and names it in `seriesId`. A negative
    `barsBefore` means the user has scrolled past the start of the
    data, which is the signal to fetch more history. Written only when
    `subscribeVisibleRange` is True.

- chartOptions (dict; default EMPTY_CHART_OPTIONS):
    Object containing all chart options. Mirrors the
    `YieldCurveChartOptions` interface of the underlying charting
    library: the ordinary chart options object plus a `yieldCurve`
    group of `baseResolution` (the smallest time unit, default 1
    month), `minimumTimeRange` (default 120, so ten years are always
    in view) and `startTimeRange` (default 0).  To label the maturity
    axis, give `localization.timeFormatter` the string name of a
    function registered on `window.dashTvlwcFunctions`. It receives
    the maturity in `baseResolution` units and returns the label;
    without one the axis falls back to `6M` and `5Y` style defaults.
    `yieldCurve.formatTime` looks like the option for that and is not.
    The upstream typings declare it, but lightweight-charts 5.2.1
    never reads it, so setting it changes nothing. Passing it here
    logs a warning pointing at `localization.timeFormatter` rather
    than failing silently.  There is no `timeScale.tickMarkFormatter`
    here either; that option belongs to time charts. Every other
    `timeScale` option applies unchanged.

    `chartOptions` is a dict with keys:

    - yieldCurve (boolean | number | string | dict | list; optional):
        Yield curve specific options. This object contains all the
        settings related to how the yield curve is displayed and
        behaves.

    - localization (boolean | number | string | dict | list; optional):
        Localization options.

    - width (number; optional):
        Width of the chart in pixels @,defaultValue,If `0` (default)
        or none value provided, then a size of the widget will be
        calculated based its container's size.

    - height (number; optional):
        Height of the chart in pixels @,defaultValue,If `0` (default)
        or none value provided, then a size of the widget will be
        calculated based its container's size.

    - autoSize (boolean; optional):
        Setting this flag to `True` will make the chart watch the
        chart container's size and automatically resize the chart to
        fit its container whenever the size changes.  This feature
        requires
        [`ResizeObserver`](https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver)
        class to be available in the global scope. Note that calling
        code is responsible for providing a polyfill if required. If
        the global scope does not have `ResizeObserver`, a warning
        will appear and the flag will be ignored.  Please pay
        attention that `autoSize` option and explicit sizes options
        `width` and `height` don't conflict with one another. If you
        specify `autoSize` flag, then `width` and `height` options
        will be ignored unless `ResizeObserver` has failed. If it
        fails then the values will be used as fallback.  The flag
        `autoSize` could also be set with and unset with
        `applyOptions` function. ```js const chart =
        LightweightCharts.createChart(document.body, {     autoSize:
        True, }); ```.

    - layout (boolean | number | string | dict | list; optional):
        Layout options.

    - leftPriceScale (boolean | number | string | dict | list; optional):
        Left price scale options.

    - rightPriceScale (boolean | number | string | dict | list; optional):
        Right price scale options.

    - defaultVisiblePriceScaleId (a value equal to: None, 'left', 'right'; optional):
        The price scale to prefer when the chart needs a default side
        and both left and right price scales share the same visibility
        state (both visible or both hidden). This affects behaviors
        that depend on the pane's default side, such as: - horizontal
        grid lines - overlay series label placement - the price scale
        used when adding a series without an explicit `priceScaleId` -
        crosshair price coordinate conversion and magnet snapping
        @,defaultValue,`'right'`.

    - overlayPriceScales (boolean | number | string | dict | list; optional):
        Overlay price scale options.

    - timeScale (boolean | number | string | dict | list; optional):
        Time scale options.

    - crosshair (boolean | number | string | dict | list; optional):
        The crosshair shows the intersection of the price and time
        scale values at any point on the chart.

    - grid (boolean | number | string | dict | list; optional):
        A grid is represented in the chart background as a vertical
        and horizontal lines drawn at the levels of visible marks of
        price and the time scales.

    - handleScroll (boolean; optional):
        Scroll options, or a boolean flag that enables/disables
        scrolling.

    - handleScale (boolean; optional):
        Scale options, or a boolean flag that enables/disables
        scaling.

    - kineticScroll (boolean | number | string | dict | list; optional):
        Kinetic scroll options.

    - trackingMode (boolean | number | string | dict | list; optional):
        TrackingModeOptions @,inheritDoc,TrackingModeOptions.

    - addDefaultPane (boolean; optional):
        Whether to add a default pane to the chart Disable this option
        when you want to create a chart with no panes and add them
        manually @,defaultValue,`True`.

    - hoveredSeriesOnTop (boolean; optional):
        Whether to draw the currently hovered series above the other
        series in the same pane.  This only affects drawing and
        hit-testing order while the series is hovered; it doesn't
        change the stored series order. @,defaultValue,`True`.

- click (boolean | number | string | dict | list; optional):
    Last-clicked chart position; read-only. Same shape as `crosshair`.
    Written only when `subscribeClick` is True.

- crosshair (boolean | number | string | dict | list; optional):
    Crosshair position; read-only. Carries `time`, `logical`,
    `paneIndex`, `point`, `seriesData` and `price` keyed by series id,
    `hoveredSeriesId` and `hoveredObjectId`. `seriesData` holds whole
    data points and is present only for series with data under the
    cursor; `price` is the price at the cursor on each series' own
    scale and is defined between bars too. Written only when
    `subscribeCrosshair` is True.

- crosshairPosition (boolean | number | string | dict | list; optional):
    Places the crosshair without a pointer, for syncing one chart to
    another. `None` clears it. Positioning this way deliberately does
    not emit a `crosshair` report, so two charts pointed at each other
    cannot loop.

- dataAction (boolean | number | string | dict | list; optional):
    Asks a series about its own data, answering on `dataResult`.
    `dataByIndex` reads back the single bar at `logicalIndex`,
    `lastValue` reads back the last price and the colour it is drawn
    in, and `pop` removes bars from the end and reads back what it
    removed. All three are O(1) in what crosses the wire, so none of
    them ships the dataset back.  `pop` leaves the chart holding less
    than `series[].data` describes, in the same way `tick` leaves it
    holding more. Both are deliberate: the next callback that writes
    `series` restores the prop as the whole truth.  Two things to know
    about `pop` specifically. It is the only action here that destroys
    anything, so a component that unmounts and remounts while this
    prop still holds a `pop` runs it again against the new chart; put
    the chart inside `dcc.Tabs` and it will pop once per visit. And on
    a series with `upDownMarkers`, the plugin keeps caching the popped
    bars, so a later `tick` at one of those times draws its first
    marker against the popped value.  Compared by content, like
    `timeScaleAction`, so change the `nonce` to repeat a query.

- dataResult (boolean | number | string | dict | list; optional):
    Answer to the last `dataAction`; read-only. Always carries the
    `action` and `seriesId` it answers, so a callback fed by several
    queries can tell which one arrived, plus:  - `dataByIndex`:
    `logicalIndex`, and `data` holding the whole data point   or
    `None` when the index falls outside the series. - `lastValue`:
    `noData`, and when that is False, `price` and `color`. - `pop`:
    `count` as asked for, and `removed` holding the bars that were
    actually taken off, newest first. It is shorter than `count` when
    the   series held fewer bars than that.  An action naming an
    unknown series, or one the library rejects, writes nothing and
    warns on the console instead, so a stale answer can outlive the
    request that failed. The `action` and `seriesId` are what tell the
    two apart.

- dblClick (boolean | number | string | dict | list; optional):
    Last double-clicked chart position; read-only. Same shape as
    `crosshair`. Written only when `subscribeDblClick` is True.

- fullChartOptions (boolean | number | string | dict | list; optional):
    Full chart options including defaults; read-only.

- fullPriceScaleOptions (boolean | number | string | dict | list; optional):
    Full options of the chart's default visible price scale, including
    defaults; read-only. That is the right scale on most charts, but
    the left one wherever only the left is visible, which is how a
    yield curve chart ships.

- fullSeriesOptions (boolean | number | string | dict | list; optional):
    Full series options including defaults, keyed by series id;
    read-only.

- fullTimeScaleOptions (boolean | number | string | dict | list; optional):
    Full horizontal scale options including defaults; read-only.

- height (string | number; default 400):
    Sets height of the parent div of the chart.

- paneOptions (list of dicts; default EMPTY_PANE_OPTIONS):
    Pane sizing, positional by pane index. Panes come into existence
    through `series[].pane`; this only sizes them.

    `paneOptions` is a list of dicts with keys:

    - height (number; optional):
        Fixed height in pixels. Mutually exclusive with
        `stretchFactor`, because the library implements a fixed height
        by rewriting every pane's stretch factor. Ignored when the
        chart has only one pane.

    - stretchFactor (number; optional):
        Share of the remaining space, relative to the other panes.
        Proportional sizing survives a resize where a fixed height
        does not, so prefer it on a responsive page.

- priceScaleWidth (number; optional):
    Width in pixels of the chart's default visible price scale;
    read-only. Picked the same way as `fullPriceScaleOptions`.
    Reported on scale resize only when `subscribeSize` is True.

- reportThrottle (number; default 0):
    Milliseconds to coalesce reports over, applied to every
    `subscribe*` stream. Zero batches to one report per animation
    frame.

- screenshot (string; optional):
    The most recent screenshot as a PNG data URI; read-only. Written
    once per change of `screenshotRequest`.

- screenshotRequest (number; default 0):
    Increment to capture the chart; the PNG arrives as a data URI on
    the `screenshot` prop. An integer counter such as a button's
    `n_clicks` is the intended shape, and `0` means no request.  The
    capture excludes the crosshair. An image watermark loaded from
    another origin taints the canvas and makes the export fail, so
    serve one with CORS headers if screenshots matter.

- series (list of dicts; default EMPTY_SERIES):
    The series drawn on this chart, each carrying its own id, type,
    data, options, markers and price lines.

    `series` is a list of dicts with keys:

    - id (string; required):
        Stable identity for this series. Used to key incremental
        updates and to key the `crosshair`, `click` and
        `fullSeriesOptions` payloads.

    - type (a value equal to: 'area', 'line'; required):
        Which kind of series to draw. The names this chart accepts are
        the ones listed on this field's type; `bar` and `candlestick`
        need OHLC points, and the rest take a single `value`.

    - data (list of boolean | number | string | dict | lists; required):
        Data points. Items carrying only `time` are whitespace and
        render as gaps.

    - options (boolean | number | string | dict | list; optional):
        Series options. See the `SeriesOptionsCommon` interface of the
        underlying charting library, plus the options specific to this
        series type.

    - priceScaleOptions (boolean | number | string | dict | list; optional):
        Options for the price scale this series is attached to. This
        is where `scaleMargins` lives; it is not a series option.

    - markers (boolean | number | string | dict | list; optional):
        Markers drawn against this series.

    - priceLines (boolean | number | string | dict | list; optional):
        Horizontal price lines drawn against this series.

    - upDownMarkers (boolean | number | string | dict | list; optional):
        Up and down markers: a temporary marker coloured by whether a
        revised value rose or fell. Options are `positiveColor`,
        `negativeColor` and `updateVisibilityDuration`; pass an empty
        object for the defaults, or omit the key for no markers. Line
        and area series only.  A marker appears only when a `tick`
        revises a bar the plugin already knows about, and it only
        learns bars through the series `data`. A tick that appends a
        new bar therefore draws nothing, and repeated revisions of the
        same bar are all coloured against the value that arrived in
        `data`, not against the previous tick.

    - pane (number; optional):
        Index of the pane this series is drawn on, counting from 0.
        Panes stack vertically and share one horizontal scale. An
        index one past the last pane creates a pane; further than that
        is clamped by the library, so keep the indices contiguous.
        Panes with no series are kept rather than collapsed, so that
        these indices, and `paneOptions`, stay stable.

- setProps (optional):
    Dash-assigned callback that fires when a prop changes.

- subscribeClick (boolean; default False):
    Whether to report chart clicks through the `click` prop.

- subscribeCrosshair (boolean; default False):
    Whether to report crosshair movement through the `crosshair` prop.
    Off by default: every report is a network round trip, and
    crosshair movement fires on every mouse move.

- subscribeDblClick (boolean; default False):
    Whether to report double clicks through the `dblClick` prop.

- subscribeSize (boolean; default False):
    Whether to report scale dimensions through `timeScaleWidth`,
    `timeScaleHeight` and `priceScaleWidth`. Off by default:
    `autoSize` drives these from a resize observer, so they fire every
    frame while the window is being dragged.

- subscribeVisibleRange (boolean; default False):
    Whether to report scale range changes through `visibleRange` and
    `visibleLogicalRange`. Off by default: these fire continuously
    while panning and zooming.

- tick (boolean | number | string | dict | list; optional):
    Appends a bar to a series without replacing its data, which is
    what keeps the visible range steady while streaming. Accepts one
    tick or a list, so a batch of bars costs one prop write.  Because
    this is a prop rather than an event, a tick identical to the
    previous one does not re-fire. A tick naming an unknown series id
    is ignored with a console warning, since it can arrive before the
    callback that creates the series.

- timeScaleAction (boolean | number | string | dict | list; optional):
    Runs a one-off horizontal scale command: `fitContent`,
    `scrollToRealTime`, `resetTimeScale` or `scrollToPosition`. The
    value is compared by content, so re-emitting the same command from
    an unrelated callback does nothing; change the `nonce` to ask for
    a genuine repeat.

- timeScaleHeight (number; optional):
    Height of the horizontal scale in pixels; read-only. Written only
    when `subscribeSize` is True.

- timeScaleWidth (number; optional):
    Width of the horizontal scale in pixels; read-only. Written only
    when `subscribeSize` is True.

- visibleLogicalRange (boolean | number | string | dict | list; optional):
    Visible range in bar indices, as `{from, to}`. Two-way, like
    `visibleRange`, and reported only while `subscribeVisibleRange` is
    True. Indices may be fractional, and may fall outside the data.
    Setting both this and `visibleRange` in one callback is ambiguous;
    this one wins.

- visibleRange (boolean | number | string | dict | list; optional):
    Visible range, as `{from, to}` in the same form the series data
    uses. Two-way: set it to move the chart, and read it to follow the
    user, though it is only reported while `subscribeVisibleRange` is
    True. The library clamps a requested range to the data that
    exists, so what is reported back will often not equal what was
    set.

- watermark (boolean | number | string | dict | list; optional):
    Draws a watermark over a pane. Give `imageUrl` for an image, or
    `lines` for text. `None` removes it.

- width (string | number; default '100%'):
    Sets width of the parent div of the chart."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_tvlwc'
    _type = 'Tvlwy'
    Series = TypedDict(
        "Series",
            {
            "id": str,
            "type": Literal["area", "line"],
            "data": typing.Sequence[typing.Any],
            "options": NotRequired[typing.Any],
            "priceScaleOptions": NotRequired[typing.Any],
            "markers": NotRequired[typing.Any],
            "priceLines": NotRequired[typing.Any],
            "upDownMarkers": NotRequired[typing.Any],
            "pane": NotRequired[typing.Union[NumberType]]
        }
    )

    PaneOptions = TypedDict(
        "PaneOptions",
            {
            "height": NotRequired[typing.Union[NumberType]],
            "stretchFactor": NotRequired[typing.Union[NumberType]]
        }
    )

    ChartOptions = TypedDict(
        "ChartOptions",
            {
            "yieldCurve": NotRequired[typing.Any],
            "localization": NotRequired[typing.Any],
            "width": NotRequired[typing.Union[NumberType]],
            "height": NotRequired[typing.Union[NumberType]],
            "autoSize": NotRequired[typing.Union[bool]],
            "layout": NotRequired[typing.Any],
            "leftPriceScale": NotRequired[typing.Any],
            "rightPriceScale": NotRequired[typing.Any],
            "defaultVisiblePriceScaleId": NotRequired[Literal[None, "left", "right"]],
            "overlayPriceScales": NotRequired[typing.Any],
            "timeScale": NotRequired[typing.Any],
            "crosshair": NotRequired[typing.Any],
            "grid": NotRequired[typing.Any],
            "handleScroll": NotRequired[typing.Union[bool]],
            "handleScale": NotRequired[typing.Union[bool]],
            "kineticScroll": NotRequired[typing.Any],
            "trackingMode": NotRequired[typing.Any],
            "addDefaultPane": NotRequired[typing.Union[bool]],
            "hoveredSeriesOnTop": NotRequired[typing.Union[bool]]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        series: typing.Optional[typing.Sequence["Series"]] = None,
        paneOptions: typing.Optional[typing.Sequence["PaneOptions"]] = None,
        tick: typing.Optional[typing.Any] = None,
        timeScaleAction: typing.Optional[typing.Any] = None,
        dataAction: typing.Optional[typing.Any] = None,
        crosshairPosition: typing.Optional[typing.Any] = None,
        watermark: typing.Optional[typing.Any] = None,
        screenshotRequest: typing.Optional[typing.Union[NumberType]] = None,
        subscribeCrosshair: typing.Optional[typing.Union[bool]] = None,
        subscribeClick: typing.Optional[typing.Union[bool]] = None,
        subscribeDblClick: typing.Optional[typing.Union[bool]] = None,
        subscribeVisibleRange: typing.Optional[typing.Union[bool]] = None,
        subscribeSize: typing.Optional[typing.Union[bool]] = None,
        reportThrottle: typing.Optional[typing.Union[NumberType]] = None,
        width: typing.Optional[typing.Union[str, NumberType]] = None,
        height: typing.Optional[typing.Union[str, NumberType]] = None,
        crosshair: typing.Optional[typing.Any] = None,
        click: typing.Optional[typing.Any] = None,
        dblClick: typing.Optional[typing.Any] = None,
        screenshot: typing.Optional[typing.Union[str]] = None,
        dataResult: typing.Optional[typing.Any] = None,
        barsInLogicalRange: typing.Optional[typing.Any] = None,
        fullChartOptions: typing.Optional[typing.Any] = None,
        fullSeriesOptions: typing.Optional[typing.Any] = None,
        fullPriceScaleOptions: typing.Optional[typing.Any] = None,
        fullTimeScaleOptions: typing.Optional[typing.Any] = None,
        priceScaleWidth: typing.Optional[typing.Union[NumberType]] = None,
        timeScaleWidth: typing.Optional[typing.Union[NumberType]] = None,
        timeScaleHeight: typing.Optional[typing.Union[NumberType]] = None,
        visibleRange: typing.Optional[typing.Any] = None,
        visibleLogicalRange: typing.Optional[typing.Any] = None,
        chartOptions: typing.Optional["ChartOptions"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'barsInLogicalRange', 'chartOptions', 'click', 'crosshair', 'crosshairPosition', 'dataAction', 'dataResult', 'dblClick', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'paneOptions', 'priceScaleWidth', 'reportThrottle', 'screenshot', 'screenshotRequest', 'series', 'setProps', 'subscribeClick', 'subscribeCrosshair', 'subscribeDblClick', 'subscribeSize', 'subscribeVisibleRange', 'tick', 'timeScaleAction', 'timeScaleHeight', 'timeScaleWidth', 'visibleLogicalRange', 'visibleRange', 'watermark', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'barsInLogicalRange', 'chartOptions', 'click', 'crosshair', 'crosshairPosition', 'dataAction', 'dataResult', 'dblClick', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'paneOptions', 'priceScaleWidth', 'reportThrottle', 'screenshot', 'screenshotRequest', 'series', 'setProps', 'subscribeClick', 'subscribeCrosshair', 'subscribeDblClick', 'subscribeSize', 'subscribeVisibleRange', 'tick', 'timeScaleAction', 'timeScaleHeight', 'timeScaleWidth', 'visibleLogicalRange', 'visibleRange', 'watermark', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Tvlwy, self).__init__(**args)

setattr(Tvlwy, "__init__", _explicitize_args(Tvlwy.__init__))

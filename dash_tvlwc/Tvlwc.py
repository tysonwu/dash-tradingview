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


class Tvlwc(Component):
    """A Tvlwc component.
Tradingview Lightweight Chart object

Keyword arguments:

- id (string; optional):
    The ID of this component.

- chartOptions (dict; default EMPTY_CHART_OPTIONS):
    Object containing all chart options. Mirrors the `ChartOptions`
    interface of the underlying charting library. Option values that
    must be functions, such as `localization.priceFormatter`, are
    given as the string name of a function registered on
    `window.dashTvlwcFunctions`.

    `chartOptions` is a dict with keys:

    - timeScale (boolean | number | string | dict | list; optional):
        Extended time scale options with option to override
        tickMarkFormatter.

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

- fullChartOptions (boolean | number | string | dict | list; optional):
    Full chart options including defaults; read-only.

- fullPriceScaleOptions (boolean | number | string | dict | list; optional):
    Full right price scale options including defaults; read-only.

- fullSeriesOptions (boolean | number | string | dict | list; optional):
    Full series options including defaults, keyed by series id;
    read-only.

- fullTimeScaleOptions (boolean | number | string | dict | list; optional):
    Full time scale options including defaults; read-only.

- height (string | number; default 400):
    Sets height of the parent div of the chart.

- priceScaleWidth (number; optional):
    Width of the right price scale in pixels; read-only. Reported on
    scale resize only when `subscribeSize` is True.

- reportThrottle (number; default 0):
    Milliseconds to coalesce reports over, applied to every
    `subscribe*` stream. Zero batches to one report per animation
    frame.

- series (list of dicts; default EMPTY_SERIES):
    The series drawn on this chart, each carrying its own id, type,
    data, options, markers and price lines.

    `series` is a list of dicts with keys:

    - id (string; required):
        Stable identity for this series. Used to key incremental
        updates and to key the `crosshair`, `click` and
        `fullSeriesOptions` payloads.

    - type (a value equal to: 'area', 'bar', 'baseline', 'candlestick', 'histogram', 'line'; required):
        One of `bar`, `candlestick`, `area`, `baseline`, `line`,
        `histogram`.

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

- setProps (optional):
    Dash-assigned callback that fires when a prop changes.

- subscribeClick (boolean; default False):
    Whether to report chart clicks through the `click` prop.

- subscribeCrosshair (boolean; default False):
    Whether to report crosshair movement through the `crosshair` prop.
    Off by default: every report is a network round trip, and
    crosshair movement fires on every mouse move.

- subscribeSize (boolean; default False):
    Whether to report scale dimensions through `timeScaleWidth`,
    `timeScaleHeight` and `priceScaleWidth`. Off by default:
    `autoSize` drives these from a resize observer, so they fire every
    frame while the window is being dragged.

- subscribeVisibleRange (boolean; default False):
    Whether to report time scale range changes through `visibleRange`
    and `visibleLogicalRange`. Off by default: these fire continuously
    while panning and zooming.

- timeScaleHeight (number; optional):
    Height of the time scale in pixels; read-only. Written only when
    `subscribeSize` is True.

- timeScaleWidth (number; optional):
    Width of the time scale in pixels; read-only. Written only when
    `subscribeSize` is True.

- visibleLogicalRange (boolean | number | string | dict | list; optional):
    Visible logical range in bar indices; read-only. Written only when
    `subscribeVisibleRange` is True.

- visibleRange (boolean | number | string | dict | list; optional):
    Visible time range; read-only. Written only when
    `subscribeVisibleRange` is True.

- width (string | number; default '100%'):
    Sets width of the parent div of the chart."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_tvlwc'
    _type = 'Tvlwc'
    ChartOptions = TypedDict(
        "ChartOptions",
            {
            "timeScale": NotRequired[typing.Any],
            "localization": NotRequired[typing.Any],
            "width": NotRequired[typing.Union[NumberType]],
            "height": NotRequired[typing.Union[NumberType]],
            "autoSize": NotRequired[typing.Union[bool]],
            "layout": NotRequired[typing.Any],
            "leftPriceScale": NotRequired[typing.Any],
            "rightPriceScale": NotRequired[typing.Any],
            "defaultVisiblePriceScaleId": NotRequired[Literal[None, "left", "right"]],
            "overlayPriceScales": NotRequired[typing.Any],
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

    Series = TypedDict(
        "Series",
            {
            "id": str,
            "type": Literal["area", "bar", "baseline", "candlestick", "histogram", "line"],
            "data": typing.Sequence[typing.Any],
            "options": NotRequired[typing.Any],
            "priceScaleOptions": NotRequired[typing.Any],
            "markers": NotRequired[typing.Any],
            "priceLines": NotRequired[typing.Any]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        chartOptions: typing.Optional["ChartOptions"] = None,
        series: typing.Optional[typing.Sequence["Series"]] = None,
        subscribeCrosshair: typing.Optional[typing.Union[bool]] = None,
        subscribeClick: typing.Optional[typing.Union[bool]] = None,
        subscribeVisibleRange: typing.Optional[typing.Union[bool]] = None,
        subscribeSize: typing.Optional[typing.Union[bool]] = None,
        reportThrottle: typing.Optional[typing.Union[NumberType]] = None,
        width: typing.Optional[typing.Union[str, NumberType]] = None,
        height: typing.Optional[typing.Union[str, NumberType]] = None,
        crosshair: typing.Optional[typing.Any] = None,
        click: typing.Optional[typing.Any] = None,
        fullChartOptions: typing.Optional[typing.Any] = None,
        fullSeriesOptions: typing.Optional[typing.Any] = None,
        fullPriceScaleOptions: typing.Optional[typing.Any] = None,
        fullTimeScaleOptions: typing.Optional[typing.Any] = None,
        priceScaleWidth: typing.Optional[typing.Union[NumberType]] = None,
        timeScaleWidth: typing.Optional[typing.Union[NumberType]] = None,
        timeScaleHeight: typing.Optional[typing.Union[NumberType]] = None,
        visibleRange: typing.Optional[typing.Any] = None,
        visibleLogicalRange: typing.Optional[typing.Any] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'chartOptions', 'click', 'crosshair', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'priceScaleWidth', 'reportThrottle', 'series', 'setProps', 'subscribeClick', 'subscribeCrosshair', 'subscribeSize', 'subscribeVisibleRange', 'timeScaleHeight', 'timeScaleWidth', 'visibleLogicalRange', 'visibleRange', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartOptions', 'click', 'crosshair', 'fullChartOptions', 'fullPriceScaleOptions', 'fullSeriesOptions', 'fullTimeScaleOptions', 'height', 'priceScaleWidth', 'reportThrottle', 'series', 'setProps', 'subscribeClick', 'subscribeCrosshair', 'subscribeSize', 'subscribeVisibleRange', 'timeScaleHeight', 'timeScaleWidth', 'visibleLogicalRange', 'visibleRange', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Tvlwc, self).__init__(**args)

setattr(Tvlwc, "__init__", _explicitize_args(Tvlwc.__init__))

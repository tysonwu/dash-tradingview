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

- chartOptions (dict; optional):
    Object containing all chart options. Mirrors the `ChartOptions`
    interface of the underlying charting library.

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

- height (string | number; default 400):
    Sets height of the parent div of the chart.

- setProps (optional):
    Dash-assigned callback that fires when a prop changes.

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


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        chartOptions: typing.Optional[typing.Union["ChartOptions"]] = None,
        width: typing.Optional[typing.Union[str, NumberType]] = None,
        height: typing.Optional[typing.Union[str, NumberType]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'chartOptions', 'height', 'setProps', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartOptions', 'height', 'setProps', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Tvlwc, self).__init__(**args)

setattr(Tvlwc, "__init__", _explicitize_args(Tvlwc.__init__))

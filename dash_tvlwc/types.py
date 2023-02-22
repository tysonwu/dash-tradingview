from enum import Enum

# StrEnum class is also available 3.11+
# With this approach, the Enum values need not to be referenced
# as Enum.attr.value but Enum.attr instead
# while maintaining immutability of Enum classes.
class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)

# Represents a type of color.
class ColorType(StrEnum):
    Solid: str = "solid"            # Solid color
    VerticalGradient: str = "gradient"   # Vertical gradient color

# Represents the crosshair mode.
class CrosshairMode(StrEnum):
    Normal: int = 0                # This mode allows crosshair to move freely on the chart.
    Magnet: int = 1                # This mode sticks crosshair's horizontal line to the price value of a single-value series or to the close price of OHLC-based series.

# Represents the type of the last price animation for series such as area or line.
class LastPriceAnimationMode(StrEnum):
    Disabled: int = 0              # Animation is always disabled
    Continuous: int = 1            # Animation is always enabled.
    OnDataUpdate: int = 2          # Animation is active after new data.

# Represents the possible line styles.
class LineStyle(StrEnum):
    Solid: int = 0                 # A solid line.
    Dotted: int = 1                # A dotted line.
    Dashed: int = 2                # A dashed line.
    LargeDashed: int = 3           # A dashed line with bigger dashes.
    SparseDotted: int = 4          # A dottled line with more space between dots.

# Represents the possible line types.
class LineType(StrEnum):
    Simple: int = 0                # A line.
    WithSteps: int = 1             # A stepped line.

# Represents the source of data to be used for the horizontal price line.
class PriceLineSource(StrEnum):
    LastBar: int = 0               # Use the last bar data.
    LastVisible: int = 1           # Use the last visible data of the chart viewport.

# Represents the price scale mode.
class PriceScaleMode(StrEnum):
    Normal: int = 0                # Price scale shows prices. Price range changes linearly.
    Logarithmic: int = 1           # Price scale shows prices. Price range changes logarithmically.
    Percentage: int = 2            # Price scale shows percentage values according the first visible value of the price scale.
                                   # The first visible value is 0% in this mode.
    IndexedTo100: int = 3          # The same as percentage mode, but the first value is moved to 100.

# Represents the type of a tick mark on the time axis.
class TickMarkType(StrEnum):
    Year: int = 0                  # The start of the year (e.g. it's the first tick mark in a year).
    Month: int = 1                 # The start of the month (e.g. it's the first tick mark in a month).
    DayOfMonth: int = 2            # A day of the month.
    Time: int = 3                  # A time without seconds.
    TimeWithSeconds: int = 4       # A time with seconds.

# Determine how to exit the tracking mode.
#
# By default, mobile users will long press to deactivate the scroll and have the ability to check values and dates.
# Another press is required to activate the scroll, be able to move left/right, zoom, etc.
class TrackingModeExitMode(StrEnum):
    OnTouchEnd: int = 0            # Tracking Mode will be deactivated on touch end event.
    OnNextTap: int = 1             # Tracking Mode will be deactivated on the next tap event.


# Additional for series types
# These Enums do not exist in original chart library but only in this Dash component
class SeriesType(StrEnum):
    Bar: str = 'bar'                    # Similar to candlestick series but OHLC values represented in bar
    Candlestick: str = 'candlestick'    # Candlestick series with OHLC values
    Area: str = 'area'                  # Similar to line series but with area shade under series
    Baseline: str = 'baseline'          # Simliar to line series but with a threshold value in mind
    Line: str = 'line'                  # Line series of single values
    Histogram: str = 'histogram'        # Vertical bars similar to conventional representation of volume in OHLCV plot

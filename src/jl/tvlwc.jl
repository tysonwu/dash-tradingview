# AUTO GENERATED FILE - DO NOT EDIT

export tvlwc

"""
    tvlwc(;kwargs...)

A Tvlwc component.
Tradingview Lightweight Chart object
Keyword arguments:
- `id` (String; optional): The ID of this component
- `colors` (Dict; optional): An object containing colors properties
- `data` (Array; optional): The data for the series
"""
function tvlwc(; kwargs...)
        available_props = Symbol[:id, :colors, :data]
        wild_props = Symbol[]
        return Component("tvlwc", "Tvlwc", "dash_tvlwc", available_props, wild_props; kwargs...)
end


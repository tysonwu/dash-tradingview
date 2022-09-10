
module Tvlwc
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/tvlwc.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "tvlwc",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "tvlwc.min.js",
    external_url = "https://unpkg.com/tvlwc@0.0.1/tvlwc/tvlwc.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "tvlwc.min.js.map",
    external_url = "https://unpkg.com/tvlwc@0.0.1/tvlwc/tvlwc.min.js.map",
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end

# Development

How to build `dash_tvlwc` from source. For using the published package, see the
[documentation site](https://dash-tradingview.readthedocs.io/).

## Requirements

- Node.js 18 or newer, npm 9 or newer
- Python 3.9 or newer

## Set up

Run everything from the repository root.

1. Install the npm packages.
    ```
    $ npm install
    ```
2. Create a virtual environment and activate it.
    ```
    $ python -m venv venv
    $ . venv/bin/activate
    ```
    _On Windows: `venv\Scripts\activate`._
3. Install the Python packages needed to build the component.
    ```
    $ pip install -r requirements.txt
    ```

## Build

```
$ npm run build
```

Two stages, which can also be run separately:

- `npm run build:js` bundles `src/lib` into `dash_tvlwc/dash_tvlwc.min.js` with
  webpack.
- `npm run build:backends` generates the Python, R and Julia classes from every
  component in `src/lib/components/`. The virtual environment must be active so
  that `dash-generate-components` is on `PATH`.

`npm run typecheck` runs `tsc --noEmit` over the TypeScript sources without
producing a bundle.

## How the source is laid out

```
src/lib/
  core/
    types.ts      prop shapes, generic in what sits on the horizontal scale
    chart.tsx     the chart implementation, generic in the same way
  components/
    Tvlwc.tsx     time axis
    Tvlwo.tsx     price axis
    Tvlwy.tsx     maturity axis
```

The three components are one implementation over three horizontal scales. That
works because the upstream API is already generic: `IChartApi` is defined as
`IChartApiBase<Time>`, and the marker and watermark factories each take the
horizontal item as a type parameter.

A file in `components/` supplies three things: the constructor to call, the
series types that chart accepts, and the prop defaults. Everything else lives in
`core/`.

Two rules worth knowing before editing:

- **`dash-generate-components` scans all of `src/lib/components/`**, so shared
  code must live outside it or it will be treated as a component.
- **Prop defaults must appear in the destructuring pattern of the component
  file.** The generator reads them from there; a default it cannot see makes the
  prop a required argument in the generated Python.

## Running the examples and the demo

```
$ python demo/app.py                      # the hosted showcase
$ PYTHONPATH=. python examples/options.py # styling
```

The apps under `examples/` import `theme` and `data_generator` as siblings, so
they need the repository root on `PYTHONPATH`. `demo/app.py` puts its own
directory on `sys.path` and does not.

## Documentation

The site under `docs/` is Sphinx with MyST markdown.

```
$ pip install -r docs/requirements.txt
$ sphinx-build -b html docs docs/_build/html
```

## Verified compatibility

| Dash   | React  | Status                              |
| ------ | ------ | ----------------------------------- |
| 4.4.1  | 18.3.1 | Works                               |
| 3.4.0  | 18.3.1 | Works                               |
| 3.0.0  | 18.3.1 | Works                               |
| 2.18.2 | 16.14  | Works, but below the declared floor |

The package declares `dash>=3.0.0`. Dash 3.0.0 and 2.18.2 need Python 3.13 or
older, as they call `pkgutil.find_loader`, which was removed in Python 3.14.

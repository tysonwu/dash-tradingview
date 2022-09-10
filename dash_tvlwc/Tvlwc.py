from dash.development.base_component import Component, _explicitize_args


class Tvlwc(Component):
    """A Tvlwc component.

Keyword arguments:

- id (string; optional)

- colors (dict; optional)

- data (list; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'tvlwc'
    _type = 'Tvlwc'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, colors=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'colors', 'data']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'colors', 'data']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tvlwc, self).__init__(**args)

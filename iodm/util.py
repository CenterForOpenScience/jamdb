def compose(type_, backend):
    return type(
        backend.__name__.replace('Backend', '') + type_.__name__,
        (type_, backend),
        {}
    )

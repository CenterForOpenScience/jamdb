from stevedore import driver


def load_schema(name, *args, **kwargs):
    return driver.DriverManager(
        'jam.schemas',
        name,
        invoke_on_load=True,
        invoke_args=args,
        invoke_kwds=kwargs,
    ).driver

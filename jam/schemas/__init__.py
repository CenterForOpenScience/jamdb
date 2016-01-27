from stevedore import driver

from jam import exceptions


def load_schema(name, *args, **kwargs):
    try:
        return driver.DriverManager(
            'jam.schemas',
            name,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds=kwargs,
        ).driver
    except driver.NoMatches:
        raise exceptions.NoSuchSchema(name)

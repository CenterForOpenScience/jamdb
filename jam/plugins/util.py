import pkg_resources

from stevedore import driver

from jam import exceptions


def get_plugins():
    return (ep.load() for ep in pkg_resources.iter_entry_points('jam.plugins'))


def get_plugin(name):
    return driver.DriverManager('jam.plugins', name).driver


def load_plugin(name, *args, **kwargs):
    try:
        return driver.DriverManager(
            'jam.plugins',
            name,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds=kwargs,
        ).driver
    except driver.NoMatches:
        raise exceptions.NoSuchPlugin(name)

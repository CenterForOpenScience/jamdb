from setuptools import setup, find_packages

from jam import __version__


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


requirements = parse_requirements('requirements.txt')

setup(
    name='jam',
    version=__version__,
    scripts=['bin/jam'],
    namespace_packages=[
        'jam',
        'jam.auth',
        'jam.schemas',
        'jam.backends',
        'jam.auth.providers'
    ],
    install_requires=requirements,
    packages=find_packages(exclude=('tests*', 'examples')),
    package_dir={'jam': 'jam'},
    include_package_data=True,
    zip_safe=False,
    provides=[
        'jam.backends',
        'jam.auth.providers',
    ],
    entry_points={
        'jam.schemas': [
            'jsonschema = jam.schemas.jsonschema:JSONSchema'
        ],
        'jam.backends': [
            'mongo = jam.backends.mongo:MongoBackend',
            'ephemeral = jam.backends.ephemeral:EphemeralBackend',
            'elasticsearch = jam.backends.elasticsearch:ElasticsearchBackend',
        ],
        'jam.auth.providers': [
            'osf = jam.auth.providers.osf:OSFAuthProvider',
            'self = jam.auth.providers.self:SelfAuthProvider',
            'anon = jam.auth.providers.anon:AnonAuthProvider',
        ],
    },
)

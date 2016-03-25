import re
from setuptools import setup, find_packages


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


def parse_requirements(requirements):
    with open(requirements) as f:
        reqs, deps = [], []
        for req in [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]:
            if req.startswith('git+'):
                deps.append(req.lstrip('git+'))
            else:
                reqs.append(req)
    return reqs, deps

requirements, dependency_links = parse_requirements('requirements.txt')

setup(
    name='jam',
    version=find_version('jam/__init__.py'),
    scripts=['bin/jam'],
    # install_requires=requirements,
    # dependency_links=dependency_links,
    packages=find_packages(exclude=('tests*', 'examples')),
    package_dir={'jam': 'jam'},
    include_package_data=True,
    zip_safe=False,
    provides=[
        'jam.plugins',
        'jam.schemas',
        'jam.backends',
        'jam.auth.providers',
    ],
    entry_points={
        'jam.plugins': [
            'user = jam.plugins.user:UserPlugin',
            'search = jam.plugins.search:SearchPlugin'
        ],
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

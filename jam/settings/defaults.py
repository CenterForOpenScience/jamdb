MONGO_DATABASE_NAME = 'jam'

NAMESPACE_BACKENDS = {
    'state': 'mongo',
    'logger': 'mongo',
    'storage': 'mongo',
}

NAMESPACEMANAGER_BACKENDS = {
    'state': 'mongo',
    'logger': 'mongo',
    'storage': 'mongo',
}

NAMESPACE_DEFAULT_BACKENDS = {
    'state': 'elasticsearch',
    'logger': 'mongo',
    'storage': 'mongo',
}

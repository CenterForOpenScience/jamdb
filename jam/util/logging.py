import logging
import logging.config

try:
    import colorlog  # noqa
    DEFAULT_FORMATTER = {
        '()': 'colorlog.ColoredFormatter',
        'format': '%(cyan)s[%(asctime)s]%(log_color)s[%(levelname)s][%(name)s]: %(reset)s%(message)s'
    }
except ImportError:
    DEFAULT_FORMATTER = {
        'format': '[%(asctime)s][%(levelname)s][%(name)s]: %(message)s',
    }


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': DEFAULT_FORMATTER,
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'console'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
})

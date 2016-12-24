import logging
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '[+] %(levelname)s :- %(message)s'
        },
    },
    'handlers': {
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'project.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {

        'project': {
            'handlers': ['proj_log_file','console'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)
rootLogger = logging.getLogger("project")

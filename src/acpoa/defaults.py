import os.path

from .configuration import Configuration


def cfg_acpoa(path):
    if not os.path.isfile(path): open(path, 'w').close()
    config = Configuration.open(path)
    config.ensure('plugins', 'enable-on-installation', 'yes')
    config.ensure('repositories', 'enable-on-installation', 'yes')
    config.save()


def cfg_plugin(path):
    if not os.path.isfile(path): open(path, 'w').close()
    config = Configuration.open(path)
    config.save()

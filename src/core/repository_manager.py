import os
import warnings

import requests

from src.core.configuration import Configuration


class RepositoryManager:
    _ACPOA_CFG_SECTION_REPO = 'repo'
    _ACPOA_CFG_SECTION_REPOSITORIES = 'repositories'

    def __init__(self, config_fname: str):
        self._config = Configuration.open(config_fname)
        self._repositories = self._load_repositories()
        self._repo_eoi = self._config.get(self._ACPOA_CFG_SECTION_REPOSITORIES, 'enable-on-installation')

    def add(self, name: str, index: str, editable: [bool, str] = False):
        """Add the repository to the list where to search plugins.

        :param name: custom name of the repository
        :param index: url, path to the repository
        :param editable: do the plugins need to be dynamically updated (development usage)
        :raise Exception: if the repository is already registered"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        if self._config.has_section(section):
            warnings.warn(Warning(f"Repository {name} already is registered."))
            return

        self._config.add_section(section)
        self._config.set(section, 'enabled', self._repo_eoi)
        self._config.set(section, 'index', index)
        self._config.setboolean(section, 'editable', editable)
        self._config.save()

        self._repositories = self._load_repositories()

    def remove(self, name: str):
        """Remove the repository from the list.

        :param name: name of the repository to remove"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.remove_section(section)
        self._config.save()

        self._repositories = self._load_repositories()

    def is_installed(self, name) -> bool:
        """Test if the given repository is installed.

        :param name: name of the repository in the config file.
        :return: whether or not the repository is installed."""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        return self._config.has_section(section)

    def is_enabled(self, name) -> bool:
        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        if not self._config.has_section(section): return False
        return self._config.getboolean(section, 'enabled')

    def enable(self, name: str):
        """Enable a repository

        :param name: name of the repository"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.setboolean(section, 'enabled', True)
        self._config.save()

        self._repositories = self._load_repositories()

    def disable(self, name: str):
        """Disable a repository.

        :param name: name of the repository"""

        section = self._config.subsection(self._ACPOA_CFG_SECTION_REPO, name)
        self._config.setboolean(section, 'enabled', False)
        self._config.save()

        self._repositories = self._load_repositories()

    def each(self):
        """Repository generator to use in a for loop."""
        for repository in self._repositories:
            yield repository

    def _load_repositories(self):
        repos = []
        for section in self._config.subsections_of(self._ACPOA_CFG_SECTION_REPO):
            if not self._config.getboolean(section, 'enabled'): continue

            index = self._config.get(section, 'index')
            editable = self._config.getboolean(section, 'editable', fallback=False)
            repos.append(Repository(index, editable))
        return repos

    @property
    def count(self):
        return len(self._repositories)


class Repository:
    def __init__(self, index: str, editable: bool):
        self._index = index
        self._editable = editable
        self._editable_opt = '-e' if editable else ''

    def install(self, package: str, upgrade: bool = False) -> int:
        """Try to install the package.

        :param package: name of the package to install
        :param upgrade: if true, upgrade the installed package
        :return: pip result"""

        command = f"pip -q install {self._editable_opt} " \
                  f"{'--upgrade' if upgrade else ''} " \
                  f"--no-cache-dir " \
                  f"--index-url {self._index} " \
                  f"{package} "
        return os.system(command)

    def upgrade(self, package) -> int:
        """Try to upgrade the package.

        :return: pip result"""

        return self.install(package, upgrade=True)

    def is_reachable(self) -> bool:
        """Test if the repository is reachable by html request.

        :return: whether or not the repository is reachable"""

        try:
            return requests.get(self._index).status_code == 200
        except:
            return False

    def remove(self, package):
        """Wrap of Repository.remove"""
        return Repository.remove(package)

    @staticmethod
    def remove(package) -> int:
        """Uninstall the package

        :return: pip result"""

        result = int(os.system(f"pip -q uninstall -y {package}"))
        os.system('pip -q cache purge')
        return result

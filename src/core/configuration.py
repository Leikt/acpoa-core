from __future__ import annotations

import configparser
import os.path


class Configuration(configparser.ConfigParser):
    """Help to manage configuration file and parsing."""

    SUBSECTION_DELIMITER = ':'

    _opened = {}

    @classmethod
    def open(cls, filename: str) -> Configuration:
        """Get a Configuration object for the given config file. It will be created if
        it does not exist.

        :param filename: configuration file
        :return: Configuration object"""
        # Open existing configuration object
        existing = cls._opened.get(filename, None)
        if existing is not None:
            return existing
        # Create Configuration object if the file exists
        config = Configuration()
        config.filename = filename
        cls._opened[filename] = config
        return config

    @classmethod
    def close_all(cls):
        """Delete all the open Configuration objects"""
        cls._opened.clear()

    @classmethod
    def close(cls, filename):
        """Delete a specific Configuration object

        :param filename: configuration filename to delete"""
        existing = cls._opened.get(filename, None)
        if existing:
            del cls._opened[filename]

    @property
    def filename(self) -> str:
        """Get the filename used by the Configuration object"""
        return self._filename

    @filename.setter
    def filename(self, value: str):
        """Change and read the configuration file

        :param value: new filename to use
        :raise FileNotFound: if the file does not exist"""
        if not os.path.isfile(value):
            raise FileNotFoundError(f"Can't find configuration file {value}")
        self._filename = value
        self.read(value)

    def save(self):
        """Apply change to the configuration file"""
        with open(self._filename, 'w') as file:
            self.write(file)

    def values(self, section) -> list[str]:
        """Return all the values of the given section

        :param section"""
        result = []
        for option in self.options(section):
            result.append(self.get(section, option))
        return result

    def subsection(self, *args) -> str:
        """Construct the name of the subsection using the given section parameters."""
        return self.SUBSECTION_DELIMITER.join(args)

    def subsections_of(self, *parents: str) -> list[str]:
        """Get all the sections that are children of given parent

        :param parents: liste of section and subsection to the wanted one"""
        parent = self.SUBSECTION_DELIMITER.join(parents)
        results = []
        for section in self.sections():
            if section.startswith(parent) and section != parent:
                results.append(section)
        return results

    def subsection_name(self, section: str) -> str:
        return section.split(self.SUBSECTION_DELIMITER)[-1]

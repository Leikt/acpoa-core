class Client:
    """Communicate with a repository."""

    def __init__(self, repository: str):
        self._repository = repository

    def update(self, force=False):
        """Update the meta data from the repository"""
        raise NotImplemented

    def install(self, package, **params) -> bool:
        """Install the package from the repository"""
        pass

    def is_provinding(self, package: str) -> bool:
        """Indicate if the repository contains the given package"""
        return False


class LocalClient(Client):
    """Communicate with a local depository"""
    pass


class DistantClient(Client):
    """Communicate with a distant depository"""
    pass

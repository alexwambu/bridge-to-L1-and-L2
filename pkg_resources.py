# Lightweight shim for pkg_resources when setuptools isn't fully installed

class DistributionNotFound(Exception):
    pass

class VersionConflict(Exception):
    pass

def get_distribution(name):
    # Fakes a distribution object with version string
    class Distribution:
        def __init__(self, project_name):
            self.project_name = project_name
            self.version = "1.0.0"
    return Distribution(name)

def require(name):
    return [get_distribution(name)]


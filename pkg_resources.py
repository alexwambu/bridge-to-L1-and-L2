# This is a compatibility shim; not for production environments
class DistributionNotFound(Exception):
    pass

class VersionConflict(Exception):
    pass

def require(name):
    return None

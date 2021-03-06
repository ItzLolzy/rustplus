class Error(Exception):
    """Base class for other exceptions"""
    pass


class ClientError(Error):
    """Raised when the client details are not valid"""
    pass

class ImageError(Error):
    """Raised when the Image Returned is not valid"""
    pass


class BaseException(Exception):
    
    def __init__(self, message, status):
        self.message = message
        self.status = status
        super().__init__(message)


class SlideRequestError(BaseException):
    pass

class UploadSlidesError(BaseException):
    pass

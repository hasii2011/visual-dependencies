
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import ART_FILE_OPEN
from wx import ART_FOLDER
from wx import ART_NORMAL_FILE
from wx import ART_OTHER
from wx import ArtProvider
from wx import ImageList


class EnhancedImageList:
    """
    Custom wrapper for this application
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        imageSize: Tuple[int, int] = (16, 16)
        imageList: ImageList       = ImageList(imageSize[0], imageSize[1])

        self._folderIndex:     int = imageList.Add(ArtProvider.GetBitmap(id=ART_FOLDER,      client=ART_OTHER, size=imageSize))
        self._folderOpenIndex: int = imageList.Add(ArtProvider.GetBitmap(id=ART_FILE_OPEN,   client=ART_OTHER, size=imageSize))
        self._fileIndex:       int = imageList.Add(ArtProvider.GetBitmap(id=ART_NORMAL_FILE, client=ART_OTHER, size=imageSize))

        self._imageList: ImageList = imageList

    @property
    def imageList(self) -> ImageList:
        return self._imageList

    @property
    def folderIndex(self) -> int:
        return self._folderIndex

    @property
    def folderOpenIndex(self) -> int:
        return self._folderOpenIndex

    def fileIndex(self) -> int:
        return self._fileIndex

from PySide2.QtCore import QUrl, Slot, QObject
import os
from utilities.settings import IMAGES_DIR


class ResourceLoader(QObject):
    @Slot(str, result=QUrl)
    def get_resource(self, resource_name):
        return QUrl().fromLocalFile(os.path.join(IMAGES_DIR, resource_name))
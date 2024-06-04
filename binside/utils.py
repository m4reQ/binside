from PyQt6 import QtCore, uic


def load_ui_from_resource(resource_path: str, base_instance: object) -> None:
    f = QtCore.QFile(resource_path)
    f.open(QtCore.QFile.OpenModeFlag.ReadOnly)

    uic.loadUi(f, base_instance)

    f.close()

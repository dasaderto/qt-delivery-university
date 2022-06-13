from PySide6.QtWidgets import QMessageBox, QWidget


def error_alert(widget: QWidget, message: str):
    dlg = QMessageBox(widget)
    dlg.setWindowTitle("Ошибка!")
    dlg.setText(message)
    dlg.show()


def alert(widget: QWidget, title: str, message: str):
    dlg = QMessageBox(widget)
    dlg.setWindowTitle(title)
    dlg.setText(message)
    dlg.show()

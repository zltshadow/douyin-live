import sys
import threading
import time

from PySide6.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QApplication, QAbstractItemView

from ob_douyin import Ui_MainWindow
import dy_live


class DouyinForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(DouyinForm, self).__init__(parent)
        self.ob_data = []
        self.setupUi(self)
        # 表格不可编辑
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 表格默认选中
        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 表格头部隐藏
        # self.tableWidget.horizontalHeader().setVisible(False)
        # 表格列号隐藏
        self.tableWidget.verticalHeader().setVisible(False)

        font = self.tableWidget.horizontalHeader().font()
        font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(font)
        # self.tableWidget.horizontalHeader().resizeSection(0, 100)
        # self.tableWidget.horizontalHeader().resizeSection(1, 100)
        self.tableWidget.horizontalHeader().resizeSection(6, 600)
        # 表格自适应宽度
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.tableWidget.setSpan(1, 2, 3, 2)
        self.pushButton.clicked.connect(self.start_observe)
        self.pushButton_2.clicked.connect(self.stop_observe)

    def update_table(self):
        # 获取当前行数
        current_row_count = self.tableWidget.rowCount()

        # 获取数组中新增的项
        new_items = self.ob_data[current_row_count:]

        if new_items:
            # 在表格中插入新的行，并填充数据
            for new_item in new_items:
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

                for col, value in enumerate(new_item):
                    item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row_position, col, item)

    def clear_table(self):
        # 清空表格内容
        self.tableWidget.clearContents()
        # 将行数设置为0
        self.tableWidget.setRowCount(0)

    def start_observe(self):
        live_room_url = self.lineEdit.text()
        print(live_room_url)
        self._stop_event = threading.Event()
        # 主线程结束立马结束子线程
        t = threading.Thread(target=self.ob_thread_function, args=(live_room_url, self._stop_event), daemon=True)
        try:
            t.start()
        except Exception as e:
            print(f"监听出错")

    def stop_observe(self):
        try:
            self._stop_event.set()
        except Exception as e:
            print(f"停止出错")

    def ob_thread_function(self, live_room_url, stop_event):
        ws, thread = dy_live.parseLiveRoomUrl(live_room_url)
        while True:
            time.sleep(1)
            if stop_event.is_set():
                ws.close()
                print('wss连接线程结束')
                break
            else:
                self.ob_data = [item.to_array() for item in dy_live.ob_data]
                self.update_table()
        # try:
        #     stop_event.wait()
        # except KeyboardInterrupt:
        #     pass
        # finally:
        #     ws.close()
        #     print('wss连接线程结束')
        print('直播监听线程结束')


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # myw = QMainWindow()
    # myWin = Ui_MainWindow().setupUi(myw)
    # myw.show()
    # sys.exit(app.exec())
    app = QApplication(sys.argv)
    myWin = DouyinForm()
    myWin.show()
    sys.exit(app.exec())

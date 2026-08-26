from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QRect, QTimer, QSize, QThread, QPoint, Signal, QPropertyAnimation
from PySide6.QtGui import QPainter, QFont, QColor, QMouseEvent, QCursor, QGuiApplication
from PySide6.QtTest import QTest
from pyqtgraph import PlotDataItem
import myUtils
from copy import deepcopy
import sys,os
from typing import Literal
from myUtils import _if

class ToastWidget(QWidget):
    def __init__(self,sizes : list,ms_lasting,ms_fade_out):
        super().__init__()
        self.ms_lasting = ms_lasting
        self.ms_fade_out = ms_fade_out
        
        self.msg = ""
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)
        self.label_msg = QLabel()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        
        
        self.layout_main.addWidget(self.label_msg)
        self.layout_main.setContentsMargins(0,0,0,0)
        self.layout_main.setSpacing(0)
        self.setStyleSheet("""
                            background-color: #2b2b2b;
                            """)
        self.set_size(sizes[0],sizes[1])

        self.close_wait_timer = QTimer()
        self.close_wait_timer.setSingleShot(True)
        self.close_wait_timer.timeout.connect(self.close_toast)
        
        self.widget_hide_timer = QTimer()
        self.widget_hide_timer.setSingleShot(True)
        self.widget_hide_timer.timeout.connect(self.hide)
    
    def set_size(self,width,height):
        self.widget_width = width
        self.widget_height= height
        
    def show_toast(self,msg):
        self.setWindowOpacity(1)
        self.msg = msg
        self.label_msg.setText(self.msg)
        self.label_msg.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        
        
        screen = QGuiApplication.primaryScreen()
        rect_screen = screen.availableGeometry()
        self.screen_size = [rect_screen.width(), rect_screen.height()]
        
        x,y,w,h = (self.screen_size[0] - self.widget_width,
                    self.screen_size[1] - self.widget_height,
                    self.widget_width,
                    self.widget_height)
        
        self.setGeometry(x,y,w,h)
        self.show()

        self.close_wait_timer.setInterval(self.ms_lasting)
        self.close_wait_timer.start()


    def close_toast(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(self.ms_fade_out)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.start()
        
        
        self.widget_hide_timer.setInterval(self.ms_fade_out)
        self.widget_hide_timer.start()

class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

class CustomSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.orientation() == Qt.Horizontal:
            # 가로 슬라이더
            groove_rect = QRect(self.rect())
            groove_rect.setHeight(40)  
            groove_rect.moveTop((self.height() - groove_rect.height()) // 2)

            # 트랙 그리기
            painter.setPen(QColor(200, 200, 200))
            painter.setBrush(QColor(200, 200, 200))
            painter.drawRect(groove_rect)

            # 핸들 위치
            handle_size = 40
            handle_pos = (self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (groove_rect.width() - handle_size)
            handle_rect = QRect(groove_rect.left() + handle_pos, groove_rect.top() - 6, handle_size, handle_size)

        else:
            # 세로 슬라이더
            groove_rect = QRect(self.rect())
            groove_rect.setWidth(40)
            groove_rect.moveLeft((self.width() - groove_rect.width()) // 2)

            # 트랙 그리기
            painter.setPen(QColor(200, 200, 200))
            painter.setBrush(QColor(200, 200, 200))
            painter.drawRect(groove_rect)

            # 핸들 위치
            handle_size = 40
            handle_pos = (self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (groove_rect.height() - handle_size)
            handle_rect = QRect(groove_rect.left() - 6, groove_rect.bottom() - handle_pos - handle_size, handle_size, handle_size)

        # 핸들 그리기
        painter.setPen(QColor(0, 120, 255))
        painter.setBrush(QColor(0, 120, 255))
        painter.drawRect(handle_rect)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.orientation() == Qt.Orientation.Horizontal:
                value = self.minimum() + (self.maximum() - self.minimum()) * event.position().x() / self.width()
                self.setValue(int(value))
                
                # 새로운 이벤트 객체 생성: 현재 값에 해당하는 위치로 포인터 위치를 조작
                pos = (self.value() - self.minimum()) / (self.maximum() - self.minimum()) * self.width()
                new_event = QMouseEvent(
                    event.type(), QPoint(int(pos), event.position().y()), event.globalPosition(), 
                    event.button(), event.buttons(), event.modifiers()
                )
                
            else: # Qt.Orientation.Vertical
                value = self.maximum() - (self.maximum() - self.minimum()) * event.position().y() / self.height()
                self.setValue(int(value))

                pos = (self.maximum() - self.value()) / (self.maximum() - self.minimum()) * self.height()
                new_event = QMouseEvent(
                    event.type(), QPoint(event.position().x(), int(pos)), event.globalPosition(), 
                    event.button(), event.buttons(), event.modifiers()
                )

            # 조작된 이벤트를 부모 클래스에 전달하여 드래그 기능 활성화
            super().mousePressEvent(new_event)
        else:
            super().mousePressEvent(event)


class DoubleSortableQListWidgetItem(QListWidgetItem):
    def __init__(self, string):
        super().__init__(string)  # 아이템의 텍스트 설정
        self.value = 0  # 정렬을 위한 정수 값 저장
    
    def set_value(self,value):
        self.value = value
    
    def __lt__(self, other):
        if isinstance(other, DoubleSortableQListWidgetItem):
            return self.value < other.value
        return super().__lt__(other)
        
class LongPressPossiblePushButton(QPushButton):
    longPressed = Signal()
    shortPressed = Signal()

    def __init__(self, *args, long_press_time=500, **kwargs):
        """
        long_press_time: 길게 누르기를 판정하는 시간 (ms)
        """
        super().__init__(*args, **kwargs)
        self._long_press_time = long_press_time
        self._long_press_timer = QTimer(self)
        self._long_press_timer.setSingleShot(True)
        self._long_press_timer.timeout.connect(self._emit_long_press)
        self._long_pressed = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._long_pressed = False
            self._long_press_timer.start(self._long_press_time)
            self.setDown(True)  # 눌림 상태 유지
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._long_press_timer.isActive():
                # 아직 타이머 만료 전 → 짧은 클릭
                self._long_press_timer.stop()
                if not self._long_pressed:
                    self.shortPressed.emit()
            self.setDown(False)  # 손 뗐을 때 눌림 해제
        super().mouseReleaseEvent(event)

    def _emit_long_press(self):
        self._long_pressed = True
        self.longPressed.emit()
        
        
class ColorMenuItem(QWidget):

    clicked = Signal(str)

    def __init__(self, color, text):
        super().__init__()

        self.color = color
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)

        color_box = QLabel()
        color_box.setFixedSize(14, 14)

        color_box.setStyleSheet(f"""
            background:{color};
            border:1px solid #666;
        """)

        label = QLabel(text)

        layout.addWidget(color_box)
        layout.addWidget(label)
        layout.addStretch()
        
    def set_normal(self):
        self.setStyleSheet("""
            background: transparent;
        """)

    def set_hover(self):
        self.setStyleSheet("""
            background: rgba(255,255,255,30);
            border-radius: 4px;
        """)

    def enterEvent(self, event):
        self.set_hover()

    def leaveEvent(self, event):
        self.set_normal()

    def mousePressEvent(self, event):
        self.clicked.emit(self.color)
        
def get_base_myApp_cd(init_layout : Literal["Horizontal","Vertical"]):
    class myApp(QWidget):
        def __init__(self):
            super().__init__()
            self.layout_main =[lambda : QHBoxLayout(), lambda : QVBoxLayout()][(init_layout == "Horizontal")^1]()
            self.setLayout(self.layout_main)
            self.setGeometry(50,50,500,500)
            self.initUI()
            self.show()
            
        def closeEvent(self, event):
            self.deleteLater()
            event.accept()
            
        def initUI(self):
            return
            
    return myApp

def run_base_myApp(app_cls):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    myApp = app_cls()
    sys.exit(app.exec())
    
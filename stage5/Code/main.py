import matplotlib
matplotlib.use('QtAgg')

import sys
from contextlib import contextmanager
from typing import List, Tuple, Union, Callable, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.style as mplstyle 
mplstyle.use('fast')
import psycopg2
from PySide6 import QtGui

from PySide6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, QDate, Signal, QSize
from PySide6.QtGui import QFont, QColor, QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout,QGroupBox,
    QFormLayout, QLabel, QLineEdit, QPushButton, QTableView, QMessageBox, QStatusBar,
    QHeaderView, QTabWidget, QSplitter, QSpinBox, QDoubleSpinBox, QDateEdit,
    QCheckBox, QListWidget, QListWidgetItem, QAbstractItemView, QDialog,QSizePolicy,
    QDialogButtonBox, QScrollArea, QFrame, QGraphicsDropShadowEffect, QGridLayout, QStyle
)
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize

# ------------------------------------------------------------------
# הגדרות עיצוב וסגנון - גרסה 5 (משופרת)
# ------------------------------------------------------------------
class AppStyles:
    PRIMARY_COLOR = "#007BFF"
    SECONDARY_COLOR = "#F8F9FA" # רקע כללי בהיר
    CONTENT_PANE_BG = "#F4F6F7" # רקע לאזורי תוכן
    BACKGROUND_COLOR = "#FFFFFF" # רקע לכרטיסים ופאנלים
    ACCENT_COLOR = "#28A745"
    DANGER_COLOR = "#DC3545"
    WARNING_COLOR = "#FFC107"
    INFO_COLOR = "#17A2B8"
    TEXT_COLOR = "#212529"
    SUBTLE_TEXT_COLOR = "#6C757D"
    BORDER_COLOR = "#DEE2E6"
    FONT_FAMILY = "Segoe UI"
    DRUG_COLOR = "#17A2B8"  # כחול-טורקיז לתרופות
    EQUIPMENT_COLOR = "#28A745" # ירוק לציוד

    STYLESHEET = f"""
        QWidget {{ font-family: "{FONT_FAMILY}"; font-size: 10pt; color: {TEXT_COLOR}; }}
        QMainWindow, QDialog {{ background-color: {SECONDARY_COLOR}; }}
        QScrollArea {{ background-color: transparent; border: none; }}

        /* --- עיצוב כרטיסים כללי --- */
        QFrame#CardWidget, QFrame#ClickableCardWidget {{
            border: 1px solid {BORDER_COLOR}; border-radius: 8px; background-color: {BACKGROUND_COLOR};
        }}
        QFrame#ClickableCardWidget:hover {{ border: 2px solid {PRIMARY_COLOR}; }}
        QLabel#CardTitle {{ font-size: 13pt; font-weight: bold; color: {PRIMARY_COLOR}; padding: 12px; border-bottom: 1px solid {BORDER_COLOR}; }}
        QLabel.UrgentStatus {{ color: white; background-color: {DANGER_COLOR}; padding: 2px 8px; border-radius: 4px; font-weight: bold; }}

        /* --- עיצוב טאבים ראשי --- */
        QTabWidget::pane {{ border: none; background-color: {CONTENT_PANE_BG}; }}
        QTabBar::tab {{ background: transparent; border: none; padding: 12px 25px; font-size: 11pt; font-weight: 600; color: {SUBTLE_TEXT_COLOR}; }}
        QTabBar::tab:selected {{ color: {PRIMARY_COLOR}; border-bottom: 3px solid {PRIMARY_COLOR}; }}

        /* --- כפתורים ושדות קלט --- */
        QPushButton {{ padding: 10px 15px; border-radius: 5px; border: none; background-color: {PRIMARY_COLOR}; color: white; font-weight: bold; }}
        QPushButton:hover {{ background-color: #0069D9; }}
        QPushButton:disabled {{ background-color: #BDBDBD; }}
        QPushButton.danger {{ background-color: {DANGER_COLOR}; }}
        QPushButton.danger:hover {{ background-color: #C82333; }}
        QPushButton.success {{ background-color: {ACCENT_COLOR}; }}
        QPushButton.success:hover {{ background-color: #218838; }}
        QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit {{ padding: 8px; border: 1px solid {BORDER_COLOR}; border-radius: 4px; background-color: #FFF; }}
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{ border: 1px solid {PRIMARY_COLOR}; }}

        /* --- עיצוב GroupBox (תיבות מקבצות) --- */
        QGroupBox {{
            font-size: 11pt;
            font-weight: bold;
            color: {PRIMARY_COLOR};
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
            margin-top: 10px;
            background-color: {BACKGROUND_COLOR};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 5px 10px;
            margin-left: 10px;
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 4px;
        }}
    """
# ------------------------------------------------------------------
# Database connection and other setup...
# ------------------------------------------------------------------
DB_DSN = "dbname=integration user=eitan password=ekfl2345 host=localhost port=5432"

@contextmanager
def get_conn(parent_widget: Optional[QWidget] = None):
    conn = None
    try:
        conn = psycopg2.connect(DB_DSN)
        yield conn
        conn.commit()
    except psycopg2.Error as e:
        if conn: conn.rollback()
        QMessageBox.critical(parent_widget, "Database Error", f"A database error occurred: {e}")
    except Exception as e:
        if conn: conn.rollback()
        QMessageBox.critical(parent_widget, "Application Error", f"An unexpected error occurred: {e}")
    finally:
        if conn: conn.close()

# ------------------------------------------------------------------
# SQL Queries from User Requirements (using the robust versions)
# ------------------------------------------------------------------
class Queries:
    ITEMS_WITH_SHORTAGE = """
        SELECT d.Name AS Item_Name, 'Drug' AS Item_Type,
               SUM(doi.Amount) AS Total_Ordered_Amount,
               (SELECT COALESCE(SUM(Amount), 0) FROM Drug_in_stock WHERE Drug_Id = d.Drug_Id) AS Total_Available_Amount,
               (SUM(doi.Amount) - (SELECT COALESCE(SUM(Amount), 0) FROM Drug_in_stock WHERE Drug_Id = d.Drug_Id)) AS Total_Shortage_Amount
        FROM Drug d JOIN Drug_order_item doi ON d.Drug_Id = doi.Drug_Id
        GROUP BY d.Drug_Id, d.Name
        HAVING SUM(doi.Amount) > (SELECT COALESCE(SUM(Amount), 0) FROM Drug_in_stock WHERE Drug_Id = d.Drug_Id)
        UNION ALL
        SELECT me.Name AS Item_Name, 'Equipment' AS Item_Type,
               SUM(eoi.Amount) AS Total_Ordered_Amount,
               (SELECT COALESCE(SUM(Amount), 0) FROM Equipment_in_stock WHERE Medical_Equipment_Id = me.Medical_Equipment_Id) AS Total_Available_Amount,
               (SUM(eoi.Amount) - (SELECT COALESCE(SUM(Amount), 0) FROM Equipment_in_stock WHERE Medical_Equipment_Id = me.Medical_Equipment_Id)) AS Total_Shortage_Amount
        FROM Medical_Equipment me JOIN Equipment_order_item eoi ON me.Medical_Equipment_Id = eoi.Medical_Equipment_Id
        GROUP BY me.Medical_Equipment_Id, me.Name
        HAVING SUM(eoi.Amount) > (SELECT COALESCE(SUM(Amount), 0) FROM Equipment_in_stock WHERE Medical_Equipment_Id = me.Medical_Equipment_Id)
        ORDER BY Total_Shortage_Amount DESC, Item_Type, Item_Name
    """
    DRUGS_NEARING_EXPIRY = """
        SELECT d.Name AS Drug_Name, w.Name AS Warehouse_Name, dis.Amount AS Amount,
               (d.Shelf_life - (CURRENT_DATE - dis.Since)) AS Days_Until_Expiry
        FROM Drug d
        JOIN Drug_in_stock dis ON d.Drug_Id = dis.Drug_Id
        JOIN Warehouse w ON dis.Warehouse_Id = w.Warehouse_Id
        WHERE (CURRENT_DATE - dis.Since) > (d.Shelf_life - 30) AND d.Shelf_life > 0
        ORDER BY Days_Until_Expiry, d.Drug_Id, dis.Warehouse_Id
    """
    MOST_ORDERED_DRUGS = """
        SELECT d.Drug_Id as Item_Id, d.Name AS Drug_Name, COUNT(DISTINCT doi.Order_Id) AS Orders_Count, SUM(doi.Amount) AS Total_Amount_Ordered
        FROM Drug d JOIN Drug_order_item doi ON d.Drug_Id = doi.Drug_Id
        GROUP BY d.Drug_Id
        ORDER BY Total_Amount_Ordered DESC, d.Drug_Id
    """
    DEPTS_WITH_URGENT_ORDERS = """
        SELECT d.Name AS Department_Name,
               (COUNT(CASE WHEN doi.Is_urgent = TRUE THEN 1 END) + COUNT(CASE WHEN eoi.Is_urgent = TRUE THEN 1 END)) AS Total_Urgent_Items_Count
        FROM Department d
        LEFT JOIN "Order" o ON d.Department_Id = o.Department_Id
        LEFT JOIN Drug_order_item doi ON o.Department_Id = doi.Department_Id AND o.Order_Id = doi.Order_Id
        LEFT JOIN Equipment_order_item eoi ON o.Department_Id = eoi.Department_Id AND o.Order_Id = eoi.Order_Id
        GROUP BY d.Department_Id
        HAVING (COUNT(CASE WHEN doi.Is_urgent = TRUE THEN 1 END) + COUNT(CASE WHEN eoi.Is_urgent = TRUE THEN 1 END)) > 0
        ORDER BY Total_Urgent_Items_Count DESC, d.Department_Id
    """
    WAREHOUSE_INVENTORY_SUMMARY = """
        SELECT w.Name AS Warehouse_Name,
               SUM(COALESCE(dis.Amount, 0)) AS Total_Drugs_Amount,
               SUM(COALESCE(eis.Amount, 0)) AS Total_Equipment_Amount
        FROM Warehouse w
        LEFT JOIN Drug_in_stock dis ON w.Warehouse_Id = dis.Warehouse_Id
        LEFT JOIN Equipment_in_stock eis ON w.Warehouse_Id = eis.Warehouse_Id
        GROUP BY w.Warehouse_Id
        ORDER BY GREATEST(SUM(COALESCE(dis.Amount, 0)), SUM(COALESCE(eis.Amount, 0))) DESC, w.Warehouse_Id
    """
    ITEM_DISTRIBUTION = """
        SELECT 'Drug' AS Item_Type, d.Name AS Item_Name, COUNT(DISTINCT dis.Warehouse_Id) AS Warehouse_Count
        FROM Drug d LEFT JOIN Drug_in_stock dis ON d.Drug_Id = dis.Drug_Id
        GROUP BY d.Drug_Id
        UNION ALL
        SELECT 'Equipment' AS Item_Type, me.Name AS Item_Name, COUNT(DISTINCT eis.Warehouse_Id) AS Warehouse_Count
        FROM Medical_Equipment me LEFT JOIN Equipment_in_stock eis ON me.Medical_Equipment_Id = eis.Medical_Equipment_Id
        GROUP BY me.Medical_Equipment_Id
        ORDER BY Warehouse_Count DESC, Item_Type, Item_Name
    """
    GET_TOP5_DOCTORS = "SELECT * FROM fn_get_top5_doctors(341);"
    GET_DRUG_POPULARITY_SCORE = "SELECT drug_id, popularity_score FROM drug WHERE drug_id = 5555;"

# ------------------------------------------------------------------
# Reusable UI Components
# ------------------------------------------------------------------
class CardWidget(QFrame):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("CardWidget")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(0, 0, 0, 10)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("CardTitle")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)
        self.content_layout = QFormLayout()
        self.content_layout.setSpacing(8)
        self.content_layout.setContentsMargins(15, 5, 15, 5)
        self.main_layout.addLayout(self.content_layout)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def add_row(self, label_text: str, value):
        label = QLabel(f"{label_text}:")
        label.setStyleSheet(f"color: {AppStyles.SUBTLE_TEXT_COLOR}; font-weight: bold;")
        if isinstance(value, bool):
            content = QLabel("Yes" if value else "No")
            content.setStyleSheet(f"color: {AppStyles.ACCENT_COLOR if value else AppStyles.DANGER_COLOR}; font-weight: bold;")
        elif isinstance(value, (int, float)):
            content = QLabel(f"{value:,}")
        else:
            content = QLabel(str(value) if value is not None else "N/A")
        self.content_layout.addRow(label, content)

    def add_status_row(self, label_text: str, value: str):
        label = QLabel(f"{label_text}:")
        label.setStyleSheet(f"color: {AppStyles.SUBTLE_TEXT_COLOR}; font-weight: bold;")
        content = QLabel(value)
        if 'urgent' in value.lower():
            content.setObjectName("UrgentStatus")
        self.content_layout.addRow(label, content)

class ClickableCardWidget(CardWidget):
    clicked = Signal()
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setObjectName("ClickableCardWidget")
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

def create_vertical_card_area():
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(QFrame.NoFrame)
    
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setAlignment(Qt.AlignTop)
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(10)
    
    scroll_area.setWidget(container)
    return scroll_area, container, layout

class AlertCard(CardWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet(f"QFrame#CardWidget {{ border-left: 5px solid {AppStyles.DANGER_COLOR}; }}")

class WarningCard(CardWidget):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.setStyleSheet(f"QFrame#CardWidget {{ border-left: 5px solid {AppStyles.WARNING_COLOR}; }}")

# ------------------------------------------------------------------
# Table Model and Login Screen (Largely Unchanged)
# ------------------------------------------------------------------
class PgTableModel(QAbstractTableModel):
    def __init__(self, header: List[str], data: List[Tuple]):
        super().__init__()
        self._header = [h.replace('_', ' ').title() for h in header]
        self._data = data
    def rowCount(self, parent=QtCore.QModelIndex()): return len(self._data)
    def columnCount(self, parent=QtCore.QModelIndex()): return len(self._header)
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._data) or index.column() >= len(self._header): return None
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, bool): return "Yes" if value else "No"
            if isinstance(value, QDate): return value.toString(Qt.ISODate)
            return "" if value is None else str(value)
        elif role == Qt.BackgroundRole:
            return QColor(AppStyles.BACKGROUND_COLOR) if index.row() % 2 else QColor("#F8F9FA")
        elif role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            return Qt.AlignRight | Qt.AlignVCenter if isinstance(value, (int, float)) else Qt.AlignLeft | Qt.AlignVCenter
        return None
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal: return self._header[section]
        if role == Qt.FontRole and orientation == Qt.Horizontal:
            font = QFont(); font.setBold(True); return font
        if role == Qt.BackgroundRole and orientation == Qt.Horizontal: return QColor("#E9ECEF")
        return None

def create_styled_table(table_view: QTableView):
    table_view.setStyleSheet(f"""
        QTableView {{
            gridline-color: {AppStyles.BORDER_COLOR};
            background-color: {AppStyles.BACKGROUND_COLOR};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            selection-background-color: {QColor(AppStyles.PRIMARY_COLOR).lighter(180).name()};
            selection-color: {AppStyles.TEXT_COLOR};
        }}
        QTableView::item {{ border: none; padding: 10px; }}
        QHeaderView::section {{
            background-color: {AppStyles.SECONDARY_COLOR};
            border: 1px solid {AppStyles.BORDER_COLOR};
            padding: 8px; font-weight: bold;
        }}
    """)
    table_view.setAlternatingRowColors(True)
    table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
    table_view.verticalHeader().hide()
    table_view.horizontalHeader().setStretchLastSection(True)
    return table_view

class LoginScreen(QWidget):
    # This class remains unchanged as its design is already polished.
    def __init__(self, switch_callback):
        super().__init__()
        self.switch_callback = switch_callback
        self.init_ui()
    def init_ui(self):
        main_layout = QHBoxLayout(self); main_layout.setContentsMargins(0, 0, 0, 0); main_layout.setSpacing(0)
        left_pane = QFrame(); left_pane.setObjectName("leftPane"); left_layout = QVBoxLayout(left_pane); left_layout.setContentsMargins(50, 50, 50, 50)
        branding_content = QWidget(); branding_layout = QVBoxLayout(branding_content); branding_layout.setSpacing(15); branding_layout.setAlignment(Qt.AlignCenter)
        logo_label = QLabel("H L"); logo_label.setObjectName("logoTextLabel")
        title_label = QLabel("Hospital Logistics"); title_label.setObjectName("brandingTitle")
        subtitle_label = QLabel("Efficiency in Every Aisle"); subtitle_label.setObjectName("brandingSubtitle")
        branding_layout.addWidget(logo_label, 0, Qt.AlignCenter); branding_layout.addWidget(title_label, 0, Qt.AlignCenter); branding_layout.addWidget(subtitle_label, 0, Qt.AlignCenter)
        left_layout.addStretch(1); left_layout.addWidget(branding_content); left_layout.addStretch(1)
        right_pane = QFrame(); right_pane.setObjectName("rightPane"); right_layout = QVBoxLayout(right_pane); right_layout.setAlignment(Qt.AlignCenter)
        form_container = QWidget(); form_container.setFixedWidth(360); form_layout = QVBoxLayout(form_container); form_layout.setContentsMargins(10, 10, 10, 10); form_layout.setSpacing(20)
        form_title = QLabel("System Access"); form_title.setObjectName("formTitle")
        self.id_input = QLineEdit(); self.id_input.setObjectName("loginInput"); self.id_input.setPlaceholderText("Enter your Worker ID"); self.id_input.returnPressed.connect(self.login)
        self.login_btn = QPushButton("Log In Securely"); self.login_btn.setObjectName("loginButton"); self.login_btn.setCursor(Qt.PointingHandCursor); self.login_btn.clicked.connect(self.login)
        form_layout.addWidget(form_title); form_layout.addSpacing(40); form_layout.addWidget(self.id_input); form_layout.addSpacing(40); form_layout.addWidget(self.login_btn)
        right_layout.addWidget(form_container); main_layout.addWidget(left_pane, 2); main_layout.addWidget(right_pane, 3)
        self.setStyleSheet(self.get_polished_stylesheet())
    def get_polished_stylesheet(self):
        LEFT_PANE_BG = "#1F2833"; RIGHT_PANE_BG = "#FFFFFF"; PRIMARY_COLOR = "#007BFF"; PRIMARY_HOVER_COLOR = "#0069D9"; PRIMARY_PRESSED_COLOR = "#0056B3"; TEXT_ON_DARK = "#ECF0F1"; TEXT_ON_LIGHT_PRIMARY = "#212529"; BORDER_COLOR = "#DEE2E6"
        return f"""QFrame#leftPane{{background-color:{LEFT_PANE_BG};}}QLabel#logoTextLabel{{font-family:"Segoe UI Light","Helvetica Neue","Arial";font-size:64px;font-weight:200;color:{PRIMARY_COLOR};border:3px solid {PRIMARY_COLOR};border-radius:60px;width:120px;height:120px;padding-bottom:5px;margin-bottom:20px;}}QLabel#brandingTitle{{font-size:36px;font-weight:600;color:white;letter-spacing:1px;}}QLabel#brandingSubtitle{{font-size:16px;font-weight:300;color:{TEXT_ON_DARK};}}QFrame#rightPane{{background-color:{RIGHT_PANE_BG};}}QLabel#formTitle{{font-size:26px;font-weight:600;color:{TEXT_ON_LIGHT_PRIMARY};text-align:left;}}QLineEdit#loginInput{{font-size:16px;padding:16px 10px;border:1px solid {BORDER_COLOR};border-radius:6px;background-color:#F8F9FA;color:{TEXT_ON_LIGHT_PRIMARY};}}QLineEdit#loginInput:focus{{border:2px solid {PRIMARY_COLOR};background-color:white;}}QPushButton#loginButton{{background-color:{PRIMARY_COLOR};color:white;font-size:16px;font-weight:700;padding:16px;border:none;border-radius:6px;border-bottom:3px solid {PRIMARY_PRESSED_COLOR};}}QPushButton#loginButton:hover{{background-color:{PRIMARY_HOVER_COLOR};}}QPushButton#loginButton:pressed{{background-color:{PRIMARY_PRESSED_COLOR};border-bottom:none;padding-top:19px;padding-bottom:13px;}}QPushButton#loginButton:disabled{{background-color:#BDBDBD;border-bottom:3px solid #9E9E9E;}}"""
    def login(self):
        self.login_btn.setText("Authenticating..."); self.login_btn.setEnabled(False); QApplication.processEvents()
        worker_id_text = self.id_input.text().strip()
        if not worker_id_text or not worker_id_text.isdigit(): self.show_error("Worker ID must be a valid number."); self.reset_login_button(); return
        worker_id = int(worker_id_text)
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                cur.execute("SELECT name FROM logistic_worker WHERE logistic_worker_id=%s", (worker_id,)); result = cur.fetchone()
                if not result: self.show_error("Worker ID not found."); self.reset_login_button(); return
                worker_name = result[0]
                cur.execute("SELECT MAX(level) FROM has_access WHERE logistic_worker_id=%s", (worker_id,)); level_result = cur.fetchone()
                is_manager = (level_result and level_result[0] is not None and level_result[0] >= 5)
                self.switch_callback("dashboard", worker_id=worker_id, worker_name=worker_name, is_manager=is_manager)
        except Exception as e: self.show_error(f"An error occurred: {e}"); self.reset_login_button()
    def show_error(self, message): msg = QMessageBox(self); msg.setIcon(QMessageBox.Warning); msg.setWindowTitle("Login Error"); msg.setText(message); msg.exec()
    def reset_login_button(self): self.login_btn.setText("Log In Securely"); self.login_btn.setEnabled(True)

# ------------------------------------------------------------------
# NEW: Compact Item Widget for Lists
# ------------------------------------------------------------------
class CompactItemWidget(QFrame):
    """וידג'ט קומפקטי ומעוצב להצגת פריט ברשימה (מלאי או הזמנה)."""
    def __init__(self, title: str, item_type: str, properties: dict):
        super().__init__()
        self.setObjectName("CompactItemWidget")
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        color_bar = QFrame()
        color_bar.setFixedWidth(5)
        type_color = AppStyles.DRUG_COLOR if item_type == 'drug' else AppStyles.EQUIPMENT_COLOR
        color_bar.setStyleSheet(f"background-color: {type_color}; border-radius: 2px;")
        
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setWordWrap(True)

        main_layout.addWidget(color_bar)
        main_layout.addWidget(title_label, 2)
        main_layout.addStretch(1)

        for key, value in properties.items():
            value_str = str(value)
            prop_label = QLabel(f"<i>{key}:</i> {value_str}")
            if 'urgent' in value_str.lower():
                prop_label.setStyleSheet(f"background-color: {AppStyles.DANGER_COLOR}; color: white; padding: 2px 5px; border-radius: 3px;")
            elif 'approved' in value_str.lower():
                prop_label.setStyleSheet(f"background-color: {AppStyles.ACCENT_COLOR}; color: white; padding: 2px 5px; border-radius: 3px;")
            main_layout.addWidget(prop_label)

        self.setStyleSheet(f"""
            QFrame#CompactItemWidget {{
                background-color: {AppStyles.BACKGROUND_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 5px;
            }}
        """)

# ------------------------------------------------------------------
# RESTORED: QuickStatsWidget for Dashboard
# ------------------------------------------------------------------
class QuickStatsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.value_labels = {}
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout(self); layout.setSpacing(20); layout.setContentsMargins(0, 0, 0, 0)
        
        stat_items = [
            ("warehouses", "Total Warehouses", "0", AppStyles.PRIMARY_COLOR, "SP_DirHomeIcon"),
            ("orders", "Active Orders", "0", AppStyles.ACCENT_COLOR, "SP_FileIcon"),
            ("workers", "Active Workers", "0", AppStyles.INFO_COLOR, "SP_DialogYesButton"),
            ("pending", "Pending Items", "0", AppStyles.WARNING_COLOR, "SP_MessageBoxWarning")
        ]
        
        for key, title, value, color, icon_name in stat_items:
            layout.addWidget(self.create_stat_card(key, title, value, color, icon_name))

    def create_stat_card(self, key: str, title: str, value: str, color: str, icon_name: str) -> QFrame:
        card = QFrame(); card.setObjectName("statCard")
        card_layout = QGridLayout(card); card_layout.setContentsMargins(15, 15, 20, 15); card_layout.setSpacing(5)
        icon_label = QLabel(); icon_label.setObjectName("statIcon"); icon_label.setStyleSheet(f"background-color: {color};")
        
        # Fixed icon color to be white on colored background
        icon = getattr(QStyle, icon_name)
        pixmap = self.style().standardPixmap(icon)
        mask = pixmap.createMaskFromColor(Qt.transparent, Qt.MaskOutColor)
        pixmap.fill(Qt.white)
        pixmap.setMask(mask)

        icon_label.setPixmap(pixmap.scaled(QSize(24, 24), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value); value_label.setObjectName("statValue")
        title_label = QLabel(title); title_label.setObjectName("statTitle")
        self.value_labels[key] = value_label
        card_layout.addWidget(icon_label, 0, 0, 2, 1); card_layout.addWidget(value_label, 0, 1); card_layout.addWidget(title_label, 1, 1); card_layout.setColumnStretch(1, 1)
        card.setStyleSheet(f"""
            QFrame#statCard {{ background-color: {AppStyles.BACKGROUND_COLOR}; border: 1px solid {AppStyles.BORDER_COLOR}; border-radius: 8px; }}
            QLabel#statIcon {{ min-width: 48px; max-width: 48px; min-height: 48px; max-height: 48px; border-radius: 24px; }}
            QLabel#statValue {{ font-size: 24pt; font-weight: 600; color: {AppStyles.TEXT_COLOR}; }}
            QLabel#statTitle {{ font-size: 10pt; font-weight: 500; color: {AppStyles.SUBTLE_TEXT_COLOR}; }}
        """)
        return card

    def update_stats(self, warehouses: int, orders: int, workers: int, pending: int):
        self.value_labels["warehouses"].setText(f"{warehouses:,}")
        self.value_labels["orders"].setText(f"{orders:,}")
        self.value_labels["workers"].setText(f"{workers:,}")
        self.value_labels["pending"].setText(f"{pending:,}")

# ------------------------------------------------------------------
# Dashboard Screen - Redesigned Tabs
# ------------------------------------------------------------------
class DashboardScreen(QWidget):
    def __init__(self, switch_callback, worker_id: int, worker_name: str, is_manager: bool, status_bar: QStatusBar):
        super().__init__()
        self.switch_callback, self.worker_id, self.worker_name, self.is_manager, self.status_bar = switch_callback, worker_id, worker_name, is_manager, status_bar
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(0, 0, 0, 0); main_layout.setSpacing(0)
        header_bar = QFrame(); header_bar.setObjectName("headerBar"); header_layout = QHBoxLayout(header_bar)
        welcome_label = QLabel(f"Welcome, <b>{self.worker_name}</b>"); welcome_label.setObjectName("headerWelcomeLabel")
        logout_btn = QPushButton("Logout"); logout_btn.setObjectName("headerLogoutButton"); logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(welcome_label); header_layout.addStretch(); header_layout.addWidget(logout_btn)
        self.tabs = QTabWidget()
        style = self.style(); icon_map = {'Dashboard': 'SP_ComputerIcon', 'My Warehouses': 'SP_DirHomeIcon', 'View Orders': 'SP_FileIcon', 'Management': 'SP_ToolBarHorizontalExtensionButton'}
        self.tabs.addTab(self.create_dashboard_tab(), style.standardIcon(getattr(QStyle, icon_map['Dashboard'])), " Dashboard")
        self.tabs.addTab(self.create_my_warehouses_tab(), style.standardIcon(getattr(QStyle, icon_map['My Warehouses'])), " My Warehouses")
        self.tabs.addTab(self.create_orders_tab(), style.standardIcon(getattr(QStyle, icon_map['View Orders'])), " View Orders")
        if self.is_manager: self.tabs.addTab(self.create_management_tab(), style.standardIcon(getattr(QStyle, icon_map['Management'])), " Management & Analytics")
        main_layout.addWidget(header_bar); main_layout.addWidget(self.tabs, 1)
        self.setStyleSheet(self.get_dashboard_stylesheet())

    def get_dashboard_stylesheet(self):
        return f"""
            QFrame#headerBar {{ background-color: #1F2833; padding: 10px 20px; }}
            QLabel#headerWelcomeLabel {{ font-size: 14pt; color: white; }}
            QPushButton#headerLogoutButton {{ background-color: transparent; color: white; border: 1px solid white; padding: 8px 20px; }}
            QPushButton#headerLogoutButton:hover {{ background-color: white; color: #1F2833; }}
            QFrame#leftPanel, QFrame#rightPanel {{ background-color: {AppStyles.BACKGROUND_COLOR}; border-radius: 8px; border: 1px solid {AppStyles.BORDER_COLOR}; }}
            QListWidget#navigationList {{ border: none; }}
            QListWidget#navigationList::item {{ padding: 15px; border-bottom: 1px solid {AppStyles.CONTENT_PANE_BG}; }}
            QListWidget#navigationList::item:hover {{ background-color: {QColor(AppStyles.PRIMARY_COLOR).lighter(190).name()}; }}
            QListWidget#navigationList::item:selected {{ background-color: {QColor(AppStyles.PRIMARY_COLOR).lighter(180).name()}; color: {AppStyles.PRIMARY_COLOR}; font-weight: 700; border-left: 4px solid {AppStyles.PRIMARY_COLOR}; }}
        """

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

    def logout(self):
        if QMessageBox.question(self, "Logout", "Are you sure?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.switch_callback("login")

    def create_dashboard_tab(self):
        main_container = QWidget()
        layout = QVBoxLayout(main_container); layout.setContentsMargins(25, 25, 25, 25); layout.setSpacing(25)
        self.quick_stats = QuickStatsWidget(); layout.addWidget(self.quick_stats)
        content_area = QWidget(); content_layout = QHBoxLayout(content_area); content_layout.setContentsMargins(0, 0, 0, 0); content_layout.setSpacing(25)
        self.left_column_layout = QVBoxLayout(); self.left_column_layout.setSpacing(25); self.left_column_layout.setAlignment(Qt.AlignTop)
        self.right_column_layout = QVBoxLayout(); self.right_column_layout.setSpacing(25); self.right_column_layout.setAlignment(Qt.AlignTop)
        content_layout.addLayout(self.left_column_layout, 2); content_layout.addLayout(self.right_column_layout, 1)
        layout.addWidget(content_area, 1)
        self.load_dashboard_data()
        return main_container

    def load_dashboard_data(self):
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM warehouse"); total_warehouses = cur.fetchone()[0]
                cur.execute('SELECT COUNT(DISTINCT order_id) FROM "Order"'); total_orders = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM logistic_worker"); total_workers = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM (SELECT 1 FROM drug_order_item WHERE status = 'pending' UNION ALL SELECT 1 FROM equipment_order_item WHERE status = 'pending') AS pending_items"); pending_items = cur.fetchone()[0]
                self.quick_stats.update_stats(total_warehouses, total_orders, total_workers, pending_items)
                self.load_dashboard_cards(cur)
                self.status_bar.showMessage("Dashboard loaded successfully.", 3000)
        except Exception as e:
            self.status_bar.showMessage(f"Failed to load dashboard data: {e}", 5000)

    def load_dashboard_cards(self, cur):
        self._clear_layout(self.left_column_layout); self._clear_layout(self.right_column_layout)
        cur.execute(Queries.ITEMS_WITH_SHORTAGE + " LIMIT 5")
        if shortages := cur.fetchall():
            card = AlertCard("Stock Shortages")
            for name, type_item, _, _, shortage in shortages: card.add_row(f"{name} ({type_item})", f"Short by {int(shortage)} units")
            self.right_column_layout.addWidget(card)
        cur.execute(Queries.DEPTS_WITH_URGENT_ORDERS + " LIMIT 5")
        if urgent_orders := cur.fetchall():
            card = AlertCard("Urgent Orders")
            for dept_name, urgent_count in urgent_orders: card.add_row(dept_name, f"{urgent_count} urgent items")
            self.right_column_layout.addWidget(card)
        self.right_column_layout.addStretch()
        cur.execute(Queries.DRUGS_NEARING_EXPIRY + " LIMIT 10")
        if expiries := cur.fetchall():
            expiry_card = WarningCard("Expiring Soon")
            for name, wh, amount, days_left in expiries: expiry_card.add_row(name, f"{int(days_left)} days left in {wh}")
            self.left_column_layout.addWidget(expiry_card)
        self.left_column_layout.addStretch()
        
    def create_my_warehouses_tab(self) -> QWidget:
        tab_container = QWidget(); tab_layout = QHBoxLayout(tab_container); tab_layout.setContentsMargins(20, 20, 20, 20); tab_layout.setSpacing(20)
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QFrame(); left_panel.setObjectName("leftPanel"); left_layout = QVBoxLayout(left_panel); left_layout.setContentsMargins(1, 1, 1, 1); left_layout.setSpacing(0)
        title_label = QLabel("<b>  Accessible Warehouses</b>"); title_label.setStyleSheet("padding: 5px;")
        left_layout.addWidget(title_label)
        self.warehouse_list = QListWidget(); self.warehouse_list.setObjectName("navigationList"); self.warehouse_list.currentItemChanged.connect(self.on_warehouse_selected)
        left_layout.addWidget(self.warehouse_list)
        right_panel = QFrame(); right_panel.setObjectName("rightPanel"); right_layout = QVBoxLayout(right_panel); right_layout.setContentsMargins(10, 10, 10, 10); right_layout.setSpacing(10)
        self.warehouse_title_label = QLabel("Select a Warehouse"); self.warehouse_title_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding-bottom: 5px;")
        self.stock_scroll_area, _, self.stock_layout = create_vertical_card_area()
        right_layout.addWidget(self.warehouse_title_label); right_layout.addWidget(self.stock_scroll_area, 1)
        splitter.addWidget(left_panel); splitter.addWidget(right_panel); splitter.setStretchFactor(0, 1); splitter.setStretchFactor(1, 3)
        tab_layout.addWidget(splitter)
        self.load_accessible_warehouses();
        if self.warehouse_list.count() > 0: self.warehouse_list.setCurrentRow(0)
        return tab_container

    def load_accessible_warehouses(self):
        self.warehouse_list.clear()
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                sql = "SELECT w.warehouse_id, w.name, CASE WHEN dw.warehouse_id IS NOT NULL THEN 'drug' WHEN mew.warehouse_id IS NOT NULL THEN 'equipment' ELSE 'unknown' END as type FROM warehouse w JOIN has_access ha ON w.warehouse_id = ha.warehouse_id LEFT JOIN drugs_warehouse dw ON w.warehouse_id = dw.warehouse_id LEFT JOIN medical_equipment_warehouse mew ON w.warehouse_id = mew.warehouse_id WHERE ha.logistic_worker_id = %s ORDER BY w.name"
                cur.execute(sql, (self.worker_id,))
                for wh_id, wh_name, wh_type in cur.fetchall():
                    item = QListWidgetItem(f"  {wh_name}"); item.setData(Qt.UserRole, {'id': wh_id, 'name': wh_name, 'type': wh_type})
                    icon = QStyle.SP_CustomBase if wh_type == 'drug' else QStyle.SP_ComputerIcon
                    item.setIcon(self.style().standardIcon(icon)); self.warehouse_list.addItem(item)
        except Exception as e: self.status_bar.showMessage(f"Failed to load warehouses: {e}", 5000)

    def on_warehouse_selected(self, current_item, _):
        if not current_item: return
        data = current_item.data(Qt.UserRole)
        self.warehouse_title_label.setText(f"Stock in: <b>{data['name']}</b>"); self.load_stock_for_warehouse(data['id'], data['type'])

    def load_stock_for_warehouse(self, warehouse_id: int, warehouse_type: str):
        self._clear_layout(self.stock_layout)
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                if warehouse_type == 'drug':
                    cur.execute("SELECT d.name, dis.amount, d.shelf_life, d.is_frozen FROM drug d JOIN drug_in_stock dis ON d.drug_id = dis.drug_id WHERE dis.warehouse_id = %s ORDER BY d.name;", (warehouse_id,))
                    for name, amount, shelf_life, is_frozen in cur.fetchall(): self.stock_layout.addWidget(CompactItemWidget(name, 'drug', {"In Stock": amount, "Shelf Life": f"{shelf_life} days", "Frozen": "Yes" if is_frozen else "No"}))
                elif warehouse_type == 'equipment':
                    cur.execute("SELECT me.name, eis.amount, me.device_category, me.emergency_use FROM medical_equipment me JOIN equipment_in_stock eis ON me.medical_equipment_id = eis.medical_equipment_id WHERE eis.warehouse_id = %s ORDER BY me.name;", (warehouse_id,))
                    for name, amount, category, emergency in cur.fetchall(): self.stock_layout.addWidget(CompactItemWidget(name, 'equipment', {"In Stock": amount, "Category": category, "Emergency": "Yes" if emergency else "No"}))
                if self.stock_layout.count() == 0: self.stock_layout.addWidget(QLabel("No items in this warehouse."))
                self.stock_layout.addStretch(1)
        except Exception as e: self.status_bar.showMessage(f"Failed to load stock data: {e}", 5000)

    def create_orders_tab(self) -> QWidget:
        tab_container = QWidget(); tab_layout = QHBoxLayout(tab_container); tab_layout.setContentsMargins(20, 20, 20, 20); tab_layout.setSpacing(20)
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QFrame(); left_panel.setObjectName("leftPanel"); left_layout = QVBoxLayout(left_panel); left_layout.setContentsMargins(10, 10, 10, 10); left_layout.setSpacing(10)
        left_layout.addWidget(QLabel("<b>My Department Orders</b>")); self.orders_scroll_area, _, self.orders_card_layout = create_vertical_card_area()
        left_layout.addWidget(self.orders_scroll_area, 1)
        right_panel = QFrame(); right_panel.setObjectName("rightPanel"); right_layout = QVBoxLayout(right_panel); right_layout.setContentsMargins(10, 10, 10, 10); right_layout.setSpacing(10)
        self.items_title_label = QLabel("Select an Order"); self.items_title_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding-bottom: 5px;")
        self.items_scroll_area, _, self.items_card_layout = create_vertical_card_area()
        right_layout.addWidget(self.items_title_label); right_layout.addWidget(self.items_scroll_area, 1)
        splitter.addWidget(left_panel); splitter.addWidget(right_panel); splitter.setStretchFactor(0, 1); splitter.setStretchFactor(1, 2)
        tab_layout.addWidget(splitter); self.load_orders(self.worker_id); return tab_container

    def load_orders(self, worker_id):
        self._clear_layout(self.orders_card_layout); self._clear_layout(self.items_card_layout)
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                sql = 'SELECT o.order_id, o.department_id, d.name, o.order_date FROM "Order" o JOIN Department d ON o.department_id = d.department_id JOIN Works_for wf ON d.department_id = wf.department_id WHERE wf.logistic_worker_id = %s ORDER BY o.order_date DESC'
                cur.execute(sql, (worker_id,)); all_orders = cur.fetchall()
                for oid, did, dname, odate in all_orders:
                    card = ClickableCardWidget(f"Order #{oid}"); card.add_row("Department", dname); card.add_row("Date", odate)
                    card.clicked.connect((lambda oid=oid, did=did: lambda: self.load_items_for_order(oid, did))())
                    self.orders_card_layout.addWidget(card)
                if all_orders: self.load_items_for_order(all_orders[0][0], all_orders[0][1])
                else: self.items_title_label.setText("No orders found")
        except Exception as e: self.status_bar.showMessage(f"Failed to load orders: {e}", 5000)

    def load_items_for_order(self, order_id, department_id):
        self.items_title_label.setText(f"Items in Order <b>#{order_id}</b>"); self._clear_layout(self.items_card_layout)
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                cur.execute("SELECT d.name, doi.amount, doi.is_urgent, doi.status FROM drug_order_item doi JOIN drug d ON doi.drug_id = d.drug_id WHERE doi.order_id = %s AND doi.department_id = %s", (order_id, department_id))
                for name, amount, is_urgent, status in cur.fetchall(): self.items_card_layout.addWidget(CompactItemWidget(name, 'drug', {"Amount": amount, "Status": f"Urgent, {status}" if is_urgent else status}))
                cur.execute("SELECT me.name, eoi.amount, eoi.is_urgent, eoi.status FROM equipment_order_item eoi JOIN medical_equipment me ON eoi.medical_equipment_id = me.medical_equipment_id WHERE eoi.order_id = %s AND eoi.department_id = %s", (order_id, department_id))
                for name, amount, is_urgent, status in cur.fetchall(): self.items_card_layout.addWidget(CompactItemWidget(name, 'equipment', {"Amount": amount, "Status": f"Urgent, {status}" if is_urgent else status}))
                if self.items_card_layout.count() == 0: self.items_card_layout.addWidget(QLabel("No items in this order."))
                self.items_card_layout.addStretch(1)
        except Exception as e: self.status_bar.showMessage(f"Failed to load items: {e}", 5000)

    def create_management_tab(self):
        container = QWidget(); layout = QVBoxLayout(container); layout.setContentsMargins(15, 15, 15, 15)
        mgmt_tabs = QTabWidget()
        mgmt_tabs.addTab(CrudScreen("logistic_worker", [("logistic_worker_id", "int"), ("name", "text"), ("shift_hours", "int")], ["logistic_worker_id"], self.status_bar), "Workers")
        mgmt_tabs.addTab(CrudScreen("warehouse", [("warehouse_id", "int"), ("name", "text"), ("location", "text"), ("active_hours", "text")], ["warehouse_id"], self.status_bar), "Warehouses")
        mgmt_tabs.addTab(CrudScreen("has_access", [("logistic_worker_id", "int"), ("warehouse_id", "int"), ("level", "int")], ["logistic_worker_id", "warehouse_id"], self.status_bar), "Access")
        mgmt_tabs.addTab(AnalyticsScreen(self.status_bar), "Analytics")
        if self.is_manager: mgmt_tabs.addTab(self.create_all_orders_tab(), "View All Orders")
        layout.addWidget(mgmt_tabs); return container

    def create_all_orders_tab(self):
        tab_container = QWidget(); tab_layout = QHBoxLayout(tab_container); tab_layout.setContentsMargins(20, 20, 20, 20); tab_layout.setSpacing(20)
        splitter = QSplitter(Qt.Horizontal)
        left_panel = QFrame(); left_panel.setObjectName("leftPanel"); left_layout = QVBoxLayout(left_panel); left_layout.setContentsMargins(10, 10, 10, 10); left_layout.setSpacing(10)
        left_layout.addWidget(QLabel("<b>All System Orders</b>")); self.all_orders_scroll_area, _, self.all_orders_card_layout = create_vertical_card_area()
        left_layout.addWidget(self.all_orders_scroll_area, 1)
        right_panel = QFrame(); right_panel.setObjectName("rightPanel"); right_layout = QVBoxLayout(right_panel); right_layout.setContentsMargins(10, 10, 10, 10); right_layout.setSpacing(10)
        self.all_orders_items_title_label = QLabel("Select an Order"); self.all_orders_items_title_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding-bottom: 5px;")
        self.all_orders_items_scroll_area, _, self.all_orders_items_card_layout = create_vertical_card_area()
        right_layout.addWidget(self.all_orders_items_title_label); right_layout.addWidget(self.all_orders_items_scroll_area, 1)
        splitter.addWidget(left_panel); splitter.addWidget(right_panel); splitter.setStretchFactor(0, 1); splitter.setStretchFactor(1, 2)
        tab_layout.addWidget(splitter); self.load_all_orders(); return tab_container

    def load_all_orders(self):
        self._clear_layout(self.all_orders_card_layout); self._clear_layout(self.all_orders_items_card_layout)
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                sql = 'SELECT o.order_id, o.department_id, d.name, o.order_date FROM "Order" o JOIN Department d ON o.department_id = d.department_id ORDER BY o.order_date DESC'
                cur.execute(sql); all_orders = cur.fetchall()
                for oid, did, dname, odate in all_orders:
                    card = ClickableCardWidget(f"Order #{oid}"); card.add_row("Department", dname); card.add_row("Date", odate)
                    card.clicked.connect((lambda oid=oid, did=did: lambda: self.load_items_for_all_orders_view(oid, did))())
                    self.all_orders_card_layout.addWidget(card)
                if all_orders: self.load_items_for_all_orders_view(all_orders[0][0], all_orders[0][1])
                else: self.all_orders_items_title_label.setText("No orders found in system")
        except Exception as e: self.status_bar.showMessage(f"Failed to load all orders: {e}", 5000)
    
    def load_items_for_all_orders_view(self, order_id, department_id):
        self.all_orders_items_title_label.setText(f"Items in Order <b>#{order_id}</b>"); self._clear_layout(self.all_orders_items_card_layout)
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                cur.execute("SELECT d.name, doi.amount, doi.is_urgent, doi.status FROM drug_order_item doi JOIN drug d ON doi.drug_id = d.drug_id WHERE doi.order_id = %s AND doi.department_id = %s", (order_id, department_id))
                for name, amount, is_urgent, status in cur.fetchall(): self.all_orders_items_card_layout.addWidget(CompactItemWidget(name, 'drug', {"Amount": amount, "Status": f"Urgent, {status}" if is_urgent else status}))
                cur.execute("SELECT me.name, eoi.amount, eoi.is_urgent, eoi.status FROM equipment_order_item eoi JOIN medical_equipment me ON eoi.medical_equipment_id = me.medical_equipment_id WHERE eoi.order_id = %s AND eoi.department_id = %s", (order_id, department_id))
                for name, amount, is_urgent, status in cur.fetchall(): self.all_orders_items_card_layout.addWidget(CompactItemWidget(name, 'equipment', {"Amount": amount, "Status": f"Urgent, {status}" if is_urgent else status}))
                if self.all_orders_items_card_layout.count() == 0: self.all_orders_items_card_layout.addWidget(QLabel("No items in this order."))
                self.all_orders_items_card_layout.addStretch(1)
        except Exception as e: self.status_bar.showMessage(f"Failed to load items: {e}", 5000)

# ------------------------------------------------------------------
# AnalyticsScreen with Improved Layout & FIXED LOGIC
# ------------------------------------------------------------------
class AnalyticsScreen(QWidget):
    def __init__(self, status_bar: QStatusBar):
        super().__init__(); self.status_bar = status_bar; self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(10, 10, 10, 10)
        tabs = QTabWidget(); tabs.addTab(self.create_reports_tab(), "Reports"); tabs.addTab(self.create_procedures_tab(), "Procedures")
        main_layout.addWidget(tabs)

    def create_reports_tab(self):
        container = QWidget(); layout = QVBoxLayout(container); layout.setSpacing(15)
        controls_widget = QWidget(); controls_layout = QHBoxLayout(controls_widget); controls_layout.setContentsMargins(0,0,0,0)
        reports_group = QGroupBox(""); reports_grid = QGridLayout(reports_group); reports_grid.setSpacing(10)
        fixed_queries = [("Items with Shortage", Queries.ITEMS_WITH_SHORTAGE),("Drugs Nearing Expiry", Queries.DRUGS_NEARING_EXPIRY),("Most Ordered Drugs", Queries.MOST_ORDERED_DRUGS),("Depts with Urgent Orders", Queries.DEPTS_WITH_URGENT_ORDERS),("Warehouse Inventory", Queries.WAREHOUSE_INVENTORY_SUMMARY),("Top 5 Doctors (Dept 341)", Queries.GET_TOP5_DOCTORS)]
        for i, (name, sql) in enumerate(fixed_queries):
            btn = QPushButton(name); btn.clicked.connect(lambda s=sql, n=name: self.run_query(s, n)); reports_grid.addWidget(btn, i // 2, i % 2)
        params_group = QGroupBox(""); params_layout = QVBoxLayout(params_group)
        pop_layout = QHBoxLayout(); self.drug_id_input = QSpinBox(); self.drug_id_input.setRange(1, 999999); self.drug_id_input.setValue(5555)
        pop_btn = QPushButton("Get Drug Popularity"); pop_btn.clicked.connect(self._run_drug_popularity_query)
        pop_layout.addWidget(QLabel("Drug ID:")); pop_layout.addWidget(self.drug_id_input); pop_layout.addWidget(pop_btn)
        params_layout.addLayout(pop_layout)
        controls_layout.addWidget(reports_group, 2); controls_layout.addWidget(params_group, 1)
        self.table_view = QTableView(); create_styled_table(self.table_view)
        layout.addWidget(controls_widget); layout.addWidget(self.table_view, 1)
        return container

    def create_procedures_tab(self):
        container = QWidget(); layout = QVBoxLayout(container); layout.setAlignment(Qt.AlignTop); layout.setSpacing(15)
        proc_group = QGroupBox(""); proc_group.setFixedWidth(400)
        proc_layout = QVBoxLayout(proc_group)
        btn_promote = QPushButton("Promote Busy Doctors"); btn_promote.clicked.connect(lambda: self.call_proc("pr_promote_busy_doctors"))
        btn_refresh = QPushButton("Refresh All Drug Popularity Scores"); btn_refresh.clicked.connect(lambda: self.call_proc("pr_refresh_drug_popularity"))
        proc_layout.addWidget(btn_promote); proc_layout.addWidget(btn_refresh)
        layout.addWidget(proc_group); return container

    def _run_drug_popularity_query(self):
        drug_id = self.drug_id_input.value()
        self.run_query(f"SELECT drug_id, popularity_score FROM drug WHERE drug_id = {drug_id};", f"Drug Pop. (ID {drug_id})")

    def run_query(self, sql, name):
        self.status_bar.showMessage(f"Running '{name}'...")
        try:
            with get_conn(self) as conn:
                cur = conn.cursor(); cur.execute(sql); data = cur.fetchall(); cols = [d[0] for d in cur.description]
                proxy = QSortFilterProxyModel(); proxy.setSourceModel(PgTableModel(cols, data))
                self.table_view.setModel(proxy); self.table_view.resizeColumnsToContents()
                self.status_bar.showMessage(f"'{name}' found {len(data)} rows.", 4000)
        except Exception as e: QMessageBox.critical(self, "Query Error", str(e))

    # In class AnalyticsScreen:

# In class AnalyticsScreen:

    def call_proc(self, proc_name: str):
        self.status_bar.showMessage(f"Calling procedure '{proc_name}'...")
        try:
            with get_conn(self) as conn:
                cur = conn.cursor()
                cur.execute(f"CALL {proc_name}()")
                conn.commit() 
                QMessageBox.information(self, "Procedure Called", f"Procedure '{proc_name}' executed successfully.")
                self.status_bar.showMessage(f"Procedure '{proc_name}' completed.", 4000)
        except psycopg2.Error as e:
            QMessageBox.critical(self, "Database Error", f"Error calling procedure '{proc_name}':\n{e}")
            self.status_bar.showMessage(f"Error calling procedure '{proc_name}'.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred:\n{e}")
            self.status_bar.showMessage(f"An unexpected error occurred with '{proc_name}'.", 5000)


# ------------------------------------------------------------------
# CRUD Screen with Improved Layout
# ------------------------------------------------------------------
class CrudScreen(QWidget):
    def __init__(self, table: str, columns: List[Tuple[str, str]], pk_cols: List[str], status_bar: QStatusBar):
        super().__init__(); self.table, self.cols, self.pks, self.status_bar = table, columns, pk_cols, status_bar; self.proxy_model = None; self.init_ui(); self.refresh()

    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(10, 10, 10, 10)
        splitter = QSplitter(Qt.Vertical)
        top_widget = QWidget(); top_layout = QVBoxLayout(top_widget); top_layout.setSpacing(10)
        search_layout = QHBoxLayout(); self.search_input = QLineEdit(); self.search_input.setPlaceholderText(f"Search in {self.table.replace('_', ' ')}..."); self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(QLabel("Search:")); search_layout.addWidget(self.search_input)
        self.view = QTableView(); self.view.setSortingEnabled(True); self.view.clicked.connect(self.row_to_inputs); create_styled_table(self.view)
        top_layout.addLayout(search_layout); top_layout.addWidget(self.view)
        form_group = QGroupBox(f""); group_layout = QVBoxLayout(form_group)
        form = QFormLayout(); self.inputs = {}
        for col, typ in self.cols:
            w = QLineEdit()
            if typ == "int": w = QSpinBox(); w.setRange(-2**31, 2**31 - 1)
            elif typ == "date": w = QDateEdit(calendarPopup=True, date=QDate.currentDate(), displayFormat="yyyy-MM-dd")
            elif typ == "bool": w = QCheckBox()
            self.inputs[col] = w; form.addRow(col.replace('_', ' ').title(), w)
        btn_row = QHBoxLayout(); self.add_btn = QPushButton("Add"); self.add_btn.setObjectName("success"); self.add_btn.clicked.connect(self.add_row)
        self.edit_btn = QPushButton("Update"); self.edit_btn.clicked.connect(self.edit_row); self.del_btn = QPushButton("Delete"); self.del_btn.setObjectName("danger"); self.del_btn.clicked.connect(self.del_row)
        self.clear_btn = QPushButton("Clear"); self.clear_btn.clicked.connect(self.clear_inputs)
        btn_row.addWidget(self.add_btn); btn_row.addWidget(self.edit_btn); btn_row.addWidget(self.del_btn); btn_row.addStretch(); btn_row.addWidget(self.clear_btn)
        group_layout.addLayout(form); group_layout.addLayout(btn_row)
        splitter.addWidget(top_widget); splitter.addWidget(form_group)
        splitter.setStretchFactor(0, 3); splitter.setStretchFactor(1, 1); main_layout.addWidget(splitter)
    
    def filter_table(self, text: str):
        if self.proxy_model: self.proxy_model.setFilterRegularExpression(text)
    def row_to_inputs(self, index):
        if not self.proxy_model: return
        source_index = self.proxy_model.mapToSource(index); row_data = self.proxy_model.sourceModel()._data[source_index.row()]
        for i, (col_name, _) in enumerate(self.cols):
            widget, value = self.inputs[col_name], row_data[i]
            if isinstance(widget, QLineEdit): widget.setText(str(value) if value is not None else "")
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)): widget.setValue(value if value is not None else 0)
            elif isinstance(widget, QDateEdit): widget.setDate(value if value else QDate.currentDate())
            elif isinstance(widget, QCheckBox): widget.setChecked(bool(value))
    def get_input_values(self):
        values = {}
        for col_name, _ in self.cols:
            widget = self.inputs[col_name]
            if isinstance(widget, QLineEdit): values[col_name] = widget.text()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)): values[col_name] = widget.value()
            elif isinstance(widget, QDateEdit): values[col_name] = widget.date().toString(Qt.ISODate)
            elif isinstance(widget, QCheckBox): values[col_name] = widget.isChecked()
        return values
    def clear_inputs(self):
        for widget in self.inputs.values():
            if isinstance(widget, QLineEdit): widget.clear()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)): widget.setValue(0)
            elif isinstance(widget, QDateEdit): widget.setDate(QDate.currentDate())
            elif isinstance(widget, QCheckBox): widget.setChecked(False)
        self.view.clearSelection()
    def refresh(self):
        try:
            with get_conn(self) as conn:
                cur = conn.cursor(); cur.execute(f"SELECT {', '.join(c for c, _ in self.cols)} FROM {self.table}"); data = cur.fetchall(); header = [d[0] for d in cur.description]
                model = PgTableModel(header, data); self.proxy_model = QSortFilterProxyModel(); self.proxy_model.setSourceModel(model); self.view.setModel(self.proxy_model)
        except Exception as e: self.status_bar.showMessage(f"Failed to load {self.table}: {e}", 5000)
    def add_row(self):
        values = self.get_input_values(); cols = [c for c, _ in self.cols]; vals = [values[c] for c in cols]
        sql = f"INSERT INTO {self.table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
        try:
            with get_conn(self) as conn: cur = conn.cursor(); cur.execute(sql, tuple(vals)); conn.commit(); self.refresh(); self.clear_inputs()
        except Exception as e: QMessageBox.critical(self, "Add Error", str(e))
    def edit_row(self):
        if not self.view.selectionModel().hasSelection(): QMessageBox.warning(self, "Update Error", "Select a row to update."); return
        values = self.get_input_values(); pk_vals = []; where_clauses = []; set_clauses = []; update_vals = []
        for c in self.pks: where_clauses.append(f"{c} = %s"); pk_vals.append(self.get_input_values()[c])
        for c, _ in self.cols:
            if c not in self.pks: set_clauses.append(f"{c} = %s"); update_vals.append(values[c])
        sql = f"UPDATE {self.table} SET {', '.join(set_clauses)} WHERE {' AND '.join(where_clauses)}"
        try:
            with get_conn(self) as conn: cur = conn.cursor(); cur.execute(sql, tuple(update_vals + pk_vals)); conn.commit(); self.refresh(); self.clear_inputs()
        except Exception as e: QMessageBox.critical(self, "Update Error", str(e))
    def del_row(self):
        if not self.view.selectionModel().hasSelection(): QMessageBox.warning(self, "Delete Error", "Select a row to delete."); return
        if QMessageBox.question(self, "Confirm Delete", "Are you sure?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No: return
        pk_vals = []; where_clauses = []
        for c in self.pks: where_clauses.append(f"{c} = %s"); pk_vals.append(self.get_input_values()[c])
        sql = f"DELETE FROM {self.table} WHERE {' AND '.join(where_clauses)}"
        try:
            with get_conn(self) as conn: cur = conn.cursor(); cur.execute(sql, tuple(pk_vals)); conn.commit(); self.refresh(); self.clear_inputs()
        except Exception as e: QMessageBox.critical(self, "Delete Error", str(e))

# ------------------------------------------------------------------
# Main Window
# ------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Logistics System"); self.setGeometry(100, 100, 1600, 900); self.showMaximized()
        self.setStyleSheet(AppStyles.STYLESHEET)
        self.status_bar = QStatusBar(); self.setStatusBar(self.status_bar); self.status_bar.showMessage("Ready.", 3000)
        self.stacked_widget = QStackedWidget(); self.setCentralWidget(self.stacked_widget)
        self.login_screen = LoginScreen(self.switch_screen); self.dashboard_screen = None
        self.stacked_widget.addWidget(self.login_screen)

    def switch_screen(self, screen_name: str, **kwargs):
        if screen_name == "login":
            if self.dashboard_screen: self.stacked_widget.removeWidget(self.dashboard_screen); self.dashboard_screen.deleteLater(); self.dashboard_screen = None
            self.stacked_widget.setCurrentWidget(self.login_screen)
        elif screen_name == "dashboard":
            self.dashboard_screen = DashboardScreen(self.switch_screen, kwargs.get("worker_id"), kwargs.get("worker_name"), kwargs.get("is_manager"), self.status_bar)
            self.stacked_widget.addWidget(self.dashboard_screen); self.stacked_widget.setCurrentWidget(self.dashboard_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
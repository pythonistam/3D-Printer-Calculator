import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QTabWidget, QFormLayout, QFrame
)
from PyQt6.QtCore import Qt

DEFAULT_CONFIG = {
    "plastic_price": 10000.0,
    "part_weight": 0.0,
    "support_weight": 0.0,
    "print_time": 0.0,
    "modeling_cost": 0.0,
    "quantity": 1,
    "batch_size": 10,
    "energy_price": 50.0,
    "printer_power": 0.3,
    "printer_wear": 20.0
}

STYLE_SHEET = """
QWidget {
    background-color: #1e1e1e;
    color: #d4d4d4;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QTabWidget::pane {
    border: 1px solid #333333;
    background-color: #1e1e1e;
    border-radius: 6px;
}

QTabBar::tab {
    background-color: #252526;
    border: 1px solid #333333;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 16px;
    margin-right: 2px;
    color: #858585;
}

QTabBar::tab:hover {
    background-color: #2d2d2d;
    color: #d4d4d4;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    color: #ffffff;
    border-bottom: 2px solid #007acc;
    font-weight: bold;
}

QLineEdit {
    background-color: #2d2d2d;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 6px;
    color: #ffffff;
    selection-background-color: #007acc;
}

QLineEdit:focus {
    border: 1px solid #007acc;
    background-color: #303030;
}

QPushButton {
    background-color: #007acc;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0098ff;
}

QPushButton:pressed {
    background-color: #005999;
}

QFrame#result_box {
    background-color: #252526;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 12px;
}

QLabel#result_title {
    color: #858585;
    font-size: 11px;
    font-weight: bold;
}

QLabel#total_result_val {
    color: #4fc1ff;
    font-size: 17px;
    font-weight: bold;
}

QLabel#part_result_val {
    color: #9cdcfe;
    font-size: 14px;
    font-weight: bold;
}

QLabel#batch_result_val {
    color: #a7dbff;
    font-size: 14px;
    font-weight: bold;
}

QMessageBox {
    background-color: #1e1e1e;
}

QMessageBox QLabel {
    color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""

def get_config_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, 'config.json')

def load_config():
    path = get_config_path()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except Exception:
            return DEFAULT_CONFIG.copy()
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

def save_config(config):
    path = get_config_path()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}")

class CostCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор стоимости 3D-печати")
        self.setFixedSize(360, 520)
        self.config = load_config()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(STYLE_SHEET)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Tab widget
        self.tabs = QTabWidget()
        
        # Tab 1: Calculation
        self.calc_tab = QWidget()
        calc_layout = QVBoxLayout()
        calc_layout.setContentsMargins(5, 10, 5, 5)
        calc_layout.setSpacing(8)
        
        calc_form = QFormLayout()
        calc_form.setSpacing(8)
        calc_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.inputs = {}
        
        calc_fields = [
            ("Цена пластика (Драм/кг):", "plastic_price"),
            ("Вес детали (г):", "part_weight"),
            ("Вес поддержек (г):", "support_weight"),
            ("Время печати (ч):", "print_time"),
            ("Моделирование (Драм):", "modeling_cost"),
            ("Количество в расчете (шт):", "quantity"),
            ("Размер партии (шт):", "batch_size"),
        ]
        
        for label_text, key in calc_fields:
            line_edit = QLineEdit()
            line_edit.setText(str(self.config.get(key, DEFAULT_CONFIG[key])))
            self.inputs[key] = line_edit
            calc_form.addRow(label_text, line_edit)
            
        calc_layout.addLayout(calc_form)
        
        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.clicked.connect(self.calculate)
        calc_layout.addWidget(self.calc_button)
        
        # Result Box
        self.result_box = QFrame()
        self.result_box.setObjectName("result_box")
        result_layout = QVBoxLayout(self.result_box)
        result_layout.setContentsMargins(12, 12, 12, 12)
        result_layout.setSpacing(6)
        
        self.result_title = QLabel("РЕЗУЛЬТАТЫ РАСЧЕТА:")
        self.result_title.setObjectName("result_title")
        result_layout.addWidget(self.result_title)
        
        self.total_result_label = QLabel("Итоговая стоимость: 0.00 Драм.")
        self.total_result_label.setObjectName("total_result_val")
        result_layout.addWidget(self.total_result_label)
        
        self.part_result_label = QLabel("Стоимость за 1 шт: 0.00 Драм.")
        self.part_result_label.setObjectName("part_result_val")
        result_layout.addWidget(self.part_result_label)

        self.batch_result_label = QLabel("Стоимость партии: 0.00 Драм.")
        self.batch_result_label.setObjectName("batch_result_val")
        result_layout.addWidget(self.batch_result_label)
        
        calc_layout.addWidget(self.result_box)
        self.calc_tab.setLayout(calc_layout)
        
        # Tab 2: Settings
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(5, 10, 5, 5)
        settings_layout.setSpacing(8)
        
        settings_form = QFormLayout()
        settings_form.setSpacing(8)
        settings_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        settings_fields = [
            ("Цена за 1 кВт⋅ч (Драм):", "energy_price"),
            ("Мощность принтера (кВт):", "printer_power"),
            ("Износ принтера (Драм/ч):", "printer_wear"),
        ]
        
        for label_text, key in settings_fields:
            line_edit = QLineEdit()
            line_edit.setText(str(self.config.get(key, DEFAULT_CONFIG[key])))
            self.inputs[key] = line_edit
            settings_form.addRow(label_text, line_edit)
            
        settings_layout.addLayout(settings_form)
        
        self.save_button = QPushButton("Сохранить настройки")
        self.save_button.clicked.connect(self.save_settings_action)
        settings_layout.addWidget(self.save_button)
        
        settings_layout.addStretch()
        self.settings_tab.setLayout(settings_layout)
        
        # Add tabs
        self.tabs.addTab(self.calc_tab, "Расчёт")
        self.tabs.addTab(self.settings_tab, "Настройки")
        
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def calculate(self):
        try:
            plastic_price = float(self.inputs["plastic_price"].text())
            part_weight = float(self.inputs["part_weight"].text())
            support_weight = float(self.inputs["support_weight"].text())
            print_time = float(self.inputs["print_time"].text())
            modeling_cost = float(self.inputs["modeling_cost"].text())
            quantity = int(self.inputs["quantity"].text())
            batch_size = int(self.inputs["batch_size"].text())

            energy_price = float(self.inputs["energy_price"].text())
            printer_power = float(self.inputs["printer_power"].text())
            printer_wear = float(self.inputs["printer_wear"].text())

            if quantity <= 0 or batch_size <= 0:
                raise ValueError("Количество деталей и размер партии должны быть больше нуля.")

            # Calculations
            material_cost = (part_weight + support_weight) / 1000 * plastic_price
            energy_cost = print_time * printer_power * energy_price
            wear_cost = print_time * printer_wear
            total_cost = material_cost + energy_cost + wear_cost + modeling_cost
            
            part_cost = total_cost / quantity
            batch_cost = part_cost * batch_size

            # Update results
            self.total_result_label.setText(f"Итоговая стоимость ({quantity} шт): {total_cost:.2f} Драм.")
            self.part_result_label.setText(f"Стоимость за 1 шт: {part_cost:.2f} Драм.")
            self.batch_result_label.setText(f"Стоимость партии ({batch_size} шт): {batch_cost:.2f} Драм.")

            self.save_current_state_to_config()
        except ValueError:
            QMessageBox.warning(
                self, 
                "Ошибка", 
                "Пожалуйста, заполните все поля корректными числами.\nКоличество и размер партии должны быть целыми числами больше 0."
            )

    def save_current_state_to_config(self):
        for key in self.inputs:
            try:
                val_str = self.inputs[key].text()
                if key in ["quantity", "batch_size"]:
                    self.config[key] = int(val_str)
                else:
                    self.config[key] = float(val_str)
            except ValueError:
                pass
        save_config(self.config)

    def save_settings_action(self):
        try:
            # Validate only settings fields
            energy_price = float(self.inputs["energy_price"].text())
            printer_power = float(self.inputs["printer_power"].text())
            printer_wear = float(self.inputs["printer_wear"].text())
            
            self.config["energy_price"] = energy_price
            self.config["printer_power"] = printer_power
            self.config["printer_wear"] = printer_wear
            
            # Save any valid calculation inputs too
            for key in ["plastic_price", "part_weight", "support_weight", "print_time", "modeling_cost", "quantity", "batch_size"]:
                try:
                    val_str = self.inputs[key].text()
                    if key in ["quantity", "batch_size"]:
                        self.config[key] = int(val_str)
                    else:
                        self.config[key] = float(val_str)
                except ValueError:
                    pass
            
            save_config(self.config)
            QMessageBox.information(self, "Успех", "Настройки успешно сохранены.")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректные числа в полях настроек.")

    def closeEvent(self, event):
        self.save_current_state_to_config()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CostCalculator()
    window.show()
    sys.exit(app.exec())

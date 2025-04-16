import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)

class CostCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор стоимости 3D-печати")
        self.setFixedSize(300, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.inputs = {}

        fields = [
            ("Цена пластика (Драм/кг)", "plastic_price", "0"),
            ("Вес детали (г)", "part_weight", "0"),
            ("Вес поддержек (г)", "support_weight", "0"),
            ("Время печати (ч)", "print_time", "0"),
            ("Цена за 1 кВт⋅ч (Драм)", "energy_price", "0"),
            ("Мощность принтера (кВт)", "printer_power", "0"),
            ("Износ принтера (Драм/ч)", "printer_wear", "0"),
            ("Моделирование (Драм)", "modeling_cost", "0"),
        ]

        for label_text, key, default_value in fields:
            h_layout = QHBoxLayout()
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setText(default_value)
            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            layout.addLayout(h_layout)
            self.inputs[key] = line_edit

        self.result_label = QLabel("Стоимость: ... Драм.")
        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.clicked.connect(self.calculate)

        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

    def calculate(self):
        try:
            plastic_price = float(self.inputs["plastic_price"].text())
            part_weight = float(self.inputs["part_weight"].text())
            support_weight = float(self.inputs["support_weight"].text())
            print_time = float(self.inputs["print_time"].text())
            energy_price = float(self.inputs["energy_price"].text())
            printer_power = float(self.inputs["printer_power"].text())
            printer_wear = float(self.inputs["printer_wear"].text())
            modeling_cost = float(self.inputs["modeling_cost"].text())

            material_cost = (part_weight + support_weight) / 1000 * plastic_price
            energy_cost = print_time * printer_power * energy_price
            wear_cost = print_time * printer_wear
            total_cost = material_cost + energy_cost + wear_cost + modeling_cost

            self.result_label.setText(f"Стоимость: {total_cost:.2f} Драм.")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля корректными числами.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CostCalculator()
    window.show()
    sys.exit(app.exec())

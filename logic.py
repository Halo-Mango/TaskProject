from PyQt6.QtWidgets import *
from PyQt6.QtCore import QStringListModel
from gui import *  # Make sure this is your correct .ui import
import csv
import os

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        # Create tasks.csv with headers (like you did with voter_info.csv)
        with open("tasks.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Task", "Date", "Time", "Category",])

        self.setupUi(self)

        self.model = QStringListModel()
        self.listView.setModel(self.model)

        self.date_line.setPlaceholderText('MM/DD')
        self.task_line.setPlaceholderText("Enter task ")
        self.time_line.setPlaceholderText("??:??AM/PM")

        self.add_task_button.clicked.connect(self.add_task)
        self.complete_button.clicked.connect(self.mark_task_complete)

        self.load_tasks()
        self.model = QStringListModel()
        self.listView.setModel(self.model)



    def add_task(self):

        task = self.task_line.text().strip()
        date = self.date_line.text().strip().lower()
        time = self.time_line.text().strip().lower()
        category = self.cat_dropdown.currentText().strip()

        if not task or not date or not time:
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")
            return

        if len(date) != 5 or date[2] != '/' or not (date[:2] + date[3:]).isdigit():
            QMessageBox.warning(self, "Input Error", "Invalid Date.")
            return

        month = int(date[:2])
        day = int(date[3:])

        if not (1 <= month <= 12 and 1 <= day <= 31):
            QMessageBox.warning(self, "Input Error", "Date must be a valid Month/Date.")
            return

        # TIME: Must be in HH:MMam or HH:MMpm format and valid
        if len(time) != 7 or time[2] != ':' or not (time[:2] + time[3:5]).isdigit():
            QMessageBox.warning(self, "Input Error", "Invalid Time")
            return

        hour = int(time[:2])
        minute = int(time[3:5])
        suffix = time[5:]

        if not (1 <= hour <= 12 and 0 <= minute <= 59):
            QMessageBox.warning(self, "Input Error", "Time must have valid hour and minute")
            return

        if suffix not in ['am', 'pm']:
            QMessageBox.warning(self, "Input Error", "'am' or 'pm'.")
            return

        row = [task, date, time, category, "Pending"]

        with open("tasks.csv", mode="r", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for existing_row in reader:
                existing_date = existing_row[1].strip().lower()
                existing_time = existing_row[2].strip().lower()
                if existing_date == date and existing_time == time:
                    QMessageBox.warning(self, "Time Conflict", f"A task already exists at {time} on {date}.")
                    return



        try:
            with open("tasks.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(row)

            self.load_tasks()
            self.task_line.clear()
            self.date_line.clear()
            self.time_line.clear()
            self.cat_dropdown.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add task:\n{e}")








    def load_tasks(self):
        try:
            with open("tasks.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                tasks = [
                    f" {row[0]:<30} Due: {row[1]:<30}  {row[2]:<30}  {row[3]}" for row in reader]
            self.model.setStringList(tasks)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load tasks:\n{e}")

    def mark_task_complete(self):
        selected_index = self.listView.currentIndex()

        if not selected_index.isValid():
            QMessageBox.warning(self, "Selection Error", "Please select a task to mark complete.")
            return

        try:
            with open("tasks.csv", mode="r", newline='') as file:
                reader = csv.reader(file)
                data = list(reader)  # Full CSV including header

            selected_row = selected_index.row() + 1  # Now it matches real row (since header is at index 0)

            if selected_row >= len(data):
                QMessageBox.warning(self, "Error", "Invalid task selection.")
                return

            del data[selected_row]

            with open("tasks.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)

            self.load_tasks()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete task:\n{e}")

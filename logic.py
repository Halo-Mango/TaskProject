from PyQt6.QtWidgets import *
from PyQt6.QtCore import QStringListModel
from gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        This function sets up the Task Manager window, it sets the layout,
        the buttons, and makes a CSV file to store the data the user will
        enter, and it also connects the buttons and shows the saved tasks.
        """
        super().__init__()

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



    def add_task(self) -> None:
        """
        This function adds a new task to the CSV file if what is entered is valid
        It also checks to make sure the task, date, and time are all valid, it also checks
        if there is already a task saved with the same date and time, if everything checks out
        it adds the task to the CSV file and clears the lines.
        """

        task = self.task_line.text().strip()
        date = self.date_line.text().strip().lower()
        time = self.time_line.text().strip().lower()
        category = self.cat_dropdown.currentText().strip()

        if not task or not date or not time:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("All fields must be filled.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        if len(date) != 5 or date[2] != '/' or not (date[:2] + date[3:]).isdigit():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Invalid Date.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        month = int(date[:2])
        day = int(date[3:])

        if not (1 <= month <= 12 and 1 <= day <= 31):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Date must be a valid Month/Date.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        if len(time) != 7 or time[2] != ':' or not (time[:2] + time[3:5]).isdigit():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Invalid Time")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        hour = int(time[:2])
        minute = int(time[3:5])
        suffix = time[5:]

        if not (1 <= hour <= 12 and 0 <= minute <= 59):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Time must have valid hour and minute.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        if suffix not in ['am', 'pm']:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Time must end in 'am' or 'pm'.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        row = [task, date, time, category, "Pending"]

        with open("tasks.csv", mode="r", newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for existing_row in reader:
                existing_date = existing_row[1].strip().lower()
                existing_time = existing_row[2].strip().lower()
                if existing_date == date and existing_time == time:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setWindowTitle("Time Conflict")
                    msg.setText(f"A task already exists at {time} on {date}.")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Failed to add task.")
            msg.setInformativeText(str(e))
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()








    def load_tasks(self) -> None:
        """
        This function just reads all the tasks that were added to the CSV file
        tasks.csv and shows them in the lists view so the user can see his tasks
        """
        try:
            with open("tasks.csv", mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                tasks = [
                    f" {row[0]:<30} Due: {row[1]:<30}  {row[2]:<30}  {row[3]}" for row in reader]
            self.model.setStringList(tasks)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Could not load tasks.")
            msg.setInformativeText(str(e))
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()


    def mark_task_complete(self) -> None:
        """
        This function removes the tasks the user clicks from the CSV file,
        It updates the list view when a task is completed, If nothing is
        selected then an error message appears
        :return:
        """
        selected_index = self.listView.currentIndex()

        if not selected_index.isValid():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Selection Error")
            msg.setText("Please select a task to mark complete.")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        try:
            with open("tasks.csv", mode="r", newline='') as file:
                reader = csv.reader(file)
                data = list(reader)

            selected_row = selected_index.row() + 1

            if selected_row >= len(data):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Invalid task selection.")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return

            del data[selected_row]

            with open("tasks.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)

            self.load_tasks()

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Error")
            msg.setText("Failed to delete task.")
            msg.setInformativeText(str(e))
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

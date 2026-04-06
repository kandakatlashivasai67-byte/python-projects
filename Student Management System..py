import json
import os

class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "id":self.student_id,
            "name": self.name,
            "grade": self.grade
        }


class StudentManager:
    def __init__(self):
        self.filename = "students.json"
        self.students = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                self.students = json.load(file)
        else:
            self.students = {}

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.students, file, indent=5)

    def add_student(self, student):
        if student.student_id in self.students:
            print("Student ID already exists!")
            return

        self.students[student.student_id] = student.to_dict()
        self.save_data()
        print("Student added successfully")

    def update_student(self, student_id, name, grade):
        if student_id not in self.students:
            print("Student not found")
            return

        self.students[student_id]["name"] = name
        self.students[student_id]["grade"] = grade
        self.save_data()
        print("Student updated successfully")

    def delete_student(self, student_id):
        if student_id not in self.students:
            print("Student not found")
            return
            
        del self.students[student_id]
        self.save_data()
        print("Student deleted successfully")

    def list_students(self):
        if not self.students:
            print("No student records found")
            return

        print("\nID\tName\t\tGrade")
        print("-" * 40)
        for sid, info in self.students.items():
            print(f"{sid}\t{info['name']}\t\t{info['grade']}")


def main():
    manager = StudentManager()

    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sid = input("Enter ID: ")
            name = input("Enter Name: ")
            grade = input("Enter Grade: ")
            student = Student(sid, name, grade)
            manager.add_student(student)

        elif choice == "2":
            sid = input("Enter ID to update: ")
            name = input("Enter new Name: ")
            grade = input("Enter new Grade: ")
            manager.update_student(sid, name, grade)

        elif choice == "3":
            sid = input("Enter ID to delete: ")
            manager.delete_student(sid)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("Exiting program")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

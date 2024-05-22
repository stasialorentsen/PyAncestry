import tkinter as tk
from tkinter import messagebox
from database_operations import update_person

class EditPersonForm:
    def __init__(self, master, driver, person_id, name, surname, birthdate):
        self.master = master
        self.driver = driver
        self.person_id = person_id
        self.name = name
        self.surname = surname
        self.birthdate = birthdate

        master.title("Edit Person")

        self.label_name = tk.Label(master, text="Name:")
        self.label_name.grid(row=0, column=0, sticky="w")
        self.entry_name = tk.Entry(master)
        self.entry_name.insert(tk.END, name)
        self.entry_name.grid(row=0, column=1)

        self.label_surname = tk.Label(master, text="Surname:")
        self.label_surname.grid(row=1, column=0, sticky="w")
        self.entry_surname = tk.Entry(master)
        self.entry_surname.insert(tk.END, surname)
        self.entry_surname.grid(row=1, column=1)

        self.label_birthdate = tk.Label(master, text="Birthdate:")
        self.label_birthdate.grid(row=2, column=0, sticky="w")
        self.entry_birthdate = tk.Entry(master)
        self.entry_birthdate.insert(tk.END, birthdate if birthdate else "")
        self.entry_birthdate.grid(row=2, column=1)

        self.save_button = tk.Button(master, text="Save", command=self.update_person_details)
        self.save_button.grid(row=3, columnspan=2)

    def update_person_details(self):
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        birthdate = self.entry_birthdate.get()

        if name or surname:
            with self.driver.session() as session:
                session.write_transaction(update_person, self.person_id, name, surname, birthdate)
            messagebox.showinfo("Success", "Person details updated successfully!")
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Please fill in at least one of the name fields.")

import tkinter as tk
from tkinter import messagebox
from database_operations import search_person_by_name_or_surname, view_person_details
from AddRelationshipForm import AddRelationshipForm

class PersonSearchForm:
    def __init__(self, master, driver):
        self.master = master
        self.driver = driver
        self.results1 = []
        self.results2 = []

        master.title("Search Person")

        # Column 1: Person 1 search
        self.label_name1 = tk.Label(master, text="Person 1 Name:")
        self.label_name1.grid(row=0, column=0, sticky="w")
        self.entry_name1 = tk.Entry(master)
        self.entry_name1.grid(row=0, column=1)

        self.label_surname1 = tk.Label(master, text="Person 1 Surname:")
        self.label_surname1.grid(row=1, column=0, sticky="w")
        self.entry_surname1 = tk.Entry(master)
        self.entry_surname1.grid(row=1, column=1)

        self.search_button1 = tk.Button(master, text="Search Person 1", command=self.person1_search)
        self.search_button1.grid(row=2, column=0, columnspan=2)

        self.listbox1 = tk.Listbox(master, exportselection=False)
        self.listbox1.grid(row=3, column=0, columnspan=2)
        self.listbox1.bind('<<ListboxSelect>>', self.on_listbox1_select)

        self.view_details_text1 = tk.Text(master, height=5, width=30)
        self.view_details_text1.grid(row=4, column=0, columnspan=2)

        # Column 2: Person 2 search
        self.label_name2 = tk.Label(master, text="Person 2 Name:")
        self.label_name2.grid(row=0, column=2, sticky="w")
        self.entry_name2 = tk.Entry(master)
        self.entry_name2.grid(row=0, column=3)

        self.label_surname2 = tk.Label(master, text="Person 2 Surname:")
        self.label_surname2.grid(row=1, column=2, sticky="w")
        self.entry_surname2 = tk.Entry(master)
        self.entry_surname2.grid(row=1, column=3)

        self.search_button2 = tk.Button(master, text="Search Person 2", command=self.person2_search)
        self.search_button2.grid(row=2, column=2, columnspan=2)

        self.listbox2 = tk.Listbox(master, exportselection=False)
        self.listbox2.grid(row=3, column=2, columnspan=2)
        self.listbox2.bind('<<ListboxSelect>>', self.on_listbox2_select)

        self.view_details_text2 = tk.Text(master, height=5, width=30)
        self.view_details_text2.grid(row=4, column=2, columnspan=2)

        # Relationship details
        self.label_relationship_type = tk.Label(master, text="Relationship Type:")
        self.label_relationship_type.grid(row=5, column=0, columnspan=2)

        self.relationship_type_var = tk.StringVar(master)
        self.relationship_type_var.set("Married to")  # Default relationship type
        self.relationship_type_dropdown = tk.OptionMenu(master, self.relationship_type_var, "Married to", "A parent of", "A child of")
        self.relationship_type_dropdown.grid(row=5, column=2, columnspan=2)

        self.add_relationship_button = tk.Button(master, text="Add Relationship", command=self.add_relationship)
        self.add_relationship_button.grid(row=6, column=0, columnspan=4)

    def person1_search(self):
        name = self.entry_name1.get()
        surname = self.entry_surname1.get()
        with self.driver.session() as session:
            results = session.write_transaction(search_person_by_name_or_surname, name, surname)
            self.results1 = results
            self.display_search_results(results, self.listbox1)

    def person2_search(self):
        name = self.entry_name2.get()
        surname = self.entry_surname2.get()
        with self.driver.session() as session:
            results = session.write_transaction(search_person_by_name_or_surname, name, surname)
            self.results2 = results
            self.display_search_results(results, self.listbox2)

    def display_search_results(self, results, listbox):
        listbox.delete(0, tk.END)
        for record in results:
            name = record['name']
            surname = record['surname']
            birthdate = record['birthdate']
            display_text = f"{name} {surname} {birthdate}"
            listbox.insert(tk.END, display_text)

    def add_relationship(self):
        selected_index1 = self.listbox1.curselection()
        selected_index2 = self.listbox2.curselection()
        if selected_index1 and selected_index2:
            selected_person1 = self.results1[selected_index1[0]]
            selected_person2 = self.results2[selected_index2[0]]
            name1 = selected_person1.get('name')
            surname1 = selected_person1.get('surname')
            birthdate1 = selected_person1.get('birthdate')
            name2 = selected_person2.get('name')
            surname2 = selected_person2.get('surname')
            birthdate2 = selected_person2.get('birthdate')

            add_relationship_window = tk.Toplevel(self.master)
            add_relationship_window.title("Add Relationship")

            add_relationship_form = AddRelationshipForm(add_relationship_window, self.driver, name1, surname1, birthdate1, name2, surname2, birthdate2)
        else:
            messagebox.showwarning("No Selection", "Please select persons 1 and 2.")

    def on_listbox1_select(self, event):
        self.display_person_details(self.listbox1, self.results1, self.view_details_text1)

    def on_listbox2_select(self, event):
        self.display_person_details(self.listbox2, self.results2, self.view_details_text2)

    def display_person_details(self, listbox, results, text_widget):
        selected_index = listbox.curselection()
        if selected_index and results:  # Check if index is not empty and results list is not empty
            selected_person = results[selected_index[0]]
            name = selected_person.get('name')
            surname = selected_person.get('surname')
            birthdate = selected_person.get('birthdate')

            with self.driver.session() as session:
                person_details = session.read_transaction(view_person_details, name, surname, birthdate)

            self.view_person_details(person_details, text_widget)
        else:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, "No person selected.")

    def view_person_details(self, person_details, text_widget):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        if person_details:
            text_widget.insert(tk.END, f"Name: {person_details['name']}\nSurname: {person_details['surname']}\nBirthdate: {person_details['birthdate']}")
        else:
            text_widget.insert(tk.END, "No details found.")
        text_widget.config(state=tk.DISABLED)

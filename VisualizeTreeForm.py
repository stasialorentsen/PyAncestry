import tkinter as tk
from tkinter import messagebox
from neo4j import GraphDatabase

class VisualizeTreeForm:
    def __init__(self, master, driver):
        self.master = master
        self.driver = driver
        master.title("Visualize Tree")
        
        self.visualize_button = tk.Button(master, text="Generate Visualization", command=self.generate_visualization)
        self.visualize_button.pack(pady=10)
        
    def generate_visualization(self):
        cypher_query = "MATCH (n)-[r]->(m) RETURN n, r, m"
        
        with self.driver.session() as session:
            result = session.run(cypher_query)
            plantuml_code = self._generate_plantuml(result)
            self._write_to_file(plantuml_code)
            
            # Show a message box indicating successful visualization
            messagebox.showinfo("Visualization", "Visualization file generated successfully.")
    
    def _generate_plantuml(self, result):
        plantuml_code = "@startuml\n"
        
        spouses = set()
        parent_child_map = {}
        
        for record in result:
            start_node = record["n"]
            relationship = record["r"]
            end_node = record["m"]
    
            start_attributes = self._format_name(start_node)
            end_attributes = self._format_name(end_node)
    
            relationship_type = relationship.type
    
            if relationship_type == "Married_to":
                # Add spouses to the set
                spouses.add(start_attributes)
                spouses.add(end_attributes)
            elif relationship_type == "Child_of":
                # Check if start node is a child
                if start_attributes in spouses:
                    parent_attributes = end_attributes
                    child_attributes = start_attributes
                else:
                    parent_attributes = start_attributes
                    child_attributes = end_attributes
                
                # Add the parent-child relationship to the map
                if parent_attributes not in parent_child_map:
                    parent_child_map[parent_attributes] = []
                parent_child_map[parent_attributes].append(child_attributes)
    
        # Add spouse relationships
        for spouse1 in spouses:
            for spouse2 in spouses:
                if spouse1 < spouse2:
                    plantuml_code += f'("{spouse1}") -- ("{spouse2}")\n'
    
        # Add parent-child relationships
        for parent, children in parent_child_map.items():
            # Ensure children are sorted for consistent rendering
            children.sort()
            # Add parent-child relationships
            for child in children:
                plantuml_code += f'("{child}") --> ("{parent}")\n'
    
        plantuml_code += "@enduml\n"
        return plantuml_code

    def _format_name(self, node):
        name = node["name"]
        surname = node["surname"]
        return f'{name} {surname}'
    
    
    def _write_to_file(self, plantuml_code):
        with open("visualization.txt", "w") as file:
            # Remove quotes from names before writing to the file
            plantuml_code = plantuml_code.replace('"', '')
            file.write(plantuml_code)
            print("PlantUML code:")
            print(plantuml_code)
        print("File written successfully")





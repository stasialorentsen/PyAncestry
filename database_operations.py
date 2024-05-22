# Function to create a new person in the database
def create_person(tx, person_details):
    # Cypher query to create a new person node with provided details
    create_person_query = "CREATE (p:Person {name: $name, surname: $surname, birthdate: $birthdate})"
    print("Create Person Cypher Query:", create_person_query)
    print("Person Details:", person_details)
    # Running the query using the transaction passed as an argument, and passing person_details as parameters
    tx.run(create_person_query, **person_details)

# Function to search for persons in the database based on name and surname
def search_person_by_name_or_surname(tx, name, surname):
    # Constructing the search query based on the provided parameters
    search_query = ""
    parameters = {}
    if name:
        search_query += "toLower(p.name) CONTAINS toLower($name) AND "
        parameters["name"] = name
    if surname:
        search_query += "toLower(p.surname) CONTAINS toLower($surname) AND "
        parameters["surname"] = surname

    # Removing the trailing "AND" if it exists
    if search_query.endswith(" AND "):
        search_query = search_query[:-5]

    # Constructing the full search query
    # search_query = (
    #     "MATCH (p:Person) "
    #     f"WHERE {search_query} "
    #     "RETURN p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    # )
    search_query = (
        "MATCH (p:Person) "
        f"WHERE {search_query} "
        "RETURN ID(p) AS person_id, p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )
    print("Search Person Query:", search_query)
    print("Search Person Parameters:", parameters)
    # Running the query using the transaction passed as an argument, and passing parameters
    result = tx.run(search_query, **parameters)

    # Returning a list of dictionaries containing the search results
    return [{"name": record['name'], "surname": record['surname'], "birthdate": record['birthdate'], "person_id": record['person_id']} for record in result]

def view_person_details(tx, name, surname, birthdate, person_id):
    # Query to retrieve details of a person with exact match on name, surname, and birthdate
    view_person_query = (
        "MATCH (p:Person) "
        "WHERE p.name = $name AND p.surname = $surname AND p.birthdate = $birthdate "
        "RETURN ID(p) AS person_id, p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )

    # Print the query with populated parameters
    print("Name:", name)
    print("Surname:", surname)
    print("Birthdate:", birthdate)

    # Run the query and return the result
    result = tx.run(view_person_query, name=name, surname=surname, birthdate=birthdate)
    record = result.single()

    # Print the person's ID
    if record:
        person_id = record.get('person_id')
        print("Person ID:", person_id)

    return record


def update_person(tx, person_id, name, surname, birthdate):
    # Check if person_id is not null or empty
    if person_id:
        update_query = (
            "MATCH (p:Person {id: $person_id}) "
            "SET p.name = $name, p.surname = $surname, p.birthdate = $birthdate"
        )
        # Debugging the actual query with the parameters
        debug_query = f"MATCH (p:Person {{id: '{person_id}'}}) SET p.name = '{name}', p.surname = '{surname}', p.birthdate = '{birthdate}'"
        print(f"Update Query: {debug_query}")
        print(f"Person ID: {person_id}, Name: {name}, Surname: {surname}, Birthdate: {birthdate}")

        # Convert person_id to string if it's an integer
        if isinstance(person_id, int):
            person_id = str(person_id)

        tx.run(update_query, person_id=person_id, name=name, surname=surname, birthdate=birthdate)
    else:
        print("Error: The person_id is null or empty.")

        
def add_relationship(tx, person1_name, person1_surname, person1_birthdate, person2_name, person2_surname, person2_birthdate, relationship_type):
    # Escape special characters in person surnames
    person1_surname = person1_surname.replace("'", "\\'")
    person2_surname = person2_surname.replace("'", "\\'")
    
    # Determine relationship types based on the direction
    if relationship_type == "A child of":
        parent_relationship = "Parent_of"
        child_relationship = "Child_of"
    elif relationship_type == "A parent of":
        parent_relationship = "Child_of"
        child_relationship = "Parent_of"
    else:
        parent_relationship = "Married_to"
        child_relationship = "Married_to"
    
    add_relationship_query = (
        "MERGE (p1:Person {name: '%s', surname: '%s', birthdate: '%s'}) "
        "MERGE (p2:Person {name: '%s', surname: '%s', birthdate: '%s'}) "
        "CREATE (p1)-[:%s]->(p2), (p2)-[:%s]->(p1)" % 
        (person1_name, person1_surname, person1_birthdate, 
         person2_name, person2_surname, person2_birthdate, 
         child_relationship, parent_relationship)
    )
  
    # Execute the query
    result = tx.run(add_relationship_query)
    
    # Return any result if needed
    return result




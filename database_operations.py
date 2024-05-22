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
            "MATCH (p:Person) WHERE ID(p) = $person_id "
            "SET p.name = $name, p.surname = $surname, p.birthdate = $birthdate"
        )
        # Debugging the actual query with the parameters
        debug_query = f"MATCH (p:Person) WHERE ID(p) = {person_id} SET p.name = '{name}', p.surname = '{surname}', p.birthdate = '{birthdate}'"
        print(f"Update Query: {debug_query}")
        
        tx.run(update_query, person_id=person_id, name=name, surname=surname, birthdate=birthdate)
    else:
        print("Error: The person_id is null or empty.")

        
def add_relationship_in_db(tx, person1_id, person2_id, relationship_type):
    if relationship_type == "A child of":
        relationship_out = "Child_of"
        relationship_in = "Parent_of"
    elif relationship_type == "A parent of":
        relationship_out = "Parent_of"
        relationship_in = "Child_of"
    else:
        relationship_out = "Married_to"
        relationship_in = "Married_to"
    
    add_relationship_query = (
        "MATCH (p1:Person WHERE ID(p1) = $person1_id) "
        "MATCH (p2:Person WHERE ID(p2) = $person2_id) "
        "MERGE (p1)-[r1:%s]->(p2)-[r2:%s]->(p1)" % (relationship_out, relationship_in)
    )
    
    print(f"Add Relationship Query: {add_relationship_query}")
    
    tx.run(add_relationship_query, person1_id=person1_id, person2_id=person2_id)
    
def delete_person_by_id(tx, person_id):
    # Check if person_id is not null or empty
    if person_id:
        delete_query = (
            "MATCH (p:Person) WHERE ID(p) = $person_id DETACH DELETE p"
        )
        # Debugging the actual query with the parameters
        debug_query = f"MATCH (p:Person) WHERE ID(p) = {person_id} DETACH DELETE p"
        print(f"Delete Query: {debug_query}")
        
        tx.run(delete_query, person_id=person_id)
    else:
        print("Error: The person_id is null or empty.")


def check_relationships_by_id(tx, person_id):
    query = (
        "MATCH (p:Person)-[r]->() WHERE ID(p) = $person_id "
        "RETURN count(r)"
    )
    # Debugging the actual query with the parameters
    debug_query = f"MATCH (p:Person)-[r]->() WHERE ID(p) = {person_id} RETURN count(r)"
    print(f"Check Relationships Query: {debug_query}")
    
    result = tx.run(query, person_id=person_id)
    return result.single()[0]  # Return the count of relationships










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
    search_query = (
        "MATCH (p:Person) "
        f"WHERE {search_query} "
        "RETURN p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )
    print("Search Person Query:", search_query)
    print("Search Person Parameters:", parameters)
    # Running the query using the transaction passed as an argument, and passing parameters
    result = tx.run(search_query, **parameters)

    # Returning a list of dictionaries containing the search results
    return [{"name": record['name'], "surname": record['surname'], "birthdate": record['birthdate']} for record in result]


def view_person_details(tx, name, surname, birthdate):
    # query to retrieve details of a person with exact match on name, surname, and birthdate
    view_person_query = (
        "MATCH (p:Person) "
        "WHERE p.name = $name AND p.surname = $surname AND p.birthdate = $birthdate "
        "RETURN p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )

    # Run the query and return the result
    result = tx.run(view_person_query, name=name, surname=surname, birthdate=birthdate)
    return result.single()

# def add_relationship(tx, person1_name, person1_surname, person1_birthdate, person2_name, person2_surname, person2_birthdate):
#     # Cypher query to create a relationship between two people based on their details
#     add_relationship_query = (
#         "MERGE (p1:Person {name: '%s', surname: '%s', birthdate: '%s'}) "
#         "MERGE (p2:Person {name: '%s', surname: '%s', birthdate: '%s'}) "
#         "CREATE (p1)-[:RELATED_TO]->(p2)" % (person1_name, person1_surname, person1_birthdate, person2_name, person2_surname, person2_birthdate)
#     )

#     print("Add Relationship Query:", add_relationship_query)
#     tx.run(add_relationship_query)

def add_relationship(tx, person1_name, person1_surname, person1_birthdate, person2_name, person2_surname, person2_birthdate):
    add_relationship_query = (
        "MERGE (p1:Person {name: '%s', surname: '%s', birthdate: '%s'}) "
        "MERGE (p2:Person {name: '%s', surname: '%s', birthdate: '%s'}) "
        "CREATE (p1)-[:RELATED_TO]->(p2)" % (person1_name, person1_surname, person1_birthdate, person2_name, person2_surname, person2_birthdate)
    )
    
    # Execute the query
    result = tx.run(add_relationship_query)
    
    # Return any result if needed
    return result


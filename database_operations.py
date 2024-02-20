<<<<<<< HEAD
# Function to create a new person in the database
def create_person(tx, person_details):
    # Cypher query to create a new person node with provided details
    create_person_query = "CREATE (p:Person {name: $name, surname: $surname, birthdate: $birthdate})"
    # Running the query using the transaction passed as an argument, and passing person_details as parameters
    tx.run(create_person_query, **person_details)

# Function to search for persons in the database based on provided parameters
def search_person(tx, search_param):
    # Cypher query to search for persons by name or surname
    search_person_query = (
        "MATCH (p:Person) "
        "WHERE p.name = $name OR p.surname = $surname "
        "RETURN p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )
    # Splitting the search parameter into name and surname (if applicable)
    name, *surname = search_param.split(" ", 1)
    surname = " ".join(surname) if surname else None
    # Running the query using the transaction passed as an argument, and passing name and surname as parameters
    result = tx.run(search_person_query, name=name, surname=surname)
    # Returning a list of dictionaries containing the search results
    return [{"name": record['name'], "surname": record['surname'], "birthdate": record['birthdate']} for record in result]

# Method to view details of the selected person
def view_person(self):
    # Cypher query to search for persons by name or surname
    search_person_query = (
        "MATCH (p:Person) "
        "WHERE p.name = $name OR p.surname = $surname "
        "RETURN p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )
    # BLAAAH



=======
# Function to create a new person in the database
def create_person(tx, person_details):
    # Cypher query to create a new person node with provided details
    create_person_query = "CREATE (p:Person {name: $name, surname: $surname, birthdate: $birthdate})"
    # Running the query using the transaction passed as an argument, and passing person_details as parameters
    tx.run(create_person_query, **person_details)

# Function to search for persons in the database based on provided parameters
def search_person(tx, search_param):
    # Cypher query to search for persons by name or surname
    search_person_query = (
        "MATCH (p:Person) "
        "WHERE p.name = $name OR p.surname = $surname "
        "RETURN p.name AS name, p.surname AS surname, p.birthdate AS birthdate"
    )
    # Splitting the search parameter into name and surname (if applicable)
    name, *surname = search_param.split(" ", 1)
    surname = " ".join(surname) if surname else None
    # Running the query using the transaction passed as an argument, and passing name and surname as parameters
    result = tx.run(search_person_query, name=name, surname=surname)
    # Returning a list of dictionaries containing the search results
    return [{"name": record['name'], "surname": record['surname'], "birthdate": record['birthdate']} for record in result]
>>>>>>> 47882a43ed388914e5cd84941a7242a8d981e127

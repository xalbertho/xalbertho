import csv
import sys

from util import Node, StackFrontier, QueueFrontier
from collections import deque

# Maps names to a set of corresponding person_ids
# recordadndo que un diccionario se puede usar de la forma diccionario[clave] = valor
#                                                           names[nombre]=valor
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f) # convierte el csv en un diccionario donde key es el titulo de cada columna (id,nombre,birth)
                                   #{id:1,nombre:alber,birth:12/12/2}
                                   #{id:2,nombre:alber,birth:12/12/2}
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names: #buscamos si no esta el nombre en el diccionario names (creado al inicio)
                names[row["name"].lower()] = {row["id"]} # en caso de no estar, agregagmos el nombre, ademas de su id
            else:
                names[row["name"].lower()].add(row["id"])# si ya esta en el diccionario, añadimos el id

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    # verifica que al ejecutar el codigo solo tenga 2 valores
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    #operador ternario    
    directory = sys.argv[1] if len(sys.argv) == 2 else "large" # si no se proporciona un directorio se toma large como predeterminado

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    if source == target: # caso donde el objetivo es el mismo que la fuente
        return [] # devolvemos una lista vacia

    frontier = QueueFrontier()  # Usamos una frontera basada en una cola (BFS)
    frontier.add(Node(state=source, parent=None, action=None)) #agregamos un nodo con su estado, lo demas vacio este sera el estado inicial


    explored = set() #para guardar los nodos que ya exploramos

    while not frontier.empty(): #mientras la frontera no este vacia
        node = frontier.remove() #removemos el nodo que entro primero
        current_person = node.state #guardamos el id en current person

        if current_person == target: # si el id es el mismo que el objetivo, ya hemos hallado el objetivo y reconstruimos el camino
            path = [] #iniciamos con el camino vacio
            while node.parent is not None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path

        explored.add(current_person)

        for movie, neighbor in neighbors_for_person(current_person):
            if not frontier.contains_state(neighbor) and neighbor not in explored:
                child = Node(state=neighbor, parent=node, action=movie)
                frontier.add(child)

    return None  # Si no se encuentra conexión



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

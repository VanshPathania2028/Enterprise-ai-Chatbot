from neo4j import GraphDatabase
from utils.logger import logger
from config import(
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD
)
# URI = "neo4j+s://60cc11e4.databases.neo4j.io"
# USERNAME = "60cc11e4"
# PASSWORD = "bl156GHUSBtLw9I3N2X_atY_B5PJZcShwGikEzJlg_E"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME,
           NEO4J_PASSWORD)

)

def get_session():
    """
    Returns a new Neo4j session.
    """
    return driver.session()

def create_entity(name, entity_type="Entity"):
    """
    Creates an Entity node.
    """

    query = """
    MERGE(n:Entity {name:$name})
    SET n.type = $type
    """
    with driver.session() as session:
        session.run(
            query,
            name=name,
            type=entity_type
        )
def create_person(name):

    with driver.session() as session:

        session.run(
            """
            CREATE (:Person {name:$name})
            """,
            name=name
        )

def execute_query(query, parametrs=None):
    """
    Execute a Cypher query and return the results.
    """
    if paramters is None:
        paramters = {}

    with driver.session() as session:
        result = session.run(query, paramters)
        return [record.data() for record in result]

    logger.info(
    f"Executing Cypher:\n{query}"
)
def create_relationship(source, relationship, target):
    """
    Creates a relationship between two Entity nodes.
    """

    query = f"""
    MERGE (a:Entity {{name:$source}})
    MERGE (b:Entity {{name:$target}})
    MERGE (a)-[:{relationship}]->(b)
    """

    with driver.session() as session:

        session.run(
            
           query,
           source=source,
           target=target
        )

def clear_graph():
    """
    Deletes all nodes and relationships.
    """
    with driver.session() as session:

        session.run("""
        MATCH (n)
        DETACH DELETE n
        """)



def close_driver():
    """
    Closes the Neo4j driver."""
    driver.close()

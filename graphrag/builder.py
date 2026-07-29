import re
from graphrag.graph_db import driver


def _sanitize_rel_type(rel_type: str) -> str:
    """Sanitize a relationship type string for safe use in Cypher queries.
    
    Replaces spaces/special chars with underscores, removes any remaining
    non-alphanumeric characters (except underscores), and uppercases.
    Falls back to 'RELATED_TO' if the result is empty.
    """
    sanitized = re.sub(r"\s+", "_", rel_type)
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "", sanitized)
    sanitized = sanitized.strip("_").upper()
    return sanitized if sanitized else "RELATED_TO"


def build_graph(graph):

    with driver.session() as session:

        for entity in graph["entities"]:

            session.run(
                """
                MERGE (n:Entity {name:$name})
                
                SET n.type=$type
                """,
                name=entity["name"],
                type=entity["type"],
            )

        for relation in graph["relationships"]:

            rel_type = _sanitize_rel_type(relation["relation"])

            query = f"""
            MATCH (a:Entity {{name:$source}})
            MATCH (b:Entity {{name:$target}})
            MERGE (a)-[:{rel_type}]->(b)
            """

            session.run(
                query,
                source=relation["source"],
                target=relation["target"]
            )

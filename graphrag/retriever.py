from graphrag.graph_db import driver


def graph_search(entity_name: str):

    query = """
    MATCH (a: Entity {name:$name})-[r]-(b)
    WHERE toLower(a.name) = toLower($name)
    OPTIONAL MATCH (a)-[r]-(b)
    RETURN
        a.name AS source,
        type(r) AS relation,
        b.name AS target
    """

    with driver.session() as session:

        result = session.run(
            query,
            name=entity_name
        )

        return [record.data() for record in result]

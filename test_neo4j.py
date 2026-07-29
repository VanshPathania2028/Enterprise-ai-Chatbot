from graphrag.graph_db import driver

with driver.session() as session:
    result = session.run("RETURN 'Connected to Neo4j' AS message")
    print(result.single()["message"])

driver.close()
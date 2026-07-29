from graphrag.graph_db import driver
from graphrag.graph_db import create_person
from graphrag.graph_db import create_relationship
with driver.session() as session:

    result  = session.run("RETURN 'Connected Successfully' AS message")
    print(result.single()["message"])

create_person("Shikha")

create_relationship(
    "Shikha",
    "Artificial Intelligence"
)
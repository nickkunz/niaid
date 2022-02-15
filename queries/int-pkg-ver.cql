// verify niaid data into pkg
MATCH (p:PERSON)-[:PROXY_TO]-(n:NAME)-[:BELONGS_TO]-(s:SECTION)-[:PART_OF]->(b:BRANCH)
RETURN p, n, s, b
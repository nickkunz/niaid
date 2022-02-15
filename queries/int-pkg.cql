// integrate niaid data into pkg

// load niaid data
LOAD CSV WITH HEADERS FROM 'file:///niaid-dir-org.csv' AS i
WITH i

// create niaid nodes
MERGE (n:NAME {Name: i.Name})
MERGE (e:EDUCATION {Name: i.Education})
MERGE (b:BRANCH {Name: i.Branch})
MERGE (s:SECTION {Name: i.Section})

// create niaid relationships
MERGE (n)-[:HAS]->(e)
MERGE (n)-[:BELONGS_TO]->(s)
MERGE (s)-[:PART_OF]->(b)

// create ic and pt subset pkg-person to niaid-name proxy relationships
UNION
MATCH (ic:IC)-[:FUNDED]-(:PROJECT)-[:PRODUCED]-(pr:PAPER)
WHERE ic.name = 'NATIONAL INSTITUTE OF ALLERGY AND INFECTIOUS DISEASES'
WITH pr
MATCH (n:NAME)
MATCH (pn:PERSON)-[:AUTHORED]-(pr)-[:IS_TYPE]->(pt:PUB_TYPE)
WHERE pt.type = 'Research Support, N.I.H., Intramural'
    AND (substring(n.Name, 0, 1) + ' ' + split(n.Name, ' ')[-1]) =
        (substring(pn.name, 0, 1) + ' ' + split(pn.name, ' ')[-1])
MERGE (pn)-[:PROXY_TO]->(n)

// create ic subset pkg-person to niaid-name proxy relationships
UNION
MATCH (n:NAME)
WHERE NOT (:PERSON)-[:PROXY_TO]->(n)
WITH n
MATCH (ic:IC)-[:FUNDED]-(:PROJECT)-[:PRODUCED]->(:PAPER)<-[:AUTHORED]-(pn:PERSON)
WHERE ic.name = 'NATIONAL INSTITUTE OF ALLERGY AND INFECTIOUS DISEASES'
WITH n, pn
WHERE (substring(n.Name, 0, 1) + ' ' + split(n.Name, ' ')[-1]) =
      (substring(pn.name, 0, 1) + ' ' + split(pn.name, ' ')[-1])
MERGE (pn)-[:PROXY_TO]->(n)

// create pt subset pkg-person to niaid-name proxy relationships
UNION
MATCH (n:NAME)
WHERE NOT (:PERSON)-[:PROXY_TO]->(n)
WITH n
MATCH (pn:PERSON)-[:AUTHORED]-(:PAPER)-[:IS_TYPE]->(pt:PUB_TYPE)
WHERE pt.type = 'Research Support, N.I.H., Intramural'
WITH n, pn
WHERE (substring(n.Name, 0, 1) + ' ' + split(n.Name, ' ')[-1]) =
      (substring(pn.name, 0, 1) + ' ' + split(pn.name, ' ')[-1])
MERGE (pn)-[:PROXY_TO]->(n)

// create all pkg-person to niaid-name proxy relationships
UNION
MATCH (n:NAME)
WHERE NOT (:PERSON)-[:PROXY_TO]->(n)
WITH n
MATCH (pn:PERSON)
WHERE (substring(n.Name, 0, 1) + ' ' + split(n.Name, ' ')[-1]) =
      (substring(pn.name, 0, 1) + ' ' + split(pn.name, ' ')[-1])
MERGE (pn)-[:PROXY_TO]->(n)

// remove proxy relationships for mismatched first names
UNION
MATCH (:PERSON)-[r:PROXY_TO]->(n:NAME)
WITH n, count(r) AS c
WHERE c > 1
MATCH (pn:PERSON)-[r:PROXY_TO]->(n:NAME)
WHERE size(split(pn.name, ' ')[0]) > 1 AND size(split(n.Name, ' ')[0]) > 1
  AND split(pn.name, ' ')[0] <> split(n.Name, ' ')[0]
DELETE r

// remove proxy relationships for mismatched middle name
UNION
MATCH (:PERSON)-[r:PROXY_TO]->(n:NAME)
WITH n, count(r) AS c
WHERE c > 1
MATCH (pn:PERSON)-[r:PROXY_TO]->(n:NAME) 
WHERE size(split(pn.name, ' ')) > 2 AND size(split(n.Name, ' ')) > 2
  AND size(split(pn.name, ' ')[1]) > 1 AND size(split(n.Name, ' ')[1]) > 1
    AND split(pn.name, ' ')[1] <> split(n.Name, ' ')[1]
DELETE r

// remove proxy relationships for mismatched middle initial
UNION
MATCH (:PERSON)-[r:PROXY_TO]->(n:NAME)
WITH n, count(r) AS c
WHERE c > 1
MATCH (pn:PERSON)-[r:PROXY_TO]->(n:NAME)
WHERE size(split(pn.name, ' ')) > 2 AND size(split(n.Name, ' ')) > 2
  AND substring(split(pn.name, ' ')[1], 0, 1) <> substring(split(n.Name, ' ')[1], 0, 1)
DELETE r

// remove proxy relationships for unknown middle initial or name
UNION
MATCH (:PERSON)-[r:PROXY_TO]->(n:NAME)
WITH n, count(r) AS c
WHERE c > 1
MATCH (pn:PERSON)-[r:PROXY_TO]->(n:NAME)
WHERE size(split(n.Name, ' ')[0]) = 1 AND size(split(n.Name, ' ')) > 2 
    AND size(split(pn.name, ' ')) = 2 AND size(split(pn.name, ' ')[0]) > 2
DELETE r
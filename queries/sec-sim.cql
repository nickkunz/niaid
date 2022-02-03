// calc section node similarity

// section node similarity by paper co-authorship
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]->(p1)
WITH s1, collect(id(p1)) as p1_papers
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]->(p2) 
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, p1_papers, s2, collect(id(p2)) AS p2_papers
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(p1_papers, p2_papers) AS paper_similarity
ORDER BY paper_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-paper.csv


// section node similarity by paper keywords
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:HAS_KEYWORD]->(k1)
WITH s1, collect(id(k1)) AS k1_words
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:HAS_KEYWORD]->(k2)
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, k1_words, s2, collect(id(k2)) AS k2_words
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(k1_words, k2_words) AS keyword_similarity
ORDER BY keyword_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-keyword.csv


// section node similarity by paper mesh keywords
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:HAS_MESH_KEYWORD]->(k1)
WITH s1, collect(id(k1)) AS k1_words
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:HAS_MESH_KEYWORD]->(k2) 
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, k1_words, s2, collect(id(k2)) AS k2_words
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(k1_words, k2_words) AS mesh_similarity
ORDER BY mesh_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-mesh.csv


// section node similarity by journal titles
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:PUBLISHED_IN]->(j1)
WITH s1, collect(id(j1)) AS j1_titles
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:PUBLISHED_IN]->(j2)
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, j1_titles, s2, collect(id(j2)) AS j2_titles
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(j1_titles, j2_titles) AS journal_similarity
ORDER BY journal_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-journal.csv


// section node similarity by journal categories
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:PUBLISHED_IN]-(:JOURNAL)-[:IN_CATEGORY]->(c1)
WITH s1, collect(id(c1)) AS c1_tags
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:AUTHORED]-(:PAPER)-[:PUBLISHED_IN]-(:JOURNAL)-[:IN_CATEGORY]->(c2)
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, c1_tags, s2, collect(id(c2)) AS c2_tags
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(c1_tags, c2_tags) AS journal_cat_similarity
ORDER BY journal_cat_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-journal-cat.csv


// name node similarity by project spending categories
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:HAS_PI]-(:PROJECT)-[:IN_SPENDING_CAT]->(c1)
WITH s1, collect(id(c1)) AS c1_tags
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:HAS_PI]-(:PROJECT)-[:IN_SPENDING_CAT]->(c2)
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, c1_tags, s2, collect(id(c2)) AS c2_tags
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(c1_tags, c2_tags) AS project_cat_similarity
ORDER BY project_cat_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-project-cat.csv


// section node similarity by project terms
MATCH (s1:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:HAS_PI]-(:PROJECT)-[:HAS_TERM]->(t1)
WITH s1, collect(id(t1)) AS t1_terms
MATCH (s2:SECTION)<-[:BELONGS_TO]-(:NAME)-[:PROXY_TO]-(:PERSON)-[:HAS_PI]-(:PROJECT)-[:HAS_TERM]->(t2)
WHERE s1 <> s2 AND s1.Name > s2.Name
WITH s1, t1_terms, s2, collect(id(t2)) AS t2_terms
RETURN s1.Name AS section_a, s2.Name AS section_b,
    gds.alpha.similarity.jaccard(t1_terms, t2_terms) AS project_term_similarity
ORDER BY project_term_similarity DESCENDING, section_a, section_b
// note: manual export to: ../data/neo4j-sim-exp/exp-project-term.csv
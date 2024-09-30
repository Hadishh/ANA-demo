LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/Persons_Parentship.csv" AS row
MATCH (p1:Person {personId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:PARENT_OF]->(p2)
Create (p2)-[:CHILD_OF]->(p1);

LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/Persons_Friend.csv" AS row
MATCH (p1:Person {personId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:FIREND_OF]->(p2)
Create (p2)-[:FIREND_OF]->(p1);

LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/Persons_GrandParent.csv" AS row
MATCH (p1:Person {personId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:GRANDPARENT_OF]->(p2)
Create (p2)-[:GRANDCHILD_OF]->(p1);

LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/Persons_Neighbor.csv" AS row
MATCH (p1:Person {personId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:NEIGHBOR_OF]->(p2)
Create (p2)-[:NEIGHBOR_OF]->(p1);

LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/Persons_sibling.csv" AS row
MATCH (p1:Person {personId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:SIBLING_OF]->(p2)
Create (p2)-[:SIBLING_OF]->(p1);

LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/Persons_Spouse.csv" AS row
MATCH (p1:Person {personId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:SPOUSE_OF]->(p2)
Create (p2)-[:SPOUSE_OF]->(p1);

LOAD CSV WITH HEADERS FROM "file:///Arthur_Morgan/isPet.csv" AS row
MATCH (p1:Pet {petId:toInteger(row.id_from)})
Match (p2:Person {personId:toInteger(row.id_to)})
Create (p1)-[:PET_OF]->(p2)
Create (p2)-[:HAS_PET]->(p1);


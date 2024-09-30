LOAD CSV WITH HEADERS FROM 'file:///Arthur_Morgan/Persons.csv' AS row
MERGE (p:Person {personId: toInteger(row.ID), first_name:row.first_name, last_name:row.last_name, birth_date:row.birth_date, birth_place:row.birth_place, gender:row.gender})
SET p.phone_number = CASE trim(row.phone_number) WHEN "" THEN null ELSE row.phone_number END;

LOAD CSV WITH HEADERS FROM 'file:///Arthur_Morgan/Pets.csv' AS row
MERGE (p:Pet {petId: toInteger(row.ID), name:row.name, species:row.species, age:toInteger(row.age), gender:row.gender})
SET p.color = CASE trim(row.color) WHEN "" THEN null ELSE row.color END;
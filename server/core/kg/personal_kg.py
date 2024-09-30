from neo4j import GraphDatabase

from config.settings.base import NEO4J_PASS, NEO4J_URL, NEO4J_USER
import datetime


class KnowledgeGraph:

    def __parse_entity(entity: dict):
        if "personId" in entity:
            month, day, year = map(int, entity["birth_date"].split("/"))
            age = datetime.date.today().year - year
            gender = "Male" if entity["gender"] == "M" else "Female"
            details = f"Full Name: {entity['first_name']} {entity['last_name']}\nAge: {age}\nPhone Number: {entity['phone_number']}"
        elif "petId" in entity:

            details = f"Name: {entity['name']}\nAge: {entity['age']}\nSpecies: {entity['species']}\nColor: {entity['color']}"
        return details

    def __init__(self, first_name, last_name) -> None:
        self.auth = (NEO4J_USER, NEO4J_PASS)
        self.url = NEO4J_URL
        self.driver = GraphDatabase.driver(self.url, auth=self.auth)
        self.relativity = {
            "child": (["son", "daughter"], "CHILD_OF"),
            "grandchild": (["grandson", "granddaughter"], "GRANDCHILD_OF"),
            "spouse": (["wife", "husband", "wifey"], "SPOUSE_OF"),
            "pet": (["dog", "cat"], "PET_OF"),
            "friend": (["friends"], "FRIEND_OF"),
            "neighbor": ([], "NEIGHBOR_OF"),
        }
        self.main_user = self.get_persons_by_full_name(first_name, last_name)[0].data()[
            "p"
        ]

        self.entities = []
        self.relations = []

    def get_all_related_to_person(self, relation_type, parentId):
        records, _, _ = self.driver.execute_query(
            f"MATCH (tgt)-[r:{relation_type}]->(p:Person {{personId: {parentId}}}) return p, tgt"
        )
        return records

    def get_persons_by_full_name(self, first_name, last_name):
        records, _, _ = self.driver.execute_query(
            "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) RETURN p LIMIT 1",
            first_name=first_name,
            last_name=last_name,
        )
        return records

    def get_persons_by_first_name(self, name):
        records, _, _ = self.driver.execute_query(
            "MATCH (p:Person {first_name: $name}) RETURN p", name=name
        )
        return records

    def get_person_by_id(self, id):
        records, _, _ = self.driver.execute_query(
            "MATCH (p:Person {personId: $id}) RETURN p", id=id
        )
        return records

    def __process_entity(self, entity, parent=None):
        if "@" in entity:
            entity = entity.replace("@", "")
            relation = None
            for key in self.relativity:
                if entity in key:
                    relation = entity, key
                    break
                for rel in self.relativity[key][0]:
                    if entity in rel:
                        relation = entity, key
            # TODO get all the relations depending on the pronoun
            if relation:
                res = self.get_all_related_to_person(
                    self.relativity[relation[1]][1], parent["personId"]
                )
                for rel in res:
                    self.entities.append(self.__parse_entity(rel["p"]))
                    self.entities.append(self.__parse_entity(rel["tgt"]))
                    name2 = f"{rel['p']['first_name']} {rel['p']['last_name']}"
                    if "pet" in relation[1].lower():
                        name1 = rel["tgt"]["name"]
                        self.relations.append(f"{name1} is {relation[1]} of {name2}")
                    else:
                        name1 = f"{rel['tgt']['first_name']} {rel['tgt']['last_name']}"
                        self.relations.append(f"{name1} is {relation[1]} of {name2}")

        else:
            #   MATCH path = shortestPath((startNode:Person {personId:1})-[*..2]-(endNode:Person {personId:2}))
            #   RETURN path
            # TODO get all the entities connected to the user
            pass

    def process_entities(self, entities: str):
        entities = entities.split(",")
        print(entities)
        if "None" in entities:
            return []

        for entity in entities:
            sub_entities = [en.replace("'s", "") for en in entity.split()]
            parent = self.main_user
            for sub_entity in sub_entities:
                records = self.__process_entity(sub_entity, parent)

    def process_function_call(self, args):
        return None

    def __del__(self):
        self.driver.close()

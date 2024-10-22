from neo4j import GraphDatabase

from config.settings.base import NEO4J_PASS, NEO4J_URL, NEO4J_USER
import datetime


class KnowledgeGraph:

    def __parse_entity(self, entity: dict):
        if "personId" in entity:
            if entity["first_name"] == "Arthur" and entity["last_name"] == "Morgan":
                details = "USER"
            # month, day, year = map(int, entity["birth_date"].split("/"))
            # age = datetime.date.today().year - year
            # gender = "Male" if entity["gender"] == "M" else "Female"
            # details = f"Full Name: {entity['first_name']} {entity['last_name']}\nAge: {age}\nPhone Number: {entity['phone_number']}"
            else:
                details = entity["first_name"]
        elif "petId" in entity:

            # details = f"Name: {entity['name']}\nAge: {entity['age']}\nSpecies: {entity['species']}\nColor: {entity['color']}"
            details = entity["name"]

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

    def get_persons_by_full_name(self, first_name, last_name):
        records, _, _ = self.driver.execute_query(
            "MATCH (p:Person {first_name: $first_name, last_name: $last_name}) RETURN p LIMIT 1",
            first_name=first_name,
            last_name=last_name,
        )
        return records

    def get_kg_data(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (n)-[r]->(m)
                RETURN DISTINCT n, r, m
            """
            )
            data = [
                (record.data()["n"], record.data()["r"], record.data()["m"])
                for record in result
            ]

        triples = []
        for _, r, _ in data:
            e1, r, e2 = r
            triples.append(
                f"{self.__parse_entity(e1)} {r.lower()} {self.__parse_entity(e2)}"
            )
        return triples

    def __del__(self):
        self.driver.close()

docker run --rm -d \
    --name neo4j --publish=7474:7474 --publish=7687:7687 \
    -v ./core/kg/import:/var/lib/neo4j/import \
    -v ./core/kg/scripts:/scripts \
    --env NEO4J_AUTH=neo4j/neo4j1234 neo4j:latest

echo "Waiting for Neo4j to start..."
sleep 15

#run the cypher hsll tool
docker exec -it neo4j cypher-shell -u neo4j -p neo4j1234 --file /scripts/create_persons.cypher
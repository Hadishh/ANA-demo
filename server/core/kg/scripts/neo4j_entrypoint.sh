#!/bin/bash

# Start Neo4j in the background
/startup/docker-entrypoint.sh neo4j &

# Function to check if Neo4j is ready
check_neo4j_ready() {
  cypher-shell -u neo4j -p neo4j1234 "RETURN 1" > /dev/null 2>&1
}

sleep 15

# Wait until Neo4j is ready to accept connections
until check_neo4j_ready; do
  echo "Waiting for Neo4j to be ready..."
  sleep 5
done

echo "Neo4j is ready. Running Cypher file..."

# Execute the Cypher file using cypher-shell
cypher-shell -u neo4j -p neo4j1234 -f /scripts/create_entities.cypher
cypher-shell -u neo4j -p neo4j1234 -f /scripts/relations.cypher

# Keep the container running after execution
wait
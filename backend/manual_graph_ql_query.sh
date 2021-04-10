curl -X POST \
-H "Content-Type: application/json" \
-d '{"query": "query { blocks{ hash } }"}' \
http://localhost:5000/graphql
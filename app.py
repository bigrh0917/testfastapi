from flask import Flask, request, jsonify
from neo4j import GraphDatabase, basic_auth
import os

app = Flask(__name__)

# 从环境变量读取配置
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)
)

@app.route("/query_neo4j", methods=["POST"])
def query_neo4j():
    data = request.get_json()
    cypher_query = data.get("cypher")
    if not cypher_query:
        return jsonify({"error": "Missing 'cypher' field"}), 400

    try:
        with driver.session() as session:
            result = session.run(cypher_query)
            records = [record.data() for record in result]
            return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()

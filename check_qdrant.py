import os
from qdrant_client import QdrantClient

url = "https://338b7f9c-4823-4c59-9963-c1f326d43658.us-east4-0.gcp.cloud.qdrant.io"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YTZjYWQ3YzktMDA4Yy00YzQzLWI2M2EtOWI4NzA1NTU5MGJiIn0.2xaC14qbLsjfgN8bqO1xjklAPf5eKDomNHaml9Pcf5A"

client = QdrantClient(url=url, api_key=api_key)

try:
    collections = client.get_collections()
    print(f"Collections: {collections}")
    for col in collections.collections:
        count = client.count(col.name)
        print(f"Collection {col.name} has {count} points.")
except Exception as e:
    print(f"Error: {e}")

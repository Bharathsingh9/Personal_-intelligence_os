from neo4j import AsyncGraphDatabase
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

class Neo4jClient:
    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
    async def close(self):
        await self.driver.close()
        
    async def run_query(self, query: str, parameters=None):
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            return await result.data()
            
neo4j_client = Neo4jClient()

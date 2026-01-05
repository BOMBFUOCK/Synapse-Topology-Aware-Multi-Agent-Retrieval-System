"""
Synapse 数据库测试脚本
测试多种开源向量数据库和图数据库的性能和兼容性
"""

import time
import statistics
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer


class DatabaseTestResult:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.insert_times = []
        self.query_times = []
        self.errors = []

    def add_insert_time(self, duration: float):
        self.insert_times.append(duration)

    def add_query_time(self, duration: float):
        self.query_times.append(duration)

    def add_error(self, error: str):
        self.errors.append(error)

    def get_stats(self) -> Dict[str, Any]:
        return {
            'db_name': self.db_name,
            'avg_insert_time': statistics.mean(self.insert_times) if self.insert_times else 0,
            'avg_query_time': statistics.mean(self.query_times) if self.query_times else 0,
            'min_insert_time': min(self.insert_times) if self.insert_times else 0,
            'max_insert_time': max(self.insert_times) if self.insert_times else 0,
            'min_query_time': min(self.query_times) if self.query_times else 0,
            'max_query_time': max(self.query_times) if self.query_times else 0,
            'total_inserts': len(self.insert_times),
            'total_queries': len(self.query_times),
            'error_count': len(self.errors),
            'errors': self.errors
        }


class VectorDatabaseTester:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.test_data = self._generate_test_data()

    def _generate_test_data(self) -> List[str]:
        return [
            "人工智能技术正在快速发展",
            "机器学习是AI的重要分支",
            "深度学习使用神经网络",
            "自然语言处理处理文本数据",
            "计算机视觉处理图像数据",
            "强化学习通过奖励学习",
            "监督学习使用标注数据",
            "无监督学习发现数据模式",
            "生成式AI创造新内容",
            "大语言模型理解和生成文本",
            "投资组合应该分散化",
            "股票市场波动性很大",
            "债券风险相对较低",
            "基金是集合投资工具",
            "通货膨胀影响购买力",
            "复利效应让财富增长",
            "风险管理很重要",
            "资产配置要合理",
            "长期投资收益更好",
            "市场时机很难把握"
        ]

    def _encode_text(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

    def test_qdrant(self) -> DatabaseTestResult:
        from qdrant_client import QdrantClient
        from qdrant_client.models import Distance, VectorParams, PointStruct
        import uuid

        result = DatabaseTestResult("Qdrant")
        
        try:
            client = QdrantClient(host="localhost", port=6333)
            collection_name = "test_synapse"
            
            try:
                client.delete_collection(collection_name)
            except:
                pass
            
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

            print(f"\n{'='*60}")
            print(f"测试 Qdrant")
            print(f"{'='*60}")

            print("插入测试数据...")
            for i, text in enumerate(self.test_data):
                start_time = time.time()
                vector = self._encode_text(text)
                client.upsert(
                    collection_name=collection_name,
                    points=[PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={"content": text, "owner_id": f"agent_{i % 3}"}
                    )]
                )
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {i+1}/{len(self.test_data)}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            query_texts = ["人工智能", "投资", "机器学习"]
            for query_text in query_texts:
                start_time = time.time()
                query_vector = self._encode_text(query_text)
                search_result = client.query_points(
                    collection_name=collection_name,
                    query=query_vector,
                    limit=5
                )
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 '{query_text}': {duration*1000:.2f}ms, 找到 {len(search_result.points)} 条结果")

            client.delete_collection(collection_name)
            print("✓ Qdrant 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ Qdrant 测试失败: {e}")

        return result

    def test_weaviate(self) -> DatabaseTestResult:
        import weaviate
        import weaviate.classes as wvc

        result = DatabaseTestResult("Weaviate")
        
        try:
            client = weaviate.connect_to_local(port=8080)
            
            if client.collections.exists("TestMemory"):
                client.collections.delete("TestMemory")
            
            client.collections.create(
                name="TestMemory",
                properties=[
                    wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="owner_id", data_type=wvc.config.DataType.TEXT)
                ]
            )

            print(f"\n{'='*60}")
            print(f"测试 Weaviate")
            print(f"{'='*60}")

            print("插入测试数据...")
            collection = client.collections.get("TestMemory")
            for i, text in enumerate(self.test_data):
                start_time = time.time()
                vector = self._encode_text(text)
                collection.data.insert(
                    properties={"content": text, "owner_id": f"agent_{i % 3}"},
                    vector=vector
                )
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {i+1}/{len(self.test_data)}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            query_texts = ["人工智能", "投资", "机器学习"]
            for query_text in query_texts:
                start_time = time.time()
                query_vector = self._encode_text(query_text)
                search_result = collection.query.near_vector(
                    near_vector=query_vector,
                    limit=5
                )
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 '{query_text}': {duration*1000:.2f}ms, 找到 {len(search_result.objects)} 条结果")

            client.collections.delete("TestMemory")
            print("✓ Weaviate 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ Weaviate 测试失败: {e}")

        return result

    def test_chroma(self) -> DatabaseTestResult:
        import chromadb

        result = DatabaseTestResult("ChromaDB")
        
        try:
            client = chromadb.HttpClient(host="localhost", port=8000)
            
            try:
                client.delete_collection("test_synapse")
            except:
                pass
            
            collection = client.create_collection(
                name="test_synapse",
                metadata={"hnsw:space": "cosine"}
            )

            print(f"\n{'='*60}")
            print(f"测试 ChromaDB")
            print(f"{'='*60}")

            print("插入测试数据...")
            for i, text in enumerate(self.test_data):
                start_time = time.time()
                vector = self._encode_text(text)
                collection.add(
                    ids=[f"doc_{i}"],
                    embeddings=[vector],
                    metadatas=[{"content": text, "owner_id": f"agent_{i % 3}"}]
                )
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {i+1}/{len(self.test_data)}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            query_texts = ["人工智能", "投资", "机器学习"]
            for query_text in query_texts:
                start_time = time.time()
                query_vector = self._encode_text(query_text)
                search_result = collection.query(
                    query_embeddings=[query_vector],
                    n_results=5
                )
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 '{query_text}': {duration*1000:.2f}ms, 找到 {len(search_result['ids'][0])} 条结果")

            client.delete_collection("test_synapse")
            print("✓ ChromaDB 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ ChromaDB 测试失败: {e}")

        return result

    def test_pgvector(self) -> DatabaseTestResult:
        import psycopg2
        from psycopg2 import sql

        result = DatabaseTestResult("pgvector")
        
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="synapse",
                user="synapse",
                password="synapse"
            )
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute("DROP TABLE IF EXISTS test_memories")
            cur.execute("""
                CREATE TABLE test_memories (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    owner_id TEXT,
                    embedding vector(384)
                )
            """)
            cur.execute("CREATE INDEX ON test_memories USING ivfflat (embedding vector_cosine_ops)")

            print(f"\n{'='*60}")
            print(f"测试 pgvector")
            print(f"{'='*60}")

            print("插入测试数据...")
            for i, text in enumerate(self.test_data):
                start_time = time.time()
                vector = self._encode_text(text)
                cur.execute(
                    "INSERT INTO test_memories (content, owner_id, embedding) VALUES (%s, %s, %s)",
                    (text, f"agent_{i % 3}", vector)
                )
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {i+1}/{len(self.test_data)}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            query_texts = ["人工智能", "投资", "机器学习"]
            for query_text in query_texts:
                start_time = time.time()
                query_vector = self._encode_text(query_text)
                cur.execute("""
                    SELECT content, owner_id, 1 - (embedding <=> %s::vector) as similarity
                    FROM test_memories
                    ORDER BY embedding <=> %s::vector
                    LIMIT 5
                """, (query_vector, query_vector))
                search_result = cur.fetchall()
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 '{query_text}': {duration*1000:.2f}ms, 找到 {len(search_result)} 条结果")

            cur.execute("DROP TABLE test_memories")
            cur.close()
            conn.close()
            print("✓ pgvector 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ pgvector 测试失败: {e}")

        return result

    def test_milvus(self) -> DatabaseTestResult:
        from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

        result = DatabaseTestResult("Milvus")
        
        try:
            connections.connect(host="localhost", port="19530")
            
            collection_name = "test_synapse"
            if utility.has_collection(collection_name):
                utility.drop_collection(collection_name)
            
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="owner_id", dtype=DataType.VARCHAR, max_length=255),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
            ]
            schema = CollectionSchema(fields, "Test collection for Synapse")
            collection = Collection(collection_name, schema)
            
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            collection.create_index("embedding", index_params)

            print(f"\n{'='*60}")
            print(f"测试 Milvus")
            print(f"{'='*60}")

            print("插入测试数据...")
            for i, text in enumerate(self.test_data):
                start_time = time.time()
                vector = self._encode_text(text)
                collection.insert([
                    [text],
                    [f"agent_{i % 3}"],
                    [vector]
                ])
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {i+1}/{len(self.test_data)}: {duration*1000:.2f}ms")

            collection.flush()
            collection.load()

            print("\n查询测试...")
            query_texts = ["人工智能", "投资", "机器学习"]
            for query_text in query_texts:
                start_time = time.time()
                query_vector = self._encode_text(query_text)
                search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
                results = collection.search(
                    data=[query_vector],
                    anns_field="embedding",
                    param=search_params,
                    limit=5,
                    expr=None
                )
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 '{query_text}': {duration*1000:.2f}ms, 找到 {len(results[0])} 条结果")

            utility.drop_collection(collection_name)
            connections.disconnect("default")
            print("✓ Milvus 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ Milvus 测试失败: {e}")

        return result


class GraphDatabaseTester:
    def __init__(self):
        self.test_data = [
            ("agent_1", "agent_2", 0.9),
            ("agent_1", "agent_3", 0.5),
            ("agent_2", "agent_3", 0.7),
            ("agent_2", "agent_4", 0.8),
            ("agent_3", "agent_4", 0.6)
        ]

    def test_redis(self) -> DatabaseTestResult:
        import redis

        result = DatabaseTestResult("Redis")
        
        try:
            client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
            
            pattern = "test_topology:*"
            for key in client.scan_iter(match=pattern):
                client.delete(key)

            print(f"\n{'='*60}")
            print(f"测试 Redis (拓扑数据库)")
            print(f"{'='*60}")

            print("插入测试数据...")
            for source, target, weight in self.test_data:
                start_time = time.time()
                key = f"test_topology:{source}"
                client.hset(key, target, str(weight))
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {source} -> {target}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            for source, _, _ in self.test_data:
                start_time = time.time()
                key = f"test_topology:{source}"
                neighbors = client.hgetall(key)
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 {source} 的邻居: {duration*1000:.2f}ms, 找到 {len(neighbors)} 个邻居")

            for key in client.scan_iter(match=pattern):
                client.delete(key)
            print("✓ Redis 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ Redis 测试失败: {e}")

        return result

    def test_neo4j(self) -> DatabaseTestResult:
        from neo4j import GraphDatabase

        result = DatabaseTestResult("Neo4j")
        
        try:
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "synapse123"))
            
            with driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")

            print(f"\n{'='*60}")
            print(f"测试 Neo4j (图数据库)")
            print(f"{'='*60}")

            print("插入测试数据...")
            with driver.session() as session:
                for source, target, weight in self.test_data:
                    start_time = time.time()
                    session.run("""
                        MERGE (a:Agent {id: $source})
                        MERGE (b:Agent {id: $target})
                        MERGE (a)-[r:CONNECTED]->(b)
                        SET r.weight = $weight
                    """, source=source, target=target, weight=weight)
                    duration = time.time() - start_time
                    result.add_insert_time(duration)
                    print(f"  插入 {source} -> {target}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            with driver.session() as session:
                for source, _, _ in self.test_data:
                    start_time = time.time()
                    result_nodes = session.run("""
                        MATCH (a:Agent {id: $source})-[r:CONNECTED]->(b:Agent)
                        RETURN b.id as target, r.weight as weight
                    """, source=source)
                    neighbors = list(result_nodes)
                    duration = time.time() - start_time
                    result.add_query_time(duration)
                    print(f"  查询 {source} 的邻居: {duration*1000:.2f}ms, 找到 {len(neighbors)} 个邻居")

            with driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
            
            driver.close()
            print("✓ Neo4j 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ Neo4j 测试失败: {e}")

        return result

    def test_arangodb(self) -> DatabaseTestResult:
        from arango import ArangoClient

        result = DatabaseTestResult("ArangoDB")
        
        try:
            client = ArangoClient(hosts="http://localhost:8529")
            db = client.db("_system", username="root", password="synapse123")
            
            if db.has_collection("test_agents"):
                db.delete_collection("test_agents")
            if db.has_collection("test_connections"):
                db.delete_collection("test_connections")
            
            agents = db.create_collection("test_agents")
            connections = db.create_collection("test_connections", edge=True)

            print(f"\n{'='*60}")
            print(f"测试 ArangoDB (多模型数据库)")
            print(f"{'='*60}")

            print("插入测试数据...")
            for source, target, weight in self.test_data:
                start_time = time.time()
                
                if not agents.has(source):
                    agents.insert({"_key": source, "id": source})
                if not agents.has(target):
                    agents.insert({"_key": target, "id": target})
                
                connections.insert({
                    "_from": f"test_agents/{source}",
                    "_to": f"test_agents/{target}",
                    "weight": weight
                })
                duration = time.time() - start_time
                result.add_insert_time(duration)
                print(f"  插入 {source} -> {target}: {duration*1000:.2f}ms")

            print("\n查询测试...")
            for source, _, _ in self.test_data:
                start_time = time.time()
                cursor = db.aql.execute("""
                    FOR v, e, p IN 1..1 OUTBOUND 'test_agents/@source' test_connections
                    RETURN {target: v.id, weight: e.weight}
                "", bind_vars={"source": source})
                neighbors = list(cursor)
                duration = time.time() - start_time
                result.add_query_time(duration)
                print(f"  查询 {source} 的邻居: {duration*1000:.2f}ms, 找到 {len(neighbors)} 个邻居")

            db.delete_collection("test_agents")
            db.delete_collection("test_connections")
            print("✓ ArangoDB 测试完成")

        except Exception as e:
            result.add_error(str(e))
            print(f"✗ ArangoDB 测试失败: {e}")

        return result


def print_comparison(results: List[DatabaseTestResult]):
    print(f"\n{'='*80}")
    print(f"数据库性能对比报告")
    print(f"{'='*80}\n")
    
    print(f"{'数据库':<15} {'平均插入(ms)':<15} {'平均查询(ms)':<15} {'错误数':<10}")
    print(f"{'-'*60}")
    
    for result in results:
        stats = result.get_stats()
        print(f"{stats['db_name']:<15} {stats['avg_insert_time']*1000:<15.2f} {stats['avg_query_time']*1000:<15.2f} {stats['error_count']:<10}")
    
    print(f"\n详细统计:")
    print(f"{'='*80}\n")
    
    for result in results:
        stats = result.get_stats()
        print(f"\n{stats['db_name']}:")
        print(f"  插入: 平均 {stats['avg_insert_time']*1000:.2f}ms, 最小 {stats['min_insert_time']*1000:.2f}ms, 最大 {stats['max_insert_time']*1000:.2f}ms")
        print(f"  查询: 平均 {stats['avg_query_time']*1000:.2f}ms, 最小 {stats['min_query_time']*1000:.2f}ms, 最大 {stats['max_query_time']*1000:.2f}ms")
        print(f"  总插入: {stats['total_inserts']}, 总查询: {stats['total_queries']}")
        if stats['errors']:
            print(f"  错误: {', '.join(stats['errors'])}")


def main():
    print("="*80)
    print("Synapse 数据库性能测试")
    print("="*80)
    
    vector_tester = VectorDatabaseTester()
    graph_tester = GraphDatabaseTester()
    
    all_results = []
    
    print("\n" + "="*80)
    print("向量数据库测试")
    print("="*80)
    
    all_results.append(vector_tester.test_qdrant())
    all_results.append(vector_tester.test_weaviate())
    all_results.append(vector_tester.test_chroma())
    all_results.append(vector_tester.test_pgvector())
    all_results.append(vector_tester.test_milvus())
    
    print("\n" + "="*80)
    print("图数据库测试")
    print("="*80)
    
    all_results.append(graph_tester.test_redis())
    all_results.append(graph_tester.test_neo4j())
    all_results.append(graph_tester.test_arangodb())
    
    print_comparison(all_results)


if __name__ == "__main__":
    main()

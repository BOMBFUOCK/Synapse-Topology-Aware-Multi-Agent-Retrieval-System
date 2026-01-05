#!/bin/bash

# Synapse 数据库测试启动脚本
# 启动所有测试数据库并运行性能测试

echo "============================================================"
echo "Synapse 数据库测试环境启动"
echo "============================================================"

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker 未运行，请先启动 Docker"
    exit 1
fi

echo ""
echo "步骤 1: 启动所有数据库容器..."
echo "============================================================"

# 使用 docker-compose 启动所有数据库
docker-compose -f docker-compose-all-dbs.yml up -d

echo ""
echo "等待数据库启动..."
sleep 10

# 检查容器状态
echo ""
echo "步骤 2: 检查数据库状态..."
echo "============================================================"

databases=(
    "synapse_redis:6379"
    "synapse_qdrant:6333"
    "synapse_milvus:19530"
    "synapse_weaviate:8080"
    "synapse_chroma:8000"
    "synapse_pgvector:5432"
    "synapse_neo4j:7687"
    "synapse_arangodb:8529"
)

for db in "${databases[@]}"; do
    name=$(echo $db | cut -d':' -f1)
    port=$(echo $db | cut -d':' -f2)
    
    if docker ps | grep -q $name; then
        echo "✓ $name (端口 $port) - 运行中"
    else
        echo "✗ $name (端口 $port) - 未运行"
    fi
done

echo ""
echo "步骤 3: 等待数据库完全就绪..."
echo "============================================================"

# 等待 Redis
echo "等待 Redis..."
until docker exec synapse_redis redis-cli ping > /dev/null 2>&1; do
    echo "  Redis 尚未就绪，等待中..."
    sleep 2
done
echo "✓ Redis 已就绪"

# 等待 Qdrant
echo "等待 Qdrant..."
until curl -sf http://localhost:6333/health > /dev/null 2>&1; do
    echo "  Qdrant 尚未就绪，等待中..."
    sleep 2
done
echo "✓ Qdrant 已就绪"

# 等待 Weaviate
echo "等待 Weaviate..."
until curl -sf http://localhost:8080/v1/.well-known/ready > /dev/null 2>&1; do
    echo "  Weaviate 尚未就绪，等待中..."
    sleep 2
done
echo "✓ Weaviate 已就绪"

# 等待 ChromaDB
echo "等待 ChromaDB..."
until curl -sf http://localhost:8000/api/v1/heartbeat > /dev/null 2>&1; do
    echo "  ChromaDB 尚未就绪，等待中..."
    sleep 2
done
echo "✓ ChromaDB 已就绪"

# 等待 pgvector
echo "等待 pgvector..."
until docker exec synapse_pgvector pg_isready -U synapse > /dev/null 2>&1; do
    echo "  pgvector 尚未就绪，等待中..."
    sleep 2
done
echo "✓ pgvector 已就绪"

# 等待 Neo4j
echo "等待 Neo4j..."
until curl -sf http://localhost:7474 > /dev/null 2>&1; do
    echo "  Neo4j 尚未就绪，等待中..."
    sleep 2
done
echo "✓ Neo4j 已就绪"

# 等待 ArangoDB
echo "等待 ArangoDB..."
until curl -sf http://localhost:8529/_api/heartbeat > /dev/null 2>&1; do
    echo "  ArangoDB 尚未就绪，等待中..."
    sleep 2
done
echo "✓ ArangoDB 已就绪"

# 等待 Milvus (需要更长时间)
echo "等待 Milvus (这可能需要几分钟)..."
until curl -sf http://localhost:9091/healthz > /dev/null 2>&1; do
    echo "  Milvus 尚未就绪，等待中..."
    sleep 5
done
echo "✓ Milvus 已就绪"

echo ""
echo "============================================================"
echo "所有数据库已就绪！"
echo "============================================================"
echo ""
echo "现在可以运行数据库测试:"
echo "  python test_databases.py"
echo ""
echo "查看数据库日志:"
echo "  docker-compose -f docker-compose-all-dbs.yml logs -f"
echo ""
echo "停止所有数据库:"
echo "  docker-compose -f docker-compose-all-dbs.yml down"
echo ""

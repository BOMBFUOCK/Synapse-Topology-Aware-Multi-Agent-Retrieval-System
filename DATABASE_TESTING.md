# Synapse 数据库测试方案

## 当前使用的数据库
- **向量数据库**: Qdrant
- **拓扑数据库**: Redis

## 推荐的开源替代方案

### 向量数据库替代方案

1. **Milvus** ⭐
   - 开源，性能优秀
   - 支持多种索引类型
   - 云原生架构
   - Docker: `milvusdb/milvus`

2. **Weaviate** ⭐
   - 开源向量搜索引擎
   - 内置向量化功能
   - GraphQL API
   - Docker: `semitechnologies/weaviate`

3. **ChromaDB** ⭐
   - 轻量级，易于使用
   - Python原生支持
   - 适合开发测试
   - Docker: `chromadb/chroma`

4. **pgvector** ⭐
   - PostgreSQL扩展
   - 关系型+向量数据库
   - 稳定可靠
   - Docker: `pgvector/pgvector`

### 拓扑数据库替代方案

1. **Neo4j** ⭐
   - 最流行的图数据库
   - Cypher查询语言
   - 社区版免费
   - Docker: `neo4j:5-community`

2. **ArangoDB** ⭐
   - 多模型数据库（图+文档+键值）
   - AQL查询语言
   - 完全开源
   - Docker: `arangodb/arangodb`

3. **JanusGraph** ⭐
   - 分布式图数据库
   - 支持多种后端存储
   - 适合大规模数据
   - Docker: `janusgraph/janusgraph`

## 测试计划

### 阶段1: 向量数据库测试
- [ ] Milvus
- [ ] Weaviate
- [ ] ChromaDB
- [ ] pgvector

### 阶段2: 图数据库测试
- [ ] Neo4j
- [ ] ArangoDB

### 阶段3: 性能对比
- [ ] 插入性能
- [ ] 查询性能
- [ ] 内存使用
- [ ] 易用性评估

## 测试指标

1. **性能指标**
   - 数据插入速度（条/秒）
   - 向量查询延迟（毫秒）
   - 并发查询能力

2. **功能指标**
   - 向量相似度搜索
   - 元数据过滤
   - 批量操作支持

3. **资源指标**
   - 内存占用
   - 磁盘使用
   - CPU使用率

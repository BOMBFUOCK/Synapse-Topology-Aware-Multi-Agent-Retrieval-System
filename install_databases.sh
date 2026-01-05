#!/bin/bash
###
 # @Descripttion: 
 # @version: 1.3
 # @Author: YaoKaiDi
 # @Date: 2026-01-04 11:20:11
 # @LastEditors: YaoKaiDi
 # @LastEditTime: 2026-01-04 15:36:43
### 

echo "=== Synapse 本地数据库安装脚本 ==="

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "错误: 未找到 Homebrew。请先安装 Homebrew: https://brew.sh/"
    exit 1
fi

# 安装 Redis
echo "检查 Redis..."
if ! command -v redis-server &> /dev/null; then
    echo "安装 Redis..."
    brew install redis
else
    echo "Redis 已安装"
fi

# 启动 Redis
echo "启动 Redis..."
brew services start redis

# 等待 Redis 启动
sleep 2

# 测试 Redis 连接
if redis-cli ping &> /dev/null; then
    echo "✓ Redis 启动成功"
else
    echo "✗ Redis 启动失败"
    exit 1
fi

# 安装 Qdrant
echo "检查 Qdrant..."
if ! command -v qdrant &> /dev/null; then
    echo "安装 Qdrant..."
    brew tap qdrant/qdrant
    brew install qdrant
else
    echo "Qdrant 已安装"
fi

# 启动 Qdrant
echo "启动 Qdrant..."
brew services start qdrant

# 等待 Qdrant 启动
sleep 3

# 测试 Qdrant 连接
if curl -s http://localhost:6333/health &> /dev/null; then
    echo "✓ Qdrant 启动成功"
else
    echo "✗ Qdrant 启动失败"
    exit 1
fi

echo ""
echo "=== 安装完成 ==="
echo "Redis: 运行在 localhost:6379"
echo "Qdrant: 运行在 localhost:6333"
echo ""
echo "管理命令:"
echo "  启动服务: brew services start redis && brew services start qdrant"
echo "  停止服务: brew services stop redis && brew services stop qdrant"
echo "  查看状态: brew services list"

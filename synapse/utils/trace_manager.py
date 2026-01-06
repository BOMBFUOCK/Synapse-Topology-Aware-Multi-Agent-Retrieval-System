from typing import List, Optional
from synapse.core.db import VectorDBClient


class InfoTraceManager:
    """工具类，用于查询和管理信息的传播路径"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.vector_client = VectorDBClient(config_path)

    def get_trace(self, info_id: str) -> List[str]:
        """获取特定信息的完整传播路径
        
        Args:
            info_id: 信息的唯一ID
            
        Returns:
            List[str]: 传播路径列表，每个元素是信息内容
        """
        return self.vector_client.get_trace(info_id)

    def get_trace_length(self, info_id: str) -> int:
        """获取传播路径的长度（传播次数）
        
        Args:
            info_id: 信息的唯一ID
            
        Returns:
            int: 传播路径长度
        """
        return self.vector_client.get_trace_length(info_id)

    def get_latest_trace(self, info_id: str, n: int = 1) -> List[str]:
        """获取最近n条传播记录
        
        Args:
            info_id: 信息的唯一ID
            n: 获取的记录数量
            
        Returns:
            List[str]: 最近n条传播记录
        """
        trace = self.get_trace(info_id)
        return trace[-n:] if n > 0 else trace

    def print_trace_info(self, info_id: str):
        """打印信息的完整传播路径
        
        Args:
            info_id: 信息的唯一ID
        """
        trace = self.get_trace(info_id)
        length = len(trace)
        
        print(f"\n{'='*60}")
        print(f"信息传播路径查询")
        print(f"{'='*60}")
        print(f"信息ID: {info_id}")
        print(f"传播次数: {length}")
        print(f"{'-'*60}")
        
        if length == 0:
            print("该信息暂无传播记录")
        else:
            for i, content in enumerate(trace, 1):
                print(f"\n[传播 {i}]")
                # 截取内容显示，最多100个字符
                display_content = content[:100] + "..." if len(content) > 100 else content
                print(f"内容: {display_content}")
        
        print(f"{'='*60}\n")

    def compare_traces(self, info_ids: List[str]) -> dict:
        """比较多个信息的传播路径长度
        
        Args:
            info_ids: 信息ID列表
            
        Returns:
            dict: 信息ID到传播长度的映射
        """
        return {info_id: self.get_trace_length(info_id) for info_id in info_ids}

    def get_all_traces_summary(self, info_ids: List[str]) -> str:
        """获取多个信息的传播路径摘要
        
        Args:
            info_ids: 信息ID列表
            
        Returns:
            str: 格式化的摘要字符串
        """
        summary = []
        for info_id in info_ids:
            length = self.get_trace_length(info_id)
            summary.append(f"{info_id[:8]}...: {length} 次传播")
        return "\n".join(summary)

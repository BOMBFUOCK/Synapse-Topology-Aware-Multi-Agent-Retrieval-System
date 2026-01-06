from typing import List, Dict, Any
from synapse.core.retriever.ripple_search import SearchResult


class TraceVisualizer:
    """工具类，用于可视化搜索结果的传播链路"""

    @staticmethod
    def to_arrow_text(trace_chain: List[str]) -> str:
        """将trace_chain转换为文本箭头图
        
        Args:
            trace_chain: 传播链路列表，格式为 [Caller_ID, Source_ID]
            
        Returns:
            str: 文本箭头图，格式为 User ➔ Agent_A ➔ Agent_B
        """
        if not trace_chain:
            return ""
        return " ➔ ".join(trace_chain)

    @staticmethod
    def to_mermaid(trace_chain: List[str]) -> str:
        """将trace_chain转换为Mermaid流程图
        
        Args:
            trace_chain: 传播链路列表，格式为 [Caller_ID, Source_ID]
            
        Returns:
            str: Mermaid流程图语法
        """
        if not trace_chain:
            return ""
        
        mermaid = "graph TD\n"
        for i in range(len(trace_chain) - 1):
            mermaid += f"    {trace_chain[i]} --> {trace_chain[i+1]}\n"
        return mermaid

    @staticmethod
    def print_trace(results: List[SearchResult]):
        """在控制台打印结构化的链路信息
        
        Args:
            results: 搜索结果列表
        """
        if not results:
            print("No results found.")
            return
        
        for i, result in enumerate(results, 1):
            print(f"\n[Result #{i}]")
            print(f"Source: {result.source_agent_id}")
            print(f"Path: {TraceVisualizer.to_arrow_text(result.trace_chain)}")
            print(f"Content: {result.content}")
            if result.metadata:
                print(f"Metadata: {result.metadata}")
            print(f"Score: {result.score:.4f}")
            print("-" * 50)

    @staticmethod
    def print_mermaid(trace_chain: List[str]):
        """在控制台打印Mermaid流程图
        
        Args:
            trace_chain: 传播链路列表
        """
        mermaid = TraceVisualizer.to_mermaid(trace_chain)
        print("\nMermaid Flow Chart:")
        print("```mermaid")
        print(mermaid)
        print("```")

"""
缺口地图（Gap Map）
用于存储和管理未闭环数节点
"""

import uuid

class GapMap:
    """缺口地图，管理未闭环数的节点网络"""
    
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, data, node_id=None, gap=0.0, meta_gap=0.0):
        """添加节点到缺口地图"""
        if node_id is None:
            node_id = f"node_{uuid.uuid4().hex[:8]}"
        
        self.nodes[node_id] = {
            'id': node_id,
            'data': data,
            'gap': gap,
            'meta_gap': meta_gap
        }
        return node_id
    
    def get_all_nodes(self):
        """获取所有节点"""
        return list(self.nodes.values())
    
    def update_node_metadata(self, node_id, metadata):
        """更新节点元数据"""
        if node_id in self.nodes:
            self.nodes[node_id]['data'].metadata.update(metadata)
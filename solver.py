from typing import List, Tuple, Dict
from visualizer import MazeVisualizer
import time

class MazeSolver:
    """Cài đặt các thuật toán tìm đường trong mê cung"""
    
    def __init__(self, visualizer: MazeVisualizer):
        """Khởi tạo solver với trình hiển thị"""
        self.visualizer = visualizer
        self.cell_size = 24  # Kích thước ô để di chuyển
    
    def get_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Lấy các ô hàng xóm hợp lệ của một vị trí"""
        x, y = position
        neighbors = []
        
        # Kiểm tra 4 hướng
        for dx, dy in [(-self.cell_size, 0), (0, +self.cell_size), (+self.cell_size, 0), (0, -self.cell_size)]:
            new_pos = (x + dx, y + dy)
            if new_pos in self.visualizer.paths:
                neighbors.append(new_pos)
        
        return neighbors
    
    def dfs(self) -> Dict[Tuple[int, int], Tuple[int, int]]:
        """
        Thuật toán tìm kiếm theo chiều sâu (DFS)
        Trả về một dictionary ánh xạ mỗi vị trí đến vị trí trước đó của nó
        """
        start = self.visualizer.start_pos
        goal = self.visualizer.end_pos
        
        # Khởi tạo các cấu trúc dữ liệu
        visited = set()
        stack = [start]
        predecessors = {start: None}
        
        while stack:
            # FIX 1: Kiểm tra xem cửa sổ có bị đóng không
            if self.visualizer.window_closed:
                break
                
            time.sleep(self.visualizer.animation_speed)  # Sử dụng tốc độ hoạt ảnh được đặt
            
            # Lấy vị trí hiện tại từ ngăn xếp (LIFO cho DFS)
            current = stack.pop()
            
            # Nếu đã đến đích thì kết thúc
            if current == goal:
                return predecessors
            
            # Nếu đã thăm rồi thì bỏ qua
            if current in visited:
                continue
            
            # Đánh dấu đã thăm
            visited.add(current)
            self.visualizer.visualize_path(current, self.visualizer.path_turtle)
            
            # Lấy các hàng xóm và thêm vào stack
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    stack.append(neighbor)
                    self.visualizer.visualize_path(neighbor, self.visualizer.frontier_turtle)
                    
                    # Chỉ ghi nhận vị trí trước đó nếu chưa được thiết lập
                    if neighbor not in predecessors:
                        predecessors[neighbor] = current
        
        return predecessors
    
    def reconstruct_path(self, predecessors: Dict[Tuple[int, int], Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Tái tạo đường đi từ điểm bắt đầu đến điểm đích dựa trên dictionary predecessor"""
        current = self.visualizer.end_pos
        path = []
        
        # Lần ngược từ đích về đầu
        while current:
            path.append(current)
            current = predecessors.get(current)
        
        # Đảo ngược để được đường đi từ đầu -> đích
        path.reverse()
        return path
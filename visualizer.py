import turtle
import time
from typing import List, Tuple

class MazeVisualizer:
    """Xử lý phần hiển thị mê cung và thuật toán tìm đường"""
    
    def __init__(self, width=1000, height=500):
        """Khởi tạo trình hiển thị với thiết lập màn hình"""
        # Thiết lập màn hình
        self.screen = turtle.Screen()
        self.screen.bgcolor("black")
        self.screen.title("Maze Solver - Optimized")
        self.screen.setup(width=1.0, height=1.0)
        self.screen.tracer(0)  # Tắt hoạt ảnh trong quá trình thiết lập
        
        # FIX 1: Thêm flag để kiểm tra cửa sổ có còn hoạt động không
        self.window_closed = False
        
        # Khởi tạo các turtle cho các thành phần khác nhau
        self.maze_turtle = self._create_turtle("square", "white")
        self.path_turtle = self._create_turtle("square", "green")
        self.frontier_turtle = self._create_turtle("square", "blue")
        self.start_turtle = self._create_turtle("square", "red")
        self.end_turtle = self._create_turtle("square", "purple")
        self.solution_turtle = self._create_turtle("square", "yellow")
        
        # Thiết lập hướng di chuyển ban đầu cho turtle bắt đầu
        self.start_turtle.setheading(270)
        
        # Khởi tạo các cấu trúc dữ liệu cho mê cung
        self.walls = set()
        self.paths = set()
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        
        # Bật lại hoạt ảnh
        self.screen.tracer(1)
        self.animation_speed = 0  # Tốc độ hoạt ảnh mặc định
    
    def _create_turtle(self, shape: str, color: str) -> turtle.Turtle:
        """Tạo và trả về một turtle với hình dạng và màu sắc chỉ định"""
        t = turtle.Turtle()
        t.shape(shape)
        t.color(color)
        t.penup()
        t.speed(0)
        return t
    
    def setup_maze(self, grid: List[List[int]]) -> None:
        """Thiết lập mê cung dựa trên lưới được cung cấp"""
        self.screen.tracer(0)  # Tắt hoạt ảnh để thiết lập nhanh hơn
        
        # Xóa dữ liệu mê cung trước đó
        self.walls = set()
        self.paths = set()
        
        # Tính toán kích thước ô và độ lệch để căn giữa
        max_width = len(grid[0])
        cell_size = 24
        offset_x = -(max_width * cell_size) // 2 + cell_size // 2
        offset_y = (len(grid) * cell_size) // 2 - cell_size // 2
        
        # Duyệt từng ô trong lưới
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                # Tính tọa độ trên màn hình
                screen_x = offset_x + (x * cell_size)
                screen_y = offset_y - (y * cell_size)
                
                position = (screen_x, screen_y)
                
                if cell == 1:  # Tường
                    self.maze_turtle.goto(position)
                    self.maze_turtle.stamp()
                    self.walls.add(position)
                elif cell == 0:  # Đường đi
                    self.paths.add(position)
                elif cell == 2:  # Điểm bắt đầu
                    self.start_pos = position
                    self.start_turtle.goto(position)
                    self.start_turtle.stamp()
                    self.paths.add(position)
                elif cell == 3:  # Điểm kết thúc
                    self.end_pos = position
                    self.end_turtle.goto(position)
                    self.end_turtle.stamp()
                    self.paths.add(position)
        
        self.screen.update()
        self.screen.tracer(1)  # Bật lại hoạt ảnh
    
    def visualize_path(self, position: Tuple[int, int], turtle_obj: turtle.Turtle) -> None:
        """Hiển thị một vị trí bằng turtle được chỉ định"""
        # FIX 1: Thêm try-catch để xử lý khi cửa sổ bị đóng
        try:
            turtle_obj.goto(position)
            turtle_obj.stamp()
            
            # Vẽ lại điểm bắt đầu và kết thúc nếu bị ghi đè
            if position == self.start_pos:
                self.start_turtle.stamp()
            elif position == self.end_pos:
                self.end_turtle.stamp()
        except:
            self.window_closed = True
    
    def visualize_solution(self, path: List[Tuple[int, int]]) -> None:
        """Hiển thị đường đi lời giải"""
        for position in path:
            if position == self.start_pos or position == self.end_pos:
                continue
            # FIX 1: Thêm try-catch để xử lý khi cửa sổ bị đóng
            try:
                self.solution_turtle.goto(position)
                self.solution_turtle.stamp()
                time.sleep(0.01) 
            except:
                self.window_closed = True
                break
    
    def set_animation_speed(self, speed: float) -> None:
        """Đặt tốc độ hoạt ảnh (thời gian chờ giữa các bước)"""
        self.animation_speed = speed
    
    def exit_on_click(self) -> None:
        """Chờ người dùng click chuột để thoát"""
        if not self.window_closed:
            try:
                self.screen.exitonclick()
            except:
                pass
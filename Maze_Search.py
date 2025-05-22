import turtle
import time
import random
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Dict

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


def generate_maze(width: int, height: int) -> List[List[int]]:

# Đảm bảo kích thước là số lẻ
    if width % 2 == 0: width += 1
    if height % 2 == 0: height += 1

    # Khởi tạo mê cung toàn tường
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # Bắt đầu từ một ô ngẫu nhiên lẻ
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0

    walls: List[Tuple[int, int, int, int]] = []
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        nx, ny = start_x + dx, start_y + dy
        if 0 < nx < width and 0 < ny < height:
            walls.append((start_x, start_y, nx, ny))

    while walls:
        x, y, nx, ny = walls.pop(random.randint(0, len(walls) - 1))
        if maze[ny][nx] == 1:
            maze[ny][nx] = 0
            maze[(y + ny) // 2][(x + nx) // 2] = 0
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                ex, ey = nx + dx, ny + dy
                if 0 < ex < width and 0 < ey < height and maze[ey][ex] == 1:
                    walls.append((nx, ny, ex, ey))

    # Đặt điểm bắt đầu và kết thúc
    maze[start_y][start_x] = 2
    maze[height - 2][width - 2] = 3

    return maze


class MazeSizeInputWindow:
    """Cửa sổ nhập kích thước mê cung"""
    def __init__(self):
        """Khởi tạo cửa sổ nhập kích thước"""
        self.root = tk.Tk()
        self.maze_size = None
        self.maze_speed = 1
        self.root.title("Tạo mê cung ngẫu nhiên")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # FIX 3: Bind Enter key để tự động click "Tạo Mê Cung"
        self.root.bind('<Return>', lambda event: self.start_maze_solver())

        for i in range(4):
            self.root.rowconfigure(i, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, weight=1)    
        
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12))
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        
        # Nhãn và ô nhập chiều rộng
        ttk.Label(self.root, text="Chiều rộng (số lẻ):").grid(row=0, column=0, sticky="nw", padx=10, pady=5)
        self.width_entry = ttk.Entry(self.root)
        self.width_entry.grid(row=0, column=1, sticky="ne", padx=10, pady=5)
        # FIX 3: Bind Enter cho width_entry
        self.width_entry.bind('<Return>', lambda event: self.start_maze_solver())
        
        # Nhãn và ô nhập chiều cao
        ttk.Label(self.root, text="Chiều cao (số lẻ):").grid(row=1, column=0, sticky="nwe", padx=10, pady=5)
        self.height_entry = ttk.Entry(self.root)
        self.height_entry.grid(row=1, column=1, sticky="ne", padx=10, pady=5)
        # FIX 3: Bind Enter cho height_entry
        self.height_entry.bind('<Return>', lambda event: self.start_maze_solver())
        
        # Nhãn và thanh trượt tốc độ
        ttk.Label(self.root, text="Tốc độ tìm đường:").grid(row=2, column=0, sticky="nwe", padx=10, pady=5)
        self.speed_slider = ttk.Scale(
            self.root, 
            from_=0, 
            to=1, 
            orient=tk.HORIZONTAL, 
            length=200
        )
        self.speed_slider.set(0.1)  # Giá trị mặc định
        self.speed_slider.grid(row=2, column=1, sticky="ne", padx=10, pady=5)
        
        # Hiển thị giá trị tốc độ
        self.speed_label = ttk.Label(self.root, text="0.1")
        self.speed_label.grid(row=3, column=1, sticky="ne", padx=10, pady=5)
        
        # Kết nối sự kiện thay đổi thanh trượt
        self.speed_slider.configure(command=self.update_speed_label)
        
        # Nút xác nhận
        ttk.Button(self.root, text="Tạo Mê Cung", command=self.start_maze_solver).grid(row=4, columnspan=2, sticky="ns", padx=10, pady=10)
        
        self.maze_size = None
        self.maze_speed = 0.1 
    def update_speed_label(self, value):
        """Cập nhật nhãn hiển thị giá trị tốc độ"""
        self.speed_label.config(text=f"{float(value):.2f}")
        self.maze_speed = float(value)
    
    def start_maze_solver(self):
        """Xử lý kích thước mê cung và bắt đầu giải mê cung"""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            
            # Kiểm tra tính hợp lệ của kích thước
            if width % 2 == 0 or height % 2 == 0:
                messagebox.showerror("Lỗi", "Chiều rộng và cao phải là số lẻ!")
                return
            
            self.maze_size = (width, height)
            self.root.quit()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên!")


def main() -> None:
    """Hàm chính để chạy chương trình giải mê cung"""
    # FIX 2: Thêm vòng lặp để có thể chạy nhiều lần
    while True:
        # Hiển thị cửa sổ nhập kích thước
        size_input = MazeSizeInputWindow()
        size_input.root.mainloop()
        
        # Kiểm tra nếu người dùng đã nhập kích thước
        if size_input.maze_size is None:
            try:
                size_input.root.destroy()
            except tk.TclError:
                pass
            break
        
        # Lấy kích thước mê cung
        width, height = size_input.maze_size
        
        # FIX 2: Đóng cửa sổ input trước khi tạo turtle
        size_input.root.destroy()
        
        # Tạo trình hiển thị và giải mê cung
        visualizer = MazeVisualizer()
        solver = MazeSolver(visualizer)
        
        # Sinh và hiển thị mê cung
        maze = generate_maze(width, height)
        visualizer.setup_maze(maze)
        
        # Đặt tốc độ hoạt ảnh từ thanh trượt
        visualizer.set_animation_speed(size_input.maze_speed)
        
        # Giải mê cung
        predecessors = solver.dfs()
        if not visualizer.window_closed:
            path = solver.reconstruct_path(predecessors)
            visualizer.visualize_solution(path)
        
        # Chờ click để đóng
        visualizer.exit_on_click()
        
        # FIX 2: Reset turtle để có thể chạy lại
        try:
            turtle.bye()
        except:
            pass

if __name__ == "__main__":
    main()
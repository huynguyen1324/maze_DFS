import random
from typing import List, Tuple

class MazeGenerator:
    """Lớp sinh mê cung ngẫu nhiên"""
    
    @staticmethod
    def generate(width: int, height: int) -> List[List[int]]:
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
        end_x, end_y = width - 2, height - 2
        maze[end_y][end_x] = 3

        # Tạo thêm lối đi gần điểm kết thúc
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ex, ey = end_x + dx, end_y + dy
            if 0 < ex < width - 1 and 0 < ey < height - 1:
                if maze[ey][ex] == 1 and random.random() < 0.5:  # Xác suất 50% mở
                    maze[ey][ex] = 0
                    maze[(ey + end_y) // 2][(ex + end_x) // 2] = 0

        return maze

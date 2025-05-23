import tkinter as tk
from tkinter import ttk, messagebox

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
            
            self.maze_size = (width, height)
            self.root.quit()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên!")
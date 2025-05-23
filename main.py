from input import MazeSizeInputWindow
from visualizer import MazeVisualizer
from solver import MazeSolver
from maze_generator import MazeGenerator
import turtle

def main():
    
    while True:
        size_input = MazeSizeInputWindow()
        size_input.root.mainloop()
        
        if size_input.maze_size is None:
            try: size_input.root.destroy()
            except: pass
            break

        width, height = size_input.maze_size
        size_input.root.destroy()

        visualizer = MazeVisualizer()
        solver = MazeSolver(visualizer)
        maze = MazeGenerator.generate(width, height)
        visualizer.setup_maze(maze)
        visualizer.set_animation_speed(size_input.maze_speed)

        predecessors = solver.dfs()
        if not visualizer.window_closed:
            path = solver.reconstruct_path(predecessors)
            visualizer.visualize_solution(path)

        visualizer.exit_on_click()
        try:
            turtle.bye()
        except:
            pass

if __name__ == "__main__":
    main()

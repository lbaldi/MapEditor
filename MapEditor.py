import Tkinter as tk
from Figure import Figure
import GraphSolver as GraphSolver


class MapEditor(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(width=400, height=400)
        self.canvas.pack(fill="both", expand=True)

        # Diccionario usado para mantener los datos de la figura que esta siendo creada
        self.__create_data = {}

        self.figures = []

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<ButtonPress-3>", self.solve_graph)

    @property
    def figure_active(self):
        flag = False
        for each in self.figures:
            if each.active:
                flag = True
                break
        return flag

    def solve_graph(self, event):

        for figure in self.figures:

            start_node = figure.get_graph_start()
            end_node = figure.get_graph_end()

            figure.clean_old_path()

            if start_node and end_node:

                graph = figure.get_graph_without_obstacles()

                path = GraphSolver.find_shortest_path(graph, start_node, end_node)

                if path:
                    path.remove(start_node)
                    path.remove(end_node)
                    for each in path:
                        self.canvas.itemconfig(each, fill="pink")

    def on_button_press(self, event):

        if not self.figure_active:

            self.__create_data['x1'] = event.x
            self.__create_data['y1'] = event.y
            self.__create_data['x2'] = event.x
            self.__create_data['y2'] = event.y
            self.__create_data['figure'] = self.canvas.create_rectangle(0, 0, 1, 1)

    def on_move_press(self, event):

        if not self.figure_active and self.__create_data:

            x = self.__create_data.get('x1')
            y = self.__create_data.get('y1')
            figure = self.__create_data.get('figure')
            self.__create_data['x2'] = event.x
            self.__create_data['y2'] = event.y

            self.canvas.coords(figure, x, y, event.x, event.y)

    def on_button_release(self, event):

        if not self.figure_active and self.__create_data:

            self.canvas.delete(self.__create_data.get('figure'))

            x1 = self.__create_data.get('x1')
            y1 = self.__create_data.get('y1')
            x2 = self.__create_data.get('x2')
            y2 = self.__create_data.get('y2')

            self.create_figure(x1, y1, x2, y2, "white")

            self.__create_data = {}

    def create_figure(self, x1, y1, x2, y2, color):

        figure = Figure(x1, y1, x2, y2, color, color, "figure", self.canvas)
        self.figures.append(figure)

from FigureGrid import FigureGrid
import copy


class Figure(object):

    def __init__(self, x1, y1, x2, y2, outline, fill, tags, canvas):

        self.id = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.outline = outline
        self.fill = fill
        self.tags = tags
        self.aux_x = 0
        self.aux_y = 0
        self.active = False
        self.grid = []
        self.canvas = canvas

        self.set_normalized_coords(x1, y1, x2, y2)
        self.draw()
        self.set_grid(40, 0, 0)

    def set_normalized_coords(self, x1, y1, x2, y2):

        # Se invierten los vertices para dejar normalizado
        if x1 > x2:
            self.x1 = x2
            self.x2 = x1
        else:
            self.x1 = x1
            self.x2 = x2

        # Se invierten los vertices para dejar normalizado
        if y1 > y2:
            self.y1 = y2
            self.y2 = y1
        else:
            self.y1 = y1
            self.y2 = y2

    @property
    def collide(self):
        """Verifica que la figura no se superponga
        con otras cosas en en lazo excepto por ella
        misma y su grilla."""

        collide_list = self.canvas.find_overlapping(self.x1, self.y1, self.x2, self.y2)
        figure_list = [self.id]
        figure_list.extend(self.get_grid_ids())

        if len(collide_list) > len(figure_list):
            return True
        else:
            return False

    def get_grid_ids(self):

        ids = []
        for node in self.grid:
            ids.append(node.id)
        return ids

    def move_grid(self, delta_x, delta_y):

        for node in self.grid:
            self.canvas.move(node.id, delta_x, delta_y)

    def move(self, delta_x, delta_y):

        if not self.canvas:
            raise Exception("Debe asignar un lazo para dicha figura.")

        self.x1 += delta_x
        self.x2 += delta_x
        self.y1 += delta_y
        self.y2 += delta_y

        self.canvas.move(self.id, delta_x, delta_y)
        self.move_grid(delta_x, delta_y)

        if self.collide:

            self.move(- delta_x, - delta_y)

    def set_grid(self, distance, shift_x, shift_y):

        initial_x = int(self.x1)
        shift_x = int(shift_x)
        final_x = int(self.x2)
        grid_distance = int(distance)
        initial_y = int(self.y1)
        shift_y = int(shift_y)
        final_y = int(self.y2)

        vector_x = []
        vector_y = []

        vector_x.append(initial_x)
        for x_grid in range(initial_x + grid_distance - shift_x, final_x, grid_distance):
            vector_x.append(x_grid)
        vector_x.append(final_x)

        vector_y.append(initial_y)
        for y_grid in range(initial_y + grid_distance - shift_y, final_y, grid_distance):
            vector_y.append(y_grid)
        vector_y.append(final_y)

        prev_y_list = []

        for i, j in zip(vector_x, vector_x[1:]):

            prev_y_node = None
            aux_y_list = []

            for m, n in zip(vector_y, vector_y[1:]):

                node = FigureGrid(i, m, j, n, "black", "white", "grid", self)

                aux_y_list.append(node)

                self.grid.append(node)

                if prev_y_node:
                    node.add_neighbour(prev_y_node)

                if prev_y_list:
                    node.add_neighbour(prev_y_list.pop())

                prev_y_node = node

            prev_y_list = copy.copy(aux_y_list)
            prev_y_list.reverse()

    def get_graph_start(self):

        for node in self.grid:
            if node.fill == "green":
                return node.id

    def get_graph_end(self):

        for node in self.grid:
            if node.fill == "blue":
                return node.id

    def get_graph_without_obstacles(self):

        graph = {}
        for node in self.grid:
            if node.fill != "red":
                graph[node.id] = node.get_neighbour_without_obstacles()
        return graph

    def delete(self):
        self.canvas.delete(self.id)
        for node in self.grid:
            self.canvas.delete(node.id)

    def draw(self):

        self.id = self.canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            outline=self.outline,
            fill=self.fill,
            tags=self.tags,
        )

        if self.collide:
            self.delete()
            raise Exception("No se pueden crear figuras superpuestas.")

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_figure_button_1_press)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_figure_motion)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_figure_release)
        self.canvas.tag_bind(self.id, "<ButtonPress-2>", self.on_figure_button_2_press)

    def on_figure_button_2_press(self, event):

        self.delete()

    def on_figure_button_1_press(self, event):

        self.active = True
        self.aux_x = event.x
        self.aux_y = event.y

    def on_figure_motion(self, event):

        delta_x = event.x - self.aux_x
        delta_y = event.y - self.aux_y

        self.move(delta_x, delta_y)

        self.aux_x = event.x
        self.aux_y = event.y

    def on_figure_release(self, event):

        self.active = False

    def clean_old_path(self):

        for node in self.grid:

            self.canvas.itemconfig(node.id, fill=node.fill)

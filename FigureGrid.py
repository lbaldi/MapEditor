class FigureGrid(object):

    def __init__(self, x1, y1, x2, y2, outline, fill, tags, figure):

        self.id = None
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.figure = figure
        self.outline = outline
        self.fill = fill
        self.tags = tags
        self.canvas = figure.canvas
        self.neighbour_nodes = []

        self.set_normalized_coords(x1, y1, x2, y2)
        self.draw()

    def get_neighbour_without_obstacles(self):
        neighbours = {}
        for neighbour in self.neighbour_nodes:
            if neighbour.fill != "red":
                neighbours[neighbour.id] = 1
        return neighbours

    def add_neighbour(self, neighbour):

        self.neighbour_nodes.append(neighbour)
        neighbour.neighbour_nodes.append(self)

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

        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.on_figure_button_1_press)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.on_figure_release)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.on_figure_motion)
        self.canvas.tag_bind(self.id, "<ButtonPress-2>", self.on_figure_button_2_press)
        self.canvas.tag_bind(self.id, "<ButtonPress-3>", self.on_figure_button_3_press)

    def on_figure_button_3_press(self, event):

        if self.fill == "blue":
            self.fill = "white"
        elif self.fill == "white":
            self.fill = "red"
        elif self.fill == "red":
            self.fill = "green"
        elif self.fill == "green":
            self.fill = "blue"

        self.figure.canvas.itemconfig(self.id, fill=self.fill)

    def on_figure_button_2_press(self, event):

        self.figure.on_figure_button_2_press(event)

    def on_figure_button_1_press(self, event):

        self.figure.on_figure_button_1_press(event)

    def on_figure_motion(self, event):

        self.figure.on_figure_motion(event)

    def on_figure_release(self, event):

        self.figure.on_figure_release(event)

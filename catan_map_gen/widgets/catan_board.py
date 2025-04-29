from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Mesh
from kivy.uix.label import Label
from kivy.clock import Clock
import math

# Resource colors
resource_colors = {
    "Wood": (0.2, 0.6, 0.2),
    "Sheep": (0.8, 1, 0.8),
    "Wheat": (1, 1, 0.4),
    "Brick": (0.8, 0.3, 0.2),
    "Ore": (0.5, 0.5, 0.5),
    "Desert": (0.95, 0.8, 0.6),
}

# Official port positions (hex edge coordinates and angles)
PORT_POSITIONS_4P = [
    (0, -2, 0),    # top
    (1, -2, 30),  # top-right
    (2, -1, 60),  # right-top
    (2, 0, 90),   # right-bottom
    (1, 1, 120),  # bottom-right
    (0, 2, 180),  # bottom
    (-1, 2, 210), # bottom-left
    (-2, 1, 240), # left-bottom
    (-2, 0, 270), # left-top
]
PORT_POSITIONS_6P = [
    (0, -3, 0),    # top
    (1, -3, 20),  # top-right
    (2, -3, 40),  # right-top
    (3, -2, 60),  # right-top2
    (3, -1, 80),  # right
    (3, 0, 100),  # right-bottom
    (2, 2, 140),  # bottom-right
    (1, 3, 180),  # bottom
    (0, 3, 200),  # bottom-left
    (-1, 3, 220), # left-bottom
    (-3, 1, 260), # left-top
]

# Official Catan 4-player port order (clockwise from top, matched to user image)
PORT_EDGES_4P_IDX = [
    ((0, 0), (0, 1)),  # top-left
    ((0, 2), 30),     # top-right corner
    ((1, 3), (2, 4)),  # right
    ((2, 4), (3, 3)),  # bottom-right
    ((4, 2), -30),    # bottom-right corner (single hex, -30-degree angle)
    ((4, 0), (4, 1)),  # bottom (between two bottom hexes)
    ((4, 0), (3, 0)),  # left-bottom
    ((0, 0), (1, 0)),  # left-top
    ((2, 0), 180),     # leftmost hex, offset left
]

class CatanBoard(Widget):
    def __init__(self, board_data, layout, ports, **kwargs):
        super().__init__(**kwargs)
        self.board_data = board_data
        self.layout = layout
        self.ports = ports
        Clock.schedule_once(self.draw_board)

    def draw_board(self, *args):
        self.canvas.clear()
        self.clear_widgets()

        # Draw white background
        with self.canvas:
            Color(1, 1, 1)  # White color
            from kivy.graphics import Rectangle
            Rectangle(pos=self.pos, size=self.size)

        radius = 50  # size of each hex tile
        spacing_x = radius * math.sqrt(3)
        spacing_y = radius * 1.5
        center_x = self.width / 2
        center_y = self.height / 2 + (len(self.layout) * 30)

        # Build a map of (row, col) to pixel centers
        hex_centers = {}
        index = 0
        for row_idx, tiles_in_row in enumerate(self.layout):
            x_start = center_x - (tiles_in_row - 1) * spacing_x / 2
            for col_idx in range(tiles_in_row):
                x = x_start + col_idx * spacing_x
                y = center_y - (row_idx - len(self.layout)/2) * spacing_y
                res, num = self.board_data[index]
                color = resource_colors.get(res, (1, 1, 1))
                self.draw_hexagon(x, y, radius, color)
                hex_centers[(row_idx, col_idx)] = (x, y)
                # Resource label
                res_lbl = Label(
                    text=res,
                    center=(x, y + 10),
                    font_size=14,
                    color=(0, 0, 0, 1)
                )
                self.add_widget(res_lbl)
                # Number label (if not desert)
                if num is not None:
                    num_lbl = Label(
                        text=str(num),
                        center=(x, y - 10),
                        font_size=16,
                        color=(0, 0, 0, 1),
                        bold=True
                    )
                    self.add_widget(num_lbl)
                index += 1

        # Draw ports for 4-player board
        if len(self.layout) == 5:
            for i, entry in enumerate(PORT_EDGES_4P_IDX):
                if i >= len(self.ports):
                    break
                # Special case for the first port (top-left)
                if i == 0:
                    (r1, c1), (r2, c2) = entry
                    if (r1, c1) in hex_centers and (r2, c2) in hex_centers:
                        x1, y1 = hex_centers[(r1, c1)]
                        x2, y2 = hex_centers[(r2, c2)]
                        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                        dx, dy = mx - center_x, my - center_y
                        norm = (dx ** 2 + dy ** 2) ** 0.5
                        if norm != 0:
                            mx += (dx / norm) * (radius * 1.7)
                            my += (dy / norm) * (radius * 1.7)
                        port = self.ports[i]
                        # Left dock line: midpoint between (0,0) at 300° and (0,1) at 240°
                        corner1a = self.get_hex_corner(x1, y1, radius, 300)
                        corner1b = self.get_hex_corner(x2, y2, radius, 300)
                        left_dock = ((corner1a[0] + corner1b[0]) / 2, (corner1a[1] + corner1b[1]) / 2)
                        # Right dock line: top edge midpoint of (0,1) (angle 90°)
                        edge2 = self.get_hex_corner(x2, y2, radius, 90)
                        with self.canvas:
                            Color(0.5, 0.5, 0.5)
                            from kivy.graphics import Line, RoundedRectangle
                            factor = 0.45  # Shorten the line
                            adj_x = mx + (left_dock[0] - mx) * factor
                            adj_y = my + (left_dock[1] - my) * factor
                            Line(points=[mx, my, adj_x, adj_y], width=2)    
                            Line(points=[mx, my, *edge2], width=2)
                            Color(0.85, 0.85, 0.85)
                            RoundedRectangle(pos=(mx-32, my-18), size=(64, 36), radius=[18])
                        port_lbl = Label(text=f"Port\n{port}", center=(mx, my), font_size=14, color=(0.2, 0.2, 0.2, 1), bold=True)
                        self.add_widget(port_lbl)
                    continue
                # Handle (hex, angle) for single-hex port
                if (
                    isinstance(entry, tuple)
                    and len(entry) == 2
                    and isinstance(entry[0], tuple)
                    and isinstance(entry[1], (int, float))
                ):
                    (r, c), angle = entry
                    if (r, c) in hex_centers:
                        x, y = hex_centers[(r, c)]
                        mx = x + math.cos(math.radians(angle)) * radius * 1.8
                        my = y + math.sin(math.radians(angle)) * radius * 2.8
                        edge_x = x + (mx - x) * (radius / (radius * 1.8))
                        edge_y = y + (my - y) * (radius / (radius * 2.8))
                        port = self.ports[i]
                        with self.canvas:
                            Color(0.5, 0.5, 0.5)
                            from kivy.graphics import Line, RoundedRectangle
                            Line(points=[mx, my, edge_x, edge_y], width=2)
                            Color(0.85, 0.85, 0.85)
                            RoundedRectangle(pos=(mx-32, my-18), size=(64, 36), radius=[18])
                        port_lbl = Label(text=f"Port\n{port}", center=(mx, my), font_size=14, color=(0.2, 0.2, 0.2, 1), bold=True)
                        self.add_widget(port_lbl)
                # Handle ((r1, c1), (r2, c2)) for two-hex port
                elif (
                    isinstance(entry, tuple)
                    and len(entry) == 2
                    and isinstance(entry[0], tuple)
                    and isinstance(entry[1], tuple)
                ):
                    (r1, c1), (r2, c2) = entry
                    if (r1, c1) in hex_centers and (r2, c2) in hex_centers:
                        x1, y1 = hex_centers[(r1, c1)]
                        x2, y2 = hex_centers[(r2, c2)]
                        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                        dx, dy = mx - center_x, my - center_y
                        norm = (dx ** 2 + dy ** 2) ** 0.5
                        if norm != 0:
                            mx += (dx / norm) * (radius * 1.7)
                            my += (dy / norm) * (radius * 1.7)
                        port = self.ports[i]
                        edge1_x = x1 + (mx - x1) * (radius / (radius * 2.7))
                        edge1_y = y1 + (my - y1) * (radius / (radius * 2.7))
                        edge2_x = x2 + (mx - x2) * (radius / (radius * 3.7))
                        edge2_y = y2 + (my - y2) * (radius / (radius * 3.7))
                        with self.canvas:
                            Color(0.5, 0.5, 0.5)
                            from kivy.graphics import Line, RoundedRectangle
                            Line(points=[mx, my, edge1_x, edge1_y], width=2)
                            Line(points=[mx, my, edge2_x, edge2_y], width=2)
                            Color(0.85, 0.85, 0.85)
                            RoundedRectangle(pos=(mx-32, my-18), size=(64, 36), radius=[18])
                        port_lbl = Label(text=f"Port\n{port}", center=(mx, my), font_size=14, color=(0.2, 0.2, 0.2, 1), bold=True)
                        self.add_widget(port_lbl)
                # Handle a 3-tuple (hex, angle, offset) for this special case
                if (
                    isinstance(entry, tuple)
                    and len(entry) == 3
                    and isinstance(entry[0], tuple)
                    and isinstance(entry[1], (int, float))
                    and isinstance(entry[2], (int, float))
                ):
                    (r, c), angle, offset = entry
                    if (r, c) in hex_centers:
                        x, y = hex_centers[(r, c)]
                        mx = x + math.cos(math.radians(angle)) * radius * offset
                        my = y + math.sin(math.radians(angle)) * radius * offset
                        edge_x = x + (mx - x) * (radius / (radius * offset))
                        edge_y = y + (my - y) * (radius / (radius * offset))
                        port = self.ports[i]
                        with self.canvas:
                            Color(0.5, 0.5, 0.5)
                            from kivy.graphics import Line, RoundedRectangle
                            Line(points=[mx, my, edge_x, edge_y], width=2)
                            Color(0.85, 0.85, 0.85)
                            RoundedRectangle(pos=(mx-32, my-18), size=(64, 36), radius=[18])
                        port_lbl = Label(text=f"Port\n{port}", center=(mx, my), font_size=14, color=(0.2, 0.2, 0.2, 1), bold=True)
                        self.add_widget(port_lbl)

    def draw_hexagon(self, x, y, radius, color):
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            px = x + radius * math.cos(angle_rad)
            py = y + radius * math.sin(angle_rad)
            points += [px, py]

        with self.canvas:
            Color(*color)
            Line(points=points + points[:2], width=2)

    def get_hex_corner(self, x, y, radius, angle_deg):
        angle_rad = math.radians(angle_deg)
        return (
            x + radius * math.cos(angle_rad),
            y + radius * math.sin(angle_rad)
        )

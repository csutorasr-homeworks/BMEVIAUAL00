from tkinter import *
import tkinter as tk
import tkinter.font as tk_font
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import xml.etree.ElementTree as ElementTree
import getpass
import alg
import util


window_width = 1280
window_height = 720


def convert_coordinates(text):
    """
    Transforms the given text's coordinates to the scale of the canvas,
    which is used in the application.
    """

    # Calculating the four edges of the text.
    minx = min([float(x) for ((x, y), time) in text[0].coordinates])
    miny = min([float(y) for ((x, y), time) in text[0].coordinates])
    maxx = max([float(x) for ((x, y), time) in text[0].coordinates])
    maxy = max([float(y) for ((x, y), time) in text[0].coordinates])

    for i in range(1, len(text)):
        temp_x_min = [float(x) for ((x, y), time) in text[i].coordinates if float(x) < minx]
        temp_y_min = [float(y) for ((x, y), time) in text[i].coordinates if float(y) < miny]
        temp_x_max = [float(x) for ((x, y), time) in text[i].coordinates if float(x) > maxx]
        temp_y_max = [float(y) for ((x, y), time) in text[i].coordinates if float(y) > maxy]

        minx = minx if len(temp_x_min) == 0 else min(temp_x_min)
        miny = miny if len(temp_y_min) == 0 else min(temp_y_min)
        maxx = maxx if len(temp_x_max) == 0 else max(temp_x_max)
        maxy = maxy if len(temp_y_max) == 0 else max(temp_y_max)

    # Calculating the scaling
    scale = 1/(maxy-miny) * 4/5 * window_height

    if (maxx-minx)*scale > window_width:
        scale = scale*1/((maxx-minx)*scale)*4/5*window_width

    # Calculating the offset value
    bias = (-minx*scale + (window_width/2 - (maxx-minx)*scale/2), -miny*scale + (window_height/2 - (maxy-miny)*scale/2))

    return scale, bias


class Gui(tk.Frame):
    """
    Gui class, for debugging purposes. The class serves only as an interface for the user,
    hence the model is not implemented here, but in the alg.py file.
    """

    def __init__(self, gui_root):
        tk.Frame.__init__(self, gui_root)
        self.gui_root = gui_root

        self.gui_root.title('RightLeft')

        self.create_menu()
        self.canvas = Canvas(self.gui_root, width=window_width, height=window_height)

        # The alg variable is the port between the model, and the gui.
        self.alg = None

        # Variable that stores the stroke data in the previously defined Stroke class as a list.
        self.strokes = []

        # Binding the move functions to the action listener.
        self.canvas.bind("<ButtonPress-1>", self.move_start)
        self.canvas.bind("<B1-Motion>", self.move_move)

        # Binding zoom (Linux)
        self.canvas.bind("<Button-4>", self.zoom_p)
        self.canvas.bind("<Button-5>", self.zoom_m)

        # Binding zoom (Windows)
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.canvas.pack()
        self.center()

    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom_p(self, event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom_m(self, event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def zoom(self, event):
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def center(self):
        """
        Adjusts the window to the center of the screen.
        :return:
        """
        self.gui_root.update_idletasks()
        width = self.gui_root.winfo_width()
        height = self.gui_root.winfo_height()
        x = (self.gui_root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.gui_root.winfo_screenheight() // 2) - (height // 2)
        self.gui_root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_menu(self):
        menu = Menu(self.gui_root)

        file_menu = Menu(menu)
        file_menu.add_command(label="Load File", command=self.load)
        file_menu.add_command(label="Save File", command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.gui_root.quit)
        menu.add_cascade(label="File", menu=file_menu)

        self.gui_root.config(menu=menu)

    def update(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, window_width, window_height, fill="white")
        self.draw()

    def draw(self):
        scale, bias = convert_coordinates(self.strokes)
        for j, stroke in enumerate(self.strokes):

            # Draws the index of each stroke onto the canvas.
            self.canvas.create_text(float(stroke.coordinates[0][0][0]) * scale + bias[0],
                                    float(stroke.coordinates[0][0][1]) * scale + bias[1], text=str(j), fill="red",
                                    font=tk_font.Font(size=8, weight="bold"))
            # Connecting the stored stroke coordinates
            for i in range(len(stroke.coordinates)-1):
                x1 = float(stroke.coordinates[i][0][0]) * scale + bias[0]
                y1 = float(stroke.coordinates[i][0][1]) * scale + bias[1]
                x2 = float(stroke.coordinates[i+1][0][0]) * scale + bias[0]
                y2 = float(stroke.coordinates[i+1][0][1]) * scale + bias[1]

                self.canvas.create_line(x1, y1, x2, y2, width=3)
        # Calculating the indexes of horizontal strokes
        h_line_indexes = self.alg.get_horizontal_lines()

        for index, stroke in enumerate(self.strokes):
            if index in h_line_indexes:
                self.canvas.create_oval(float(stroke.coordinates[0][0][0]) * scale + bias[0] - 3,
                                        float(stroke.coordinates[0][0][1]) * scale + bias[1] - 3,
                                        float(stroke.coordinates[0][0][0]) * scale + bias[0] + 3,
                                        float(stroke.coordinates[0][0][1]) * scale + bias[1] + 3,
                                        fill="green")

    def load(self):
        user = getpass.getuser()
        file_name = askopenfilename(filetypes=(("XML files", "*.xml"), ("All files", "*.*")),
                                    initialdir='/media/patrik/1EDB65B8599DD93E/Data/Erika/Data')
        if file_name:
            try:
                self.alg = alg.Algorithm(str(file_name))
                self.extract_data(str(file_name))
                self.update()
            except IOError:
                showerror("Open Source File", "Failed to read file\n'%s'" % file_name)

    def extract_data(self, file):
        """
        Gathers the stroke data from the xml.
        :param file: String, containing the absolute path of the file.
        :return:
        """
        tree = ElementTree.parse(file)
        xml_root = tree.getroot()

        stroke_set = None
        for child in xml_root:
            if str(child.tag) == 'StrokeSet':
                stroke_set = child
                break

        if stroke_set is None:
            return

        self.strokes = []
        for stroke in stroke_set:
            coordinates = []
            for point in stroke:
                coordinates.append(((point.attrib['x'], point.attrib['y']), point.attrib['time']))

            self.strokes.append(util.Stroke(float(stroke.attrib['start_time']), float(stroke.attrib['end_time']),
                                            coordinates=coordinates))

    def save(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    Gui(root).pack()
    root.mainloop()

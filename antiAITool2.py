import PIL
from PIL import Image
import random
from random import randrange

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

def generate_normalized_random_map(width, height, intensity):
    arr = []
    for i in range(width):
        row = []
        for j in range(height):
            row.append(0)
        arr.append(row)

    for i in range(width-1):
        for j in range(height-1):
            r = randrange(-intensity,intensity)
            arr[i][j] += r
            arr[i][j+1] -= r
            arr[i+1][j] -= r
            arr[i+1][j+1] -= r
            

    return arr

def constrain(value, min, max):
    if value > max:
        value = max
    if value < min:
        value = min
    return value

print(generate_normalized_random_map(10,10,10))

file_path = ""

def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Images", ["*.png","*.jpeg","*.jpg"])])
    if not file_path:
        messagebox.showerror("No File Selected", "No file was selected! AntiAI will now close.")
        exit()
    return file_path


def process_image(intensity):
    img = Image.open(file_path)
    pixels = img.load()
    width, height = img.size
    new_img = Image.new(mode="RGB", size=(width*2, height*2))
    new_pixels = new_img.load()
    rmap = generate_normalized_random_map(width,height,intensity)
    gmap = generate_normalized_random_map(width,height,intensity)
    bmap = generate_normalized_random_map(width,height,intensity)
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y][:3] # Get RGB values, ignore alpha if present
            
            # Modify pixel values (example: invert colors)
            new_r, new_g, new_b = constrain(r + rmap[x][y],0,255),constrain(g + gmap[x][y],0,255),constrain(b + bmap[x][y],0,255)
            new_pixels[x*2, y*2] = (new_r, new_g, new_b)  # Update pixel
            new_r, new_g, new_b = constrain(r - rmap[x][y],0,255),constrain(g - gmap[x][y],0,255),constrain(b - bmap[x][y],0,255)
            new_pixels[x*2, y*2+1] = (new_r, new_g, new_b)  # Update pixel
            new_r, new_g, new_b = constrain(r - rmap[x][y],0,255),constrain(g - gmap[x][y],0,255),constrain(b - bmap[x][y],0,255)
            new_pixels[x*2+1, y*2] = (new_r, new_g, new_b)  # Update pixel
            new_r, new_g, new_b = constrain(r + rmap[x][y],0,255),constrain(g + gmap[x][y],0,255),constrain(b + bmap[x][y],0,255)
            new_pixels[x*2+1, y*2+1] = (new_r, new_g, new_b)  # Update pixel
    new_img.save(file_path+"_AntiAI2.png")



def open_slider_dialog(title, prompt, min_val, max_val, initial_val):
    """Opens a slider dialog and returns the selected value."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    value = simpledialog.askinteger(title, prompt, minvalue=min_val, maxvalue=max_val, initialvalue=initial_val)

    root.destroy()  # Destroy the temporary root window
    return value

if __name__ == '__main__':
    file_path = ""
    open_file_dialog()
    slider_value = open_slider_dialog("Select Intensity", "Enter an intensity between 1 and 300.\nHigher intensity provides more protection, at the expense of image quality.", 1, 300, 10)
    if slider_value is not None:
        process_image(slider_value)
        messagebox.showinfo("Success", "File processing was successful! You should find the protected image in the same folder as the original.")
    else:
        messagebox.showerror("Cancelled", "File processing was cancelled! AntiAI will now close.")
        print()
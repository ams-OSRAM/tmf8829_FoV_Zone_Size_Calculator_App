# *****************************************************************************
# * Copyright by ams OSRAM AG                                                 *
# * All rights are reserved.                                                  *
# *                                                                           *
# *FOR FULL LICENSE TEXT SEE LICENSES-MIT.TXT                                 *
# *****************************************************************************
"""
Script to calculate FoV and projected zone sizes
"""

from math import sqrt, atan, pi, tan
from sys import exit 
from tkinter import messagebox, Label, OptionMenu, Button, Tk, StringVar, Entry
from PIL import Image, ImageTk
from io import BytesIO
from base64 import b64decode

rgb_color = (251, 248, 243)
hex_color = "#%02x%02x%02x" % rgb_color
options = ["         8 x 8 (64 depth-pixels)", "   16 x 16 (256 depth-pixels)", "32 x 32 (1,024 depth-pixels)", "48 x 32 (1,536 depth-pixels)"]

def center_window(width=300, height=300):
    """Window setup """
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def display_results():
    """Calculate & populate result fields """
    try:
        spad_x_max = 48                                                                                             # max x SPAD count
        spad_y_max = 32                                                                                             # max y SPAD count
        spad_x_size = 15                                                                                            # x SPAD size in um
        spad_y_size = 16.875                                                                                        # y SPAD size in um
        focal_distance = 540                                                                                        # focal distance in um

        res_calc_diag_value = round((atan(sqrt((float(entered_x_value.get())*spad_x_size)**2 + 
                                                         (float(entered_y_value.get())*spad_y_size)**2)/focal_distance/2)*2/pi*180),1)
        res_full_diag_value = round((atan(sqrt((float(spad_x_max)*spad_x_size)**2 + 
                                                         (float(spad_y_max)*spad_y_size)**2)/focal_distance/2)*2/pi*180),1)

        res_calc_x_fov_spad_value = round((2*atan(spad_x_size/2/focal_distance)/pi*180),1)
        res_calc_y_fov_spad_value = round((2*atan(spad_y_size/2/focal_distance)/pi*180),1)
        
        res_calc_x_spad_size = round((2*float(entered_dist_value.get())*tan((res_calc_x_fov_spad_value/180*pi)/2)),1)
        res_calc_y_spad_size = round((2*float(entered_dist_value.get())*tan((res_calc_y_fov_spad_value/180*pi)/2)),1)

        res_calc_x_fov_full_value = round((2*atan(float(entered_x_value.get())*spad_x_size/2/focal_distance)/pi*180),1)
        res_calc_y_fov_full_value = round((2*atan(float(entered_y_value.get())*spad_y_size/2/focal_distance)/pi*180),1)

        res_calc_x_size_full_value = round((float(spad_x_max)*2*float(entered_dist_value.get())*tan((res_calc_x_fov_spad_value/180*pi)/2)),1)
        res_calc_y_size_full_value = round((float(spad_y_max)*2*float(entered_dist_value.get())*tan((res_calc_y_fov_spad_value/180*pi)/2)),1)
        
        res_calc_x_zone_size_value = round((float(entered_x_value.get())*2*float(entered_dist_value.get())*tan((res_calc_x_fov_spad_value/180*pi)/2)),1)
        res_calc_y_zone_size_value = round((float(entered_y_value.get())*2*float(entered_dist_value.get())*tan((res_calc_y_fov_spad_value/180*pi)/2)),1)

    except Exception as ex:
        messagebox.showerror("Invalid Input", "Input must be numeric and within range!")
        clear_inputs_outputs()
        return

    calc_diag_value.set(res_calc_diag_value)
    calc_full_diag_value.set(res_full_diag_value)
    calc_x_fov_spad_value.set(res_calc_x_fov_spad_value)
    calc_y_fov_spad_value.set(res_calc_y_fov_spad_value)
    calc_x_spad_size.set(res_calc_x_spad_size)
    calc_y_spad_size.set(res_calc_y_spad_size)
    calc_x_fov_full_value.set(res_calc_x_fov_full_value)
    calc_y_fov_full_value.set(res_calc_y_fov_full_value)
    calc_x_size_full_value.set(f"{res_calc_x_size_full_value:,}")
    calc_y_size_full_value.set(f"{res_calc_y_size_full_value:,}")
    calc_x_zone_size_value.set(f"{res_calc_x_zone_size_value:,}")
    calc_y_zone_size_value.set(f"{res_calc_y_zone_size_value:,}")

def clear_inputs_outputs():
    """Clear result fields """
    fields = [entered_x_value, entered_y_value, entered_dist_value, calc_diag_value, calc_full_diag_value, calc_x_fov_spad_value,
              calc_y_fov_spad_value, calc_x_spad_size, calc_y_spad_size, calc_x_fov_full_value, calc_y_fov_full_value, calc_x_size_full_value, 
              calc_y_size_full_value, calc_x_zone_size_value, calc_y_zone_size_value]
    for i in fields:
        i.set('')

    selected_option.set(options[0])                                                                                 # Re-set to 8x8 default value
    dropdown = OptionMenu(root, selected_option, *options)
    dropdown.grid(row=0, column = 1, columnspan=2)

def quit_calculator():
    """Exit calculator """
    exit()

def update_dropdown(*args):
    """Pre-fill based on drop down selection """
    selected_value = selected_option.get()
    if selected_value == "         8 x 8 (64 depth-pixels)":
        entered_x_value.set(6)
        entered_y_value.set(4)
    
    elif selected_value == "   16 x 16 (256 depth-pixels)":
        entered_x_value.set(3)
        entered_y_value.set(2)

    elif selected_value == "32 x 32 (1,024 depth-pixels)":
        entered_x_value.set(1.5)
        entered_y_value.set(1)

    elif selected_value == "48 x 32 (1,536 depth-pixels)":
        entered_x_value.set(1)
        entered_y_value.set(1)

# configure window
root = Tk()
center_window(985, 500)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.title("ams OSRAM - TMF8829 FoV calculator")
root.configure(bg=hex_color)


# setup string variables for input / output
selected_option = StringVar()                                                                                       # input - resolution mode of operation 
entered_x_value = StringVar()                                                                                       # input - number of SPADs in x 
entered_y_value = StringVar()                                                                                       # input - number of SPADs in y
entered_dist_value = StringVar()                                                                                    # input - distance from sensor to target

calc_diag_value = StringVar()                                                                                       # output - calculated diagonal FoV value (°)
calc_full_diag_value = StringVar()                                                                                  # output - calculated full diagonal FoV value (°)
calc_x_fov_spad_value = StringVar()                                                                                 # output - calculated SPAD x FoV value (°)
calc_y_fov_spad_value = StringVar()                                                                                 # output - calculated SPAD y FoV value (°)
calc_x_spad_size = StringVar()                                                                                      # output - calculated SPAD x size value (°)
calc_y_spad_size  = StringVar()                                                                                     # output - calculated SPAD y size value (°)
calc_x_fov_full_value = StringVar()                                                                                 # output - calculated full x FoV value (°)
calc_y_fov_full_value = StringVar()                                                                                 # output - calculated full y FoV value (°)
calc_x_size_full_value = StringVar()                                                                                # output - calculated full size x value (mm)
calc_y_size_full_value = StringVar()                                                                                # output - calculated full size y value (mm)
calc_x_zone_size_value = StringVar()                                                                                # output - calculated zone size x value (mm)
calc_y_zone_size_value = StringVar()                                                                                # output - calculated zone sizw y value (mm)

# ams OSRAM logo
image_string = "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"

# Decode the string and open the image
image_data = b64decode(image_string)

tk_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))
label = Label(root, image=tk_image, bg=hex_color)
label.grid(row=0, column=5, columnspan=3, rowspan=4)

# insert dropdown box to select mode
label = Label(root, text='Please select resolution :', bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=0, column=0, padx=10, pady=10)
selected_option.trace_add('write',update_dropdown)
selected_option.set(options[0])                                                                                     # Set default value
dropdown = OptionMenu(root, selected_option, *options)
dropdown.grid(row=0, column = 1, columnspan=2)

# create Text label & widget for number of x & y SPADs and distance inputs
label = Label(root, text='Depth-pixel SPADs in x :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=1, column=0, padx=10, pady=10)
unit_label = Label(root, text='max = 48', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=1, column=2, padx=10)
Entry(root, textvariable = entered_x_value, width=10, justify="center").grid(row=1, column=1, padx=10, pady=10)

label = Label(root, text='Depth-pixel SPADs in y :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=2, column=0, padx=10)
unit_label = Label(root, text='max = 32', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=2, column=2, padx=10)
Entry(root, textvariable = entered_y_value, width=10, justify="center").grid(row=2, column=1, padx=10, pady=10)

label = Label(root, text='Enter distance :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=3, column=0, padx=10)
unit_label = Label(root, text='    mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=3, column=2, padx=10)
Entry(root, textvariable = entered_dist_value, width=10, justify="center").grid(row=3, column=1, padx=10, pady=10)

# create Text label & widget for calculated outputs
label = Label(root, text='Single SPAD FoV x :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=8, column=0, padx=10)
unit_label = Label(root, text='   °             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=8, column=2, padx=10)
Entry(root, textvariable = calc_x_fov_spad_value, width=10, justify="center").grid(row=8, column=1, padx=10, pady=10)

label = Label(root, text='Single SPAD FoV y :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=8, column=5, padx=10)
unit_label = Label(root, text='   °             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=8, column=7, padx=10)
Entry(root, textvariable = calc_y_fov_spad_value, width=10, justify="center").grid(row=8, column=6, padx=10, pady=10)

label = Label(root, text='Single SPAD size x :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=9, column=0, padx=10)
unit_label = Label(root, text='   mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=9, column=2, padx=10)
Entry(root, textvariable = calc_x_spad_size, width=10, justify="center").grid(row=9, column=1, padx=10, pady=10)

label = Label(root, text='Single SPAD size y :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=9, column=5, padx=10)
unit_label = Label(root, text='   mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=9, column=7, padx=10)
Entry(root, textvariable = calc_y_spad_size, width=10, justify="center").grid(row=9, column=6, padx=10, pady=10)

label = Label(root, text='Depth-pixel FoV diagonal :', width=25, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=10, column=0, padx=10)
unit_label = Label(root, text='   °             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=10, column=2, padx=10)
Entry(root, textvariable = calc_diag_value, width=10, justify="center").grid(row=10, column=1, padx=10, pady=10)

label = Label(root, text='Full FoV diagonal :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=10, column=5, padx=10)
unit_label = Label(root, text='   °             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=10, column=7, padx=10)
Entry(root, textvariable = calc_full_diag_value, width=10, justify="center").grid(row=10, column=6, padx=10, pady=10)

label = Label(root, text='Depth-pixel FoV x :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=11, column=0, padx=10)
unit_label = Label(root, text='    °             ', bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=11, column=2, padx=10)
Entry(root, textvariable = calc_x_fov_full_value, width=10, justify="center").grid(row=11, column=1, padx=10, pady=10)

label = Label(root, text='Depth-pixel FoV y :', bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=11, column=5, padx=10)
unit_label = Label(root, text='    °             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=11, column=7, padx=10)
Entry(root, textvariable = calc_y_fov_full_value, width=10, justify="center").grid(row=11, column=6, padx=10, pady=10)

label = Label(root, text='Depth-pixel size x :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=12, column=0, padx=10)
unit_label = Label(root, text='    mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=12, column=2, padx=10)
Entry(root, textvariable = calc_x_zone_size_value, width=10, justify="center").grid(row=12, column=1, padx=10, pady=10)

label = Label(root, text='Depth-pixel size y :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=12, column=5, padx=10)
unit_label = Label(root, text='    mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=12, column=7, padx=10)
Entry(root, textvariable = calc_y_zone_size_value, width=10, justify="center").grid(row=12, column=6, padx=10, pady=10)

label = Label(root, text='Full size x :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=13, column=0, padx=10)
unit_label = Label(root, text='    mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=13, column=2, padx=10)
Entry(root, textvariable = calc_x_size_full_value, width=10, justify="center").grid(row=13, column=1, padx=10, pady=10)

label = Label(root, text='Full size y :', width=20, bg=hex_color, font=("Arial", 10, "bold"))
label.grid(row=13, column=5, padx=10)
unit_label = Label(root, text='    mm             ', width=20, bg=hex_color, font=("Arial", 10, "bold"))
unit_label.grid(row=13, column=7, padx=10)
Entry(root, textvariable = calc_y_size_full_value, width=10, justify="center").grid(row=13, column=6, padx=10, pady=10)

label = Label(root, text=' Calculated values are approximate', bg=hex_color, font=("Arial", 14, "bold"))
label.grid(row=4, column=5, columnspan=4)

# Add a button to reset calculator
reset_button = Button(root, text="Reset", justify="center", font = ("bold"),command=clear_inputs_outputs)
reset_button.grid(row=4, column=0, pady=10)

# Add a button to trigger the calulate and display function
submit_button = Button(root, text="Calculate", justify="center", fg="green", font = ("bold"), command=display_results)
submit_button.grid(row=4, column=1, pady=10)
root.bind('<Return>', lambda event: display_results())

# Add a button to quit calculator
quit_button = Button(root, text="Quit", justify="center", fg="red", font = ("bold"),command=quit_calculator)
quit_button.grid(row=4, column=2, pady=10)

# Run the application
root.mainloop()
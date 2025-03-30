import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class PathLossCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Path Loss Calculator")
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create frames for each model
        self.main_frame = ttk.Frame(self.notebook)
        self.hata_frame = ttk.Frame(self.notebook)
        self.cost231_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.main_frame, text="Main Menu")
        self.notebook.add(self.hata_frame, text="Hata Model")
        self.notebook.add(self.cost231_frame, text="COST231 Model")
        
        self.setup_main_menu()
        self.setup_hata_model()
        self.setup_cost231_model()

    def setup_main_menu(self):
        # Main menu setup
        title_label = ttk.Label(self.main_frame, 
                              text="Path Loss Calculator",
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)
        
        ttk.Label(self.main_frame, 
                 text="Select a model to calculate path loss:",
                 font=('Helvetica', 12)).pack(pady=10)
        
        ttk.Button(self.main_frame, 
                  text="Hata Model",
                  command=lambda: self.notebook.select(1)).pack(pady=5)
        
        ttk.Button(self.main_frame, 
                  text="COST231 Model",
                  command=lambda: self.notebook.select(2)).pack(pady=5)

    def setup_hata_model(self):
        # Hata model input frame
        input_frame = ttk.LabelFrame(self.hata_frame, text="Input Parameters")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Input fields
        self.hata_inputs = {}
        parameters = {
            'fc': 'Frequency (MHz)',
            'hte': 'Base Station Height (m)',
            'hre': 'Mobile Station Height (m)',
            'd': 'Distance (km)',
            'start_d': 'Start Distance (km)',
            'end_d': 'End Distance (km)'
        }
        
        for i, (key, label) in enumerate(parameters.items()):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=2)
            self.hata_inputs[key] = ttk.Entry(input_frame)
            self.hata_inputs[key].grid(row=i, column=1, padx=5, pady=2)
        
        # Area type selection
        ttk.Label(input_frame, text="Area Type:").grid(row=len(parameters), column=0, padx=5, pady=2)
        self.hata_area = ttk.Combobox(input_frame, 
                                    values=['Urban', 'Suburban', 'Rural'],
                                    state='readonly')
        self.hata_area.set('Urban')
        self.hata_area.grid(row=len(parameters), column=1, padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(self.hata_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, 
                  text="Calculate",
                  command=self.calculate_hata).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                  text="Plot",
                  command=self.plot_hata).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                  text="Clear",
                  command=lambda: self.clear_inputs('hata')).pack(side='left', padx=5)
        
        # Result display
        self.hata_result = ttk.Label(self.hata_frame, text="")
        self.hata_result.pack(pady=10)
        
        # Plot area
        self.hata_fig, self.hata_ax = plt.subplots(figsize=(6, 4))
        self.hata_canvas = FigureCanvasTkAgg(self.hata_fig, self.hata_frame)
        self.hata_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

    def setup_cost231_model(self):
        # COST231 model input frame
        input_frame = ttk.LabelFrame(self.cost231_frame, text="Input Parameters")
        input_frame.pack(fill='x', padx=10, pady=5)
        
        # Input fields
        self.cost231_inputs = {}
        parameters = {
            'fc': 'Frequency (MHz)',
            'hte': 'Base Station Height (m)',
            'hre': 'Mobile Station Height (m)',
            'd': 'Distance (km)',
            'start_d': 'Start Distance (km)',
            'end_d': 'End Distance (km)'
        }
        
        for i, (key, label) in enumerate(parameters.items()):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=2)
            self.cost231_inputs[key] = ttk.Entry(input_frame)
            self.cost231_inputs[key].grid(row=i, column=1, padx=5, pady=2)
        
        # Area type selection
        ttk.Label(input_frame, text="Area Type:").grid(row=len(parameters), column=0, padx=5, pady=2)
        self.cost231_area = ttk.Combobox(input_frame, 
                                       values=['Urban', 'Suburban', 'Rural'],
                                       state='readonly')
        self.cost231_area.set('Urban')
        self.cost231_area.grid(row=len(parameters), column=1, padx=5, pady=2)
        
        # Buttons
        button_frame = ttk.Frame(self.cost231_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, 
                  text="Calculate",
                  command=self.calculate_cost231).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                  text="Plot",
                  command=self.plot_cost231).pack(side='left', padx=5)
        
        ttk.Button(button_frame, 
                  text="Clear",
                  command=lambda: self.clear_inputs('cost231')).pack(side='left', padx=5)
        
        # Result display
        self.cost231_result = ttk.Label(self.cost231_frame, text="")
        self.cost231_result.pack(pady=10)
        
        # Plot area
        self.cost231_fig, self.cost231_ax = plt.subplots(figsize=(6, 4))
        self.cost231_canvas = FigureCanvasTkAgg(self.cost231_fig, self.cost231_frame)
        self.cost231_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

    def calculate_hata(self):
        try:
            fc = float(self.hata_inputs['fc'].get())
            hte = float(self.hata_inputs['hte'].get())
            hre = float(self.hata_inputs['hre'].get())
            d = float(self.hata_inputs['d'].get())
            area_type = self.hata_area.get().lower()
            
            # Calculate path loss using Hata model
            if area_type == 'urban':
                if fc <= 300:
                    ahm = (8.29 * (np.log10(1.54 * hre))**2) - 1.1
                else:
                    ahm = (3.2 * (np.log10(11.75 * hre))**2) - 4.97
            else:
                ahm = ((1.1 * np.log10(fc) - 0.7) * hre) - (1.56 * np.log10(fc) - 0.8)
            
            PL = 69.55 + (26.16 * np.log10(fc)) - (13.82 * np.log10(hte)) - ahm + \
                 (44.9 - 6.55 * np.log10(hte)) * np.log10(d)
            
            self.hata_result.config(text=f"Path Loss: {PL:.2f} dB")
        except ValueError:
            self.hata_result.config(text="Invalid input values")

    def calculate_cost231(self):
        try:
            fc = float(self.cost231_inputs['fc'].get())
            hte = float(self.cost231_inputs['hte'].get())
            hre = float(self.cost231_inputs['hre'].get())
            d = float(self.cost231_inputs['d'].get())
            area_type = self.cost231_area.get().lower()
            
            # Calculate path loss using COST231 model
            if area_type == 'urban':
                Cm = 3
            else:
                Cm = 0
                
            ahm = ((1.1 * np.log10(fc) - 0.7) * hre) - (1.56 * np.log10(fc) - 0.8)
            
            PL = 46.3 + (33.9 * np.log10(fc)) - (13.82 * np.log10(hte)) - ahm + \
                 (44.9 - 6.55 * np.log10(hte)) * np.log10(d) + Cm
            
            self.cost231_result.config(text=f"Path Loss: {PL:.2f} dB")
        except ValueError:
            self.cost231_result.config(text="Invalid input values")

    def plot_hata(self):
        try:
            fc = float(self.hata_inputs['fc'].get())
            hte = float(self.hata_inputs['hte'].get())
            hre = float(self.hata_inputs['hre'].get())
            start_d = float(self.hata_inputs['start_d'].get())
            end_d = float(self.hata_inputs['end_d'].get())
            area_type = self.hata_area.get().lower()
            
            distances = np.linspace(start_d, end_d, 100)
            path_losses = []
            
            for d in distances:
                if area_type == 'urban':
                    if fc <= 300:
                        ahm = (8.29 * (np.log10(1.54 * hre))**2) - 1.1
                    else:
                        ahm = (3.2 * (np.log10(11.75 * hre))**2) - 4.97
                else:
                    ahm = ((1.1 * np.log10(fc) - 0.7) * hre) - (1.56 * np.log10(fc) - 0.8)
                
                PL = 69.55 + (26.16 * np.log10(fc)) - (13.82 * np.log10(hte)) - ahm + \
                     (44.9 - 6.55 * np.log10(hte)) * np.log10(d)
                path_losses.append(PL)
            
            self.hata_ax.clear()
            self.hata_ax.plot(distances, path_losses)
            self.hata_ax.set_xlabel('Distance (km)')
            self.hata_ax.set_ylabel('Path Loss (dB)')
            self.hata_ax.set_title('Hata Model Path Loss vs Distance')
            self.hata_ax.grid(True)
            self.hata_canvas.draw()
        except ValueError:
            self.hata_result.config(text="Invalid input values for plotting")

    def plot_cost231(self):
        try:
            fc = float(self.cost231_inputs['fc'].get())
            hte = float(self.cost231_inputs['hte'].get())
            hre = float(self.cost231_inputs['hre'].get())
            start_d = float(self.cost231_inputs['start_d'].get())
            end_d = float(self.cost231_inputs['end_d'].get())
            area_type = self.cost231_area.get().lower()
            
            distances = np.linspace(start_d, end_d, 100)
            path_losses = []
            
            Cm = 3 if area_type == 'urban' else 0
            
            for d in distances:
                ahm = ((1.1 * np.log10(fc) - 0.7) * hre) - (1.56 * np.log10(fc) - 0.8)
                PL = 46.3 + (33.9 * np.log10(fc)) - (13.82 * np.log10(hte)) - ahm + \
                     (44.9 - 6.55 * np.log10(hte)) * np.log10(d) + Cm
                path_losses.append(PL)
            
            self.cost231_ax.clear()
            self.cost231_ax.plot(distances, path_losses)
            self.cost231_ax.set_xlabel('Distance (km)')
            self.cost231_ax.set_ylabel('Path Loss (dB)')
            self.cost231_ax.set_title('COST231 Model Path Loss vs Distance')
            self.cost231_ax.grid(True)
            self.cost231_canvas.draw()
        except ValueError:
            self.cost231_result.config(text="Invalid input values for plotting")

    def clear_inputs(self, model):
        if model == 'hata':
            for entry in self.hata_inputs.values():
                entry.delete(0, 'end')
            self.hata_result.config(text="")
            self.hata_ax.clear()
            self.hata_canvas.draw()
        else:
            for entry in self.cost231_inputs.values():
                entry.delete(0, 'end')
            self.cost231_result.config(text="")
            self.cost231_ax.clear()
            self.cost231_canvas.draw()

def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = PathLossCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
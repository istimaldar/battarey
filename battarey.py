import tkinter as tk
from tkinter import ttk
from time import sleep
import threading
import os


class MainWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.current_charge = 0
        self.status = ""
        self.statuses = {"Discharging": "Батарея не заряжается", "Charging": "Батарея заряжается",
                       "Full": "Батарея полна"}

        self.progress_frame = tk.Frame(self)
        self.progress_frame.pack(side=tk.TOP, expand=True, fill=tk.X)
        self.charge_label = tk.Label(self.progress_frame, text="Заряд батареи:")
        self.charge_label.pack(side=tk.LEFT)
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient = "horizontal",
                                            length = 200, mode = "determinate")
        self.progress_bar.pack(side=tk.LEFT)
        self.progress_bar["maximum"]= 1000
        self.progres_label = tk.Label(self.progress_frame)
        self.progres_label.pack(side=tk.LEFT)

        self.mode = tk.Label(self)
        self.mode.pack(side=tk.BOTTOM)

        self.update_thred = threading.Thread(target=self.update_thred_function)
        self.update_thred.daemon = True
        self.update_thred.start()
        self.mainloop()

    def update_thred_function(self):
        while True:
            self.update()
            sleep(1)

    def update(self):
        full_energy = int(open('/sys/class/power_supply/BAT0/energy_full', 'r').readline().rsplit()[0])
        current_energy = int(open('/sys/class/power_supply/BAT0/energy_now', 'r').readline().rsplit()[0])
        self.current_charge = current_energy * 100 // full_energy
        old_status = self.status
        self.status = open('/sys/class/power_supply/BAT0/status', 'r').readline().rsplit()[0]
        if self.status != old_status:
            self.adjust_brightness()
        self.progress_bar["value"] = self.current_charge * 10
        self.progres_label.config(text='{}%'.format(self.current_charge))
        self.mode.config(text="Статус батареи: {}".format(self.statuses[self.status]))

    def adjust_brightness(self):
        if self.status == "Discharging":
            os.system('xbacklight -set 10')
        else:
            os.system('xbacklight -set 50')

if __name__ == '__main__':
    MainWindow()
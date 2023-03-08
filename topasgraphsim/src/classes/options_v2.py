import customtkinter as ctk
import tkinter.filedialog as fd
from ..resources.language import Text

from ..classes.sim_import import Simulation

class Options(ctk.CTkTabview):
    
    """The options frame of the TGS application.
    """
    
    def __init__(self, parent, index, lang):
        
        self.parent = parent      
        self.index = index
        self.lang = lang  
        super().__init__(self.parent, width=200, border_color="black", border_width=1)
        
        self.newtabname = ""
        
        self.add(Text().data[self.lang])
        self.add(Text().settings[self.lang])
        self.add(Text().analysis[self.lang])
        
        self.load_topas_button = ctk.CTkButton(self.tab(Text().data[self.lang]), text = Text().loadsim[self.lang], command = self.load_topas, width=20)
        self.load_topas_button.pack(side="top", pady=5, padx=5, fill="x")
        self.change_name_button = ctk.CTkButton(self.tab(Text().data[self.lang]), text=Text().edittabname[self.lang], command = self.change_name, width=20)
        self.close_tab_button = ctk.CTkButton(self.tab(Text().data[self.lang]), text=Text().closetab1[self.lang], command = lambda: self.parent.master.master.remove_tab(self.parent.master.master.tabnames.index(self.parent.name)), fg_color="red")
        self.close_tab_button.pack(side="bottom", pady=5, padx=5, fill="x")
        self.change_name_button.pack(side="bottom", pady=5, padx=5)
        
    def load_topas(self):
        path = fd.askopenfilename(filetypes=[("TOPAS files", "*.csv")])
        
        if path != "":
            sim = Simulation(path)
            
            self.parent.ax.plot(sim.axis, sim.dose)
            self.parent.canvas.draw()
            
    def change_name(self):
        
        
        """Add a tab to the tabview.
        """
        root = self.parent.master.master.parent        
        window = ctk.CTkToplevel(root)
        window.wm_attributes("-toolwindow", True)
        window.geometry(f"180x120+{root.winfo_rootx()+root.winfo_width()//2-90}+{root.winfo_rooty()+root.winfo_height()//2-60}")
        window.title("")
        
        def move(event):
            window.lift()
            entry.focus()
            window.geometry(f"180x120+{root.winfo_rootx()+root.winfo_width()//2-90}+{root.winfo_rooty()+root.winfo_height()//2-60}")
        
        def submit():
            self.newtabname = entry.get()
            window.destroy()
            if self.newtabname == "":
                return
     
            tab = self.newtabname
            self.newtabname = ""
            self.parent.master.master._current_name = tab
            
            self.parent.master.master.parent.parent.menubar.tabmenu.entryconfig(self.index+2, label=Text().closetab[self.lang].format(tab), 
                command = lambda: self.parent.master.master.remove_tab(self.index))
                                                                                
            frame = self.parent.master.master._tab_dict[self.parent.master.master._name_list[self.index]]
            self.parent.master.master._tab_dict.pop(self.parent.master.master._name_list[self.index])
            self.parent.master.master._tab_dict[tab] = frame
            self.parent.master.master._name_list[self.index] = tab
            self.parent.master.master._segmented_button._value_list[self.index] = tab
            button = self.parent.master.master._segmented_button._buttons_dict[self.parent.master.master.tabnames[self.index]]
            button.configure(text=tab)
            self.parent.master.master._segmented_button._buttons_dict.pop(self.parent.master.master.tabnames[self.index])
            self.parent.master.master._segmented_button._buttons_dict[tab] = button
            self.parent.master.master.tabnames[self.index] = tab
            self.parent.name = tab
            values = self.parent.master.master._segmented_button.cget("values")
            values[self.index] = tab
            self.parent.master.master._segmented_button.configure(values=values)
            self.parent.master.master._configure_tab_background_corners_by_name(tab)
            self.parent.master.master._segmented_button.set(tab)
            self.parent.master.master._draw()
            return
        
        textlabel = ctk.CTkLabel(window, text=Text().newtabname[self.lang], font=("Bahnschrift", 16))
        textlabel.pack(padx=5, pady=5, fill="x", expand=True)
        entry = ctk.CTkEntry(window, takefocus=True)
        submitbutton = ctk.CTkButton(window, text="OK", command=submit, width=30, font=("Bahnschrift", 12))
        entry.pack(fill="x", expand=True, padx=5, pady=5)
        submitbutton.pack(padx=5, pady=5)
        entry.focus()
        window.bind("<Configure>", move)
        window.bind("<Escape>", lambda event: window.destroy())
        window.bind("<Return>", lambda event: submit())
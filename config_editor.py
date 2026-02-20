import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class AppConfigEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("AppForge - Config Editor")
        self.root.geometry("560x580")
        self.root.minsize(560, 580)
        self.root.resizable(False, False)
        
        self.config_path = "app.config.json"
        self.config = {}
        
        self.default_permissions = [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.CAMERA",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.RECORD_AUDIO",
            "android.permission.READ_CONTACTS",
            "android.permission.WRITE_CONTACTS",
            "android.permission.VIBRATE",
            "android.permission.FOREGROUND_SERVICE",
            "android.permission.RECEIVE_BOOT_COMPLETED",
            "android.permission.SCHEDULE_EXACT_ALARM",
            "android.permission.READ_PHONE_STATE",
            "android.permission.BLUETOOTH",
            "android.permission.NFC",
        ]
        
        self.permission_vars = {}
        self.custom_permissions = []
        self.deep_link_paths = []
        
        self.compile_var = tk.BooleanVar(value=True)
        self.emulator_var = tk.BooleanVar(value=False)
        self.deeplinks_enabled_var = tk.BooleanVar(value=False)
        
        self.style_widgets()
        self.create_widgets()
        self.load_config()
    
    def style_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background='#f5f5f5')
        style.configure('TNotebook.Tab', padding=[12, 4], font=('Segoe UI', 9))
        style.map('TNotebook.Tab', background=[('selected', '#fff')])
        
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 9))
        style.configure('TButton', font=('Segoe UI', 9), padding=[10, 5])
        style.configure('TCheckbutton', background='#f5f5f5', font=('Segoe UI', 9))
        style.configure('TLabelframe', background='#f5f5f5')
        style.configure('TLabelframe.Label', background='#f5f5f5', font=('Segoe UI', 9, 'bold'))
        
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2196F3')
        style.configure('Subheader.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#333')
        style.configure('Info.TLabel', foreground='#666', font=('Segoe UI', 8))
        style.configure('Success.TLabel', foreground='#4CAF50', font=('Segoe UI', 8))
        style.configure('Warning.TLabel', foreground='#FF9800', font=('Segoe UI', 8))
        style.configure('Path.TLabel', foreground='#1976D2', font=('Segoe UI', 8))
        
        style.configure('Small.TButton', font=('Segoe UI', 8), padding=[5, 2])
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(header, text="AppForge", style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Label(header, text="Config Editor", style='Info.TLabel').pack(side=tk.LEFT, padx=(8, 0), pady=(6, 0))
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_app_tab()
        self.create_permissions_tab()
        self.create_build_tab()
        self.create_deeplinks_tab()
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        
        ttk.Button(btn_frame, text="Cargar", command=self.open_file, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Guardar", command=self.save_config, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="+ Version", command=self.increment_version, width=10).pack(side=tk.LEFT, padx=2)
        
        self.status_var = tk.StringVar(value="Listo")
        ttk.Label(main_frame, textvariable=self.status_var, style='Info.TLabel').pack(pady=(5, 0))
    
    def create_app_tab(self):
        frame = ttk.Frame(self.notebook, padding="8")
        self.notebook.add(frame, text="App")
        
        ttk.Label(frame, text="Identificacion", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        self.app_id = self.create_field(frame, "App ID:", "com.empresa.miapp")
        self.app_name = self.create_field(frame, "Nombre:", "Mi App")
        
        vf = ttk.Frame(frame)
        vf.pack(fill=tk.X, pady=3)
        ttk.Label(vf, text="Version:", width=12, anchor=tk.W).pack(side=tk.LEFT, padx=(5, 0))
        self.version = ttk.Entry(vf, width=15)
        self.version.pack(side=tk.LEFT, padx=(5, 0))
        self.version.insert(0, "1.0.0")
        ttk.Label(vf, text="Code:", style='Info.TLabel').pack(side=tk.LEFT, padx=(15, 0))
        self.version_code = ttk.Entry(vf, width=6)
        self.version_code.pack(side=tk.LEFT, padx=(5, 0))
        self.version_code.insert(0, "1")
        
        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=8)
        ttk.Label(frame, text="Android SDK", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        self.min_sdk = self.create_field(frame, "Min SDK:", "24", 10)
        self.target_sdk = self.create_field(frame, "Target SDK:", "34", 10)
        
        info = ttk.Frame(frame)
        info.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(info, text="SDK 24 = Android 7.0  |  SDK 34 = Android 14", style='Info.TLabel').pack(anchor=tk.W)
    
    def create_permissions_tab(self):
        frame = ttk.Frame(self.notebook, padding="8")
        self.notebook.add(frame, text="Permisos")
        
        ttk.Label(frame, text="Permisos de Android", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        btn_row = ttk.Frame(frame)
        btn_row.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_row, text="Todos", command=self.select_all_perms, style='Small.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="Ninguno", command=self.deselect_all_perms, style='Small.TButton').pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="Comunes", command=self.select_common_perms, style='Small.TButton').pack(side=tk.LEFT, padx=2)
        
        perms_container = ttk.Frame(frame)
        perms_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(perms_container, bg='#f5f5f5', highlightthickness=0, height=140)
        scrollbar = ttk.Scrollbar(perms_container, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for perm in self.default_permissions:
            name = perm.replace("android.permission.", "")
            var = tk.BooleanVar(value=False)
            self.permission_vars[perm] = var
            
            row = ttk.Frame(scrollable)
            row.pack(fill=tk.X, pady=1)
            ttk.Checkbutton(row, variable=var).pack(side=tk.LEFT)
            ttk.Label(row, text=name, width=22, anchor=tk.W).pack(side=tk.LEFT, padx=(5, 0))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=6)
        
        custom_frame = ttk.LabelFrame(frame, text="Personalizados", padding="5")
        custom_frame.pack(fill=tk.X)
        
        custom_input = ttk.Frame(custom_frame)
        custom_input.pack(fill=tk.X)
        
        ttk.Label(custom_input, text="Nuevo:", width=8, anchor=tk.W).pack(side=tk.LEFT)
        self.custom_perm_entry = ttk.Entry(custom_input, width=30)
        self.custom_perm_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.custom_perm_entry.insert(0, "android.permission.")
        ttk.Button(custom_input, text="+", command=self.add_custom_permission, style='Small.TButton').pack(side=tk.LEFT, padx=5)
        
        self.custom_perms_list = ttk.Frame(custom_frame)
        self.custom_perms_list.pack(fill=tk.X, pady=(5, 0))
    
    def create_build_tab(self):
        frame = ttk.Frame(self.notebook, padding="8")
        self.notebook.add(frame, text="Build")
        
        ttk.Label(frame, text="Opciones de Compilacion", style='Subheader.TLabel').pack(anchor=tk.W, pady=(0, 6))
        
        compile_card = ttk.LabelFrame(frame, text="Compilacion", padding="6")
        compile_card.pack(fill=tk.X, pady=3)
        
        ttk.Checkbutton(compile_card, text="Compilar automaticamente", variable=self.compile_var).pack(anchor=tk.W)
        ttk.Label(compile_card, text="Genera APK en cada push", style='Info.TLabel').pack(anchor=tk.W)
        
        emulator_card = ttk.LabelFrame(frame, text="Emulador", padding="6")
        emulator_card.pack(fill=tk.X, pady=3)
        
        ttk.Checkbutton(emulator_card, text="Ejecutar en emulador", variable=self.emulator_var).pack(anchor=tk.W)
        ttk.Label(emulator_card, text="Instala APK y toma 3 capturas", style='Info.TLabel').pack(anchor=tk.W)
        ttk.Label(emulator_card, text="+10-15 min de build", style='Warning.TLabel').pack(anchor=tk.W)
        
        keywords_card = ttk.LabelFrame(frame, text="Keywords", padding="6")
        keywords_card.pack(fill=tk.X, pady=3)
        
        ttk.Label(keywords_card, text="[compile] [compilar] [build] - Fuerza build", style='Success.TLabel').pack(anchor=tk.W)
        ttk.Label(keywords_card, text="[skip] [noc] - Salta build", style='Warning.TLabel').pack(anchor=tk.W)
    
    def create_deeplinks_tab(self):
        frame = ttk.Frame(self.notebook, padding="8")
        self.notebook.add(frame, text="Deep Links")
        
        ttk.Checkbutton(frame, text="Habilitar Deep Links", variable=self.deeplinks_enabled_var).pack(anchor=tk.W, pady=(0, 6))
        
        config_card = ttk.LabelFrame(frame, text="Configuracion", padding="6")
        config_card.pack(fill=tk.X, pady=3)
        
        self.dl_scheme = self.create_field(config_card, "Scheme:", "miapp")
        self.dl_host = self.create_field(config_card, "Host:", "miapp.com")
        
        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=6)
        
        paths_card = ttk.LabelFrame(frame, text="Rutas (Paths)", padding="6")
        paths_card.pack(fill=tk.X, pady=3)
        
        path_input = ttk.Frame(paths_card)
        path_input.pack(fill=tk.X)
        
        ttk.Label(path_input, text="Path:", width=8, anchor=tk.W).pack(side=tk.LEFT)
        self.path_entry = ttk.Entry(path_input, width=22)
        self.path_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.path_entry.insert(0, "/producto/:id")
        ttk.Button(path_input, text="+", command=self.add_path, style='Small.TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(path_input, text="Ejs", command=self.show_path_examples, style='Small.TButton').pack(side=tk.LEFT, padx=2)
        
        self.paths_list_frame = ttk.Frame(paths_card)
        self.paths_list_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=6)
        
        examples_card = ttk.LabelFrame(frame, text="Ejemplos", padding="6")
        examples_card.pack(fill=tk.X, pady=3)
        
        ttk.Label(examples_card, text="miapp://producto/123", style='Path.TLabel').pack(anchor=tk.W)
        ttk.Label(examples_card, text="https://miapp.com/usuario/juan", style='Path.TLabel').pack(anchor=tk.W)
    
    def create_field(self, parent, label, placeholder, width=30):
        f = ttk.Frame(parent)
        f.pack(fill=tk.X, pady=2)
        ttk.Label(f, text=label, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=(5, 0))
        entry = ttk.Entry(f, width=width)
        entry.pack(side=tk.LEFT, padx=(5, 0))
        entry.insert(0, placeholder)
        return entry
    
    def add_custom_permission(self):
        perm = self.custom_perm_entry.get().strip()
        if perm and perm not in self.custom_permissions and perm != "android.permission.":
            self.custom_permissions.append(perm)
            self.refresh_custom_perms_list()
            self.custom_perm_entry.delete(0, tk.END)
            self.custom_perm_entry.insert(0, "android.permission.")
    
    def remove_custom_permission(self, perm):
        if perm in self.custom_permissions:
            self.custom_permissions.remove(perm)
            self.refresh_custom_perms_list()
    
    def refresh_custom_perms_list(self):
        for widget in self.custom_perms_list.winfo_children():
            widget.destroy()
        
        if self.custom_permissions:
            ttk.Label(self.custom_perms_list, text="Agregados:", style='Info.TLabel').pack(anchor=tk.W)
            for perm in self.custom_permissions:
                row = ttk.Frame(self.custom_perms_list)
                row.pack(fill=tk.X, pady=2)
                ttk.Label(row, text=perm, style='Success.TLabel').pack(side=tk.LEFT)
                ttk.Button(row, text="x", command=lambda p=perm: self.remove_custom_permission(p), style='Small.TButton', width=3).pack(side=tk.RIGHT)
    
    def add_path(self):
        path = self.path_entry.get().strip()
        if path and path not in self.deep_link_paths:
            self.deep_link_paths.append(path)
            self.refresh_paths_list()
    
    def remove_path(self, path):
        if path in self.deep_link_paths:
            self.deep_link_paths.remove(path)
            self.refresh_paths_list()
    
    def refresh_paths_list(self):
        for widget in self.paths_list_frame.winfo_children():
            widget.destroy()
        
        if self.deep_link_paths:
            ttk.Label(self.paths_list_frame, text="Rutas configuradas:", style='Info.TLabel').pack(anchor=tk.W)
            for path in self.deep_link_paths:
                row = ttk.Frame(self.paths_list_frame)
                row.pack(fill=tk.X, pady=2)
                ttk.Label(row, text=path, style='Path.TLabel').pack(side=tk.LEFT)
                ttk.Button(row, text="x", command=lambda p=path: self.remove_path(p), style='Small.TButton', width=3).pack(side=tk.RIGHT)
    
    def show_path_examples(self):
        examples = [
            "/producto/:id",
            "/usuario/:username",
            "/categoria/:cat/producto/:id",
            "/promo/:codigo",
            "/configuracion",
            "/reset-password",
            "/verify-email"
        ]
        
        win = tk.Toplevel(self.root)
        win.title("Ejemplos de Paths")
        win.geometry("320x280")
        win.transient(self.root)
        
        ttk.Label(win, text="Ejemplos:", style='Subheader.TLabel').pack(anchor=tk.W, padx=10, pady=10)
        
        for ex in examples:
            row = ttk.Frame(win)
            row.pack(fill=tk.X, padx=10, pady=2)
            ttk.Label(row, text=ex, style='Path.TLabel').pack(side=tk.LEFT)
            ttk.Button(row, text="Usar", command=lambda e=ex: self.use_example_path(e, win), style='Small.TButton').pack(side=tk.RIGHT)
    
    def use_example_path(self, path, win):
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)
        win.destroy()
    
    def select_all_perms(self):
        for var in self.permission_vars.values():
            var.set(True)
    
    def deselect_all_perms(self):
        for var in self.permission_vars.values():
            var.set(False)
    
    def select_common_perms(self):
        self.deselect_all_perms()
        common = [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.CAMERA",
        ]
        for perm in common:
            if perm in self.permission_vars:
                self.permission_vars[perm].set(True)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="app.config.json"
        )
        if file_path:
            self.config_path = file_path
            self.load_config()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                
                self.app_id.delete(0, tk.END)
                self.app_id.insert(0, self.config.get('appId', ''))
                
                self.app_name.delete(0, tk.END)
                self.app_name.insert(0, self.config.get('appName', ''))
                
                self.version.delete(0, tk.END)
                self.version.insert(0, self.config.get('version', ''))
                
                self.version_code.delete(0, tk.END)
                self.version_code.insert(0, str(self.config.get('versionCode', 1)))
                
                android = self.config.get('android', {})
                self.min_sdk.delete(0, tk.END)
                self.min_sdk.insert(0, str(android.get('minSdkVersion', 24)))
                
                self.target_sdk.delete(0, tk.END)
                self.target_sdk.insert(0, str(android.get('targetSdkVersion', 34)))
                
                permissions = android.get('permissions', [])
                for perm in self.permission_vars:
                    self.permission_vars[perm].set(perm in permissions)
                
                self.custom_permissions = [p for p in permissions if p not in self.permission_vars]
                self.refresh_custom_perms_list()
                
                build = self.config.get('build', {})
                self.compile_var.set(build.get('compile', True))
                self.emulator_var.set(build.get('emulator', False))
                
                deeplinks = self.config.get('deepLinks', {})
                self.deeplinks_enabled_var.set(deeplinks.get('enabled', False))
                
                self.dl_scheme.delete(0, tk.END)
                self.dl_scheme.insert(0, deeplinks.get('scheme', 'miapp'))
                
                self.dl_host.delete(0, tk.END)
                self.dl_host.insert(0, deeplinks.get('host', ''))
                
                self.deep_link_paths = deeplinks.get('paths', [])
                self.refresh_paths_list()
                
                self.status_var.set(f"Cargado")
            else:
                messagebox.showwarning("Aviso", f"No existe {self.config_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar: {str(e)}")
    
    def save_config(self):
        try:
            permissions = [perm for perm, var in self.permission_vars.items() if var.get()]
            permissions.extend(self.custom_permissions)
            
            config = {
                "appId": self.app_id.get().strip(),
                "appName": self.app_name.get().strip(),
                "version": self.version.get().strip(),
                "versionCode": int(self.version_code.get().strip() or "1"),
                "description": self.config.get('description', ''),
                "author": self.config.get('author', {"name": "", "email": "", "url": ""}),
                "android": {
                    "minSdkVersion": int(self.min_sdk.get().strip() or "24"),
                    "targetSdkVersion": int(self.target_sdk.get().strip() or "34"),
                    "compileSdkVersion": int(self.target_sdk.get().strip() or "34"),
                    "permissions": permissions
                },
                "deepLinks": {
                    "enabled": self.deeplinks_enabled_var.get(),
                    "scheme": self.dl_scheme.get().strip(),
                    "host": self.dl_host.get().strip(),
                    "paths": self.deep_link_paths
                },
                "build": {
                    "compile": self.compile_var.get(),
                    "emulator": self.emulator_var.get()
                }
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.status_var.set("Guardado")
            messagebox.showinfo("OK", "Configuracion guardada")
        except ValueError:
            messagebox.showerror("Error", "Version Code y SDK deben ser numeros")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def increment_version(self):
        try:
            version = self.version.get().strip()
            parts = version.split('.')
            
            if len(parts) >= 3:
                parts[2] = str(int(parts[2]) + 1)
                new_version = '.'.join(parts)
                
                self.version.delete(0, tk.END)
                self.version.insert(0, new_version)
                
                current_code = int(self.version_code.get().strip() or "1")
                self.version_code.delete(0, tk.END)
                self.version_code.insert(0, str(current_code + 1))
                
                self.status_var.set(f"v{new_version}")
            else:
                messagebox.showwarning("Formato", "La version debe ser x.x.x")
        except ValueError:
            messagebox.showerror("Error", "No se pudo incrementar")

def main():
    root = tk.Tk()
    AppConfigEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

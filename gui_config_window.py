import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from gui_config import GUIConfig
from gui_snipe_client import GUISnipeITClient

class ConfigWindow:
    """Ventana de configuración de Snipe IT"""
    
    def __init__(self, parent=None, on_success_callback=None):
        self.parent = parent
        self.on_success_callback = on_success_callback
        self.config = GUIConfig()
        self.client = GUISnipeITClient(self.config)
        
        # Crear ventana
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.load_existing_config()
    
    def setup_window(self):
        """Configurar ventana principal"""
        self.window.title("Configuración - Snipe IT PDF Generator")
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
        
        # Hacer ventana modal si tiene padre
        if self.parent:
            self.window.transient(self.parent)
            self.window.grab_set()
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Configuración de Snipe IT", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Descripción
        desc_text = ("Configure la conexión a su servidor Snipe IT.\n"
                    "Necesitará la URL del servidor y un token de API válido.")
        desc_label = ttk.Label(main_frame, text=desc_text, justify=tk.CENTER)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # URL del servidor
        ttk.Label(main_frame, text="URL del servidor Snipe IT:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(
            main_frame, 
            textvariable=self.url_var, 
            font=("Arial", 10),
            width=50
        )
        url_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Ejemplo de URL
        url_example = ttk.Label(
            main_frame, 
            text="Ejemplo: https://assets.miempresa.com", 
            font=("Arial", 8),
            foreground="gray"
        )
        url_example.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # API Token
        ttk.Label(main_frame, text="Token de API:").grid(
            row=5, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.token_var = tk.StringVar()
        token_entry = ttk.Entry(
            main_frame, 
            textvariable=self.token_var, 
            font=("Arial", 10),
            show="*",
            width=50
        )
        token_entry.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Checkbox para mostrar/ocultar token
        self.show_token_var = tk.BooleanVar()
        show_token_cb = ttk.Checkbutton(
            main_frame,
            text="Mostrar token",
            variable=self.show_token_var,
            command=lambda: token_entry.config(show="" if self.show_token_var.get() else "*")
        )
        show_token_cb.grid(row=7, column=0, sticky=tk.W, pady=(0, 15))
        
        # Link para obtener API Token
        help_frame = ttk.Frame(main_frame)
        help_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        help_frame.columnconfigure(1, weight=1)
        
        ttk.Label(help_frame, text="¿Cómo obtener el token de API?").grid(
            row=0, column=0, sticky=tk.W
        )
        
        help_link = ttk.Label(
            help_frame, 
            text="Haga clic aquí para ver las instrucciones",
            foreground="blue",
            cursor="hand2",
            font=("Arial", 9, "underline")
        )
        help_link.grid(row=0, column=1, sticky=tk.E)
        help_link.bind("<Button-1>", self.open_help)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=(20, 0))
        
        # Botón probar conexión
        self.test_btn = ttk.Button(
            button_frame,
            text="Probar Conexión",
            command=self.test_connection
        )
        self.test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón guardar
        self.save_btn = ttk.Button(
            button_frame,
            text="Guardar Configuración",
            command=self.save_config,
            style="Accent.TButton"
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón cancelar
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.cancel
        )
        cancel_btn.pack(side=tk.LEFT)
        
        # Frame para status
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.grid(row=10, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E))
        self.status_frame.columnconfigure(0, weight=1)
        
        # Label de status (inicialmente oculto)
        self.status_label = ttk.Label(
            self.status_frame,
            text="",
            font=("Arial", 9),
            justify=tk.CENTER
        )
        
        # Progress bar (inicialmente oculta)
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            mode='indeterminate'
        )
    
    def load_existing_config(self):
        """Cargar configuración existente si existe"""
        if self.config.is_configured():
            self.url_var.set(self.config.get_snipe_url())
            self.token_var.set(self.config.get_api_token())
    
    def open_help(self, event):
        """Abrir ayuda para obtener API Token"""
        help_text = """Para obtener un token de API en Snipe IT:

1. Inicie sesión en su instalación de Snipe IT
2. Vaya a Account Settings (Configuración de cuenta)
3. Haga clic en la pestaña "API Keys"
4. Haga clic en "Create New Token"
5. Déle un nombre al token (ej: "PDF Generator")
6. Copie el token generado y péguelo en este campo

Nota: El token debe tener permisos de lectura para usuarios y activos."""
        
        messagebox.showinfo("Obtener Token de API", help_text)
    
    def show_status(self, message, is_error=False):
        """Mostrar mensaje de status"""
        self.status_label.config(
            text=message,
            foreground="red" if is_error else "green"
        )
        self.status_label.grid(row=0, column=0, pady=(10, 0))
    
    def hide_status(self):
        """Ocultar mensaje de status"""
        self.status_label.grid_remove()
    
    def show_progress(self):
        """Mostrar barra de progreso"""
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.progress_bar.start()
    
    def hide_progress(self):
        """Ocultar barra de progreso"""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
    
    def test_connection(self):
        """Probar conexión con Snipe IT"""
        url = self.url_var.get().strip()
        token = self.token_var.get().strip()
        
        if not url or not token:
            self.show_status("Por favor complete todos los campos", is_error=True)
            return
        
        # Validar URL básica
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
            self.url_var.set(url)
        
        # Deshabilitar botones durante la prueba
        self.test_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        
        # Mostrar progreso
        self.show_progress()
        self.hide_status()
        
        # Actualizar config temporalmente para probar
        temp_config = GUIConfig()
        temp_config.save_config(url, token)
        temp_client = GUISnipeITClient(temp_config)
        
        # Probar conexión en hilo separado para no bloquear UI
        self.window.after(100, lambda: self._test_connection_worker(temp_client))
    
    def _test_connection_worker(self, client):
        """Worker para probar conexión"""
        try:
            result = client.test_connection()
            
            # Ocultar progreso
            self.hide_progress()
            
            if result['success']:
                user = result.get('user', {})
                username = user.get('username', 'Usuario')
                self.show_status(f"✓ Conexión exitosa. Conectado como: {username}")
            else:
                self.show_status(f"✗ {result['error']}", is_error=True)
        
        except Exception as e:
            self.hide_progress()
            self.show_status(f"✗ Error inesperado: {str(e)}", is_error=True)
        
        finally:
            # Rehabilitar botones
            self.test_btn.config(state='normal')
            self.save_btn.config(state='normal')
    
    def save_config(self):
        """Guardar configuración"""
        url = self.url_var.get().strip()
        token = self.token_var.get().strip()
        
        if not url or not token:
            self.show_status("Por favor complete todos los campos", is_error=True)
            return
        
        # Validar URL básica
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        # Guardar configuración
        if self.config.save_config(url, token):
            self.show_status("✓ Configuración guardada exitosamente")
            
            # Llamar callback si existe
            if self.on_success_callback:
                self.window.after(1500, lambda: [
                    self.on_success_callback(),
                    self.window.destroy() if self.parent else None
                ])
            else:
                messagebox.showinfo(
                    "Configuración guardada",
                    "La configuración se ha guardado correctamente.\n"
                    "Ahora puede usar la aplicación."
                )
        else:
            self.show_status("✗ Error al guardar la configuración", is_error=True)
    
    def cancel(self):
        """Cancelar configuración"""
        if self.parent:
            self.window.destroy()
        else:
            self.window.quit()
    
    def run(self):
        """Ejecutar ventana principal (solo si no tiene padre)"""
        if not self.parent:
            self.window.mainloop()

if __name__ == "__main__":
    # Ejecutar ventana de configuración standalone
    config_window = ConfigWindow()
    config_window.run()
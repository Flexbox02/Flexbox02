import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
import os

from gui_config import GUIConfig
from gui_snipe_client import GUISnipeITClient
from gui_config_window import ConfigWindow
from pdf_generator import ITResourcesPDFGenerator

class MainGUI:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.config = GUIConfig()
        self.client = GUISnipeITClient(self.config)
        self.pdf_generator = ITResourcesPDFGenerator()
        
        # Variables para datos del usuario actual
        self.current_user_data = None
        self.current_assets_data = None
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
        # Verificar configuración al inicio
        self.check_initial_config()
    
    def setup_window(self):
        """Configurar ventana principal"""
        self.root.title("Snipe IT - Generador de Reportes PDF")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
        
        # Icono (si existe)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def create_widgets(self):
        """Crear widgets de la interfaz"""
        # Menú
        self.create_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título y info de conexión
        self.create_header(main_frame)
        
        # Sección de búsqueda
        self.create_search_section(main_frame)
        
        # Sección de resultados
        self.create_results_section(main_frame)
        
        # Barra de estado
        self.create_status_bar(main_frame)
    
    def create_menu(self):
        """Crear menú de la aplicación"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Configuración...", command=self.open_config)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de...", command=self.show_about)
    
    def create_header(self, parent):
        """Crear sección de encabezado"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text="Generador de Reportes PDF - Snipe IT",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Status de conexión
        ttk.Label(header_frame, text="Estado:").grid(row=1, column=0, sticky=tk.W)
        
        self.connection_status = ttk.Label(
            header_frame,
            text="No configurado",
            foreground="red"
        )
        self.connection_status.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Botón configurar
        self.config_btn = ttk.Button(
            header_frame,
            text="Configurar",
            command=self.open_config
        )
        self.config_btn.grid(row=1, column=2, padx=(10, 0))
    
    def create_search_section(self, parent):
        """Crear sección de búsqueda"""
        search_frame = ttk.LabelFrame(parent, text="Buscar Usuario", padding="15")
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        # Email
        ttk.Label(search_frame, text="Correo electrónico:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(
            search_frame,
            textvariable=self.email_var,
            font=("Arial", 11),
            width=40
        )
        self.email_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self.email_entry.bind('<Return>', lambda e: self.search_user())
        
        # Botones
        button_frame = ttk.Frame(search_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        self.search_btn = ttk.Button(
            button_frame,
            text="Buscar Usuario",
            command=self.search_user,
            style="Accent.TButton"
        )
        self.search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="Limpiar",
            command=self.clear_search
        )
        self.clear_btn.pack(side=tk.LEFT)
    
    def create_results_section(self, parent):
        """Crear sección de resultados"""
        self.results_frame = ttk.LabelFrame(parent, text="Resultados", padding="15")
        self.results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1)
        
        # Info del usuario
        self.user_info_frame = ttk.Frame(self.results_frame)
        self.user_info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.user_info_frame.columnconfigure(1, weight=1)
        
        # Inicialmente oculto
        self.user_info_frame.grid_remove()
        
        # Tabla de activos
        self.create_assets_table()
        
        # Frame para acciones
        self.actions_frame = ttk.Frame(self.results_frame)
        self.actions_frame.grid(row=2, column=0, pady=(10, 0))
        
        self.generate_pdf_btn = ttk.Button(
            self.actions_frame,
            text="Generar Reporte PDF",
            command=self.generate_pdf,
            style="Accent.TButton"
        )
        self.generate_pdf_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_csv_btn = ttk.Button(
            self.actions_frame,
            text="Exportar CSV",
            command=self.export_csv
        )
        self.export_csv_btn.pack(side=tk.LEFT)
        
        # Inicialmente deshabilitados
        self.generate_pdf_btn.config(state='disabled')
        self.export_csv_btn.config(state='disabled')
    
    def create_assets_table(self):
        """Crear tabla de activos"""
        # Frame para tabla con scrollbar
        table_frame = ttk.Frame(self.results_frame)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview
        columns = ('tipo', 'nombre', 'modelo', 'serie', 'tag', 'estado', 'ubicacion')
        self.assets_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.assets_tree.heading('tipo', text='Tipo')
        self.assets_tree.heading('nombre', text='Nombre')
        self.assets_tree.heading('modelo', text='Modelo')
        self.assets_tree.heading('serie', text='Serie')
        self.assets_tree.heading('tag', text='Tag/Código')
        self.assets_tree.heading('estado', text='Estado')
        self.assets_tree.heading('ubicacion', text='Ubicación')
        
        # Configurar ancho de columnas
        self.assets_tree.column('tipo', width=80, minwidth=60)
        self.assets_tree.column('nombre', width=150, minwidth=100)
        self.assets_tree.column('modelo', width=150, minwidth=100)
        self.assets_tree.column('serie', width=120, minwidth=80)
        self.assets_tree.column('tag', width=100, minwidth=70)
        self.assets_tree.column('estado', width=100, minwidth=70)
        self.assets_tree.column('ubicacion', width=120, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.assets_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.assets_tree.xview)
        self.assets_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid
        self.assets_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_status_bar(self, parent):
        """Crear barra de estado"""
        self.status_frame = ttk.Frame(parent)
        self.status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        self.status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Listo",
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="5"
        )
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            mode='indeterminate'
        )
    
    def check_initial_config(self):
        """Verificar configuración inicial"""
        if self.config.is_configured():
            self.update_connection_status()
        else:
            self.connection_status.config(text="No configurado", foreground="red")
    
    def update_connection_status(self):
        """Actualizar estado de conexión"""
        if not self.config.is_configured():
            self.connection_status.config(text="No configurado", foreground="red")
            return
        
        url = self.config.get_snipe_url()
        self.connection_status.config(text=f"Conectado a {url}", foreground="green")
        
        # Actualizar cliente
        self.client._update_config()
    
    def open_config(self):
        """Abrir ventana de configuración"""
        ConfigWindow(self.root, self.update_connection_status)
    
    def show_about(self):
        """Mostrar información sobre la aplicación"""
        about_text = """Snipe IT - Generador de Reportes PDF

Versión: 1.0.0

Esta aplicación permite generar reportes PDF de los activos
asignados a usuarios en Snipe IT.

Desarrollado para la gestión eficiente de recursos informáticos.

© 2024"""
        messagebox.showinfo("Acerca de", about_text)
    
    def set_status(self, message):
        """Establecer mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def show_progress(self):
        """Mostrar barra de progreso"""
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        self.progress_bar.start()
    
    def hide_progress(self):
        """Ocultar barra de progreso"""
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
    
    def search_user(self):
        """Buscar usuario por email"""
        email = self.email_var.get().strip()
        
        if not email:
            messagebox.showwarning("Email requerido", "Por favor ingrese un correo electrónico")
            return
        
        if not self.config.is_configured():
            messagebox.showwarning("Configuración requerida", "Por favor configure la conexión a Snipe IT primero")
            self.open_config()
            return
        
        # Deshabilitar interfaz durante búsqueda
        self.search_btn.config(state='disabled')
        self.email_entry.config(state='disabled')
        self.show_progress()
        self.set_status(f"Buscando usuario: {email}...")
        
        # Ejecutar búsqueda en hilo separado
        threading.Thread(target=self._search_user_worker, args=(email,), daemon=True).start()
    
    def _search_user_worker(self, email):
        """Worker para búsqueda de usuario"""
        try:
            # Obtener datos completos del usuario
            result = self.client.get_user_complete_data(email)
            
            # Volver al hilo principal
            self.root.after(0, self._handle_search_result, result)
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
            self.root.after(0, self._handle_search_result, error_result)
    
    def _handle_search_result(self, result):
        """Manejar resultado de búsqueda"""
        # Rehabilitar interfaz
        self.search_btn.config(state='normal')
        self.email_entry.config(state='normal')
        self.hide_progress()
        
        if result['success']:
            self.current_user_data = result
            self.display_user_data(result)
            self.set_status(f"Usuario encontrado. {len(result['assets'])} activos asignados.")
        else:
            self.clear_results()
            self.set_status("Usuario no encontrado")
            messagebox.showerror("Error", result['error'])
    
    def display_user_data(self, data):
        """Mostrar datos del usuario y sus activos"""
        user = data['user']
        assets = data['assets']
        breakdown = data.get('assets_breakdown', {})
        
        # Mostrar info del usuario
        self.show_user_info(user, breakdown)
        
        # Llenar tabla de activos
        self.populate_assets_table(assets)
        
        # Habilitar botones de acción
        self.generate_pdf_btn.config(state='normal')
        self.export_csv_btn.config(state='normal')
    
    def show_user_info(self, user, breakdown):
        """Mostrar información del usuario"""
        # Limpiar frame anterior
        for widget in self.user_info_frame.winfo_children():
            widget.destroy()
        
        # Recrear info
        info_text = f"Usuario: {user.get('first_name', '')} {user.get('last_name', '')}"
        if user.get('employee_num'):
            info_text += f" ({user.get('employee_num')})"
        
        ttk.Label(self.user_info_frame, text=info_text, font=("Arial", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        
        # Detalles
        details = []
        if user.get('email'):
            details.append(f"Email: {user['email']}")
        if user.get('job_title'):
            details.append(f"Cargo: {user['job_title']}")
        if user.get('department', {}).get('name'):
            details.append(f"Departamento: {user['department']['name']}")
        if user.get('location', {}).get('name'):
            details.append(f"Ubicación: {user['location']['name']}")
        
        detail_text = " | ".join(details)
        ttk.Label(self.user_info_frame, text=detail_text).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        
        # Resumen de activos
        summary_parts = []
        if breakdown.get('hardware', 0) > 0:
            summary_parts.append(f"{breakdown['hardware']} equipos")
        if breakdown.get('accessories', 0) > 0:
            summary_parts.append(f"{breakdown['accessories']} accesorios")
        if breakdown.get('licenses', 0) > 0:
            summary_parts.append(f"{breakdown['licenses']} licencias")
        
        summary_text = f"Activos asignados: {', '.join(summary_parts) if summary_parts else 'Ninguno'}"
        ttk.Label(self.user_info_frame, text=summary_text, font=("Arial", 9)).grid(
            row=2, column=0, columnspan=2, sticky=tk.W
        )
        
        # Mostrar frame
        self.user_info_frame.grid()
    
    def populate_assets_table(self, assets):
        """Llenar tabla de activos"""
        # Limpiar tabla
        for item in self.assets_tree.get_children():
            self.assets_tree.delete(item)
        
        # Agregar activos
        for asset in assets:
            asset_type = asset.get('type', 'hardware')
            
            # Mapear tipo
            type_map = {
                'hardware': 'Equipo',
                'accessory': 'Accesorio',
                'license': 'Licencia'
            }
            tipo = type_map.get(asset_type, asset_type.title())
            
            # Obtener datos según tipo
            if asset_type == 'hardware':
                nombre = asset.get('name', '')
                modelo = asset.get('model', {}).get('name', '') if asset.get('model') else ''
                serie = asset.get('serial', '')
                tag = asset.get('asset_tag', '')
                estado = asset.get('status_label', {}).get('name', '') if asset.get('status_label') else ''
                ubicacion = asset.get('location', {}).get('name', '') if asset.get('location') else ''
            
            elif asset_type == 'accessory':
                nombre = asset.get('name', '')
                modelo = asset.get('model_number', '')
                serie = ''
                tag = ''
                estado = 'Asignado'
                ubicacion = asset.get('location', {}).get('name', '') if asset.get('location') else ''
            
            elif asset_type == 'license':
                nombre = asset.get('name', '')
                modelo = asset.get('product_key', '')[:20] + '...' if asset.get('product_key') else ''
                serie = asset.get('serial', '')
                tag = ''
                estado = 'Asignado'
                ubicacion = ''
            
            else:
                nombre = asset.get('name', '')
                modelo = ''
                serie = ''
                tag = ''
                estado = ''
                ubicacion = ''
            
            # Insertar en tabla
            self.assets_tree.insert('', 'end', values=(
                tipo, nombre, modelo, serie, tag, estado, ubicacion
            ))
    
    def clear_search(self):
        """Limpiar búsqueda"""
        self.email_var.set("")
        self.clear_results()
        self.set_status("Listo")
    
    def clear_results(self):
        """Limpiar resultados"""
        # Ocultar info del usuario
        self.user_info_frame.grid_remove()
        
        # Limpiar tabla
        for item in self.assets_tree.get_children():
            self.assets_tree.delete(item)
        
        # Deshabilitar botones
        self.generate_pdf_btn.config(state='disabled')
        self.export_csv_btn.config(state='disabled')
        
        # Limpiar datos
        self.current_user_data = None
    
    def generate_pdf(self):
        """Generar reporte PDF"""
        if not self.current_user_data:
            messagebox.showwarning("Sin datos", "No hay datos de usuario para generar el reporte")
            return
        
        # Seleccionar archivo de destino
        user = self.current_user_data['user']
        default_name = f"Reporte_{user.get('first_name', '')}_{user.get('last_name', '')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        default_name = default_name.replace(' ', '_')
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar reporte PDF",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialname=default_name
        )
        
        if not file_path:
            return
        
        # Generar PDF en hilo separado
        self.generate_pdf_btn.config(state='disabled')
        self.show_progress()
        self.set_status("Generando reporte PDF...")
        
        threading.Thread(target=self._generate_pdf_worker, args=(file_path,), daemon=True).start()
    
    def _generate_pdf_worker(self, file_path):
        """Worker para generar PDF"""
        try:
            # Adaptar datos para el generador PDF
            pdf_data = {
                'user': self.current_user_data['user'],
                'assets': self.current_user_data['assets']
            }
            
            # Generar PDF
            self.pdf_generator.generate_pdf(pdf_data, file_path)
            
            # Volver al hilo principal
            self.root.after(0, self._handle_pdf_result, True, file_path, None)
            
        except Exception as e:
            self.root.after(0, self._handle_pdf_result, False, file_path, str(e))
    
    def _handle_pdf_result(self, success, file_path, error):
        """Manejar resultado de generación PDF"""
        self.generate_pdf_btn.config(state='normal')
        self.hide_progress()
        
        if success:
            self.set_status(f"PDF generado: {file_path}")
            messagebox.showinfo(
                "PDF Generado",
                f"El reporte PDF se ha generado exitosamente:\n\n{file_path}"
            )
        else:
            self.set_status("Error al generar PDF")
            messagebox.showerror("Error", f"Error al generar PDF:\n{error}")
    
    def export_csv(self):
        """Exportar datos a CSV"""
        if not self.current_user_data:
            messagebox.showwarning("Sin datos", "No hay datos para exportar")
            return
        
        # Seleccionar archivo de destino
        user = self.current_user_data['user']
        default_name = f"Activos_{user.get('first_name', '')}_{user.get('last_name', '')}_{datetime.now().strftime('%Y%m%d')}.csv"
        default_name = default_name.replace(' ', '_')
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar CSV",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            initialname=default_name
        )
        
        if not file_path:
            return
        
        try:
            import csv
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir encabezados
                writer.writerow(['Tipo', 'Nombre', 'Modelo', 'Serie', 'Tag/Código', 'Estado', 'Ubicación'])
                
                # Escribir datos
                for item in self.assets_tree.get_children():
                    values = self.assets_tree.item(item, 'values')
                    writer.writerow(values)
            
            self.set_status(f"CSV exportado: {file_path}")
            messagebox.showinfo("Exportación completa", f"Datos exportados a:\n{file_path}")
            
        except Exception as e:
            self.set_status("Error al exportar CSV")
            messagebox.showerror("Error", f"Error al exportar CSV:\n{str(e)}")
    
    def run(self):
        """Ejecutar aplicación principal"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainGUI()
    app.run()
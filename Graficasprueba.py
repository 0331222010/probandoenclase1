import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

# ==========================================================
# PALETA DE COLORES Y ESTILOS
# ==========================================================
COLOR_FONDO = "#181825"
COLOR_PANEL = "#1e1e2e"
COLOR_TARJETA = "#2b2b3b"
COLOR_TEXTO = "#cdd6f4"
COLOR_SUBTEXTO = "#a6adc8"
COLOR_ACENTO = "#3b82f6"
COLOR_EXITO = "#10b981"
COLOR_BORDE = "#313244"

VENTANA = tk.Tk()
VENTANA.title("Graficador Geométrico 3D | Suite Profesional")
VENTANA.geometry("1280x800")
VENTANA.minsize(1050, 700)
VENTANA.configure(bg=COLOR_FONDO)

estilo = ttk.Style()
estilo.theme_use("clam")

# Configuración global del tema ttk
estilo.configure(".", background=COLOR_PANEL, foreground=COLOR_TEXTO, fieldbackground=COLOR_TARJETA, font=("Segoe UI", 10))
estilo.configure("TFrame", background=COLOR_PANEL)
estilo.configure("TLabel", background=COLOR_PANEL, foreground=COLOR_TEXTO)

# Encabezado
estilo.configure("HeaderMain.TLabel", background=COLOR_FONDO, foreground="#f3f4f6", font=("Segoe UI", 18, "bold"))
estilo.configure("HeaderSub.TLabel", background=COLOR_FONDO, foreground=COLOR_SUBTEXTO, font=("Segoe UI", 10))
estilo.configure("TituloSection.TLabel", font=("Segoe UI", 12, "bold"), foreground=COLOR_ACENTO)

# Notebook (Pestañas)
estilo.configure("TNotebook", background=COLOR_FONDO, borderwidth=0)
estilo.configure("TNotebook.Tab", background=COLOR_TARJETA, foreground=COLOR_SUBTEXTO, padding=[18, 10], font=("Segoe UI", 10, "bold"), borderwidth=0)
estilo.map("TNotebook.Tab", background=[("selected", COLOR_ACENTO)], foreground=[("selected", "#ffffff")])

# Botones
estilo.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=COLOR_ACENTO, foreground="#ffffff", borderwidth=0, padding=8)
estilo.map("Accent.TButton", background=[("active", "#2563eb")])

estilo.configure("Secondary.TButton", font=("Segoe UI", 10), background=COLOR_TARJETA, foreground=COLOR_TEXTO, borderwidth=1, bordercolor=COLOR_BORDE, padding=8)
estilo.map("Secondary.TButton", background=[("active", COLOR_BORDE)])

# Inputs y Combobox
estilo.configure("TEntry", fieldbackground="#11111b", foreground="#ffffff", insertcolor="#ffffff", padding=5)
estilo.configure("TCombobox", fieldbackground="#11111b", background=COLOR_TARJETA, foreground="#ffffff", padding=5)

# LabelFrame
estilo.configure("TLabelframe", background=COLOR_PANEL, foreground=COLOR_ACENTO, bordercolor=COLOR_BORDE, borderwidth=1, padding=12)
estilo.configure("TLabelframe.Label", background=COLOR_PANEL, foreground=COLOR_ACENTO, font=("Segoe UI", 11, "bold"))

# ==========================================================
# FUNCIONES AUXILIARES DE INTERFAZ
# ==========================================================

def crear_entrada(parent, texto, valor="0"):
    marco = ttk.Frame(parent)
    marco.pack(fill="x", padx=4, pady=4)

    lbl = ttk.Label(marco, text=texto, width=20, anchor="w")
    lbl.pack(side="left")

    entrada = ttk.Entry(marco, width=12)
    entrada.pack(side="right", expand=True, fill="x")
    entrada.insert(0, str(valor))

    return entrada


def obtener_valor(entrada):
    return float(entrada.get())


def mostrar_error(error):
    messagebox.showerror("Error en los parámetros", f"Verifica los datos ingresados:\n\n{error}")


def configurar_grafica_3d(ax, titulo):
    ax.clear()
    ax.set_facecolor("#11111b")
    ax.figure.patch.set_facecolor(COLOR_PANEL)

    ax.set_title(titulo, fontsize=12, fontweight="bold", color=COLOR_TEXTO, pad=15)
    ax.set_xlabel("Eje X", color=COLOR_SUBTEXTO, labelpad=8)
    ax.set_ylabel("Eje Y", color=COLOR_SUBTEXTO, labelpad=8)
    ax.set_zlabel("Eje Z", color=COLOR_SUBTEXTO, labelpad=8)

    ax.tick_params(colors=COLOR_SUBTEXTO, labelsize=8)
    ax.grid(True, linestyle=":", color="#45475a", alpha=0.5)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=25, azim=-55)


def actualizar_grafica(fig, canvas):
    fig.tight_layout()
    canvas.draw()


def configurar_limites_3d(ax, puntos):
    puntos = np.asarray(puntos)
    minimo = np.min(puntos, axis=0)
    maximo = np.max(puntos, axis=0)
    centro = (minimo + maximo) / 2
    rango = np.max(maximo - minimo)

    if rango < 1:
        rango = 1

    margen = rango * 0.65
    ax.set_xlim(centro[0] - margen, centro[0] + margen)
    ax.set_ylim(centro[1] - margen, centro[1] + margen)
    ax.set_zlim(centro[2] - margen, centro[2] + margen)
    ax.set_box_aspect((1, 1, 1))

# ==========================================================
# ENCABEZADO PRINCIPAL
# ==========================================================

header_frame = tk.Frame(VENTANA, bg=COLOR_FONDO)
header_frame.pack(fill="x", padx=20, pady=(15, 5))

ttk.Label(header_frame, text="GRAFICADOR GEOMÉTRICO 3D", style="HeaderMain.TLabel").pack(anchor="w")
ttk.Label(header_frame, text="Visualización interactiva de curvas y vectores en el espacio tridimensional", style="HeaderSub.TLabel").pack(anchor="w")

# ==========================================================
# PESTAÑAS PRINCIPALES
# ==========================================================

pestanas = ttk.Notebook(VENTANA)
pestanas.pack(fill="both", expand=True, padx=20, pady=10)

tab_circunferencia = ttk.Frame(pestanas)
tab_elipse = ttk.Frame(pestanas)
tab_recta = ttk.Frame(pestanas)

pestanas.add(tab_circunferencia, text=" Circunferencia 3D ")
pestanas.add(tab_elipse, text=" Elipse 3D ")
pestanas.add(tab_recta, text=" Recta 3D ")

# ----------------------------------------------------------
# 1. CIRCUNFERENCIA 3D
# ----------------------------------------------------------
marco_circulo = ttk.Frame(tab_circunferencia)
marco_circulo.pack(fill="both", expand=True, padx=10, pady=10)

panel_circulo = ttk.LabelFrame(marco_circulo, text=" Parámetros de Control ")
panel_circulo.pack(side="left", fill="y", padx=(0, 10), pady=5)

c_x = crear_entrada(panel_circulo, "Centro X (h):", 0)
c_y = crear_entrada(panel_circulo, "Centro Y (k):", 0)
c_z = crear_entrada(panel_circulo, "Centro Z (z0):", 0)
c_r = crear_entrada(panel_circulo, "Radio (r):", 5)

ttk.Label(panel_circulo, text="Plano de proyección:", style="TituloSection.TLabel").pack(anchor="w", padx=4, pady=(15, 4))
plano_circulo = ttk.Combobox(panel_circulo, values=["XY", "XZ", "YZ"], state="readonly")
plano_circulo.set("XY")
plano_circulo.pack(fill="x", padx=4, pady=2)

fig_circulo = Figure(figsize=(6, 5), dpi=100)
ax_circulo = fig_circulo.add_subplot(111, projection="3d")
configurar_grafica_3d(ax_circulo, "CIRCUNFERENCIA EN EL ESPACIO 3D")

right_frame_circ = ttk.Frame(marco_circulo)
right_frame_circ.pack(side="right", fill="both", expand=True)

canvas_circulo = FigureCanvasTkAgg(fig_circulo, master=right_frame_circ)
canvas_circulo.get_tk_widget().pack(fill="both", expand=True)

toolbar_circulo = NavigationToolbar2Tk(canvas_circulo, right_frame_circ, pack_toolbar=False)
toolbar_circulo.config(background=COLOR_PANEL)
toolbar_circulo.update()
toolbar_circulo.pack(fill="x", pady=(5, 0))


def graficar_circunferencia_3d():
    try:
        h, k, z0, r = obtener_valor(c_x), obtener_valor(c_y), obtener_valor(c_z), obtener_valor(c_r)
        plano = plano_circulo.get()

        if r <= 0:
            raise ValueError("El radio debe ser un número positivo.")

        t = np.linspace(0, 2 * np.pi, 300)
        if plano == "XY":
            x, y, z = h + r * np.cos(t), k + r * np.sin(t), np.full_like(t, z0)
        elif plano == "XZ":
            x, y, z = h + r * np.cos(t), np.full_like(t, k), z0 + r * np.sin(t)
        else:
            x, y, z = np.full_like(t, h), k + r * np.cos(t), z0 + r * np.sin(t)

        configurar_grafica_3d(ax_circulo, f"CIRCUNFERENCIA 3D (Plano {plano})")
        ax_circulo.plot(x, y, z, linewidth=2.5, color="#38bdf8", label="Circunferencia")
        ax_circulo.scatter(h, k, z0, color="#f43f5e", s=60, label="Centro")

        ax_circulo.legend(facecolor=COLOR_TARJETA, edgecolor=COLOR_BORDE, labelcolor=COLOR_TEXTO)
        configurar_limites_3d(ax_circulo, np.column_stack((x, y, z)))
        actualizar_grafica(fig_circulo, canvas_circulo)
    except Exception as error:
        mostrar_error(error)


def limpiar_circunferencia():
    for entrada, val in [(c_x, 0), (c_y, 0), (c_z, 0), (c_r, 5)]:
        entrada.delete(0, tk.END)
        entrada.insert(0, str(val))
    plano_circulo.set("XY")
    configurar_grafica_3d(ax_circulo, "CIRCUNFERENCIA EN EL ESPACIO 3D")
    canvas_circulo.draw()


ttk.Button(panel_circulo, text="Graficar Curva", style="Accent.TButton", command=graficar_circunferencia_3d).pack(fill="x", padx=4, pady=(20, 5))
ttk.Button(panel_circulo, text="Restablecer", style="Secondary.TButton", command=limpiar_circunferencia).pack(fill="x", padx=4, pady=5)

# ----------------------------------------------------------
# 2. ELIPSE 3D
# ----------------------------------------------------------
marco_elipse = ttk.Frame(tab_elipse)
marco_elipse.pack(fill="both", expand=True, padx=10, pady=10)

panel_elipse = ttk.LabelFrame(marco_elipse, text=" Parámetros de Control ")
panel_elipse.pack(side="left", fill="y", padx=(0, 10), pady=5)

e_x = crear_entrada(panel_elipse, "Centro X (h):", 0)
e_y = crear_entrada(panel_elipse, "Centro Y (k):", 0)
e_z = crear_entrada(panel_elipse, "Centro Z (z0):", 0)
e_a = crear_entrada(panel_elipse, "Semieje mayor (a):", 6)
e_b = crear_entrada(panel_elipse, "Semieje menor (b):", 3)

ttk.Label(panel_elipse, text="Plano de proyección:", style="TituloSection.TLabel").pack(anchor="w", padx=4, pady=(15, 4))
plano_elipse = ttk.Combobox(panel_elipse, values=["XY", "XZ", "YZ"], state="readonly")
plano_elipse.set("XY")
plano_elipse.pack(fill="x", padx=4, pady=2)

fig_elipse = Figure(figsize=(6, 5), dpi=100)
ax_elipse = fig_elipse.add_subplot(111, projection="3d")
configurar_grafica_3d(ax_elipse, "ELIPSE EN EL ESPACIO 3D")

right_frame_elipse = ttk.Frame(marco_elipse)
right_frame_elipse.pack(side="right", fill="both", expand=True)

canvas_elipse = FigureCanvasTkAgg(fig_elipse, master=right_frame_elipse)
canvas_elipse.get_tk_widget().pack(fill="both", expand=True)

toolbar_elipse = NavigationToolbar2Tk(canvas_elipse, right_frame_elipse, pack_toolbar=False)
toolbar_elipse.config(background=COLOR_PANEL)
toolbar_elipse.update()
toolbar_elipse.pack(fill="x", pady=(5, 0))


def graficar_elipse_3d():
    try:
        h, k, z0, a, b = obtener_valor(e_x), obtener_valor(e_y), obtener_valor(e_z), obtener_valor(e_a), obtener_valor(e_b)
        plano = plano_elipse.get()

        if a <= 0 or b <= 0:
            raise ValueError("Los semiejes deben ser valores positivos.")

        t = np.linspace(0, 2 * np.pi, 300)
        if plano == "XY":
            x, y, z = h + a * np.cos(t), k + b * np.sin(t), np.full_like(t, z0)
        elif plano == "XZ":
            x, y, z = h + a * np.cos(t), np.full_like(t, k), z0 + b * np.sin(t)
        else:
            x, y, z = np.full_like(t, h), k + a * np.cos(t), z0 + b * np.sin(t)

        configurar_grafica_3d(ax_elipse, f"ELIPSE 3D (Plano {plano})")
        ax_elipse.plot(x, y, z, linewidth=2.5, color="#34d399", label="Elipse")
        ax_elipse.scatter(h, k, z0, color="#f43f5e", s=60, label="Centro")

        ax_elipse.legend(facecolor=COLOR_TARJETA, edgecolor=COLOR_BORDE, labelcolor=COLOR_TEXTO)
        configurar_limites_3d(ax_elipse, np.column_stack((x, y, z)))
        actualizar_grafica(fig_elipse, canvas_elipse)
    except Exception as error:
        mostrar_error(error)


def limpiar_elipse():
    for entrada, val in [(e_x, 0), (e_y, 0), (e_z, 0), (e_a, 6), (e_b, 3)]:
        entrada.delete(0, tk.END)
        entrada.insert(0, str(val))
    plano_elipse.set("XY")
    configurar_grafica_3d(ax_elipse, "ELIPSE EN EL ESPACIO 3D")
    canvas_elipse.draw()


ttk.Button(panel_elipse, text="Graficar Curva", style="Accent.TButton", command=graficar_elipse_3d).pack(fill="x", padx=4, pady=(20, 5))
ttk.Button(panel_elipse, text="Restablecer", style="Secondary.TButton", command=limpiar_elipse).pack(fill="x", padx=4, pady=5)

# ----------------------------------------------------------
# 3. RECTA 3D
# ----------------------------------------------------------
marco_recta = ttk.Frame(tab_recta)
marco_recta.pack(fill="both", expand=True, padx=10, pady=10)

panel_recta = ttk.LabelFrame(marco_recta, text=" Parámetros de Control ")
panel_recta.pack(side="left", fill="y", padx=(0, 10), pady=5)

ttk.Label(panel_recta, text="Punto Inicial (P0):", style="TituloSection.TLabel").pack(anchor="w", padx=4, pady=(5, 2))
r_x = crear_entrada(panel_recta, "Coordenada X:", 0)
r_y = crear_entrada(panel_recta, "Coordenada Y:", 0)
r_z = crear_entrada(panel_recta, "Coordenada Z:", 0)

ttk.Label(panel_recta, text="Vector Director (V):", style="TituloSection.TLabel").pack(anchor="w", padx=4, pady=(10, 2))
r_dx = crear_entrada(panel_recta, "Dirección X (a):", 1)
r_dy = crear_entrada(panel_recta, "Dirección Y (b):", 2)
r_dz = crear_entrada(panel_recta, "Dirección Z (c):", 1)

ttk.Label(panel_recta, text="Rango Paramétrico:", style="TituloSection.TLabel").pack(anchor="w", padx=4, pady=(10, 2))
r_tmin = crear_entrada(panel_recta, "Mínimo (t):", -10)
r_tmax = crear_entrada(panel_recta, "Máximo (t):", 10)

fig_recta = Figure(figsize=(6, 5), dpi=100)
ax_recta = fig_recta.add_subplot(111, projection="3d")
configurar_grafica_3d(ax_recta, "RECTA VECTORIAL EN EL ESPACIO 3D")

right_frame_recta = ttk.Frame(marco_recta)
right_frame_recta.pack(side="right", fill="both", expand=True)

canvas_recta = FigureCanvasTkAgg(fig_recta, master=right_frame_recta)
canvas_recta.get_tk_widget().pack(fill="both", expand=True)

toolbar_recta = NavigationToolbar2Tk(canvas_recta, right_frame_recta, pack_toolbar=False)
toolbar_recta.config(background=COLOR_PANEL)
toolbar_recta.update()
toolbar_recta.pack(fill="x", pady=(5, 0))


def graficar_recta_3d():
    try:
        x0, y0, z0 = obtener_valor(r_x), obtener_valor(r_y), obtener_valor(r_z)
        dx, dy, dz = obtener_valor(r_dx), obtener_valor(r_dy), obtener_valor(r_dz)
        t_min, t_max = obtener_valor(r_tmin), obtener_valor(r_tmax)

        if dx == 0 and dy == 0 and dz == 0:
            raise ValueError("El vector director no puede ser nulo (0,0,0).")
        if t_min >= t_max:
            raise ValueError("El valor t_máx debe ser mayor que t_mín.")

        t = np.linspace(t_min, t_max, 300)
        x, y, z = x0 + dx * t, y0 + dy * t, z0 + dz * t

        configurar_grafica_3d(ax_recta, "RECTA VECTORIAL EN EL ESPACIO 3D")
        ax_recta.plot(x, y, z, linewidth=2.5, color="#a855f7", label="Recta")
        ax_recta.scatter(x0, y0, z0, color="#f43f5e", s=60, label="Punto P0")

        # Dibujar vector director
        ax_recta.quiver(x0, y0, z0, dx, dy, dz, color="#f59e0b", length=1, normalize=False, label="Vector V")

        ax_recta.legend(facecolor=COLOR_TARJETA, edgecolor=COLOR_BORDE, labelcolor=COLOR_TEXTO)
        configurar_limites_3d(ax_recta, np.column_stack((x, y, z)))
        actualizar_grafica(fig_recta, canvas_recta)
    except Exception as error:
        mostrar_error(error)


def limpiar_recta():
    for entrada, val in [(r_x, 0), (r_y, 0), (r_z, 0), (r_dx, 1), (r_dy, 2), (r_dz, 1), (r_tmin, -10), (r_tmax, 10)]:
        entrada.delete(0, tk.END)
        entrada.insert(0, str(val))
    configurar_grafica_3d(ax_recta, "RECTA VECTORIAL EN EL ESPACIO 3D")
    canvas_recta.draw()


ttk.Button(panel_recta, text="Graficar Curva", style="Accent.TButton", command=graficar_recta_3d).pack(fill="x", padx=4, pady=(15, 5))
ttk.Button(panel_recta, text="Restablecer", style="Secondary.TButton", command=limpiar_recta).pack(fill="x", padx=4, pady=5)

# ==========================================================
# INICIAR APLICACIÓN
# ==========================================================
VENTANA.mainloop()

# 🎮 2048 Pro Edition - Python

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Una recreación fiel, robusta y mejorada del clásico juego **2048**, desarrollada íntegramente en Python utilizando la librería nativa `tkinter`.

Esta versión no es solo un clon; incluye características avanzadas como una interfaz 100% responsiva que mantiene la proporción áurea del tablero, persistencia de datos y un sistema de "Deshacer" movimientos.

## ✨ Características "Ultra Pro"

Este proyecto va más allá de la lógica básica:

* **📐 Interfaz Responsive Geométrica:** El tablero mantiene siempre su forma cuadrada perfecta y se centra automáticamente, sin importar cómo redimensiones la ventana.
* **↩️ Sistema de Deshacer (Undo):** ¿Cometiste un error? Tienes hasta **5 oportunidades** por partida para retroceder en el tiempo (Stack History).
* **💾 Persistencia de Datos:** El juego guarda automáticamente tu **High Score** en un archivo local (`highscore.txt`).
* **🎨 Estética Fiel:** Colores y tipografías idénticas al juego original.
* **🔠 Tipografía Dinámica:** Los números ajustan su tamaño automáticamente según el tamaño de la ventana.
* **🎲 Probabilidad Realista:** 90% de aparición de baldosas '2' y 10% de baldosas '4'.

## 🚀 Requisitos e Instalación

Lo mejor de este proyecto es que **no requiere instalar nada externo**. Utiliza las librerías estándar de Python.

1.  Asegúrate de tener Python instalado (versión 3.6 o superior).
2.  Clona este repositorio o descarga el archivo `.py`.
3.  Ejecuta el juego:

## 🎮 Cómo Jugar

El objetivo es sumar baldosas del mismo número deslizándolas hasta conseguir la baldosa **2048**.

### Controles

| Acción | Teclado | Alternativa |
| :--- | :---: | :---: |
| **Mover Arriba** | `⬆️ Flecha Arriba` | `W` |
| **Mover Abajo** | `⬇️ Flecha Abajo` | `S` |
| **Mover Izquierda** | `⬅️ Flecha Izquierda` | `A` |
| **Mover Derecha** | `➡️ Flecha Derecha` | `D` |
| **Deshacer** | `Control` + `Z` | Botón en Pantalla |

## 📦 Crear Ejecutable (.exe)

Si deseas convertir el juego en un archivo ejecutable para compartirlo con amigos que no tienen Python:

1.  Instala PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Genera el ejecutable:
    ```bash
    pyinstaller --onefile --noconsole --name="2048_Pro" tu_archivo.py
    ```

3.  El archivo `.exe` estará en la carpeta `/dist`.

## 🧠 Estructura del Código

El proyecto utiliza Programación Orientada a Objetos (POO) con una clase principal `Juego2048` que hereda de `tk.Frame`.

* **Frontend:** Gestión de `grid`, `place` y eventos `<Configure>` para la responsividad.
* **Backend:** Lógica de matrices (transposición, inversión y compresión) para calcular los movimientos.
* **State Management:** Uso de listas para el historial de movimientos (Undo System).

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para animaciones suaves o una IA que juegue sola, siéntete libre de hacer un Fork.

---
>Hecho con 🧡, 🐍 y mucho ☕.

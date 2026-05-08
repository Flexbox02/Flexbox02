# Control de visitas: oficina y finca

Aplicación web sencilla para registrar los días que visitas la **oficina** o la **finca**.

## Funcionalidades

- Registro de visitas por lugar y fecha.
- Historial de visitas ordenado por fecha (más reciente primero).
- Alerta automática si pasan más de **60 días** sin visitar la finca.
- Persistencia local con `localStorage` del navegador.

## Publicación en GitHub Pages

Este repositorio ya incluye un workflow de GitHub Actions para desplegar automáticamente en Pages:

- Archivo: `.github/workflows/deploy-pages.yml`
- Se ejecuta al hacer push a `main` o `work`.

### Pasos para activarlo en tu repositorio

1. Sube este código a un repositorio en GitHub.
2. Ve a **Settings → Pages**.
3. En **Build and deployment**, selecciona **Source: GitHub Actions**.
4. Haz push a la rama `main` (o `work`) y espera a que finalice el workflow.
5. Tu web quedará publicada en una URL tipo:
   - `https://TU_USUARIO.github.io/TU_REPO/`

## Uso local

1. Abre `index.html` en tu navegador.
2. Elige el lugar (oficina o finca).
3. Selecciona la fecha y pulsa **Guardar visita**.
4. Revisa el estado de la finca y el historial.

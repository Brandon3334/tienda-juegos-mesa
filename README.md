# Tienda de Juegos de Mesa

Aplicación web desarrollada con Django para administrar y consultar un catálogo de juegos de mesa, controlar stock y registrar pedidos públicos sin exigir inicio de sesión.

## Funcionalidades

- Panel administrativo de Django.
- Gestión de categorías.
- Gestión de juegos e imágenes.
- Control de precio y stock.
- Catálogo público.
- Búsqueda por nombre y descripción.
- Filtro por categoría.
- Detalle del juego.
- Estados Disponible y Agotado.
- Formulario público de pedidos.
- Validaciones de nombre, correo, teléfono y cantidad.
- Cantidad máxima de 5 unidades.
- Descuento transaccional y seguro de stock.
- Código único de pedido con formato `PED-XXXXXXXX`.
- Comprobante de pedido.
- Prevención de pedidos duplicados al recargar mediante POST-Redirect-GET.
- Usuario administrador.
- Usuario de personal Bodega con permisos limitados.
- Pruebas automatizadas.

## Tecnologías utilizadas

- Python 3.15.2
- Django 6.1.3
- SQLite
- HTML5
- CSS3
- Pillow
- Git

## Estructura principal

- `tienda_juegos/`: configuración, URLs y archivos de entrada del proyecto Django.
- `catalogo/`: aplicación principal con modelos, formularios, vistas, administración y pruebas.
- `catalogo/templates/`: plantillas HTML del catálogo, detalles, pedidos y comprobantes.
- `catalogo/static/`: hoja de estilos CSS de la aplicación.
- `catalogo/templatetags/`: filtro de precios en pesos chilenos.
- `media/juegos/`: portadas finales de las cajas, almacenadas localmente.
- `db.sqlite3`: base de datos SQLite incluida para la evaluación.
- `manage.py`: utilidad de administración de Django.
- `requirements.txt`: dependencias necesarias para instalar el proyecto.

## Instalación en Windows

1. Clonar el repositorio:

   ```powershell
   git clone URL_DEL_REPOSITORIO
   ```

   `URL_DEL_REPOSITORIO` se reemplazará después de crear el repositorio remoto.

2. Entrar a la carpeta:

   ```powershell
   cd tienda-juegos-mesa
   ```

3. Crear el entorno virtual:

   ```powershell
   python -m venv .venv
   ```

4. Activarlo en PowerShell:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

5. Instalar las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Comprobar el proyecto:

   ```powershell
   python manage.py check
   ```

7. Ejecutar las migraciones:

   ```powershell
   python manage.py migrate
   ```

8. Ejecutar las pruebas:

   ```powershell
   python manage.py test
   ```

9. Iniciar el servidor:

   ```powershell
   python manage.py runserver
   ```

10. Abrir en el navegador:

   - Catálogo: <http://127.0.0.1:8000/>
   - Administración: <http://127.0.0.1:8000/admin/>

## Variable de entorno opcional

Para mantener una clave estable durante el desarrollo, se puede configurar en PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "REEMPLAZAR_POR_UNA_CLAVE_LOCAL_SEGURA"
```

El valor mostrado es un ejemplo y debe reemplazarse localmente. No debe escribirse en el repositorio. Si no se configura, Django genera una clave temporal adecuada para la demostración local. En producción siempre debe configurarse una variable privada y estable.

## Datos incluidos

- 3 categorías.
- 6 juegos de demostración.
- 4 pedidos de demostración.
- Un juego agotado.
- Un juego no disponible.
- Portadas finales de las cajas almacenadas localmente.

## Usuarios y permisos

- Existe un superusuario llamado `admin`.
- Existe un usuario de personal llamado `bodega`.
- `bodega` pertenece al grupo `Bodega`.
- `bodega` tiene permisos limitados sobre categorías, juegos y pedidos.
- Las contraseñas no se incluyen en el repositorio ni en esta documentación.

## Pruebas

Ejecutar:

```powershell
python manage.py test
```

Actualmente existen 17 pruebas automatizadas para:

- Validaciones del formulario.
- Límites de cantidad.
- Correo y teléfono.
- Juegos agotados o no disponibles.
- Creación de pedidos.
- Descuento de stock.
- Código único.
- Redirección al comprobante.
- Prevención de duplicados.
- Respuestas 404.

## Git

El proyecto se desarrolló mediante commits pequeños y progresivos, separando la configuración inicial, los modelos, la administración, los permisos, el catálogo público, los datos de demostración y el flujo de pedidos.

## Autor

Brandon Jorquera  
Estudiante de Ingeniería en Informática

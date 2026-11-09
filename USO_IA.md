# Registro de uso de inteligencia artificial

## Herramientas utilizadas

- Microsoft Copilot.
- GitHub Copilot integrado en Visual Studio Code.

## Forma de trabajo

La inteligencia artificial se utilizó por etapas:

1. Análisis de la pauta.
2. Preparación del entorno.
3. Creación inicial de Django.
4. Definición de modelos y migraciones.
5. Configuración del panel administrativo.
6. Configuración de usuarios, grupo y permisos.
7. Implementación del catálogo.
8. Creación de datos e imágenes provisionales.
9. Implementación del flujo de pedidos.
10. Escritura y ejecución de pruebas.
11. Documentación y revisión final.

El proyecto no se construyó completo de una sola vez. Cada etapa fue comprobada antes de continuar y se realizaron commits después de cada avance estable. Los resultados se probaron manualmente y los errores se analizaron antes de realizar modificaciones.

El estudiante revisó el funcionamiento de las funcionalidades. Las contraseñas se ingresaron manualmente y no fueron compartidas con la inteligencia artificial.

## Ejemplos de prompts utilizados

- Comprobar Python, pip y Git antes de crear el proyecto.
- Crear los modelos Categoria, Juego y Pedido sin adelantar vistas.
- Configurar Django Admin con columnas, filtros y búsquedas.
- Crear el grupo Bodega con permisos restringidos.
- Implementar el catálogo público con búsqueda y categoría combinables.
- Implementar pedidos utilizando `transaction.atomic` y `select_for_update`.
- Crear pruebas para validar cantidades, stock y comprobantes.
- Comprobar que recargar el comprobante no duplique el pedido.

## Código generado o apoyado por IA

La inteligencia artificial apoyó la creación o revisión de:

- Configuración inicial de Django.
- Modelos.
- Administración.
- Formularios.
- Vistas.
- URLs.
- Plantillas.
- CSS.
- Pruebas automatizadas.
- Comandos Git.
- Documentación.

## Validaciones realizadas por el estudiante

- Ejecución de `python manage.py check`.
- Ejecución de `python manage.py test`.
- Comprobación visual del catálogo.
- Comprobación de búsqueda y filtros.
- Comprobación de detalles y respuestas 404.
- Pruebas de admin y bodega.
- Pruebas de validación del pedido.
- Verificación del descuento de stock.
- Recarga del comprobante con F5.
- Comprobación del historial Git.

## Limitaciones y decisiones

- Las imágenes actuales son provisionales y fueron generadas localmente con Pillow.
- Se reemplazarán por imágenes apropiadas de las cajas antes de la entrega final.
- La lógica esencial no depende de JavaScript.
- La generación del código utiliza `secrets`.
- El control de stock utiliza transacciones.
- Las pruebas utilizan una base de datos temporal independiente.

## Responsabilidad

El estudiante revisó, ejecutó y comprobó el código generado o sugerido por las herramientas de inteligencia artificial y asume la responsabilidad sobre la entrega final.

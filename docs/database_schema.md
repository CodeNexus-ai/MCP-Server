# Esquema de la Base de Datos

Este documento describe la estructura de las tablas en la base de datos PostgreSQL.

## Tabla: categorias

| Columna | Tipo | Nullable | Default | Descripción |
|---------|------|----------|----------|-------------|
| id_categoria | integer | No | nextval('categorias_id_categoria_seq') | Clave primaria |
| nombre | varchar(100) | No | - | Nombre de la categoría |
| descripcion | text | Sí | - | Descripción detallada de la categoría |

Total de registros: 8

## Tabla: productos

| Columna | Tipo | Nullable | Default | Descripción |
|---------|------|----------|----------|-------------|
| id_producto | integer | No | nextval('productos_id_producto_seq') | Clave primaria |
| nombre | varchar(100) | No | - | Nombre del producto |
| descripcion | text | Sí | - | Descripción del producto |
| precio | numeric | No | - | Precio del producto |
| stock | integer | No | 0 | Cantidad en inventario |
| id_categoria | integer | Sí | - | Referencia a categorias.id_categoria |
| fecha_creacion | date | Sí | CURRENT_DATE | Fecha de creación del producto |

Total de registros: 100

## Tabla: clientes

| Columna | Tipo | Nullable | Default | Descripción |
|---------|------|----------|----------|-------------|
| id_cliente | integer | No | nextval('clientes_id_cliente_seq') | Clave primaria |
| nombre | varchar(50) | No | - | Nombre del cliente |
| apellido | varchar(50) | No | - | Apellido del cliente |
| email | varchar(100) | No | - | Correo electrónico |
| telefono | varchar(20) | Sí | - | Número de teléfono |
| direccion | varchar(200) | Sí | - | Dirección postal |
| ciudad | varchar(50) | Sí | - | Ciudad |
| pais | varchar(50) | Sí | - | País |
| fecha_registro | date | Sí | CURRENT_DATE | Fecha de registro del cliente |

Total de registros: 100

## Tabla: pedidos

| Columna | Tipo | Nullable | Default | Descripción |
|---------|------|----------|----------|-------------|
| id_pedido | integer | No | nextval('pedidos_id_pedido_seq') | Clave primaria |
| id_cliente | integer | Sí | - | Referencia a clientes.id_cliente |
| fecha_pedido | timestamp | Sí | CURRENT_TIMESTAMP | Fecha y hora del pedido |
| estado | varchar(20) | Sí | 'Pendiente' | Estado del pedido |
| total | numeric | Sí | - | Monto total del pedido |

Total de registros: 100

## Tabla: detalles_pedido

| Columna | Tipo | Nullable | Default | Descripción |
|---------|------|----------|----------|-------------|
| id_detalle | integer | No | nextval('detalles_pedido_id_detalle_seq') | Clave primaria |
| id_pedido | integer | Sí | - | Referencia a pedidos.id_pedido |
| id_producto | integer | Sí | - | Referencia a productos.id_producto |
| cantidad | integer | No | - | Cantidad de productos |
| precio_unitario | numeric | No | - | Precio por unidad |
| subtotal | numeric | No | - | Subtotal (cantidad * precio_unitario) |

Total de registros: 150

## Relaciones

- `productos.id_categoria` → `categorias.id_categoria`
- `pedidos.id_cliente` → `clientes.id_cliente`
- `detalles_pedido.id_pedido` → `pedidos.id_pedido`
- `detalles_pedido.id_producto` → `productos.id_producto`
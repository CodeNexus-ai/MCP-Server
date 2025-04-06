# Descripción General de las Funciones del Servidor MCP PostgreSQL

## Clase de Conexión a Base de Datos

### `DatabaseConnection`
- **Propósito**: Gestiona las conexiones a la base de datos PostgreSQL
- **Parámetros del Constructor**:
  - `host`: str (por defecto: "localhost")
  - `database`: str (por defecto: "postgres")
  - `user`: str (por defecto: "postgres")
  - `password`: str (por defecto: "codenexus")
- **Métodos**:
  - `close()`: Cierra la conexión a la base de datos

## Funciones Auxiliares

### `json_serializer(obj: Any) -> Any`
- **Propósito**: Serializa tipos de datos especiales a JSON
- **Maneja**:
  - objetos datetime/date → formato ISO
  - números Decimal → float

### `get_db() -> DatabaseConnection`
- **Propósito**: Patrón Singleton para la conexión a la base de datos
- **Retorna**: Instancia global de la conexión a la base de datos o None si la conexión falla

## Funciones Principales de Base de Datos

### `list_tables(db: DatabaseConnection) -> str`
- **Propósito**: Lista todas las tablas en la base de datos
- **Retorna**: Cadena formateada con los nombres de las tablas

### `get_table_info(db: DatabaseConnection, table: str) -> str`
- **Propósito**: Obtiene información detallada sobre una tabla específica
- **Retorna**: Cadena formateada con:
  - Detalles de columnas (nombre, tipo, longitud, nullable, valor por defecto)
  - Claves primarias
  - Conteo total de filas

### `query_table(db: DatabaseConnection, table: str, limit: Optional[int] = 5) -> str`
- **Propósito**: Consulta datos de una tabla
- **Parámetros**:
  - `table`: Tabla a consultar
  - `limit`: Máximo de filas a retornar (por defecto: 5)
- **Retorna**: Cadena formateada con los resultados de la consulta

### `execute_query(db: DatabaseConnection, query: str, params: Optional[tuple] = None) -> str`
- **Propósito**: Ejecuta consultas SQL personalizadas
- **Parámetros**:
  - `query`: Consulta SQL a ejecutar
  - `params`: Parámetros opcionales de la consulta
- **Retorna**: Resultados de la consulta o conteo de filas afectadas

## Herramientas MCP (API Expuesta)

### `@mcp.tool() list_tables_tool(args: dict) -> str`
- **Propósito**: Punto de entrada API para listar tablas
- **Retorna**: Lista de tablas disponibles o mensaje de error

### `@mcp.tool() get_table_info_tool(args: dict) -> str`
- **Propósito**: Punto de entrada API para información de tabla
- **Argumentos Requeridos**:
  - `table`: Nombre de la tabla a inspeccionar
- **Retorna**: Información detallada de la tabla o mensaje de error

### `@mcp.tool() query_table_tool(args: dict) -> str`
- **Propósito**: Punto de entrada API para consultar tablas
- **Argumentos Requeridos**:
  - `table`: Nombre de la tabla a consultar
- **Argumentos Opcionales**:
  - `limit`: Máximo de filas a retornar (por defecto: 5)
- **Retorna**: Resultados de la consulta o mensaje de error

### `@mcp.tool() execute_query_tool(args: dict) -> str`
- **Propósito**: Punto de entrada API para consultas SQL personalizadas
- **Argumentos Requeridos**:
  - `query`: Consulta SQL a ejecutar
- **Argumentos Opcionales**:
  - `params`: Parámetros de la consulta
- **Retorna**: Resultados de la consulta o mensaje de error
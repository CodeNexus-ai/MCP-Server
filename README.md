# PostgreSQL MCP Server Functions Overview

## Database Connection Class

### `DatabaseConnection`
- **Purpose**: Manages PostgreSQL database connections
- **Constructor Parameters**:
  - `host`: str (default: "localhost")
  - `database`: str (default: "postgres")
  - `user`: str (default: "postgres")
  - `password`: str (default: "codenexus")
- **Methods**:
  - `close()`: Closes the database connection

## Helper Functions

### `json_serializer(obj: Any) -> Any`
- **Purpose**: Serializes special data types to JSON
- **Handles**:
  - datetime/date objects → ISO format
  - Decimal numbers → float

### `get_db() -> DatabaseConnection`
- **Purpose**: Singleton pattern for database connection
- **Returns**: Global database connection instance or None if connection fails

## Core Database Functions

### `list_tables(db: DatabaseConnection) -> str`
- **Purpose**: Lists all tables in the database
- **Returns**: Formatted string of table names

### `get_table_info(db: DatabaseConnection, table: str) -> str`
- **Purpose**: Gets detailed information about a specific table
- **Returns**: Formatted string with:
  - Column details (name, type, length, nullable, default)
  - Primary keys
  - Total row count

### `query_table(db: DatabaseConnection, table: str, limit: Optional[int] = 5) -> str`
- **Purpose**: Queries data from a table
- **Parameters**:
  - `table`: Table to query
  - `limit`: Max rows to return (default: 5)
- **Returns**: Formatted string of query results

### `execute_query(db: DatabaseConnection, query: str, params: Optional[tuple] = None) -> str`
- **Purpose**: Executes custom SQL queries
- **Parameters**:
  - `query`: SQL query to execute
  - `params`: Optional query parameters
- **Returns**: Query results or affected rows count

## MCP Tools (Exposed API)

### `@mcp.tool() list_tables_tool(args: dict) -> str`
- **Purpose**: API endpoint for listing tables
- **Returns**: List of available tables or error message

### `@mcp.tool() get_table_info_tool(args: dict) -> str`
- **Purpose**: API endpoint for table information
- **Required Args**:
  - `table`: Name of table to inspect
- **Returns**: Detailed table information or error message

### `@mcp.tool() query_table_tool(args: dict) -> str`
- **Purpose**: API endpoint for querying tables
- **Required Args**:
  - `table`: Name of table to query
- **Optional Args**:
  - `limit`: Maximum rows to return (default: 5)
- **Returns**: Query results or error message

### `@mcp.tool() execute_query_tool(args: dict) -> str`
- **Purpose**: API endpoint for custom SQL queries
- **Required Args**:
  - `query`: SQL query to execute
- **Optional Args**:
  - `params`: Query parameters
- **Returns**: Query results or error message
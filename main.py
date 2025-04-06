#!/usr/bin/env python3
from typing import Any, Dict, List, Optional
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
from decimal import Decimal
from mcp.server.fastmcp import FastMCP

class DatabaseConnection:
    def __init__(self, host: str = "localhost", database: str = "postgres", 
                 user: str = "postgres", password: str = "codenexus"):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def close(self):
        if self.conn:
            self.conn.close()

def json_serializer(obj: Any) -> Any:
    """Serialize special data types to JSON."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

async def list_tables(db: DatabaseConnection) -> str:
    """Get list of all tables in the database."""
    try:
        cur = db.conn.cursor()
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [table[0] for table in cur.fetchall()]
        cur.close()
        
        if not tables:
            return "No tables found in the database."
        
        return "\n".join([
            "Available tables:",
            *[f"- {table}" for table in tables]
        ])
    except Exception as e:
        return f"Error listing tables: {str(e)}"

async def get_table_info(db: DatabaseConnection, table: str) -> str:
    """Get detailed information about a specific table.
    
    Args:
        table: Name of the table to get information about
    """
    try:
        cur = db.conn.cursor()
        
        # Get column information
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table,))
        columns = cur.fetchall()
        
        # Get row count
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        
        # Get primary key information
        cur.execute("""
            SELECT a.attname
            FROM   pg_index i
            JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                AND a.attnum = ANY(i.indkey)
            WHERE  i.indrelid = %s::regclass
            AND    i.indisprimary
        """, (table,))
        primary_keys = [pk[0] for pk in cur.fetchall()]
        
        cur.close()
        
        # Format the table information
        info = [f"Table: {table}"]
        info.append("\nColumns:")
        for col in columns:
            info.append(f"- {col[0]}")
            info.append(f"  Type: {col[1]}")
            if col[2]:
                info.append(f"  Max Length: {col[2]}")
            info.append(f"  Nullable: {col[4] == 'YES'}")
            if col[3]:
                info.append(f"  Default: {col[3]}")
                
        info.append(f"\nPrimary Keys: {', '.join(primary_keys)}")
        info.append(f"Total Rows: {count}")
        
        return "\n".join(info)
    except Exception as e:
        return f"Error getting table info for {table}: {str(e)}"

async def query_table(db: DatabaseConnection, table: str, limit: Optional[int] = 5) -> str:
    """Query data from a table.
    
    Args:
        table: Name of the table to query
        limit: Maximum number of rows to return (default: 5)
    """
    try:
        cur = db.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {table} LIMIT {limit}")
        rows = cur.fetchall()
        cur.close()
        
        if not rows:
            return f"No data found in table {table}"
        
        # Format the results
        result = [f"Data from {table} (showing {len(rows)} rows):"]
        for row in rows:
            result.append("\nRow:")
            for key, value in row.items():
                result.append(f"  {key}: {value}")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error querying table {table}: {str(e)}"

async def execute_query(db: DatabaseConnection, query: str, params: Optional[tuple] = None) -> str:
    """Execute a custom SQL query.
    
    Args:
        query: SQL query to execute
        params: Optional tuple of parameters for the query
    """
    try:
        cur = db.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, params)
        
        if cur.description:  # If the query returns data
            rows = cur.fetchall()
            result = ["Query results:"]
            for row in rows:
                result.append("\nRow:")
                for key, value in row.items():
                    result.append(f"  {key}: {value}")
        else:
            affected = cur.rowcount
            result = [f"Query executed successfully. {affected} rows affected."]
            
        db.conn.commit()
        cur.close()
        return "\n".join(result)
    except Exception as e:
        db.conn.rollback()
        return f"Error executing query: {str(e)}"

# Initialize FastMCP server
mcp = FastMCP("postgres")

_db = None

def get_db():
    global _db
    if _db is None:
        try:
            _db = DatabaseConnection()
        except Exception as e:
            return None
    return _db


@mcp.tool()
async def list_tables_tool(args: dict) -> str:
    """List all tables in the database."""
    db = get_db()
    if not db:
        return "Error: Could not connect to database"
    try:
        return await list_tables(db)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def get_table_info_tool(args: dict) -> str:
    """Get detailed information about a specific table.
    
    Args:
        table: Name of the table to get information about
    """
    db = get_db()
    if not db:
        return "Error: Could not connect to database"
    
    table = args.get("table")
    if not table:
        return "Error: table name is required"
    
    try:
        return await get_table_info(db, table)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def query_table_tool(args: dict) -> str:
    """Query data from a specific table.
    
    Args:
        table: Name of the table to query
        limit: Maximum number of rows to return (optional, default: 5)
    """
    db = get_db()
    if not db:
        return "Error: Could not connect to database"
    
    table = args.get("table")
    limit = args.get("limit", 5)
    
    if not table:
        return "Error: table name is required"
    
    try:
        return await query_table(db, table, limit)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
async def execute_query_tool(args: dict) -> str:
    """Execute a custom SQL query.
    
    Args:
        query: SQL query to execute
        params: Optional tuple of parameters for the query (optional)
    """
    db = get_db()
    if not db:
        return "Error: Could not connect to database"
    
    query = args.get("query")
    params = args.get("params")
    
    if not query:
        return "Error: query is required"
    
    try:
        return await execute_query(db, query, params)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    try:
        mcp.run(transport='stdio')
    finally:
        if _db:
            _db.close()
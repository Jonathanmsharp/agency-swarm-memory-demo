from agency_swarm.tools import BaseTool
from pydantic import Field
import os
import logging
import sys
import subprocess
from dotenv import load_dotenv
import json
from typing import Optional, List, Dict, Any, Union
import datetime

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SQL Server connection details from environment variables
server = os.getenv("MSSQL_SERVER")
user = os.getenv("MSSQL_USER")
password = os.getenv("MSSQL_PASSWORD")
database = os.getenv("MSSQL_DATABASE")

class SQLQueryTool(BaseTool):
    """
    Tool for interacting with SQL Server databases. This tool allows agents to:
    1. List available tables in a SQL Server database
    2. Read table contents (with optional filtering)
    3. Execute custom SQL queries
    All operations use secure connection details from environment variables.
    """
    
    operation: str = Field(
        ..., 
        description="Operation to perform: 'list_tables', 'read_table', or 'execute_query'"
    )
    
    table_name: Optional[str] = Field(
        None, 
        description="Table name to read data from (required for 'read_table' operation)"
    )
    
    query: Optional[str] = Field(
        None, 
        description="SQL query to execute (required for 'execute_query' operation)"
    )
    
    limit: Optional[int] = Field(
        100, 
        description="Maximum number of rows to return (default: 100)"
    )
    
    where_clause: Optional[str] = Field(
        None, 
        description="WHERE clause for filtering data when reading a table"
    )
    
    verbose_reasoning: bool = Field(
        False,
        description="Whether to include detailed reasoning in the output"
    )
    
    def __ensure_dependencies(self):
        """Ensure all required dependencies are installed"""
        try:
            import pyodbc
        except ImportError:
            logger.info("Installing required dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyodbc"])
            import pyodbc
        return True
    
    def __get_connection(self):
        """Establish connection to SQL Server using environment variables"""
        try:
            import pyodbc
            conn_str = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};UID={user};PWD={password}"
            connection = pyodbc.connect(conn_str)
            return connection
        except Exception as e:
            logger.error(f"Failed to connect to the database: {str(e)}")
            return None
    
    def __list_tables(self):
        """List all tables in the database"""
        connection = self.__get_connection()
        if not connection:
            return {"error": "Failed to connect to the database"}
        
        try:
            cursor = connection.cursor()
            tables = []
            
            cursor.execute("""
                SELECT TABLE_SCHEMA, TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """)
            
            for schema, table in cursor.fetchall():
                tables.append(f"{schema}.{table}")
            
            return {"tables": tables}
        except Exception as e:
            logger.error(f"Error listing tables: {str(e)}")
            return {"error": f"Failed to list tables: {str(e)}"}
        finally:
            connection.close()
    
    def __read_table(self):
        """Read contents of a specified table with optional filtering"""
        if not self.table_name:
            return {"error": "Table name is required for read_table operation"}
        
        connection = self.__get_connection()
        if not connection:
            return {"error": "Failed to connect to the database"}
        
        try:
            cursor = connection.cursor()
            query = f"SELECT TOP {self.limit} * FROM {self.table_name}"
            
            if self.where_clause:
                query += f" WHERE {self.where_clause}"
            
            cursor.execute(query)
            
            columns = [column[0] for column in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = {}
                for i, value in enumerate(row):
                    # Convert non-serializable types to strings
                    if isinstance(value, (bytes, bytearray)):
                        value = f"<binary data of length {len(value)}>"
                    row_dict[columns[i]] = value
                results.append(row_dict)
            
            return {
                "columns": columns,
                "rows": results,
                "count": len(results),
                "query": query
            }
        except Exception as e:
            logger.error(f"Error reading table: {str(e)}")
            return {"error": f"Failed to read table: {str(e)}"}
        finally:
            connection.close()
    
    def __execute_query(self):
        """Execute a custom SQL query"""
        if not self.query:
            return {"error": "SQL query is required for execute_query operation"}
        
        connection = self.__get_connection()
        if not connection:
            return {"error": "Failed to connect to the database"}
        
        try:
            cursor = connection.cursor()
            cursor.execute(self.query)
            
            # Check if the query returns results
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                results = []
                
                for row in cursor.fetchall():
                    row_dict = {}
                    for i, value in enumerate(row):
                        # Convert non-serializable types to strings
                        if isinstance(value, (bytes, bytearray)):
                            value = f"<binary data of length {len(value)}>"
                        row_dict[columns[i]] = value
                    results.append(row_dict)
                
                return {
                    "columns": columns,
                    "rows": results,
                    "count": len(results),
                    "query": self.query
                }
            else:
                # For non-SELECT queries
                connection.commit()
                return {
                    "message": "Query executed successfully",
                    "rows_affected": cursor.rowcount,
                    "query": self.query
                }
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return {"error": f"Failed to execute query: {str(e)}"}
        finally:
            connection.close()
    
    def run(self):
        """Run SQL operation"""
        reasoning = []
        
        # Step 1: Dependency and environment check
        reasoning.append("2. ENVIRONMENT CHECK: Verifying dependencies and connection details.")
        self.__ensure_dependencies()
        
        if not all([server, user, password, database]):
            missing_vars = []
            if not server: missing_vars.append("MSSQL_SERVER")
            if not user: missing_vars.append("MSSQL_USER")
            if not password: missing_vars.append("MSSQL_PASSWORD")
            if not database: missing_vars.append("MSSQL_DATABASE")
            reasoning.append(f"Missing required connection variables: {', '.join(missing_vars)}")
            return json.dumps({
                "error": f"Missing environment variables: {', '.join(missing_vars)}",
                "reasoning": reasoning if self.verbose_reasoning else None
            })
        
        # Step 2: Operation-specific reasoning
        reasoning.append(f"3. OPERATION ANALYSIS: Planning execution of '{self.operation}' operation.")
        
        if self.operation == "list_tables":
            reasoning.append("- This operation will query INFORMATION_SCHEMA views, which is typically fast.")
            reasoning.append("- Security implications: Minimal, as this only returns metadata.")
            result = self.__list_tables()
                
        elif self.operation == "read_table":
            if not self.table_name:
                reasoning.append("- Error: Missing required table_name parameter.")
                result = {"error": "Table name is required for read_table operation"}
            else:
                reasoning.append(f"- Planning to read from table: {self.table_name}")
                reasoning.append(f"- Limiting results to {self.limit} rows for performance.")
                if self.where_clause:
                    reasoning.append(f"- Applying filter: {self.where_clause}")
                    reasoning.append("- Security note: WHERE clause should be sanitized to prevent SQL injection.")
                result = self.__read_table()
                    
        elif self.operation == "execute_query":
            if not self.query:
                reasoning.append("- Error: Missing required query parameter.")
                result = {"error": "SQL query is required for execute_query operation"}
            else:
                reasoning.append("- Analyzing custom query:")
                query_lower = self.query.lower()
                if "delete" in query_lower or "drop" in query_lower or "truncate" in query_lower:
                    reasoning.append("  * CAUTION: Query contains potentially destructive operations.")
                if "where" not in query_lower and ("update" in query_lower or "delete" in query_lower):
                    reasoning.append("  * WARNING: Update/delete without WHERE clause will affect all rows.")
                if "select *" in query_lower:
                    reasoning.append("  * PERFORMANCE NOTE: Consider specifying only needed columns instead of SELECT *.")
                result = self.__execute_query()
        else:
            reasoning.append(f"- Error: Invalid operation '{self.operation}'.")
            result = {"error": f"Invalid operation: {self.operation}. Use 'list_tables', 'read_table', or 'execute_query'."}
        
        # Include reasoning in output if verbose mode is on
        if self.verbose_reasoning:
            result["reasoning"] = reasoning
        
        return json.dumps(result, default=str, indent=2)

if __name__ == "__main__":
    # Test listing tables
    list_tables_tool = SQLQueryTool(operation="list_tables")
    print("Listing tables:")
    print(list_tables_tool.run())
    
    # Read table test code
    read_table_tool = SQLQueryTool(
        operation="read_table",
        table_name="[Staging].[dbo].[Account]",
        limit=1
    )
    print("\nReading table:")
    print(read_table_tool.run())

    
    # Uncomment to test executing a query
    execute_query_tool = SQLQueryTool(
        operation="execute_query",
        query="SELECT TOP 5 * FROM [Staging].[dbo].[Account]"
    )
    print("\nExecuting query:")
    print(execute_query_tool.run()) 
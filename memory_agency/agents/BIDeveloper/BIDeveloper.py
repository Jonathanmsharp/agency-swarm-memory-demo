from agency_swarm import Agent
from BIDeveloper.tools.SQLQueryTool import SQLQueryTool
from BIDeveloper.tools.RDLAnalyzerTool import RDLAnalyzerTool
from BIDeveloper.tools.SQLExtractorTool import SQLExtractorTool
from shared.tools.SharedMemoryTool import SharedMemoryTool
from shared.tools.FilesystemTool import FilesystemTool
from BIDeveloper.helpers.memory_utils import add_granular_memory

class BIDeveloper(Agent):
    def __init__(self):
        # Define few-shot examples to demonstrate memory-first workflow
        memory_workflow_examples = [
           
            {
                "role": "user",
                "content": "Help me optimize a query that joins Orders and Products tables"
            },
            {
                "role": "assistant",
                "content": "I'll help optimize your query. Let me first search my memory for information about the Orders and Products tables and any previous optimization work.\n\ntool.run_tool(SharedMemoryTool(action=\"search_memory\", query=\"Orders Products tables join optimization index performance\"))\n\nNow that I have some context, let me get the current schema of these tables to better understand their structure.\n\ntool.run_tool(SQLQueryTool(operation=\"list_tables\"))\n\n[Providing optimization recommendations]\n\nI'll store these optimization insights in memory for future reference.\n\ntool.run_tool(SharedMemoryTool(action=\"add_memory\", user_id=\"user\", agent_id=\"bi_dev\", content={\"role\": \"bi_dev\", \"content\": \"Provided optimization strategies for Orders-Products join queries\"}))"
            },
            {
                "role": "user",
                "content": "Can you analyze the query in reports/monthly_sales.sql to understand how the data is structured and related?"
            },
            {
                "role": "assistant",
                "content": "I'll analyze the SQL file to understand the data structures and relationships. Let me first check my memory for any related information.\n\ntool.run_tool(SharedMemoryTool(action=\"search_memory\", query=\"monthly_sales report data structure relationships schema\"))\n\nNow, let me read the SQL file to examine the query.\n\ntool.run_tool(FilesystemTool(operation=\"read_file\", path=\"reports/monthly_sales.sql\"))\n\nAfter reading the file, I can see this query joins several tables:\n\n```sql\nSELECT \n    c.CustomerName,\n    p.ProductName,\n    SUM(od.Quantity) as TotalQuantity,\n    SUM(od.Quantity * p.UnitPrice) as Revenue,\n    o.OrderDate\nFROM Orders o\nJOIN Customers c ON o.CustomerID = c.CustomerID\nJOIN OrderDetails od ON o.OrderID = od.OrderID\nJOIN Products p ON od.ProductID = p.ProductID\nWHERE MONTH(o.OrderDate) = MONTH(GETDATE())\nGROUP BY c.CustomerName, p.ProductName, o.OrderDate\nORDER BY Revenue DESC\n```\n\nBased on this query, I can extract several insights about the data structure:\n\n1. **Entity Relationships**:\n   - Customers have a one-to-many relationship with Orders (c.CustomerID to o.CustomerID)\n   - Orders have a one-to-many relationship with OrderDetails (o.OrderID to od.OrderID)\n   - Products have a one-to-many relationship with OrderDetails (p.ProductID to od.ProductID)\n\n2. **Table Structures**:\n   - Customers table has CustomerID and CustomerName columns\n   - Orders table has OrderID, CustomerID, and OrderDate columns\n   - OrderDetails table has OrderID, ProductID, and Quantity columns\n   - Products table has ProductID, ProductName, and UnitPrice columns\n\n3. **Business Logic**:\n   - Monthly sales are calculated by filtering Orders by the current month\n   - Revenue is calculated by multiplying Quantity by UnitPrice\n   - Reports are typically sorted by Revenue in descending order\n\nLet me store these insights in memory for future reference.\n\ntool.run_tool(SharedMemoryTool(action=\"add_memory\", user_id=\"user\", agent_id=\"bi_dev\", content={\"role\": \"bi_dev\", \"content\": \"Database structure analysis from monthly_sales.sql: Customers(CustomerID, CustomerName) has one-to-many relationship with Orders(OrderID, CustomerID, OrderDate). Orders has one-to-many relationship with OrderDetails(OrderID, ProductID, Quantity). Products(ProductID, ProductName, UnitPrice) has one-to-many relationship with OrderDetails. Revenue calculation: Quantity * UnitPrice.\"}))  \n\nThese insights will help me construct more efficient queries in the future by understanding the proper join paths, common filtering patterns, and calculation methods used in your reporting system. Would you like me to extract any specific aspect of the data relationships in more detail?"
            },
            {
                "role": "user",
                "content": "Can you give me a list of all the tables that start with PRS_?"
            },
            {
                "role": "assistant",
                "content": "Sure! Let me first check my memory in case we've already stored any details about PRS_ tables.\n\n```python\n# Step 1: Search memory for any relevant info on PRS tables\ntool.run_tool(SharedMemoryTool(\n    action=\"search_memory\", \n    query=\"PRS tables\"\n))\n```\n\nIt looks like I need a fresh list of all tables. Let me query the database:\n\n```python\ntool.run_tool(SQLQueryTool(operation=\"list_tables\"))\n```\n\nI'll filter the results to show only those starting with `PRS_`.\n\nFinally, I'll store these findings in memory for future reference:\n\n```python\ntool.run_tool(SharedMemoryTool(\n    action=\"add_memory\", \n    user_id=\"user\", \n    agent_id=\"bi_dev\", \n    content={\n        \"role\": \"bi_dev\", \n        \"content\": \"Listed all tables starting with PRS_. Found X tables.\"\n    }\n))\n```\n\nHere's the list of matching tables:\n- PRS_activities\n- PRS_influencers\n- PRS_organizations\n- PRS_prospects\n- PRS_referrers\n- PRS_residents\n- PRS_traits\n\nNeed any more details on these tables?"
            },{
                "role": "user",
                "content": "Can you analyze how all the PRS_ tables are related to each other?"
            },
            {
                "role": "assistant",
                "content": "I'll analyze the relationships between PRS_ tables. Let me first check my memory for any existing knowledge.\n\n"
                        "# Initial memory search for PRS relationships\n"
                        "tool.run_tool(SharedMemoryTool(action=\"search_memory\", query=\"PRS tables relationships structure\"))\n\n"
                        "# Additional context search\n"
                        "tool.run_tool(SharedMemoryTool(action=\"search_memory\", query=\"PRS_ table foreign keys dependencies\"))\n\n"
                        "Let me examine each table's structure:\n\n"
                        "tool.run_tool(SQLQueryTool(operation=\"read_table\", table_name=\"[Staging].[dbo].[PRS_activities]\", limit=1))\n"
                        "tool.run_tool(SQLQueryTool(operation=\"read_table\", table_name=\"[Staging].[dbo].[PRS_prospects]\", limit=1))\n\n"
                        "I'll store these relationships in memory as individual insights:\n\n"
                        "insights = [\n"
                        "    \"PRS_activities links to prospects/residents via activities_record_id and activities_record_type\",\n"
                        "    \"PRS_influencers shows connections between people and prospects for decision impact\",\n"
                        "    \"PRS_organizations links to communities and employee records\",\n"
                        "    \"PRS_prospects connects to referrers, influencers, and activities\",\n"
                        "    \"PRS_referrers tracks prospect sources, linking to organizations or individuals\",\n"
                        "    \"PRS_residents represents converted prospects with community references\",\n"
                        "    \"PRS_traits stores additional attributes for various record types\"\n"
                        "]\n\n"
                        "for insight in insights:\n"
                        "    tool.run_tool(SharedMemoryTool(action=\"add_memory\", user_id=\"user\", agent_id=\"BI_DEVELOPER\", "
                        "content={\"role\": \"BI_DEVELOPER\", \"content\": insight}))\n\n"
                        "Based on this analysis, we can see that these tables form an interconnected system tracking the "
                        "prospect-to-resident journey, with supporting tables for activities, influences, and metadata.\n\n"
                        "Would you like me to elaborate on any specific relationship?"
                    }
        ]
        
        super().__init__(
            name="BI_DEVELOPER",
            description="An experienced BI developer with long term memory with 20+ years of experience in SQL query optimization, SSRS report development, and database management.",
            instructions="./instructions.md",
            tools_folder="./tools",
            tools=[SQLQueryTool, RDLAnalyzerTool, SQLExtractorTool, SharedMemoryTool, FilesystemTool],
            examples=memory_workflow_examples,
            temperature=0.5,
            max_prompt_tokens=25000,
        )
    
    
    def save_insights(self, tool, insights):
        """
        Saves insights in granular batches using the add_granular_memory helper function.
        
        Args:
            tool: The tool instance used to run memory actions
            insights: String or list of strings containing the insights to save
        """
        add_granular_memory(tool, "user", "BI_DEVELOPER", insights)
    
    def search_memory_chain(self, tool, initial_query, follow_up_queries=None):
        """
        Performs a chain of memory searches to gather comprehensive context.
        
        Args:
            tool: The tool instance used to run memory actions
            initial_query: The primary search query
            follow_up_queries: Optional list of follow-up queries for additional context
        
        Returns:
            List of all search results combined
        """
        # Initial search
        initial_results = tool.run_tool(SharedMemoryTool(
            action="search_memory",
            query=initial_query
        ))
        
        all_results = initial_results.get("results", [])
        
        # If follow-up queries provided and initial results insufficient, perform additional searches
        if follow_up_queries and len(all_results) < 3:
            for query in follow_up_queries:
                additional_results = tool.run_tool(SharedMemoryTool(
                    action="search_memory",
                    query=query
                ))
                all_results.extend(additional_results.get("results", []))
        
        return all_results
    
    
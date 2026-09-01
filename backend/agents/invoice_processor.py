from deepagents import create_deep_agent
from agents.line_item_extractor import line_item_extractor
from agents.tax_categorizer import tax_categorizer
from models.invoice_extraction import InvoiceExtraction
from agents.tools.tax_tools import calculate_line_item_taxes
from agents.tools.invoice_tools import put_invoice_extraction, convert_to_extraction_result
from langgraph.checkpoint.memory import InMemorySaver # This does not work long term because lambdas are serverless. Just putting it here so we remember to implement a cloud based one.
from langchain_quickjs import CodeInterpreterMiddleware
from deepagents.backends import FilesystemBackend
from pathlib import Path
from agents.constants import INVOICE_AGENT_WORKSPACE_DIR



INVOICE_PROCESSOR_SYSTEM_PROMPT = """
You are an expert invoice processor.

You will receive an invoice ID and do the following:
1. Delegate line item extraction the the line item extractor sub agent.
2. Give the extracted line items to the tax categorizer agent to categorzie each line item by its tax code.
3. Pass the categorized line items from the tax_categorizer to the calculate_line_item_taxes tool to calculate and return line items with tax.
4. Pass the list of TaxedLineItems and the invoice id from the calculate_line_item_taxes tool to conver_to_extraction_result to create the final Invoice Extraction.
5. Persist the final extraction rseult using put_invoice_extraction_tool.
6. Reply with the extraction result.
If an invoice id is not provided, reply only with "Please provide an invoice id."
Do not assist the user with any other queries.
"""

checkpointer = InMemorySaver() # Again, does not work for follow ups in serverless


INVOICE_AGENT_WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
agent_backend = FilesystemBackend(root_dir=str(INVOICE_AGENT_WORKSPACE_DIR), virtual_mode=True)


invoice_processor = create_deep_agent(
    model="openai:gpt-5.5",
    system_prompt=INVOICE_PROCESSOR_SYSTEM_PROMPT,
    tools=[calculate_line_item_taxes, put_invoice_extraction, convert_to_extraction_result],
    subagents=[
        line_item_extractor,
        tax_categorizer
    ],
    response_format=InvoiceExtraction,
    checkpointer=checkpointer,
    middleware=[CodeInterpreterMiddleware()], # Not explicitly instructing it to use this, but it may choose to.
    backend=agent_backend # Sub agents inherit this - line_item_extractor is the one that needs it for downloaded invoice.
)
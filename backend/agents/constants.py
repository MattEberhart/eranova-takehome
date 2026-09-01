from pathlib import Path
INVOICE_AGENT_WORKSPACE_DIR = Path("/tmp/invoice-agent")

# Luna for processor, just following system prompt order really
# Terra for doing the real work of extracting and categorizing
# Sorry for using 5.5 for so long. $.20 an invoice was crazy expensive, didn't realize newer models were cheaper till now.
processor_model = "openai:gpt-5.6-luna"
extractor_model = "openai:gpt-5.6-terra"
tax_categorizer_model = "openai:gpt-5.6-terra"
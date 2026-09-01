# Eranova Invoice Ingestion Agent

## Task
Build an agentic invoice processor that extracts line items from documents of varying form factors, correlates the line items to their appropriate tax categories, and calculates tax per line item and total for the invoice. Create a React front end, AWS resources, and GitHub actions to deploy.

## Stack
- NextJS Static Web App, deployed to S3, served by CloudFront
- Lambda Functions for creating, listing, and processing invoices
- API Gateway to route traffic to lambdas and handle CORS
- S3 to store the invoice documents uploaded by users
- DynamoDB tables: First to store document metadata, second to store extraction results
- CloudFormation for IaC to provision resources, push the latest NextJS package to S3, and package and deploy the python to the lambdas.

## Web App
- Upload Invoice button opens UploadModal. 
- UploadModal gives a file picker and an "Upload" button
- Upload button calls a lambda to get a pre authed upload url then uploads the document. The lambda wrote invoice metadata like id, s3 key, upload time, and status to dynamo

- List of Documents is fetched from a list_invoices lambda
- Each row is actually a button to be clicked to reveal details like extraction results and source document

## Lambdas
- create_invoice - writes invoice metadata to track the file and processing status. Returns a pre authed upload url. Called by HttpApi
- list_invoices - fetches and returns the list of invoice metadatas for the home page. The service class limits to 10. Need to add some pagination and filtering and orderin eventually. Called by HttpApi.
- process_invoice - marks the invoice as processing. Invokes a langchain agent which extracts, categorizes, taxes, and persists line items to dynamo db. Triggered by uploads to the invoice s3 bucket. 
- get_invoice - gets a single invoice. not currently used. Will turn it into or replace it with get_invoice_details which will get the document url and extraction info. Called by HttpApi.
- health - just returns ok. Wrote this while I was setting up the IaC to prove bits were deployed.

## Agents
I used LangChain deep agents sdk for the agentic extraction/categorization. Each agent uses response_format and pydantic classes to enforce extraction formats. The main agent utilizes sub agents for extraction and categorization as well as tools for apply tax and persisting. I made use of CodInterpreterMiddleware as well so that the agent will process line items programatically and not require the LLM to remember each record. The lambda is setting a thread id that I am passing to the main agent. Each extraction should be traced in LangSmith. For follow ups, I need to implement a remote checkpointer. Will come in handy if I implement HITL.

- invoice_processor is the main agent. The process_invoice lambda invokes it and passes an invoice id. It immediately passes the id to the line item extractor agent to extract line items. Then it feeds the line items to the categorizer sub agent to categorize. Then it uses it's tools to deterministically apply and persist appropriate tax amounts based on those categories.
- line_item_extractor has just a tool to get the invoice s3 url. I am relying heavily on the model and deep agent harness to extract line items based on system prompt and pydantic response format. Excited to see how this goes and learn how to improve it.
- tax_categorizer has no tools. The categories and their description are injectred to the system prompt. I did give it a code interpreter so that it can programatically categorize each line item - the system prompt uses the magic "Workflow" word to force this.

Extra Note: I extended some and wrote specific model classes for certain use cases. The idea was to force the model's hand when it extracted data. For example rather than allow it to write the final Extraction object when it extracts line items, I force it to write a custom object which is a list of LineItems. And this LineItem doesn't include tax or tax amount, just the fields I expecte the model to find. Feels like there is probably a better way to do that because I feel I have too many of the same-looking model classes.
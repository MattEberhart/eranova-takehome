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
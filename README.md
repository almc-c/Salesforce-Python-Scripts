# Salesforce-Python-Scripts
various scripts for interacting with salesforce from python

# filesExtractRunner.py

This python script is designed to export in bulk the "files" saved against records, file libraries or your personal files.  
In Salesforce, these are stored in the ContentVersion object from the Salesforce org.  https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_contentversion.htm
The provided script is designed to fetch files by Title only.
The running user should have the Query All Files permission assigned https://help.salesforce.com/s/articleView?id=000381258&type=1
Set the authentication in the .env file and run it from the command line.
Files will be downloaded and placed into a salesforce_downloads folder in the working directory.

**Example use case:** Extract pdf files for use in AI training or as knowledge for RAG.  You could use these data to train a Document AI OCR model on your particular documents.  You could also export these documents as predetermined "knowledge" for feeding into a RAG search system for their text extraction, chunking and embedding in a vector database.  https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview

Ideas for future improvement: 
* Use of the MD5 Checksum to verify file transfer integrity.
* Specify the WHERE clause in .env file or through param query string.
* Allowing to define the LinkedEntity or ContentWorkspace (aka Library) from where the files should be retrieved.  May or may not be used in conjunction with file title.

To install: It is recommended to use a virtual environment then git clone into your local directly.  
To install dependencies: python -m pip install -r requirements.txt 
To run: 
* Update the .env-sample as .env with your specific environment variables for the target org.  
* Update the WHERE clause for the specific files needed.  A subquery such as ```WHERE FirstPublishedLocationId in (SELECT id FROM Account)``` will also work for files loaded against a record. 

Help me develop a battery knowledge search webapp. It can use hybird search with vector search. The knowledge is stored in bunch of .html file. The webapp is for internal use. 
You can use streamlit. You can generate some sample data related to battery engineering. The data is about lithium-ion battery used for consumer electronics.

## Environment Variables

The following environment variables should be set in the `.env` file:

- `EMBEDDING_MODEL`: The name of the sentence transformer model to use for embeddings (default: "all-MiniLM-L6-v2")
- // ... other existing variables ...

## Metadata Structure

The indexing process now stores metadata for each chunk in the following format:

## Regenerating Data and Index

To quickly regenerate sample data and rebuild the index, you can use the provided shell script:

1. Ensure the script is executable:
   ```
   chmod +x regenerate_data_and_index.sh
   ```

2. Run the script:
   ```
   ./regenerate_data_and_index.sh
   ```

This script will generate new sample data and create a fresh index based on that data.
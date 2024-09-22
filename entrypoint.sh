#!/bin/bash

# Exit on any error
set -e

# Step 1: Download the dataset using wget and extract it
DATASET_URL="https://huggingface.co/datasets/Morson/mimic_ex/resolve/main/dataset.zip?download=true"
LOCAL_DIR="/datasets/mimiciii"
ZIP_FILE="dataset.zip"

# Ensure the dataset directory exists
mkdir -p $LOCAL_DIR

echo "Downloading dataset from: $DATASET_URL..."
wget -O $ZIP_FILE $DATASET_URL

echo "Extracting dataset to $LOCAL_DIR..."
unzip -o $ZIP_FILE -d $LOCAL_DIR

# Clean up the zip file
rm $ZIP_FILE

# Step 2: Prepare Neo4j Database
echo "Populating Neo4j Database..."
# Ensure Neo4j environment variables are set
if [ -z "$NEO4J_URI" ] || [ -z "$NEO4J_PASSWORD" ]; then
  echo "Error: Neo4j environment variables are not set."
  exit 1
fi

# Example Python script to construct and populate the graph (replace with your actual script)
echo "Running graph construction script..."
python run.py -dataset mimic_ex -data_path $LOCAL_DIR -grained_chunk True -ingraphmerge True -construct_graph True
echo "Graph construction completed."

# Step 3: Execute the command passed via the Docker Compose file
# Correcting the module path to /app/api/main.py
echo "Executing command: uvicorn api.main:app $@"

# Correctly execute the uvicorn command with the updated module path
exec uvicorn api.main:app "$@"

#!/bin/bash

# Directory for models
MODEL_DIR="./ads_model"
TOKENIZER_DIR="./ads_tokenizer"

# Check if model directories exist
if [ ! -d "$MODEL_DIR" ]; then
    echo "Model directory does not exist. Downloading from S3..."
    # Install AWS CLI
    pip install awscli
    # Download model directory from S3
    aws s3 cp s3://fyp-project-adsmodel/ads_model/ $MODEL_DIR --recursive
else
    echo "Model directory exists. Skipping download."
fi

if [ ! -d "$TOKENIZER_DIR" ]; then
    echo "Tokenizer directory does not exist. Downloading from S3..."
    # Download tokenizer directory from S3
    aws s3 cp s3://fyp-project-adsmodel/ads_tokenizer/ $TOKENIZER_DIR --recursive
else
    echo "Tokenizer directory exists. Skipping download."
fi

#!/bin/bash

echo "Before downloading the Unsplash Lite Dataset, you must agree to the Unsplash Lite Dataset Terms."
echo "The full terms can be found at: https://github.com/unsplash/datasets/blob/master/TERMS.md"
echo
read -p "Do you agree to the Unsplash Lite Dataset Terms? (yes/no): " agreement

if [[ ! "$agreement" =~ ^[Yy][Ee]?[Ss]?$ ]]; then
    echo "You must agree to the terms to download the dataset."
    exit 1
fi

# Create dataset directory if it doesn't exist
mkdir -p ./dataset

# Download the dataset
echo "Downloading Unsplash Lite dataset..."
curl -L https://unsplash.com/data/lite/latest -o ./dataset/unsplash_lite.zip

# Unzip the dataset
echo "Extracting dataset..."
unzip ./dataset/unsplash_lite.zip -d ./dataset

# Clean up the zip file
rm ./dataset/unsplash_lite.zip

echo "Setup complete! Dataset is ready in ./dataset directory"


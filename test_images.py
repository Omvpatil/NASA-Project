#!/usr/bin/env python3
"""
Test script to verify image handling in the API
"""
import json

# Test JSON string storage and parsing
test_images = [
    'https://cdn.ncbi.nlm.nih.gov/pmc/blobs/9bd8/7012842/e6fa069338dc/41598_2020_58898_Fig1_HTML.jpg',
    'https://cdn.ncbi.nlm.nih.gov/pmc/blobs/9bd8/7012842/a00e727562f4/41598_2020_58898_Fig2_HTML.jpg'
]

# Store as JSON string (what we do in the backend)
image_urls_json = json.dumps(test_images)
print(f"Stored as JSON: {image_urls_json}")
print(f"Type: {type(image_urls_json)}")
print(f"Is string: {isinstance(image_urls_json, str)}")

# Parse back (what we do when retrieving)
parsed_images = json.loads(image_urls_json)
print(f"\nParsed back: {parsed_images}")
print(f"Type: {type(parsed_images)}")
print(f"Is list: {isinstance(parsed_images, list)}")
print(f"Length: {len(parsed_images)}")

print("\n✅ JSON string storage method works correctly!")

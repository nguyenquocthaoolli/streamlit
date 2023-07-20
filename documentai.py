import os
from typing import Iterator, MutableSequence, Optional, Sequence, Tuple

import google.cloud.documentai_v1 as docai
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "a")
API_LOCATION = os.getenv("API_LOCATION", "us")

assert PROJECT_ID, "PROJECT_ID is undefined"
assert API_LOCATION in ("us", "eu"), "API_LOCATION is incorrect"

# Test processors
document_ocr_display_name = "document-ocr"
form_parser_display_name = "form-parser"

test_processor_display_names_and_types = (
    (document_ocr_display_name, "OCR_PROCESSOR"),
    (form_parser_display_name, "FORM_PARSER_PROCESSOR"),
)

def get_client() -> docai.DocumentProcessorServiceClient:
    client_options = {"api_endpoint": f"{API_LOCATION}-documentai.googleapis.com"}
    return docai.DocumentProcessorServiceClient(client_options=client_options)

def get_parent(client: docai.DocumentProcessorServiceClient) -> str:
    return client.common_location_path(PROJECT_ID, API_LOCATION)

def get_client_and_parent() -> Tuple[docai.DocumentProcessorServiceClient, str]:
    client = get_client()
    parent = get_parent(client)
    return client, parent

def fetch_processor_types() -> MutableSequence[docai.ProcessorType]:
    client, parent = get_client_and_parent()
    response = client.fetch_processor_types(parent=parent)

    return response.processor_types

def print_processor_types(processor_types: Sequence[docai.ProcessorType]):
    def sort_key(pt):
        return (not pt.allow_creation, pt.category, pt.type_)

    sorted_processor_types = sorted(processor_types, key=sort_key)
    data = processor_type_tabular_data(sorted_processor_types)
    headers = next(data)
    colalign = next(data)

    print(tabulate(data, headers, tablefmt="pretty", colalign=colalign))
    print(f"→ Processor types: {len(sorted_processor_types)}")

def processor_type_tabular_data(
    processor_types: Sequence[docai.ProcessorType],
) -> Iterator[Tuple[str, str, str, str]]:
    def locations(pt):
        return ", ".join(sorted(loc.location_id for loc in pt.available_locations))

    yield ("type", "category", "allow_creation", "locations")
    yield ("left", "left", "left", "left")
    if not processor_types:
        yield ("-", "-", "-", "-")
        return
    for pt in processor_types:
        yield (pt.type_, pt.category, f"{pt.allow_creation}", locations(pt))

def create_processor(display_name: str, type: str) -> docai.Processor:
    client, parent = get_client_and_parent()
    processor = docai.Processor(display_name=display_name, type_=type)

    return client.create_processor(parent=parent, processor=processor)
    
separator = "=" * 80
for display_name, type in test_processor_display_names_and_types:
    print(separator)
    print(f"Creating {display_name} ({type})...")
    try:
        create_processor(display_name, type)
    except Exception as err:
        print(err)
print(separator)
print("Done")
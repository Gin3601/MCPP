def extract_output_urls(result: dict) -> list[str]:
    if not isinstance(result, dict):
        raise RuntimeError(f"Invalid result type: {type(result)}")

    data = result.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(f"Missing 'data' in result: {result}")

    outputs = data.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise RuntimeError(f"No outputs returned: {result}")

    return outputs

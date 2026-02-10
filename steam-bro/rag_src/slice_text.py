def slice_text(slices):
    """Convert time slices to readable text format"""
    slice_texts = []
    for slice in slices:
        # Format: "User: message (timestamp)"
        texts = [f"{msg[0]}: {msg[1]}" for msg in slice]
        slice_text = "\n".join(texts)
        slice_texts.append(slice_text)
    return slice_texts
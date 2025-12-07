def slice_text(slices):
    slice_texts = []
    for slice in slices:
        texts = [f"{msg[0] , msg[1] , msg[2]}" for msg in slice]
        slice_text = " ".join(texts)
        slice_texts.append(slice_text)
    return slice_texts
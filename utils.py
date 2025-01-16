import os

def get_unique_path(base_path):
    directory = os.path.dirname(base_path)
    filename = os.path.basename(base_path)
    name, ext = os.path.splitext(filename)

    # Remove any existing numbers from name
    base_name = name.split("-")[0]

    counter = 1
    while True:
        new_path = os.path.join(directory, f"{base_name}-{counter:03d}{ext}")
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def get_resized_filename(input_path):
    """Generate output filename by adding '-resized' before extension"""
    base, ext = os.path.splitext(input_path)
    return f"{base}-resized{ext}"
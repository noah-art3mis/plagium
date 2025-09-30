def get_data(path: str) -> str:
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: Could not find file - {e}")

from pathlib import Path

def matchDir(direc: Path, file: Path) -> bool:
    """
    Checks if 'direc' is an ancestor directory of 'file' 
    (or if 'file' resides within 'direc').
    """
    try:
        resolved_direc = direc.resolve()
        resolved_file = file.resolve()
    except (FileNotFoundError, RuntimeError):
        # Fallback if paths cannot be fully resolved
        resolved_direc = direc.absolute()
        resolved_file = file.absolute()

    # Ensure 'direc' is not a file (if it exists)
    if resolved_direc.exists() and resolved_direc.is_file():
        raise NotADirectoryError("[utils-matchDir] 'direc' must be a directory path.")

    # is_relative_to checks if resolved_file is inside resolved_direc (or is equal to it)
    try:
        return resolved_file.is_relative_to(resolved_direc)
    except ValueError:
        return False

if __name__== "__main__":
    print(mathDir(Path(".batata/another_batata/"), Path(".batata/another_batata/teste.txt")))

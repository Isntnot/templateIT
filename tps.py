import os
from pathlib import Path
CURRENT_DIR = Path(os.getcwd())
def getTPS(path: Path = CURRENT_DIR) -> list[Path]:
    if path.is_file():
        raise Exception(f"[TPS-getTPS] Tried to search for tps in a file \"{path}\"")
    matches = path.glob("template.txt")
    return list(matches)


def getTemplateTps(path: Path) -> dict[Path, Path]:
    # Fixed missing parentheses ()
    if not path.is_file():
        raise Exception(f"[TPS-getTemplateTps] Tried to get template data from a folder \"{path}\"")
    
    d2p: dict[Path, Path] = {} 
    tps_dir = path.parent  # The directory containing the template.txt file
    
    try:
        with open(str(path), "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line_stripped = line.strip()
                # Skip empty lines or comments
                if not line_stripped or line_stripped.startswith("#"):
                    continue
                
                if "=" not in line_stripped:
                    raise ValueError(f"Missing '=' separator on line {i}")
                
                folder_str, file_str = line_stripped.split("=", 1)
                
                # Clean up whitespace
                folder = Path(folder_str.strip())
                template_file = Path(file_str.strip())
                
                # Resolve relative paths against the .tps file's directory
                if not folder.is_absolute():
                    folder = (tps_dir / folder).resolve()
                else:
                    folder = folder.resolve()
                    
                if not template_file.is_absolute():
                    template_file = (tps_dir / template_file).resolve()
                else:
                    template_file = template_file.resolve()
                
                if folder.exists() and folder.is_file():
                    raise Exception(f"[TPS-getTemplateTps] Tried to use a file as a folder on line {i}: \"{line_stripped}\"")
                
                if template_file.exists() and template_file.is_dir():
                    raise Exception(f"[TPS-getTemplateTps] Tried to use a folder as a template on line {i}: \"{line_stripped}\"")
                
                d2p[folder] = template_file
                
        return d2p
        
    except FileNotFoundError:
        raise Exception(f"[TPS-getTemplateTps] File not found {path}")
    except ValueError as e:
        raise Exception(f"[TPS-getTemplateTps] Malformed syntax on line {i}: \"{line.strip()}\" ({e})")

from pathlib import Path
def createFile(file: Path,
               source: str,
               substitute: bool =  False
             ):
    if file.exists() and not substitute:
        #print("[utils-fileCopy] Warning: Trying to substitute a existing File")
        raise FileExistsError("[utils-createFile] File already exists")
    with open(str(file), "w") as f:
        f.write(source)

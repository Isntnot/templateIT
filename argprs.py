import argparse
from pathlib import Path 
parser = argparse.ArgumentParser(
                    prog='TemplateIT',
                    description='A program that acts as a substitute for formatter (the obsidian plugin)',
                    )
parser.add_argument("filename", type=Path)
parser.add_argument("-s", "--substitute")


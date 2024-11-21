import sys
from VMTranslator import VMTranslator

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>.vm")
        sys.exit(1)

    input_file: str = sys.argv[1]
    output_file: str = input_file.replace(".vm", ".asm")

    translator = VMTranslator(input_file, output_file)
    translator.translate()
    translator.close()
    print(f"Translated {input_file} to {output_file}")

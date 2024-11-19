import sys
from Assembler import Assembler


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <input.asm> <output.hack>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    assembler = Assembler(input_file, output_file)
    assembler.assemble()
    print(f"Assembly complete. Output written to {output_file}")


if __name__ == "__main__":
    main()

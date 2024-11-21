from typing import Union


class CodeWriter:
    def __init__(self, output_file: str) -> None:
        self.output_file = open(output_file, 'w')
        self.function_name: Optional[str] = None
        self.label_counter: int = 0

    def write_arithmetic(self, command: str) -> None:
        if command == "add":
            self.output_file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D+M\n")
        elif command == "sub":
            self.output_file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=M-D\n")
        elif command == "neg":
            self.output_file.write("@SP\nA=M-1\nM=-M\n")
        elif command == "eq":
            label_true = f"EQ_TRUE_{self.label_counter}"
            label_end = f"EQ_END_{self.label_counter}"
            self.label_counter += 1
            self.output_file.write(
                f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{label_true}\nD;JEQ\n@{label_end}\n0;JMP\n")
            self.output_file.write(
                f"({label_true})\n@SP\nA=M-1\nM=-1\n@{label_end}\n0;JMP\n")
            self.output_file.write(f"({label_end})\n")
        elif command == "gt":
            label_true = f"GT_TRUE_{self.label_counter}"
            label_end = f"GT_END_{self.label_counter}"
            self.label_counter += 1
            self.output_file.write(
                f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{label_true}\nD;JGT\n@{label_end}\n0;JMP\n")
            self.output_file.write(
                f"({label_true})\n@SP\nA=M-1\nM=-1\n@{label_end}\n0;JMP\n")
            self.output_file.write(f"({label_end})\n")
        elif command == "lt":
            label_true = f"LT_TRUE_{self.label_counter}"
            label_end = f"LT_END_{self.label_counter}"
            self.label_counter += 1
            self.output_file.write(
                f"@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D\n@{label_true}\nD;JLT\n@{label_end}\n0;JMP\n")
            self.output_file.write(
                f"({label_true})\n@SP\nA=M-1\nM=-1\n@{label_end}\n0;JMP\n")
            self.output_file.write(f"({label_end})\n")
        elif command == "and":
            self.output_file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D&M\n")
        elif command == "or":
            self.output_file.write("@SP\nAM=M-1\nD=M\nA=A-1\nM=D|M\n")
        elif command == "not":
            self.output_file.write("@SP\nA=M-1\nM=!M\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        if command == "C_PUSH":
            if segment == "constant":
                self.output_file.write(
                    f"@{index}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "local":
                self.output_file.write(
                    f"@LCL\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "argument":
                self.output_file.write(
                    f"@ARG\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "this":
                self.output_file.write(
                    f"@THIS\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "that":
                self.output_file.write(
                    f"@THAT\nD=M\n@{index}\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "pointer":
                self.output_file.write(
                    f"@{3+index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "temp":
                self.output_file.write(
                    f"@{5+index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "static":
                self.output_file.write(
                    f"@{16+index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        elif command == "C_POP":
            if segment == "local":
                self.output_file.write(
                    f"@LCL\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "argument":
                self.output_file.write(
                    f"@ARG\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "this":
                self.output_file.write(
                    f"@THIS\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "that":
                self.output_file.write(
                    f"@THAT\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "pointer":
                self.output_file.write(
                    f"@{3+index}\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "temp":
                self.output_file.write(
                    f"@{5+index}\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")
            elif segment == "static":
                self.output_file.write(
                    f"@{16+index}\nD=A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n")

    def close(self) -> None:
        self.output_file.close()

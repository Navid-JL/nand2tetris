from Parser import Parser
from Code import CodeWriter


class VMTranslator:
    def __init__(self, input_file: str, output_file: str) -> None:
        self.parser = Parser(input_file)
        self.code_writer = CodeWriter(output_file)

    def translate(self) -> None:
        while self.parser.has_more_commands():
            self.parser.advance()
            command_type = self.parser.command_type()

            if command_type == "C_ARITHMETIC":
                self.code_writer.write_arithmetic(self.parser.arg1())
            elif command_type == "C_PUSH" or command_type == "C_POP":
                self.code_writer.write_push_pop(
                    command_type, self.parser.arg1(), self.parser.arg2())  # type: ignore

    def close(self) -> None:
        self.code_writer.close()

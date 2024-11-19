from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable


class Assembler:
    def __init__(self, input_file: str, output_file: str) -> None:
        self.input_file = input_file
        self.output_file = output_file
        self.symbol_table = SymbolTable()
        self.next_variable_address = 16  # Start assigning variables at RAM[16]
        self.code = Code()

    def assemble(self) -> None:
        """Runs the two-pass assembly process."""
        self._first_pass()
        self._second_pass()

    def _first_pass(self) -> None:
        """First pass: add label symbols to the symbol table."""
        parser = Parser(self.input_file)
        rom_address = 0

        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == "L_COMMAND":
                symbol = parser.symbol()
                self.symbol_table.add_entry(symbol, rom_address)
            else:
                rom_address += 1

    def _second_pass(self) -> None:
        """Second pass: translate commands into binary and write to output file."""
        parser = Parser(self.input_file)
        binary_output = []

        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == "A_COMMAND":
                symbol = parser.symbol()
                if symbol.isdigit():
                    address = int(symbol)
                else:
                    if not self.symbol_table.contains(symbol):
                        self.symbol_table.add_entry(
                            symbol, self.next_variable_address)
                        self.next_variable_address += 1
                    address = self.symbol_table.get_address(symbol)
                binary_output.append(f"{address:016b}")
            elif parser.command_type() == "C_COMMAND":
                binary_output.append(
                    "111" + self.code.comp(parser.comp()) + self.code.dest(
                        parser.dest()) + self.code.jump(parser.jump())
                )

        with open(self.output_file, "w") as file:
            file.writelines("\n".join(binary_output) + "\n")

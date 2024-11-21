from typing import List, Optional


class Parser:
    def __init__(self, input_file: str) -> None:
        self.input_file: str = input_file
        self.lines: List[str] = []
        self.current_line: int = -1
        self._read_file()

    def _read_file(self) -> None:
        with open(self.input_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("//"):
                    self.lines.append(line)

    def has_more_commands(self) -> bool:
        return self.current_line + 1 < len(self.lines)

    def advance(self) -> None:
        if self.has_more_commands():
            self.current_line += 1

    def command_type(self) -> Optional[str]:
        command = self.lines[self.current_line]
        if command.startswith("push"):
            return "C_PUSH"
        elif command.startswith("pop"):
            return "C_POP"
        elif command.startswith("label"):
            return "C_LABEL"
        elif command.startswith("goto"):
            return "C_GOTO"
        elif command.startswith("if-goto"):
            return "C_IF"
        elif command.startswith("function"):
            return "C_FUNCTION"
        elif command.startswith("return"):
            return "C_RETURN"
        elif command.startswith("call"):
            return "C_CALL"
        elif command.startswith("add") or command.startswith("sub") or command.startswith("neg") or \
                command.startswith("eq") or command.startswith("gt") or command.startswith("lt") or \
                command.startswith("and") or command.startswith("or") or command.startswith("not"):
            return "C_ARITHMETIC"
        return None

    def arg1(self) -> str:
        command = self.lines[self.current_line].split()
        if self.command_type() == "C_ARITHMETIC":
            return command[0]
        return command[1]

    def arg2(self) -> Optional[int]:
        command = self.lines[self.current_line].split()
        if self.command_type() in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return int(command[2])
        return None

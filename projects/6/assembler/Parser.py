from typing import List, Optional


class Parser:
    def __init__(self, filename: str) -> None:
        """Opens the input file and initializes the parser."""
        with open(filename, "r") as file:
            self.lines: List[str] = file.readlines()
        self.current_command: Optional[str] = None
        self.current_index: int = -1
        self.commands: List[str] = self._preprocess(self.lines)

    def _preprocess(self, lines: List[str]) -> List[str]:
        """Removes whitespace and comments from the input lines."""
        processed: List[str] = []
        for line in lines:
            # Remove inline comments and trim whitespace
            line = line.split("//")[0].strip()
            if line:  # Skip empty lines
                processed.append(line)
        return processed

    def has_more_commands(self) -> bool:
        """Returns true if there are more commands in the input."""
        return self.current_index + 1 < len(self.commands)

    def advance(self) -> None:
        """Moves to the next command in the input."""
        if self.has_more_commands():
            self.current_index += 1
            self.current_command = self.commands[self.current_index]

    def command_type(self) -> str:
        """Returns the type of the current command."""
        if self.current_command is None:
            raise ValueError("No current command to determine type.")
        if self.current_command.startswith("@"):
            return "A_COMMAND"  # Address command
        elif self.current_command.startswith("(") and self.current_command.endswith(")"):
            return "L_COMMAND"  # Label command
        else:
            return "C_COMMAND"  # Compute command

    def symbol(self) -> str:
        """Returns the symbol or decimal of the current A or L command."""
        if self.current_command is None:
            raise ValueError("No current command to extract symbol.")
        if self.command_type() == "A_COMMAND":
            return self.current_command[1:]  # Strip '@'
        elif self.command_type() == "L_COMMAND":
            return self.current_command[1:-1]  # Strip '(' and ')'
        raise ValueError("symbol() called on a non-A/L command")

    def dest(self) -> str:
        """Returns the destination mnemonic of the current C command."""
        if self.current_command is None:
            raise ValueError("No current command to extract destination.")
        if "=" in self.current_command:
            return self.current_command.split("=")[0]
        return ""

    def comp(self) -> str:
        """Returns the computation mnemonic of the current C command."""
        if self.current_command is None:
            raise ValueError("No current command to extract computation.")
        command = self.current_command
        if "=" in command:
            command = command.split("=")[1]
        if ";" in command:
            command = command.split(";")[0]
        return command

    def jump(self) -> str:
        """Returns the jump mnemonic of the current C command."""
        if self.current_command is None:
            raise ValueError("No current command to extract jump.")
        if ";" in self.current_command:
            return self.current_command.split(";")[1]
        return ""

# Standard
from __future__ import annotations
from typing import NoReturn, TYPE_CHECKING
from dataclasses import dataclass
from enum import StrEnum, auto
import sys

# Local
from utils.general import render_tabs
if TYPE_CHECKING:
    from utils.module import Module


class ErrorType(StrEnum):
    """Type of a error"""

    SYNTAX = "Syntax Error"
    STRING = "String Error"
    INCLUDE = "Include Error"
    VALUE = "Value Error"
    REFERENCE = "Reference Error"
    INSTRUCTION = "Instruction Error"


@dataclass(frozen=True, slots=True)
class Error:
    """Error with location, type and message"""

    module: Module
    line: int
    type: ErrorType
    message: str

    def report(self) -> str:

        result = "-" * 80 + "\n"
        result += "FATAL ERROR".center(80) + "\n"
        result += "-" * 80 + "\n\n"
        result += f'File "{self.module.path}" | Line {self.line + 1}'.center(80) + "\n\n"

        if 0 < self.line - 6:
            result += "         ...\n\n"
        for i in range(self.line - 6, self.line + 7):
            if 0 <= i < len(self.module.lines):
                code = render_tabs(self.module.lines[i].replace("\n", ""))
                result += f"{'>>>' if i == self.line else '   '} {i + 1:<5}{code}\n"
        if self.line + 7 < len(self.module.lines):
            result += "\n         ...\n"

        result += "\n" + "-" * 80 + "\n\n"
        result += f"{self.type.value}:\n\n{self.message}\n\n"
        result += "-" * 80

        return result

    def exit(self) -> NoReturn:

        print(self.report())

        sys.exit(1)


from llama_index.core.tools import FunctionTool
from typing import Callable

class ToolManager:
    def create_tool(self, callback: Callable, description: str) -> "FunctionTool":
        return FunctionTool.from_defaults(
            callback, description=description
        )

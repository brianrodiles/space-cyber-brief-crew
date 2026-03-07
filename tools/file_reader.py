import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class FileReaderInput(BaseModel):
    directory: str = Field(default="sources", description="Path to source directory.")


class FileReaderTool(BaseTool):
    name: str = "Source Document Reader"
    description: str = "Reads all .txt and .md files from a directory and returns their contents."
    args_schema: Type[BaseModel] = FileReaderInput

    def _run(self, directory: str = "sources") -> str:
        supported = (".txt", ".md")
        results = []
        if not os.path.isdir(directory):
            return f"Error: Directory '{directory}' not found."
        source_files = sorted([
            f for f in os.listdir(directory)
            if f.endswith(supported) and not f.startswith(".")
        ])
        if not source_files:
            return f"No source documents found in '{directory}'."
        for filename in source_files:
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                results.append(
                    f"=== SOURCE: {filename} ===\n{content}\n=== END: {filename} ===\n"
                )
            except Exception as e:
                results.append(
                    f"=== SOURCE: {filename} ===\nError: {e}\n=== END: {filename} ===\n"
                )
        return f"Found {len(source_files)} source document(s):\n\n" + "\n".join(results)

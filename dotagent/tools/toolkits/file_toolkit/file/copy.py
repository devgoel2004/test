import shutil
from typing import Optional, Type

from pydantic import BaseModel, Field

from dotagent.tools.basetool import BaseTool
from dotagent.tools.toolkits.file_toolkit.file.utils import (
    INVALID_PATH_TEMPLATE,
    BaseFileToolMixin,
    FileValidationError,
)


class FileCopyInput(BaseModel):
    """Input for CopyFileTool."""

    source_path: str = Field(..., description="Path of the file to copy")
    destination_path: str = Field(..., description="Path to save the copied file")


class CopyFileTool(BaseFileToolMixin, BaseTool):
    name: str = "copy_file"
    args_schema: Type[BaseModel] = FileCopyInput
    description: str = "Create a copy of a file in a specified location"

    def run(
        self,
        source_path: str,
        destination_path: str,
    ) -> str:
        try:
            source_path_ = self.get_relative_path(source_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(
                arg_name="source_path", value=source_path
            )
        try:
            destination_path_ = self.get_relative_path(destination_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(
                arg_name="destination_path", value=destination_path
            )
        try:
            shutil.copy2(source_path_, destination_path_, follow_symlinks=False)
            return f"File copied successfully from {source_path} to {destination_path}."
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(
        self,
        source_path: str,
        destination_path: str
    ) -> str:
        # TODO: Add aiofiles method
        raise NotImplementedError
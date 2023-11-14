from typing import List, Optional
from pydantic import BaseModel


class Note(BaseModel):
    """
    A representation of a note.
    Attributes:
        title (str): The title of the note.
        content (str): The content or body of the note.
        tags (Optional[List[str]]): A list of tags associated with the note
        (optional).
    """

    title: str
    content: str
    tags: Optional[List[str]] = None


class NotesStructure(BaseModel):
    """
    Represents the structure of notes.
    Attributes:
        notes (List[Note]): A list of Note objects.
    """

    notes: List[Note]

    class Config:
        """
        Configuration options for the NotesStructure schema.

        Attributes:
            validate_assignment (bool): If True, validation is applied
            during assignment.
        """
        validate_assignment = True


def build_dto_by_schema(
        title: str, content: str, tags: List[str]
) -> dict:
    """
    Builds and returns a dictionary based on the NotesStructure schema.
    :param title: The title of the note.
    :param content: The content or body of the note.
    :param tags: A list of tags associated with the note.
    :return: A dictionary representing the NotesStructure schema.
    """
    note = Note(title=title, content=content, tags=tags)
    return NotesStructure(notes=[note]).model_dump()

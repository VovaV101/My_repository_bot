from typing import List

from tabulate import tabulate

from bot_helper.record import RecordAlreadyExistsException, \
    RecordWasNotFoundException
from bot_helper.save_data.save_on_disk import SaveAddressBookOnDisk
from bot_helper.notes.notes_data_strcture \
    import build_dto_by_schema, Note


class NotesBook:
    def __init__(self, data_save_tool: SaveAddressBookOnDisk):
        """
        Initialize a NotesBook instance.
        :param data_save_tool: An instance of SaveAddressBookOnDisk for data
        saving.
        """
        self.data_save_tool = data_save_tool

    @staticmethod
    def input_error_notes(func: callable) -> callable:
        """
        Decorator that wraps the function to handle possible errors.
        :param func: Function that should be wrapped.
        :return: Wrapped function.
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except RecordAlreadyExistsException:
                return f"Note already exists, try to use an unique title. " \
                       f"Params: {kwargs}. Changes were not applied."
            except RecordWasNotFoundException:
                return f"Note was not found. Params: {kwargs}."

        return wrapper

    @staticmethod
    def _note_exists(*, title: str, existing_data: dict) -> bool:
        """
        Check that note exists in the existing data by title.
        :param title: Exact match of title used to find a note in an array of
        data.
        :param existing_data: Data structure used to search for a note by the
        specified title.
        :return: True if the note was found by title, False otherwise.
        """
        return any(
            note['title'] == title for note in existing_data.get("notes", [])
        )

    def _read_existing_data(self) -> dict:
        """
        Read existing data from the specified path.
        :return: A dictionary containing existing data.
        """
        return self.data_save_tool.read_info(path=self.data_save_tool.address)

    @input_error_notes
    def add_note(
            self, *, title: str, content: str, tags: List[str] | list = None
    ) -> str:
        """
        Add a new note with the specified title, content and tags.
        :param title: The title of the note.
        :param content: The content of the note.
        :param tags: A list of tags associated with the note.
        :return: A message indicating the success or failure of the operation.
        """
        existing_data = self._read_existing_data()
        record_notes = build_dto_by_schema(
            title=title, content=content, tags=tags
        )

        if self._note_exists(title=title, existing_data=existing_data):
            raise RecordAlreadyExistsException

        existing_data.setdefault("notes", [])
        existing_data["notes"].append(record_notes.get("notes")[0])

        self.data_save_tool.save_info(
            path=self.data_save_tool.address,
            data=existing_data
        )
        return f"Note with title '{title}' added successfully."

    @input_error_notes
    def delete_note(self, *, title: str) -> str:
        """
        Delete a note with the specified title.
        :param title: The title of the note to be deleted.
        :return: A message indicating the success or failure of the operation.
        """
        existing_data = self._read_existing_data()
        if not self._note_exists(title=title, existing_data=existing_data):
            raise RecordWasNotFoundException
        # Find the index of the note with the specified title
        index_to_remove = next(
            (idx for idx, note in enumerate(existing_data["notes"]) if
             note.get("title") == title),
            None
        )
        if index_to_remove is not None:
            # Remove the note by the found index
            del existing_data["notes"][index_to_remove]
            self.data_save_tool.save_info(
                path=self.data_save_tool.address, data=existing_data
            )
            return f"Note with title '{title}' deleted successfully."
        raise RecordWasNotFoundException

    def show_all_notes(self) -> str:
        """
        Retrieve and display information about all notes.
        :return: A formatted string containing information about all notes.
        """
        existing_data = self.data_save_tool.read_info(
            path=self.data_save_tool.address
        )
        if not existing_data or not existing_data.get("notes"):
            return "Notes book is empty. " \
                   "Should be at least one note to display."

        notes_list = []
        for idx, note_data in enumerate(existing_data.get("notes", []),
                                        start=1):
            note = Note(**note_data)
            note_info = [
                idx,
                note.title,
                note.content,
                ", ".join(note.tags or []),
            ]
            notes_list.append(note_info)

        headers = ["N", "Title", "Content", "Tags"]
        formatted_table = tabulate(
            notes_list,
            headers=headers,
            tablefmt="fancy_grid",
            colalign=("center", "left", "left", "left"),
            numalign="center"
        )
        return f"\nAll Notes:\n{formatted_table}\n"

    @staticmethod
    def _sort_notes(
            *, data: list, sort_key: str, reverse: bool = False
    ) -> list | str:
        """
        Sort a list of notes based on the specified key and order.
        :param data: The list of notes to be sorted.
        :param sort_key: The key by which to sort the notes.
        :param reverse: A boolean indicating whether to sort in descending
        order.
        :return: A sorted list of notes or an error message if the sort key is
        invalid.
        """
        if "desc" in sort_key:
            reverse = True
        sort_keys = {
            'title_asc': lambda note: note[0],
            'title_desc': lambda note: note[0],
            'tag_count_asc':
                lambda note: len(note[2].split(', ')) if note[2] else 0,
            'tag_count_desc':
                lambda note: len(note[2].split(', ')) if note[2] else 0,
        }
        if (sort_function := sort_keys.get(sort_key)) is None:
            return f"Invalid sort_key: {sort_key}."
        return sorted(
            data, key=sort_function, reverse=reverse
        )

    def search_note(
            self, *, query: str, sort_by: str = 'title_asc',
    ) -> str:
        """
        Search for notes based on the specified query and sorting parameters.
        :param query: The search query. Param should not include spaces.
        :param sort_by: The key by which to sort the search results.
        :return: A formatted string containing the search results.
        """
        existing_data = self._read_existing_data()

        found_notes = []
        for note_data in existing_data.get("notes", []):
            note = Note(**note_data)
            if query.lower() in note.title.lower() or (note.tags and any(
                    query.lower() in tag.lower() for tag in note.tags
            )):
                found_notes.append([
                    note.title,
                    note.content,
                    ", ".join(note.tags or []),
                ])

        tag_description = f"Tag '{query}'" if query.startswith(
            "tag_") else f"Query '{query}'"

        if found_notes:
            # Sort the notes
            sorted_notes = self._sort_notes(
                data=found_notes, sort_key=sort_by
            )
            # Return error text if notes were not found
            if isinstance(sorted_notes, str):
                return sorted_notes

            headers = ["Title", "Content", "Tags"]
            formatted_table = tabulate(
                sorted_notes,
                headers=headers,
                tablefmt="fancy_grid",
                colalign=("left", "left", "left"),
                numalign="center"
            )
            return f"Search Result by {tag_description} (Sorted by " \
                   f"{sort_by}):\n{formatted_table}\n"
        else:
            return f"\nNotes were not found by {tag_description}.\n"

    @input_error_notes
    def add_tags_by_title(self, *, title: str, tags: List[str]) -> str:
        """
        Add tags to a note with the specified title.
        :param title: The title of the note to which tags will be added.
        :param tags: A list of tags to be added.
        :return: A message indicating the success or failure of the operation.
        """
        existing_data = self._read_existing_data()

        note_found = False
        unique_tags_added = []
        existing_tags = []

        for idx, note_data in enumerate(existing_data.get("notes", [])):
            note = Note(**note_data)
            if note.title == title:
                note_found = True
                existing_tags = note.tags or []

                # Add only unique tags
                for tag in tags:
                    if tag not in existing_tags:
                        existing_tags.append(tag)
                        unique_tags_added.append(tag)

                existing_data["notes"][idx]["tags"] = existing_tags

        if not note_found:
            raise RecordWasNotFoundException

        self.data_save_tool.save_info(
            path=self.data_save_tool.address,
            data=existing_data
        )

        if unique_tags_added:
            return f"Tags added successfully to the note with title " \
                   f"'{title}'.\n" \
                   f"Added Tags: {', '.join(unique_tags_added)}\n" \
                   f"Existing Tags: {', '.join(existing_tags)}"

        return f"All specified tags already exist for the note with title " \
               f"'{title}'.\nExisting Tags: {', '.join(existing_tags)}"

    @input_error_notes
    def change_note_title(self, title: str, new_title: str) -> str:
        """
        Change the title of a note.
        :param title: The current title of the note.
        :param new_title: The new title for the note.
        :return: A message indicating the success or failure of the operation.
        """
        existing_data = self._read_existing_data()

        if not self._note_exists(title=title, existing_data=existing_data):
            raise RecordWasNotFoundException

        if self._note_exists(title=new_title, existing_data=existing_data):
            raise RecordAlreadyExistsException

        for note_data in existing_data["notes"]:
            if note_data["title"] == title:
                note_data["title"] = new_title
                break

        self.data_save_tool.save_info(
            path=self.data_save_tool.address,
            data=existing_data
        )

        return f"Note title changed from '{title}' to " \
               f"'{new_title}' successfully."

    @input_error_notes
    def change_note_content(self, *, title: str, new_content: str) -> str:
        """
        Change the content of a note.
        :param title: The title of the note.
        :param new_content: The new content for the note.
        :return: A message indicating the success or failure of the operation.
        """
        existing_data = self._read_existing_data()

        if not self._note_exists(title=title, existing_data=existing_data):
            raise RecordWasNotFoundException

        for note_data in existing_data["notes"]:
            if note_data["title"] == title:
                note_data["content"] = new_content
                break

        self.data_save_tool.save_info(
            path=self.data_save_tool.address,
            data=existing_data
        )

        return f"Note content changed for '{title}' successfully."


if __name__ == '__main__':
    notes = NotesBook(
        data_save_tool=SaveAddressBookOnDisk(address="notes_data.json")
    )

    print(notes.show_all_notes())

    # Add notes
    rec1 = notes.add_note(
        title="title_1",
        content="some string",
        tags=["tag_1", "tag_2"]
    )
    print(rec1)
    rec2 = notes.add_note(
        title="title_2",
        content="some string 2",
        tags=["tag_3", "tag_4", "tag_5", "tag_6"]
    )
    print(rec2)
    rec3 = notes.add_note(
        title="title_3",
        content="some string 3"
    )
    print(rec3)

    # Test change note content
    change_content_result = notes.change_note_content(
        title="title_2", new_content="Updated content for title_2."
    )
    print(change_content_result)

    # Test change content for non-existing note
    change_content_nonexistent_result = notes.change_note_content(
        title="nonexistent title", new_content="New content."
    )
    print(change_content_nonexistent_result)

    # Test change note title with existing new title
    change_title_existing_result = notes.change_note_title(
        title="title_3", new_title="title_2"
    )
    print(change_title_existing_result)

    # Test change note title with non-existing new title
    change_title_result = notes.change_note_title(
        title="title_2", new_title="new_title_2"
    )
    print(change_title_result)

    # Show all notes after changing title
    all_notes_after_change_title = notes.show_all_notes()
    print(all_notes_after_change_title)

    # Sort by default (ASC by title)
    search_result_default = notes.search_note(query="titl")
    print(search_result_default)

    # Sort by DESC title
    search_result_desc_title = notes.search_note(
        query="titl", sort_by="title_desc"
    )
    print(search_result_desc_title)

    # Sort by ASC number of existing tags (many to low)
    search_result_asc_tags_count = notes.search_note(
        query="titl", sort_by="tag_count_asc"
    )
    print(search_result_asc_tags_count)

    # Sort by DESC number of existing tags (low to many)
    search_result_desc_tags_count = notes.search_note(
        query="titl", sort_by="tag_count_desc"
    )
    print(search_result_desc_tags_count)

    # Show all notes
    all_notes = notes.show_all_notes()
    print(all_notes)

    # Test search by title
    search_result_by_title = notes.search_note(query="title_2")
    print(search_result_by_title)

    # Test search by tag
    search_result_by_tag = notes.search_note(query="tag_3")
    print(search_result_by_tag)

    # Test search by nonexistent data
    search_result_by_nonexistent = notes.search_note(query="nonexistent")
    print(search_result_by_nonexistent)

    # Delete notes (testing)
    delete_rec1 = notes.delete_note(title="title_1")
    print(delete_rec1)

    delete_rec3 = notes.delete_note(title="nonexistent title")
    print(delete_rec3)

    # Show all notes
    all_notes = notes.show_all_notes()
    print(all_notes)

    # Test add tags by title
    add_tags_result = notes.add_tags_by_title(
        title="title_2", tags=["new_tag_1", "new_tag_2", "tag_1+"]
    )
    print(add_tags_result)

    add_tags_result2 = notes.add_tags_by_title(
        title="title_3", tags=["second_add_tag_new"]
    )
    print(add_tags_result2)

    add_tags_nonexistent = notes.add_tags_by_title(
        title="nonexistent", tags=["tag_should_not_exist"]
    )
    print(add_tags_nonexistent)

    # Show all notes after adding tags
    all_notes_after_adding_tags = notes.show_all_notes()
    print(all_notes_after_adding_tags)

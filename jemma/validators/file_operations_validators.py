

def validate_file_read_range(first_line: int, last_line: int) -> bool:

    """
    Ensure that the model has outputted valid offsets,bottom must be >= top offset 

    Args:

        top_offset: Where to start reading the file from
        bottom offset: Where to stop reading the file from
    """

    return last_line > first_line
    


def validate_section_replacement(original_section: str, model_recalled_original_section: str) -> bool:
    """
    A harsh, token‑expensive validator for section replacement.
    Ensures the model correctly recalled the section it is about to replace.

    Args:
        original_section: The original content of the file (on disk) within the edit offsets.
        model_recalled_original_section: The model's recall of the section it intends to replace.

    Returns:
        True if both strings are identical, False otherwise.
    """
    return original_section == model_recalled_original_section


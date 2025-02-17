

def markdown_to_blocks(markdown):
    split_string = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return split_string



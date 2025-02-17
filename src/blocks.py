import re

def markdown_to_blocks(markdown):
    split_string = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return split_string

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return "heading"
    elif re.match(r"^```(?:.|\n)*```$", block):
        return "code"
    elif re.match(r"^(> .*(\n>? .*)*)$", block):
        return "quote"
    elif re.match(r"^([-*] .+(\n[-*] .+)*)$", block):
        return "unordered_list"   
    elif all(line.startswith(str(i + 1) + ". ") for i, line in enumerate(block.split("\n"))):
        return "ordered_list"
    return "paragraph"
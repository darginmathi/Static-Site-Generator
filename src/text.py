import re
from textnode import TextType, TextNode


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)] 
    
    if any(extract_markdown_images(node.text) for node in nodes):
        nodes = split_nodes_image(nodes) 
    if any(extract_markdown_links(node.text) for node in nodes):
        nodes = split_nodes_link(nodes)
    
    if '`' in text:
        nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    if '**' in text:
        nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    if '*' in text:
        nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not delimiter:
        raise Exception("delimiter must be a string")
    
    for node in old_nodes:
        if node.text == "":
            new_nodes.append(node)
            continue
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
                    #does not work on nested delimiters
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    if not any(extract_markdown_images(node.text) for node in old_nodes):
        return old_nodes
    
    new_nodes = []
    for node in old_nodes:
        image = extract_markdown_images(node.text)
        if not image:
            new_nodes.append(node)
        else:
            image_alt, image_url = image[0]
            markdown = f"![{image_alt}]({image_url})"
            sections = node.text.split(markdown, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                
            if sections[1] != "":
                remaining_nodes = split_nodes_image([TextNode(sections[1], TextType.TEXT)])
                new_nodes.extend(remaining_nodes)
                
    return new_nodes


def split_nodes_link(old_nodes):
    if not any(extract_markdown_links(node.text) for node in old_nodes):
        return old_nodes
    
    new_nodes = []
    for node in old_nodes:
        link = extract_markdown_links(node.text)
        if not link:
            new_nodes.append(node)
        else:
            link_text, link_url = link[0]
            markdown = f"[{link_text}]({link_url})"
            sections = node.text.split(markdown, 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                
            if sections[1] != "":
                remaining_nodes = split_nodes_link([TextNode(sections[1], TextType.TEXT)])
                new_nodes.extend(remaining_nodes)
                
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


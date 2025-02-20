from blocks import markdown_to_html_node
from blocks import markdown_to_blocks
import os


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        if block.startswith('# '):
            return block.lstrip("#").strip()    
    raise Exception("no heading found")
            
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        content = file.read()
    with open(template_path, "r") as file:
        template = file.read()
        
    html_node = markdown_to_html_node(content)
    title = extract_title(content)
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())
    
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html_page)
    
    
def generate_page_recursive(content_dir_path, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    
    for item in os.listdir(content_dir_path):
        src_path = os.path.join(content_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)
    
        if os.path.isfile(src_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(src_path, template_path, dest_path)
            
        elif os.path.isdir(src_path):
            generate_page_recursive(src_path, template_path, dest_path)
            

import os
import shutil

from copy_dir import copy_dir, clear_dir
from generatepage import generate_page, extract_title


main_dir = os.path.dirname(__file__)
public_dir_path = os.path.join(main_dir, "..", "public")
static_dir_path = os.path.join(main_dir, "..", "static") 
content_index = os.path.join(main_dir, "..", "content", "index.md")
template = os.path.join(main_dir, "..", "template.html")
public_index = os.path.join(main_dir, "..", "public", "index.html")


def main():
    clear_dir(public_dir_path)
    copy_dir(static_dir_path, public_dir_path)
    generate_page(content_index, template, public_index)
    
    

        


            
                    
    
    


if __name__ == "__main__":
    main()    
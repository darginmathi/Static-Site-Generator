import os
import shutil

from copy_dir import copy_dir


main_dir = os.path.dirname(__file__)
public_dir_path = os.path.join(main_dir, "..", "public")
static_dir_path = os.path.join(main_dir, "..", "static") 


def main():
    clear_dir(public_dir_path)
    copy_dir(static_dir_path, public_dir_path)
    
    
def clear_dir(dir):
    if os.path.exists(dir):
        print("Folder already exists!")
        try:
            shutil.rmtree(dir, ignore_errors=False, onerror=None)
            print("removed public dir")
        except Exception as e:
            print(f"error while removing dir{e}")
    try:        
        os.makedirs(dir)
        print(f'dir created: {dir}')
    except Exception as e:
        print(f"error while creating dir{e}")
        


            
                    
    
    


if __name__ == "__main__":
    main()    
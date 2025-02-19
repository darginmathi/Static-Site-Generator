import os
import shutil


def copy_dir(from_dir, to_dir):
    os.makedirs(to_dir, exist_ok=True)
    
    for item in os.listdir(from_dir):
        src_path = os.path.join(from_dir, item)
        dst_path = os.path.join(to_dir, item)
        
        if os.path.isfile(src_path):
            try:
                shutil.copy(src_path, dst_path)
                print(f"copying {src_path} to {dst_path}")
            except Exception as e:
                print(f"Error copying {src_path} to {dst_path}: {e}")            
        elif os.path.isdir(src_path):
            try:
                copy_dir(src_path, dst_path)
                print(f"{src_path} is a dir") 
            except Exception as e:
                print(f"error processing dir {src_path}; {e}")
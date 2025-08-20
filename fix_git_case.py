#!/usr/bin/env python3
import subprocess
import os

def fix_git_case_sensitivity():
    """Fix Git case sensitivity issues by using git mv"""
    
    # Get all files tracked by git in docs/
    result = subprocess.run(['git', 'ls-files', 'docs/'], 
                          capture_output=True, text=True)
    files = result.stdout.strip().split('\n')
    
    renamed_count = 0
    errors = []
    
    for file_path in files:
        if not file_path:
            continue
            
        # Get the directory and filename
        dir_path = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        lower_filename = filename.lower()
        
        # Check if filename has uppercase letters
        if filename != lower_filename:
            new_path = os.path.join(dir_path, lower_filename) if dir_path else lower_filename
            
            try:
                # Use git mv to rename (handles case sensitivity properly)
                cmd = ['git', 'mv', file_path, new_path]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    renamed_count += 1
                    print(f"Renamed: {file_path} -> {new_path}")
                else:
                    # If direct rename fails due to case conflict, use temp name
                    temp_path = new_path + '.tmp'
                    subprocess.run(['git', 'mv', file_path, temp_path], check=True)
                    subprocess.run(['git', 'mv', temp_path, new_path], check=True)
                    renamed_count += 1
                    print(f"Renamed (via temp): {file_path} -> {new_path}")
                    
            except subprocess.CalledProcessError as e:
                errors.append(f"Error renaming {file_path}: {str(e)}")
    
    print(f"\n[SUCCESS] Renamed {renamed_count} files")
    if errors:
        print(f"\n[WARNING] Errors encountered:")
        for error in errors[:10]:
            print(f"  - {error}")
    
    return renamed_count, errors

if __name__ == "__main__":
    count, errors = fix_git_case_sensitivity()
    
    if count > 0:
        print("\nFiles have been renamed. Please commit the changes.")
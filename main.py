import subprocess
import sys
from pathlib import Path
import os

# Function to get the size of a directory
def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

# Get a list of installed packages and their versions
installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list'], text=True)

# Split the output into lines and ignore the first two lines (header)
package_lines = installed_packages.split('\n')[2:]

for line in package_lines:
    if line:
        package_name, version = line.split()[:2]
        package_info = subprocess.check_output([sys.executable, '-m', 'pip', 'show', package_name], text=True)
        # Extract the location of the package
        for info_line in package_info.split('\n'):
            if info_line.startswith('Location:'):
                location = info_line.split(':', 1)[1].strip()
                package_path = Path(location) / package_name
                # Calculate the size of the package directory
                size = get_dir_size(package_path)
                print(f"{package_name} ({version}) - {size/1024/1024:.2f} MB")
                break

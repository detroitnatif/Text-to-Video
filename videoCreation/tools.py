import os
import re
import pkg_resources  # Part of setuptools

def list_imports_with_versions(folder_path):
    # Regular expressions to match import statements
    import_re = re.compile(r'^import (\S+)')
    from_import_re = re.compile(r'^from (\S+) import')

    # Dictionary to store package names and their versions
    packages = {}

    # Walk through the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a Python file
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        # Check for direct import statements
                        match = import_re.match(line)
                        if match:
                            package_name = match.group(1).split('.')[0]
                            packages[package_name] = None  # Initialize with None

                        # Check for from...import statements
                        match = from_import_re.match(line)
                        if match:
                            package_name = match.group(1).split('.')[0]
                            packages[package_name] = None  # Initialize with None

    # Attempt to find versions for each package
    for package in packages.keys():
        try:
            version = pkg_resources.get_distribution(package).version
            packages[package] = version
        except pkg_resources.DistributionNotFound:
            # Package might be a standard library or not installed in the current environment
            packages[package] = "Not Found or Standard Library"

    return packages

# Example usage
folder_path = '/Users/tylerklimas/Desktop/openaisandbox/videoCreation'  
packages_with_versions = list_imports_with_versions(folder_path)
for package, version in packages_with_versions.items():
    print(f"{package}: {version}")


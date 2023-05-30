import pkg_resources
import pip

# Read the packages from the requirements file
with open('requirements.txt', 'r') as f:
    required_packages = f.read().splitlines()

# Remove any inline comments
required_packages = [pkg.split('#')[0].strip() for pkg in required_packages]

# Remove version specifiers if any
required_packages = [pkg.split('==')[0].split('>=')[0].split('<=')[0] for pkg in required_packages]

# Get a list of all installed packages
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

# Print versions of packages
for package in required_packages:
    if package in installed_packages:
        print(f'{package}=={installed_packages[package]}')
    else:
        print(f'{package} is not installed')

import re

def parse_requirements(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    requirements = []
    for line in lines:
        match = re.match(r'(\S+)>=(\S+)', line)
        if match:
            package, version = match.groups()
            requirements.append(f"{package}=={version}")
    return requirements

def write_requirements(file_path, requirements):
    with open(file_path, 'w') as file:
        for requirement in requirements:
            file.write(requirement + '\n')

if __name__ == "__main__":
    requirements = parse_requirements('requirements.txt')
    write_requirements('requirements-oldest.txt', requirements)
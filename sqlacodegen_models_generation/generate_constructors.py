import re


def add_constructors(file_content):
    # Define the regex pattern to match class definitions
    class_pattern = re.compile(r'class (\w+)[\s\S]*?(?=\bclass \w+|$)')

    # Find all class matches in the file content
    class_matches = class_pattern.finditer(file_content)

    # Iterate over the matches and add constructors
    modified_content = file_content

    for match in class_matches:
        class_name = match.group(1)
        fields = get_class_fields(file_content, class_name)
        constructor_code = f'\n    def __init__(self, {", ".join(f"{field}Param" for field in fields)}):'
        for field in fields:
            constructor_code += "\n\t\t" + f"self.{field}={field}Param"
        constructor_code += '\n'
        modified_content = modified_content.replace(match.group(), match.group() + constructor_code, 1)

    return modified_content


def get_class_fields(file_content, class_name):
    # Define the regex pattern to match class fields
    class_content_pattern = re.compile(rf'class {class_name}\(Base\):(.*?)class', re.DOTALL)

    file_content += "\nclass"

    # Find the first match for class definition
    class_match = class_content_pattern.search(file_content)
    fields = []
    # Extract the fields from the matched class definition
    if class_match:
        fields_str = class_match.group(1)
        field_pattern = re.compile(r'(\w+)\s*=\s*Column')
        fields_matches = field_pattern.finditer(fields_str)
        for match in fields_matches:
            field = match.group(1)
            fields.append(field)
        fields.remove("id")
        return fields
    else:
        return []


def main(input_file, output_file):
    # Read the content of the input Python file
    with open(input_file, 'r') as file:
        file_content = file.read()

    # Add constructors to the class definitions
    modified_content = add_constructors(file_content)

    # Save the modified content to a new file
    with open(output_file, 'w') as output_file:
        output_file.write(modified_content)


if __name__ == "__main__":
    # Specify the input and output file names
    input_file_name = "models.py"
    output_file_name = "output_file_with_constructors.py"

    # Run the main function
    main(input_file_name, output_file_name)

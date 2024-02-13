import subprocess

# Replace the following with your MySQL credentials and database information
mysql_connection_string = "mysql://janko:janko@192.168.1.200:3306/prvaBaza"

# Run sqlacodegen as a subprocess and capture the output
command = f"sqlacodegen {mysql_connection_string}"

output = subprocess.check_output(command, shell=True, text=True)

# Save the generated code to a file
with open("models.py", "w") as file:
    file.write(output)

from generate_constructors import main

main("models.py", "models.py")

print("Models generated and saved to models.py")

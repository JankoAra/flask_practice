import re

# Your input text containing the class definitions
input_text = """
class DrugaTabela(Base):
    __tablename__ = 'drugaTabela'

    id = Column(INTEGER(11), primary_key=True)
    email = Column(String(45))


class PrvaTabela(Base):
    __tablename__ = 'prvaTabela'

    id = Column(INTEGER(11), primary_key=True)
    ime = Column(String(255))
    broj = Column(INTEGER(11))
    
class
"""

# Define regular expressions for each class
druga_tabela_pattern = re.compile(r'class DrugaTabela\(Base\):(.*?)class', re.DOTALL)
prva_tabela_pattern = re.compile(r'class PrvaTabela\(Base\):(.*?)class', re.DOTALL)


# Find matches for each class in the input text
druga_tabela_match = re.search(druga_tabela_pattern, input_text)
prva_tabela_match = re.search(prva_tabela_pattern, input_text)

# Extract content for each class
druga_tabela_content = druga_tabela_match.group(1).strip() if druga_tabela_match else None
prva_tabela_content = prva_tabela_match.group(1).strip() if prva_tabela_match else None

# Print the separated content for each class
print("DrugaTabela Content:")
print(druga_tabela_content)

print("\nPrvaTabela Content:")
print(prva_tabela_content)

import os
from lexer import Lexer
from rat24f_parser import Rat24FParser

# Globals
memory_address = 9000
instr_idx = 1
sym_table = []  # Symbol table: [lexeme, memory_address, type]
instruction_table = []  # Instruction table: [index, operation, operand]

# Symbol Table Handling
def add_to_symbol_table(name, id_type):
    global memory_address
    for entry in sym_table:
        if entry[0] == name:
            return  # Identifier already exists
    sym_table.append([name, memory_address, id_type])
    memory_address += 1

# Instruction Generation
def add_instruction(op, operand=None):
    global instr_idx
    instruction_table.append([instr_idx, op, operand])
    instr_idx += 1

# Traverse the AST and generate instructions
def traverse_ast(ast):
    if ast["type"] == "declaration":
        for identifier in ast["identifiers"]:
            add_to_symbol_table(identifier, ast["data_type"])
    elif ast["type"] == "assignment":
        traverse_ast(ast["right"])
        address = next((entry[1] for entry in sym_table if entry[0] == ast["left"]), None)
        add_instruction("POPM", address)
    elif ast["type"] == "literal":
        add_instruction("PUSHI", ast["value"])
    elif ast["type"] == "identifier":
        address = next((entry[1] for entry in sym_table if entry[0] == ast["name"]), None)
        add_instruction("PUSHM", address)
    elif ast["type"] == "output":
        traverse_ast(ast["value"])
        add_instruction("STDOUT")
    elif ast["type"] == "while":
        loop_start = instr_idx
        traverse_ast(ast["condition"])
        jump_address = instr_idx
        add_instruction("JUMPZ", None)
        for stmt in ast["body"]:
            traverse_ast(stmt)
        add_instruction("JUMP", loop_start)
        instruction_table[jump_address - 1][2] = instr_idx

# Write outputs to files
def write_to_file(filename):
    with open(f"{filename}_symbol_table.txt", "w") as st_file, open(f"{filename}_instruction_table.txt", "w") as it_file:
        st_file.write("Symbol Table\n")
        st_file.writelines(f"{name}\t{addr}\t{typ}\n" for name, addr, typ in sym_table)
        it_file.write("Instruction Table\n")
        it_file.writelines(f"{idx}\t{op}\t{opd}\n" for idx, op, opd in instruction_table)

# Main program
def main():
    test_cases = [
        ("test_case_1.txt", "output_test_case_1"),
        ("test_case_2.txt", "output_test_case_2"),
        ("test_case_3.txt", "output_test_case_3")
    ]

    for input_file, output_name in test_cases:
        global memory_address, instr_idx, sym_table, instruction_table
        # Reset globals for each test case
        memory_address = 9000
        instr_idx = 1
        sym_table = []
        instruction_table = []

        with open(input_file, "r") as file:
            source_code = file.read()

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # Use Rat24FParser
        parser = Rat24FParser(tokens)
        ast = parser.parse()

        for node in ast:
            traverse_ast(node)

        write_to_file(output_name)
        print(f"Processed {input_file}, outputs written to {output_name}_symbol_table.txt and {output_name}_instruction_table.txt")

if __name__ == "__main__":
    main()

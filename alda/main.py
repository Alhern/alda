#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sys import argv
import argparse
from alda.alda_lexer import AldaLexer
from alda.alda_parser import AldaParser
from alda.alda_interpreter import AldaExecute

lexer = AldaLexer()
parser = AldaParser()
env = {}

art =''' _____  __     ____   _____    
|  _  ||  |   |    \ |  _  |  
|     ||  |__ |  |  ||     |  
|__|__||_____||____/ |__|__|   
'''


def extension_check(filename):
    if not filename.lower().endswith('.alda'):
        raise argparse.ArgumentTypeError("File extension must be .alda")
    return filename

def execute_from_file(file):
    tree = parser.parse(lexer.tokenize(file))
    AldaExecute(tree, env)


def alda_shell():
    print(art)
    print("---ALDA shell (1.0.0)---\n")
    while True:
        try:
            text = input('>> ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            AldaExecute(tree, env)


def main():
    parser = argparse.ArgumentParser(description='Welcome to the ALDA interpreter')
    parser.add_argument('-f', '--file', help='Execute program from .alda file', type=extension_check)
    parser.add_argument('-s', '--shell', action='store_true', help='Start ALDA shell')
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            print("---Now executing your ALDA file---\n")
            execute_from_file(f.read())

    if args.shell:
        alda_shell()

    if len(argv) == 1:
        parser.print_usage()
        exit(1)


if __name__ == '__main__':
    main()

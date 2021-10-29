#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import argparse
from package.binary import BinaryFile


def main(args):
    import time

         
    bfiles = [
        "DUMPS/dump004_ok.BIN", "DUMPS/dump005_ok.BIN", "DUMPS/dump000.BIN", "DUMPS/dump001.BIN", "DUMPS/dump002.BIN",
        # "DUMPS/dump003.BIN", "DUMPS/dump006.BIN", "DUMPS/dump007.BIN", "DUMPS/dump008.BIN"
    ]
    
    t = time.process_time()
    files = BinaryFile(*bfiles)
    
    if args.compare:
        error_nb = files.compare()
        t = time.process_time()-t
        print("Résultat:", files.result, "%.3f s" % t)
        print(f"Nombre d'erreur: {error_nb}")
    elif args.generator:
        error_nb = files.generate(args.output_file)
        t = time.process_time()-t
        print("Generating file terminated :)", "%.3f s" % t)
        print(f"Nombre d'erreur: {error_nb}")
    else:
        print("Erreur d'arguments")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='binary file comparator and generator.')

    # Arguments command
    parser.add_argument('-c', '--compare', action='store_true', dest='compare', help='Binary compare')
    parser.add_argument('-g', '--generator', action='store_true', dest='generator', help='Binary generator')
    parser.add_argument('-o', '--output_file', action='store', dest='output_file', type=str, default="binary_generate.bin" , help='Output file for generator')
    args = parser.parse_args()

    main(args)

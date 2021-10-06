#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import os
import binascii


class BinaryFile:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self, *args, **kwargs) -> None:
        self.bfc = list(args)
        self.lgbuf = kwargs.get('lgbuf', 16)
        self.result = False

    def compare(self):
        number = error_nb = 0
        files = [None for f in self.bfc[:4]]
        try:
            if self.get_size():
                print("SIZE OK")
                files = [open(f, "rb") for f in self.bfc[:4]]
                while True:
                    buf = [binascii.hexlify(file.read(self.lgbuf)).decode("utf8").upper() for file in files]
                    if len(buf[0]) == 0:
                        self.result = True
                        break
                    if buf[0] != buf[1] or buf[0] != buf[2] or buf[1] != buf[2]:
                        print(f"OFFSET: {self.OKGREEN}{hex(number):10}{self.ENDC}", end=" ")
                        print(self.data_color(buf[0], buf[1], buf[2], buf[3]), end=" - ")
                        print(self.data_color(buf[1], buf[0], buf[2], buf[3]), end=" - ")
                        print(self.data_color(buf[2], buf[0], buf[1], buf[3]), end=" - ")
                        print(self.data_color(buf[3], buf[0], buf[1], buf[2]))
                        error_nb += 1
                    number += 16
            [f.close() for f in files]
        except:
            for file in files:
                if file != None: file.close()
            raise IOError
        return error_nb

    def generate(self, filename):
        number = error_nb = 0
        f = open(filename, "wb")
        files = [None for f in self.bfc]
        try:
            if self.get_size():
                print("SIZE OK")
                files = [open(f, "rb") for f in self.bfc]
                while True:
                    buf = [file.read(2) for file in files]
                    if len(buf[0]) == 0:
                        self.result = True
                        break
                    max_value = max(buf, key=buf.count)
                    f.write(max_value)
            [f.close() for f in files]
        except:
            for file in files:
                if file != None: file.close()
            raise IOError
        return error_nb
    
    def data_color(self, buffer, *args):
        data = ""
        for i in range(len(buffer)):
            val = f"{buffer[i]}"
            for compare in args:
                if buffer[i] != compare[i]:
                    val = f"{self.FAIL}{buffer[i]}{self.ENDC}"
                    break
            data += val
        return data

    def get_size(self):
        for bfc in self.bfc:
            if os.path.getsize(self.bfc[0]) != os.path.getsize(bfc):
                return False
        return True


if __name__ == "__main__":
 
    import time
 
    bfiles = [
        "test3.bin", "dump001.BIN", "dump002.BIN","dump003.BIN", "dump004_ok.BIN", 
        "dump005_ok.BIN", "dump006.BIN", "dump007.BIN", "dump008.BIN", "dump009.BIN"
    ]

    t = time.process_time()
    files = BinaryFile(*bfiles)
    error_nb = files.compare()
    t = time.process_time()-t
    print("Résultat:", files.result, "%.3f s" % t)
    print(f"Nombre d'erreur: {error_nb}")

    # files.generate("test3.bin")
    # t = time.process_time()-t
    # print("Generate file terminated:", "%.3f s" % t)

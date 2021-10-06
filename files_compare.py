#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import os
import binascii


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def data_color(buffer, compare1, compare2):
    data = ""
    for i in range(len(buffer)):
        if buffer[i] == compare1[i] or buffer[i] == compare2[i]:
            data += f"{buffer[i]}"
        else:
            data += f"{bcolors.FAIL}{buffer[i]}{bcolors.ENDC}"
    return data


def compfichiers(nfc1, nfc2, nfc3, lgbuf=16):
    """Compare les 2 fichiers et renvoie True seulement s'ils ont un contenu identique"""
    f1 = f2 = f3 = None
    result = False
    number = error_nb = 0
    try:
        if os.path.getsize(nfc1) == os.path.getsize(nfc2) == os.path.getsize(nfc3):
            print("SIZE OK")
            f1 = open(nfc1, "rb")
            f2 = open(nfc2, "rb")
            f3 = open(nfc3, "rb")
            while True:
                buf1 = binascii.hexlify(f1.read(lgbuf)).decode("utf8").upper()
                if len(buf1) == 0:
                    result = True
                    break
                buf2 = binascii.hexlify(f2.read(lgbuf)).decode("utf8").upper()
                buf3 = binascii.hexlify(f3.read(lgbuf)).decode("utf8").upper()
                if buf1 != buf2 or buf1 != buf3 or buf2 != buf3:
                    print(f"OFFSET: {bcolors.OKGREEN}{hex(number)}{bcolors.ENDC}", end=" ")
                    print(data_color(buf1, buf2, buf3), end=" - ")
                    print(data_color(buf2, buf1, buf3), end=" - ")
                    print(data_color(buf3, buf1, buf2))
                    error_nb += 1
                number += 16
            f1.close()
            f2.close()
            f3.close()
    except:
        if f1 != None: f1.close()
        if f2 != None: f2.close()
        if f3 != None: f3.close()
        raise IOError
    return result, error_nb


if __name__ == "__main__":
 
    import time
 
    # 1er cas: les 2 fichiers sont identiques 
    nf1 = "1 NAND 306 tolerance1 without correction.BIN"
    nf2 = "2 NAND 306 tolerance1 without correction.BIN"
    nf3 = "3 NAND 306 tolerance1 without correction.BIN"
 
    t = time.process_time()
    result, error_nb = compfichiers(nf1, nf2, nf3)
    t = time.process_time()-t
    print("Résultat:", result, "%.3f s" % t)
    print(f"Nombre d'erreur: {error_nb}")

    t = time.process_time()-t
    print("Résultat: Erreur", "%.3f s" % t)

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
        self.manual = kwargs.get('manual', False)
        self.maxSize = os.path.getsize(self.bfc[0])
        self.result = False
        self.outFile = None 

    def compare(self):
        number = error_nb = 0
        files = [None for f in self.bfc[:4]]
        try:
            if self.get_size():
                print("SIZE OK")
                files = [open(f, "rb") for f in self.bfc[:4]]
                while True:
                    rows = [file.read(self.lgbuf) for file in files]
                    buf = [binascii.hexlify(row).decode("utf8").upper() for row in rows]
                    if len(buf[0]) == 0:
                        self.result = True
                        break
                    if len(set(buf)) != 1:
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
        buf_ascii = data_ascii = ""
        bufs = []
        self.outFile = open(filename, "wb")
        files = [None for f in self.bfc]
        try:
            if self.get_size():
                print("SIZE OK, Generating file in progress...")
                files = [open(f, "rb") for f in self.bfc]
                while True:
                    buf = [file.read(1) for file in files]
                    if len(buf[0]) == 0:
                        self.result = True
                        break
                    max_value = max(buf, key=buf.count)
                    if buf.count(max_value) < (len(buf) / 2 + 2):
                        buf_ascii += f"\rOFFSET: {self.OKGREEN}{hex(number):10}{self.ENDC} {buf.count(max_value)}*{binascii.hexlify(max_value).decode('utf8').upper()}"
                        for val in buf:
                            buf_ascii += f" - {binascii.hexlify(val).decode('utf8').upper()}"
                        data_ascii += f"{self.FAIL}{binascii.hexlify(buf[0]).decode('utf8').upper()}{self.ENDC}"
                        error_nb += 1
                        bufs.append([max_value, buf, 1])
                    else:
                        data_ascii += f"{binascii.hexlify(buf[0]).decode('utf8').upper()}"
                        bufs.append([max_value, buf, 0])
                    number += 1
                    if number % 16 == 0:
                        self._display_generate(buf_ascii, data_ascii, bufs)
                        buf_ascii = data_ascii = ""
                        bufs = []
                    if number % 65536 == 0:
                        self._progress_bar(filename, os.path.getsize(filename), bar_length=50, width=len(filename))
            [f.close() for f in files]
            print()
        except:
            for file in files:
                if file != None: file.close()
            raise IOError
        if self.outFile != None: self.outFile.close()
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

    def _progress_bar(self, name, current_size, bar_length=20, width=20):
        percent = float(current_size) / self.maxSize
        arrow = '-' * int(round(percent*bar_length) - 1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        print("\r{0: <{1}} : [{2}]{3}% ".format(name, width, arrow + spaces, int(round(percent*100))), end="", flush=True)
    
    def _display_generate(self, buf_ascii, data_ascii, bufs):
        if buf_ascii:
            print(f"{buf_ascii}  ||  {data_ascii}")
            if self.manual:
                bufs_value = [value[0] for value in bufs]
                for i, data in enumerate(bufs):
                    if data[2] == 1 and bufs_value.count(max(bufs_value, key=bufs_value.count)) > len(bufs_value) -2:
                        default_val = binascii.hexlify(data[0]).decode("utf8").upper()
                        try:
                            select = int(input(f'Select default {default_val} or 0 at {len(data[1]) - 1} : '))
                            print(binascii.hexlify(data[1][select]).decode("utf8").upper())
                            bufs[i][0] = data[1][select]
                        except ValueError:
                            print(default_val)
        self.outFile.write(b"".join([value[0] for value in bufs]))

    def get_size(self):
        for bfc in self.bfc:
            if os.path.getsize(self.bfc[0]) != os.path.getsize(bfc):
                return False
        return True

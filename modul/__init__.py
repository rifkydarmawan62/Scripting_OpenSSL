from platform import system
from subprocess import run
from colorama import Fore
from tkinter.filedialog import askdirectory as pilih_folder
from platform import system as sistem_operasi
from tkinter.messagebox import askyesno
from os.path import exists
from os import environ, remove
from getpass import getpass
from typing import Literal
from configparser import RawConfigParser

def bersihkan_layar(teks : str | None = None):
    if system() == "Windows":
        run("cls", shell = True)
    else:
        run("clear", shell = True)
    if teks:
        print(teks)
def input_kata_sandi_untuk_parameter(dh_atau_dhx : Literal["DSA", "DH", "DHX"]) -> tuple[str, str]:
    direktori_sementara, file_sementara = "", ""
    if askyesno("Konfirmasi", f"Gunakan kata sandi untuk file paramater {dh_atau_dhx}?"):
        if sistem_operasi() == "Windows":
            for kategori in environ:
                match kategori:
                    case "TEMP" | "TMP":
                        direktori_sementara = environ[kategori].replace("\\", "/")
                        break
            else:
                direktori_sementara = pilih_folder(title = "Pilih file sementara (temporary) untuk input kata sandi")
        else:
            direktori_sementara = pilih_folder(title = "Pilih file sementara (temporary) untuk input kata sandi")
        if direktori_sementara:
            file_sementara = direktori_sementara + "/temporary.bin"
            KATA_SANDI = getpass("Masukkan kata sandi : ")
            if KATA_SANDI:
                with open(file_sementara, "w") as file:
                    file.write(KATA_SANDI)
                return f"-pass file:\"{file_sementara}\" ", file_sementara
            else:
                print(f"{Fore.LIGHTRED_EX}Input kata sandi kosong!{Fore.RESET}")
                return "", file_sementara
        else:
            print(f"{Fore.LIGHTRED_EX}Folder sementara tidak dipilih!{Fore.RESET}")
            return "", file_sementara
    else:
        return "", file_sementara
def input_parameter_prima_p() -> str:
    parameter_prima_p = input("Masukkan nilai parameter prima p (default = 2048) [>= 512]: ").strip()
    if parameter_prima_p == "":
        return ""
    else:
        try:
            parameter_prima_p = int(parameter_prima_p)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
            return ""
        else:
            if parameter_prima_p >= 512:
                return f"-pkeyopt dh_paramgen_prime_len:{parameter_prima_p} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input harus lebih dari atau sama dengan 512!{Fore.RESET}")
                return ""
def input_parameter_subprima_q() -> str:
    parameter_subprima_q = input("Masukkan nilai parameter subprima q (default = 224) : ").lower().strip()
    if parameter_subprima_q == "":
        return ""
    else:
        try:
            parameter_subprima_q = int(parameter_subprima_q)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
            return ""
        else:
            if parameter_subprima_q >= 0:
                return f"-pkeyopt dh_paramgen_subprime_len:{parameter_subprima_q} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
                return ""
def input_digest():
    DIGEST = input("Pilih digest [sha1 | sha224 | sha256] : ").lower().strip()
    if DIGEST in ("sha1", "sha224", "sha256"):
        return f"-pkeyopt digest:{DIGEST} "
    elif DIGEST == "":
        return ""
    else:
        print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
        return ""
def input_indeks_g() -> str:
    indeks_g = input("Masukkan indeks untuk pembuatan kanonik dan verifikasi generator g (default = -1) [0 - 255] : ").strip()
    if indeks_g == "":
        return ""
    else:
        try:
            indeks_g = int(indeks_g)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
            return ""
        else:
            if indeks_g >= -1 and indeks_g <= 255:
                return f"-pkeyopt gindex:{indeks_g} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input harus dalam jangkauan -1 sampai 255!{Fore.RESET}")
                return ""
def hapus_file_sementara(file_sementara : str):
    if exists(file_sementara):
        print(f"{Fore.YELLOW}Menghapus file sementara ...{Fore.RESET}")
        remove(file_sementara)
        print(f"{Fore.LIGHTGREEN_EX}File sementara dihapus!{Fore.RESET}")
class kustom_raw_konfig(RawConfigParser):
    def optionxform(self, optionstr: str) -> str:
        return optionstr
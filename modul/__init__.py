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
def input_kata_sandi_untuk(argumen : Literal["parameter DSA", "parameter DH", "parameter DHX", "kunci private DH"]) -> tuple[str, str]:
    direktori_sementara, file_sementara = "", ""
    if askyesno("Konfirmasi", f"Gunakan kata sandi untuk file {argumen}?"):
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
    if parameter_prima_p != "":
        try:
            parameter_prima_p = int(parameter_prima_p)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
        else:
            if parameter_prima_p >= 512:
                return f"-pkeyopt dh_paramgen_prime_len:{parameter_prima_p} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input harus lebih dari atau sama dengan 512!{Fore.RESET}")
    return ""
def input_parameter_subprima_q() -> str:
    parameter_subprima_q = input("Masukkan nilai parameter subprima q (default = 224) : ").lower().strip()
    if parameter_subprima_q != "":
        try:
            parameter_subprima_q = int(parameter_subprima_q)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
        else:
            if parameter_subprima_q >= 0:
                return f"-pkeyopt dh_paramgen_subprime_len:{parameter_subprima_q} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
    return ""
def input_digest(teks : None | Literal["RSA-PSS", "RSA-PSS untuk parameter MGF1"] = None):
    if teks == None:
        DIGEST = input("Pilih digest [sha1 | sha224 | sha256] : ").lower().strip()
        if DIGEST in ("sha1", "sha224", "sha256"):
            return f"-pkeyopt digest:{DIGEST} "
        elif DIGEST != "":
            print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
    else:
        DIGEST = input(f"{Fore.LIGHTRED_EX}*{Fore.RESET}Pilih digest {teks} (blake2b512 | blake2s256 | md4 | md5 | md5-sha1 | mdc2 | ripemd | ripemd160 | rmd160 | sha1 | sha224 | sha256 | sha3-224 | sha3-256 | sha3-384 | sha3-512 | sha384 | sha512 | sha512-224 | sha512-256 | shake128 | shake256 | sm3 | ssl3-md5 | ssl3-sha1 | whirlpool)").strip().lower()
        if DIGEST in ("blake2b512", "blake2s256", "md4", "md5", "md5-sha1", "mdc2", "ripemd", "ripemd160", "rmd160", "sha1", "sha224", "sha256", "sha3-224", "sha3-256", "sha3-384", "sha3-512", "sha384", "sha512", "sha512-224", "sha512-256", "shake128", "shake256", "sm3", "ssl3-md5", "ssl3-sha1", "whirlpool"):
            if teks == "RSA-PSS":
                return f"-pkeyopt rsa_pss_keygen_md:{DIGEST} "
            else:
                return f"-pkeyopt rsa_keygen_mgf1_md:{DIGEST} "
        elif DIGEST != "":
            print(f"{Fore.LIGHTRED_EX}Digest Tidak Valid!{Fore.RESET}")
    return ""
def input_indeks_g() -> str:
    indeks_g = input("Masukkan indeks untuk pembuatan kanonik dan verifikasi generator g (default = -1) [0 - 255] : ").strip()
    if indeks_g != "":
        try:
            indeks_g = int(indeks_g)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
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
def pilih_chiper():
    chiper = input("Pilih enkripsi chiper opsional [aes128 | aes192 | aes256 | camellia128 | camellia192 | camellia256 | des | des3 | idea] : ").strip().lower()
    if chiper in ("aes128", "aes192", "aes256", "camellia128", "camellia192", "camellia256", "des", "des3", "idea"):
        return f"-{chiper} "
    elif chiper != "":
        print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
    return ""
def input_bit_rsa(teks : Literal["RSA", "RSA-PSS"]):
    ukuran_bit = input(f"Masukkan ukuran bit {teks} (default = 2048) : ").strip()
    if ukuran_bit != "":
        try:
            ukuran_bit = int(ukuran_bit)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
        else:
            if ukuran_bit >= 512:
                return f"-pkeyopt rsa_keygen_bits:{ukuran_bit} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input harus lebih dari atau sama dengan 512!{Fore.RESET}")
    return ""
def input_prima_rsa(teks : Literal["RSA", "RSA-PSS"]):
    nilai_prima = input(f"Masukkan nilai prima {teks} (default = 2) : ").strip()
    if nilai_prima != "":
        try:
            nilai_prima = int(nilai_prima)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
        else:
            if nilai_prima >= 0:
                return f"-pkeyopt rsa_keygen_primes:{nilai_prima} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
    return ""
def input_eksponent_publik_rsa(teks : Literal["RSA", "RSA-PSS"]):
    nilai_eksponent = input(f"Masukkan nilai eksponen publik {teks} (default = 65537) : ").strip()
    if nilai_eksponent != "":
        try:
            nilai_eksponent = int(nilai_eksponent)
        except ValueError:
            print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
        else:
            if nilai_eksponent >= 0:
                return f"-pkeyopt rsa_keygen_pubexp:{nilai_eksponent} "
            else:
                print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
    return ""
def pilih_group_parameter():
    group_parameter = input("Pilih group parameter DH [ffdhe2048 | ffdhe3072 | ffdhe4096 | ffdhe6144 | ffdhe8192 | modp_1536 | modp_2048 | modp_3072 | modp_4096 | modp_6144 | modp_8192] : ").strip().lower()
    if group_parameter in ("ffdhe2048", "ffdhe3072", "ffdhe4096", "ffdhe6144", "ffdhe8192", "modp_1536", "modp_2048", "modp_3072", "modp_4096", "modp_6144", "modp_8192"):
        return f"-pkeyopt group:\"{group_parameter}\" "
    elif group_parameter != "":
        print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
    return ""
class kustom_raw_konfig(RawConfigParser):
    def optionxform(self, optionstr: str) -> str:
        return optionstr
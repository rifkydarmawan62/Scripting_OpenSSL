from subprocess import run, CalledProcessError
from colorama import Fore, Back
from modul import bersihkan_layar
from tkinter.filedialog import asksaveasfilename as simpan_file
from tkinter.messagebox import askyesno
from os.path import exists
from os import remove

# Dokumentasi : https://www.openssl.org/docs/man3.2/man1/openssl-genpkey.html#DH-Parameter-Generation-Options

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = False, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        FILE_OUTPUT = simpan_file(title = "Pilih lokasi file parameter DHX disimpan", defaultextension = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], initialfile = ".pem", confirmoverwrite = True)
        if FILE_OUTPUT:
            perintah = f"openssl genpkey -out \"{FILE_OUTPUT}\" -algorithm DHX -outform PEM -genparam -verbose "
            if askyesno("Konfirmasi", "Gunakan kata sandi untuk file paramater DHX?"):
                perintah += "-pass stdin "
            PARAMETER_RFC5114 = input("Pilih parameter RFC5114 [dh_1024_160 | dh_2048_224 | dh_2048_256] : ").lower().strip()
            match PARAMETER_RFC5114:
                case "dh_1024_160":
                    perintah += "-pkeyopt dh_rfc5114:1 "
                case "dh_2048_224":
                    perintah += "-pkeyopt dh_rfc5114:2 "
                case "dh_2048_256":
                    perintah += "-pkeyopt dh_rfc5114:3 "
                case "":
                    pass
                case _:
                    print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            parameter_prima_p = input("Masukkan nilai parameter prima p (default = 2048) : ").lower().strip()
            if parameter_prima_p == "":
                pass
            else:
                try:
                    parameter_prima_p = int(parameter_prima_p)
                except ValueError:
                    print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
                else:
                    if parameter_prima_p >= 0:
                        perintah += f"-pkeyopt dh_paramgen_prime_len:{parameter_prima_p} "
                    else:
                        print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
            parameter_subprima_q = input("Masukkan nilai parameter subprima q (default = 224) : ").lower().strip()
            if parameter_subprima_q == "":
                pass
            else:
                try:
                    parameter_subprima_q = int(parameter_subprima_q)
                except ValueError:
                    print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
                else:
                    if parameter_subprima_q >= 0:
                        perintah += f"-pkeyopt dh_paramgen_subprime_len:{parameter_subprima_q} "
                    else:
                        print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
            TIPE = input("Pilih tipe parameter [fips186_4 | fips186_2 | default] : ").lower().strip()
            if TIPE in ("fips186_4", "fips186_2", "default"):
                perintah += f"-pkeyopt type:\"{TIPE}\" "
            elif TIPE == "":
                pass
            else:
                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            TIPE_PARAMETER_DH = input("Pilih tipe parameter DH [generator | fips186_2 | fips186_4 | group] : ").strip().lower()
            match TIPE_PARAMETER_DH:
                case "generator":
                    perintah += "-pkeyopt dh_paramgen_type:0 "
                case "fips186_2":
                    perintah += "-pkeyopt dh_paramgen_type:1 "
                case "fips186_4":
                    perintah += "-pkeyopt dh_paramgen_type:2 "
                case "group":
                    perintah += "-pkeyopt dh_paramgen_type:3 "
                case "":
                    pass
                case _:
                    print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!")
            DIGEST = input("Pilih digest [sha1 | sha224 | sha256] : ").lower().strip()
            if DIGEST in ("sha1", "sha224", "sha256"):
                perintah += f"-pkeyopt digest:{DIGEST} "
            elif DIGEST == "":
                pass
            else:
                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            indeks_g = input("Masukkan indeks untuk pembuatan kanonik dan verifikasi generator g (default = -1) [0 - 255] : ").strip()
            if indeks_g == "":
                pass
            else:
                try:
                    indeks_g = int(indeks_g)
                except ValueError:
                    print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
                else:
                    if indeks_g >= -1 and indeks_g <= 255:
                        perintah += f"-pkeyopt gindex:{indeks_g} "
                    else:
                        print(f"{Fore.LIGHTRED_EX}Input harus dalam jangkauan -1 sampai 255!{Fore.RESET}")
            perintah = perintah.strip()
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = False, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Gagal membuat file parameter DHX!{Fore.RESET}")
                if exists(FILE_OUTPUT):
                    remove(FILE_OUTPUT)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}File parameter DHX batal dibuat!{Fore.RESET}")
                if exists(FILE_OUTPUT):
                    remove(FILE_OUTPUT)
            else:
                print(f"{Fore.LIGHTGREEN_EX}File parameter DHX berhasil dibuat!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File parameter DHX tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")
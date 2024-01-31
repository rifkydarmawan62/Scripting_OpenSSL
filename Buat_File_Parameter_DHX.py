from subprocess import run, CalledProcessError
from colorama import Fore, Back
from modul import bersihkan_layar, input_kata_sandi_untuk_parameter, input_parameter_prima_p, input_parameter_subprima_q, input_indeks_g, input_digest
from tkinter.filedialog import asksaveasfilename as simpan_file
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
            perintah_tambahan, file_sementara = input_kata_sandi_untuk_parameter("DHX")
            perintah += perintah_tambahan; del perintah_tambahan
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
            perintah += input_parameter_prima_p()
            perintah += input_parameter_subprima_q()
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
                    print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            perintah += input_digest()
            perintah += input_indeks_g()
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
            if exists(file_sementara):
                print(f"{Fore.YELLOW}Menghapus file sementara ...")
                remove(file_sementara)
                print(f"{Fore.LIGHTGREEN_EX}File sementara dihapus!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File parameter DHX tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")
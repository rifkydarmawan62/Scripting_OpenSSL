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
        FILE_OUTPUT = simpan_file(title = "Pilih lokasi file parameter DH disimpan", defaultextension = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], initialfile = ".pem", confirmoverwrite = True)
        if FILE_OUTPUT:
            perintah = f"openssl genpkey -out \"{FILE_OUTPUT}\" -algorithm DH -outform PEM -genparam -verbose "
            if askyesno("Konfirmasi", "Gunakan kata sandi untuk file paramater DH?"):
                perintah += "-pass stdin "
            PARAMETER_DH = input("Pilih parameter DH [ffdhe2048 | ffdhe3072 | ffdhe4096 | ffdhe6144 | ffdhe8192 | modp_1536 | modp_2048 | modp_3072 | modp_4096 | modp_6144 | modp_8192] : ").strip().lower()
            if PARAMETER_DH in ("ffdhe2048", "ffdhe3072", "ffdhe4096", "ffdhe6144", "ffdhe8192", "modp_1536", "modp_2048", "modp_3072", "modp_4096", "modp_6144", "modp_8192"):
                perintah += f"-pkeyopt dh_param:\"{PARAMETER_DH}\" "
            elif PARAMETER_DH == "":
                pass
            else:
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
            nilai_generator_g = input("Masukkan nilai generator g (default = 2) : ").strip()
            if nilai_generator_g == "":
                pass
            else:
                try:
                    nilai_generator_g = int(nilai_generator_g)
                except ValueError:
                    print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
                else:
                    if nilai_generator_g >= 0:
                        perintah += f"-pkeyopt dh_paramgen_generator:{nilai_generator_g} "
                    else:
                        print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
            TIPE = input("Pilih tipe parameter [generator | group | default] : ").lower().strip()
            if TIPE in ("generator", "group", "default"):
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
                print(f"{Fore.LIGHTRED_EX}Gagal membuat file parameter DH!{Fore.RESET}")
                if exists(FILE_OUTPUT):
                    remove(FILE_OUTPUT)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}File parameter DH batal dibuat!{Fore.RESET}")
                if exists(FILE_OUTPUT):
                    remove(FILE_OUTPUT)
            else:
                print(f"{Fore.LIGHTGREEN_EX}File parameter DH berhasil dibuat!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")
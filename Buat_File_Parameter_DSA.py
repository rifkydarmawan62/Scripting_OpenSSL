from subprocess import run, CalledProcessError
from colorama import Fore, Back
from modul import bersihkan_layar, input_kata_sandi_untuk_parameter, input_digest, input_indeks_g
from tkinter.filedialog import asksaveasfilename as simpan_file
from tkinter.messagebox import askyesno
from os.path import exists
from os import remove

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        FILE_OUTPUT = simpan_file(title = "*Pilih lokasi file parameter DSA (Digital Signature Algorithm) disimpan", defaultextension = ".pem", initialfile = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], confirmoverwrite = True)
        if FILE_OUTPUT:
            perintah = f"openssl genpkey -out \"{FILE_OUTPUT}\" -algorithm DSA -outform PEM -verbose -genparam "
            perintah_tambahan, file_sementara = input_kata_sandi_untuk_parameter("DSA")
            perintah += perintah_tambahan; del perintah_tambahan
            try:
                UKURAN_BIT_DSA = int(input("Masukkan ukuran bit DSA (default = 2048) [> 0] : ").strip())
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
            else:
                if UKURAN_BIT_DSA > 0:
                    perintah += f"-pkeyopt dsa_paramgen_bits:{UKURAN_BIT_DSA} "
                else:
                    print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
            UKURAN_BIT_PARAMETER_Q = input("Masukkan ukuran bit untuk parameter q (default = 224) [160 | 256] : ").strip()
            if UKURAN_BIT_PARAMETER_Q in ("160", "224", "256"):
                perintah += f"-pkeyopt dsa_paramgen_q_bits:{UKURAN_BIT_PARAMETER_Q} "
            elif UKURAN_BIT_PARAMETER_Q == "":
                pass
            else:
                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            perintah += input_digest()
            if askyesno(title = "Pilih tipe", message = "\"Ya\" untuk gunakan parameter generasi FIPS186-2\n\"Tidak\" untuk gunakan parameter generasi FIPS186-4"):
                perintah += "-pkeyopt type:1 "
            perintah += input_indeks_g()
            perintah = perintah.strip()
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Gagal membuat file parameter DSA!{Fore.RESET}")
                if exists(FILE_OUTPUT):
                    remove(FILE_OUTPUT)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}File parameter DSA batal dibuat!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}File parameter DSA berhasil dibuat!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File paramater tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")
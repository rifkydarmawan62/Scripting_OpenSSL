from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from colorama import Fore, Back
from os.path import exists
from os import remove
from modul import bersihkan_layar

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        INPUT_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if INPUT_FILE_KUNCI_PRIVATE:
            OUTPUT_FILE_CSR = simpan_file(title = "*Pilih lokasi file Certificate Signing Requests (CSR) disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", confirmoverwrite = True, initialfile = ".pem", initialdir = "/".join(INPUT_FILE_KUNCI_PRIVATE.split("/")[:-1]))
            if OUTPUT_FILE_CSR:
                PERINTAH = f"openssl req -new -key \"{INPUT_FILE_KUNCI_PRIVATE}\" -verbose -out \"{OUTPUT_FILE_CSR}\""
                print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                try:
                    run(PERINTAH, shell = True, check = True)
                except CalledProcessError:
                    print(f"{Fore.LIGHTRED_EX}CSR gagal dibuat!{Fore.RESET}")
                    if exists(OUTPUT_FILE_CSR):
                        remove(OUTPUT_FILE_CSR)
                except KeyboardInterrupt:
                    print(f"{Fore.LIGHTRED_EX}CSR batal dibuat!{Fore.RESET}")
                    if exists(OUTPUT_FILE_CSR):
                        remove(OUTPUT_FILE_CSR)
                else:
                    print(f"{Fore.LIGHTGREEN_EX}CSR dibuat di direktori \"{OUTPUT_FILE_CSR}\"{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}File CSR tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup{Fore.RESET}")
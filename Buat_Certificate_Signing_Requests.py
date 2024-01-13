from subprocess import run, CalledProcessError
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from getpass import getpass
from colorama import Fore

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.LIGHTBLUE_EX}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    try:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
        DIREKTORI_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            DIREKTORI_FILE_CSR = simpan_file(title = "*Pilih lokasi file Certificate Signing Requests (CSR) disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", confirmoverwrite = True, initialfile = ".pem", initialdir = "/".join(DIREKTORI_FILE_KUNCI_PRIVATE.split("/")[:-1]))
            if DIREKTORI_FILE_CSR:
                print(f"{Fore.LIGHTGREEN_EX}File Kunci Private = \"{DIREKTORI_FILE_KUNCI_PRIVATE}\"\nFile CSR disimpan = \"{DIREKTORI_FILE_CSR}\"")
                PERINTAH = f"openssl req -new -key \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -verbose -out \"{DIREKTORI_FILE_CSR}\""
                print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
                try:
                    run(PERINTAH, shell = True, check = True)
                except CalledProcessError:
                    print(f"{Fore.LIGHTRED_EX}Gagal membuat CSR!")
                try:
                    getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
                except KeyboardInterrupt:
                    pass
            else:
                print(f"{Fore.LIGHTRED_EX}File CSR tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup{Fore.RESET}")
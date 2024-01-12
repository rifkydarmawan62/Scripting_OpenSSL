from getpass import getpass
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
from colorama import Fore
from subprocess import run, CalledProcessError

print(f"{Fore.LIGHTYELLOW_EX}Memeriksa instalasi OpenSSL melalui CLI ...{Fore.LIGHTBLUE_EX}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    showerror("Gagal menjalankan aplikasi", "Perintah OpenSSL Tidak Ditemukan\nSilahkan download OpenSSL dari openssl.org dan atur konfigurasi file agar perintah OpenSSL dapat dijalankan")
else:
    try:
        print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
        DIREKTORI_FILE_KUNCI_PRIVATE = asksaveasfilename(title = "*Lokasi file kunci private disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", initialfile = ".pem", confirmoverwrite = True)
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            PERINTAH_BUAT_KUNCI_PRIVATE = f"openssl genrsa -f4 -out \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -verbose"
            print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH_BUAT_KUNCI_PRIVATE}] ...{Fore.LIGHTBLUE_EX}")
            run(PERINTAH_BUAT_KUNCI_PRIVATE, shell = True)
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak disimpan!")
        try:
            getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
        except KeyboardInterrupt:
            pass
    except KeyboardInterrupt:
        showerror("Error!", "Interupsi Keyboard Ctrl + C!\nProgram ditutup")
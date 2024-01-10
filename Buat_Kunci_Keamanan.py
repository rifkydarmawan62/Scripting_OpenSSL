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
        DIREKTORI_FILE_KUNCI_PRIVATE = asksaveasfilename(title = "*Lokasi file kunci private disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], defaultextension = ".pem", initialfile = ".pem")
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            print(f"{Fore.LIGHTGREEN_EX}direktori file kunci private = \"{DIREKTORI_FILE_KUNCI_PRIVATE}\"")
            INISIAL_DIREKTORI = "/".join(DIREKTORI_FILE_KUNCI_PRIVATE.split("/")[:-1])
            PERINTAH_BUAT_KUNCI_PRIVATE = f"openssl genrsa -f4 -out \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -verbose"
            print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
            DIREKTORI_FILE_KUNCI_PUBLIK = asksaveasfilename(title = "Lokasi file kunci publik disimpan (Opsional)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Personal Information Exchange", "*.pvk")], initialdir = INISIAL_DIREKTORI, defaultextension = ".pem")
            if DIREKTORI_FILE_KUNCI_PUBLIK:
                print(f"{Fore.LIGHTGREEN_EX}direktori file kunci publik = \"{DIREKTORI_FILE_KUNCI_PUBLIK}\"")
                PERINTAH_BUAT_KUNCI_PUBLIK = f"openssl rsa -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -inform PEM -out \"{DIREKTORI_FILE_KUNCI_PUBLIK}\" -outform {DIREKTORI_FILE_KUNCI_PUBLIK[-3:].upper()} -pubout"
            else:
                PERINTAH_BUAT_KUNCI_PUBLIK = None
            print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
            DIREKTORI_FILE_KUNCI_PUBLIK_RSA = asksaveasfilename(title = "Lokasi file kunci publik RSA disimpan (Opsional)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Personal Information Exchange", "*.pvk")], initialdir = INISIAL_DIREKTORI, defaultextension = ".pem")
            if DIREKTORI_FILE_KUNCI_PUBLIK_RSA:
                print(f"{Fore.LIGHTGREEN_EX}direktori file kunci publik RSA = \"{DIREKTORI_FILE_KUNCI_PUBLIK_RSA}\"")
                PERINTAH_BUAT_KUNCI_PUBLIK_RSA = f"openssl rsa -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -inform PEM -out \"{DIREKTORI_FILE_KUNCI_PUBLIK_RSA}\" -outform {DIREKTORI_FILE_KUNCI_PUBLIK_RSA[-3:].upper()} -RSAPublicKey_out"
            else:
                PERINTAH_BUAT_KUNCI_PUBLIK_RSA = None
            print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH_BUAT_KUNCI_PRIVATE}] ...{Fore.LIGHTBLUE_EX}")
            run(PERINTAH_BUAT_KUNCI_PRIVATE, shell = True)
            if PERINTAH_BUAT_KUNCI_PUBLIK != None:
                print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH_BUAT_KUNCI_PUBLIK}] ...{Fore.LIGHTBLUE_EX}")
                run(PERINTAH_BUAT_KUNCI_PUBLIK, shell = True)
            if PERINTAH_BUAT_KUNCI_PUBLIK_RSA != None:
                print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH_BUAT_KUNCI_PUBLIK_RSA}] ...{Fore.LIGHTBLUE_EX}")
                run(PERINTAH_BUAT_KUNCI_PUBLIK_RSA)
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak disimpan!")
        getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
    except KeyboardInterrupt:
        showerror("Error!", "Interupsi Keyboard Ctrl + C!\nProgram ditutup")
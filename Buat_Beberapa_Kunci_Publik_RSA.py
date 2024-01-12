from subprocess import run, CalledProcessError
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from tkinter.messagebox import showerror
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
            DIREKTORI_FILE_KUNCI_PUBLIK_RSA = simpan_file(title = "*Pilih lokasi file kunci publik disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der")], defaultextension = ".pem", initialdir = "/".join(DIREKTORI_FILE_KUNCI_PRIVATE.split("/")[:-1]), confirmoverwrite = True, initialfile = ".pem")
            if DIREKTORI_FILE_KUNCI_PUBLIK_RSA:
                while True:
                    try:
                        jumlah_kunci_publik_rsa = int(input(f"{Fore.RESET}Masukkan jumlah kunci publik RSA [> 0] : ").strip())
                    except ValueError:
                        print(f"{Fore.LIGHTRED_EX}Input harus berupa angka")
                    else:
                        if jumlah_kunci_publik_rsa >= 0:
                            break
                        else:
                            print(f"{Fore.LIGHTRED_EX}Angka tidak boleh bilangan negatif!")
                if jumlah_kunci_publik_rsa == 1:
                    PERINTAH = f"openssl pkey -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -out \"{DIREKTORI_FILE_KUNCI_PUBLIK_RSA}\" -outform {DIREKTORI_FILE_KUNCI_PUBLIK_RSA[-3:].upper()} -RSAPublicKey_out"
                    print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
                    try:
                        run(PERINTAH, shell = True, check = True)
                    except CalledProcessError:
                        print(f"{Fore.LIGHTRED_EX}Gagal membuat kunci publik!")
                elif jumlah_kunci_publik_rsa > 1:
                    DIREKTORI_FILE = "/".join(DIREKTORI_FILE_KUNCI_PUBLIK_RSA.split("/")[:-1])
                    NAMA_FILE = ".".join(DIREKTORI_FILE_KUNCI_PUBLIK_RSA.split("/")[-1].split(".")[:-1])
                    JENIS_FILE = DIREKTORI_FILE_KUNCI_PUBLIK_RSA.split(".")[-1]
                    for urutan_kunci in range(jumlah_kunci_publik_rsa):
                        PERINTAH = f"openssl pkey -in \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -out \"{DIREKTORI_FILE}/{NAMA_FILE}-{urutan_kunci}.{JENIS_FILE} -outform {JENIS_FILE.upper()} -RSAPublicKey_out"
                        print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{PERINTAH}] ...{Fore.LIGHTBLUE_EX}")
                        try:
                            run(PERINTAH, shell = True, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Gagal membuat kunci publik!")
                            break
                try:
                    getpass(f"{Fore.RESET}Tekan Enter untuk keluar")
                except KeyboardInterrupt:
                    pass
            else:
                print(f"{Fore.LIGHTRED_EX}File kunci publik tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        showerror("Error!", "Interupsi Keyboard Ctrl + C!\nProgram ditutup")
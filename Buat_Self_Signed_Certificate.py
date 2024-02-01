from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import run, CalledProcessError
from colorama import Fore, Back
from os.path import exists
from os import remove
from modul import bersihkan_layar, kustom_raw_konfig
from tkinter.messagebox import askyesno

bersihkan_layar(f"{Fore.YELLOW}Memeriksa Instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL Tidak Ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        DIREKTORI_FILE_KUNCI_PRIVATE = pilih_file(title = "*Pilih file kunci private", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
        if DIREKTORI_FILE_KUNCI_PRIVATE:
            DIREKTORI_FILE_CSR = pilih_file(title = "*Pilih file Certificate Signing Requests (CSR)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rules", "*.der"), ("Semua File", "*.*")])
            if DIREKTORI_FILE_CSR:
                PERINTAH_VALIDASI_CSR = f"openssl req -in \"{DIREKTORI_FILE_CSR}\" -verify -noout"
                print(f"{Fore.YELLOW}Menjalankan perintah validasi {Fore.LIGHTYELLOW_EX}{Back.BLUE}{PERINTAH_VALIDASI_CSR}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                try:
                    run(PERINTAH_VALIDASI_CSR, shell = True, check = True)
                except CalledProcessError:
                    print(f"{Fore.LIGHTRED_EX}CSR tidak valid!{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTGREEN_EX}CSR valid!\n{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
                    DIREKTORI_FILE_SERTIFIKAT = simpan_file(title = "*Pilih lokasi file Self Signed Certificate disimpan", filetypes = [("Privacy Enhanced Mail", "*.pem")], initialfile = ".pem", initialdir = "/".join(DIREKTORI_FILE_CSR.split("/")[:-1]), defaultextension = ".pem", confirmoverwrite = True)
                    if DIREKTORI_FILE_SERTIFIKAT:
                        DIREKTORI_FOLDER = "/".join(DIREKTORI_FILE_SERTIFIKAT.split("/")[:-1])
                        DIREKTORI_FILE_KONFIGURASI = f"{DIREKTORI_FOLDER}/konfigurasi.cnf"
                        DIREKTORI_FILE_DATABASE = f"{DIREKTORI_FOLDER}/index.txt"
                        perintah = f"openssl ca -verbose -in \"{DIREKTORI_FILE_CSR}\" -out \"{DIREKTORI_FILE_SERTIFIKAT}\" -config \"{DIREKTORI_FILE_KONFIGURASI}\" -keyfile \"{DIREKTORI_FILE_KUNCI_PRIVATE}\" -selfsign "
                        if askyesno("Konfirmasi", "Gunakan format teks UTF-8?"):
                            perintah += "-utf8 "
                        with open(DIREKTORI_FILE_DATABASE, "w") as file_database:
                            pass
                        print(f"{Fore.LIGHTGREEN_EX}File database dibuat di di direktori \"{DIREKTORI_FILE_DATABASE}\"{Fore.RESET}")
                        data_konfigurasi = kustom_raw_konfig()
                        data_konfigurasi["ca"] = {"default_ca" : "CA_default"}
                        data_konfigurasi["CA_default"] = {"dir" : DIREKTORI_FOLDER,
                                                          "database" : "$dir/index.txt",
                                                          "new_certs_dir" : "$dir",
                                                          "certificate" : "none",
                                                          "serial" : "$dir/nomor_sertifikat",
                                                          "rand_serial" : "yes",
                                                          "private_key" : DIREKTORI_FILE_KUNCI_PRIVATE,
                                                          "default_days" : "1000",
                                                          "default_crl_days" : "30",
                                                          "default_md" : "sha256",
                                                          "policy" : "policy_anything",
                                                          "email_in_dn" : "none",
                                                          "name_opt" : "ca_default",
                                                          "cert_opt" : "ca_default",
                                                          "copy_extensions" : "none"}
                        data_konfigurasi["policy_anything"] = {"countryName" : "optional",
                                                               "stateOrProvinceName" : "optional",
                                                               "organizationName" : "optional",
                                                               "organizationalUnitName" : "optional",
                                                               "commonName" : "optional",
                                                               "emailAddress" : "optional"}
                        with open(DIREKTORI_FILE_KONFIGURASI, "w") as file_konfigurasi:
                            data_konfigurasi.write(file_konfigurasi)
                        print(f"{Fore.LIGHTGREEN_EX}File konfigurasi dibuat di direktori \"{DIREKTORI_FILE_KONFIGURASI}\"{Fore.RESET}")
                        perintah = perintah.strip()
                        print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                        try:
                            run(perintah, shell = True, check = True)
                        except CalledProcessError:
                            print(f"{Fore.LIGHTRED_EX}Self signed certificate gagal dibuat!{Fore.RESET}")
                            if exists(DIREKTORI_FILE_SERTIFIKAT):
                                remove(DIREKTORI_FILE_SERTIFIKAT)
                        else:
                            print(f"{Fore.LIGHTGREEN_EX}Self signed certificate dibuat di direktori \"{DIREKTORI_FILE_SERTIFIKAT}\"{Fore.RESET}")
                    else:
                        print(f"{Fore.LIGHTRED_EX}File self signed certificate tidak disimpan!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}File CSR tidak dipilih!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Keyboard Ctrl + C!\nProgram ditutup!{Fore.RESET}")
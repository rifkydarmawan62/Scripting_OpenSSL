from subprocess import CalledProcessError
from tkinter.filedialog import asksaveasfilename as simpan_file
from modul import bersihkan_layar, pilih_chiper, run, Fore, input_bit_rsa, input_prima_rsa, input_eksponent_publik_rsa, exists, remove, input_digest
from colorama import Back

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        OUTPUT_KUNCI_PRIVATE = simpan_file(title = "*Pilih lokasi kunci private RSA-PSS (Rivest Shamir Addleman-Probabilistic Signature Scheme) disimpan", defaultextension = ".pem", initialfile = ".pem", confirmoverwrite = True, filetypes = [("Privacy Enhanced Mail", "*.pem")])
        if OUTPUT_KUNCI_PRIVATE:
            perintah = f"openssl genpkey -out \"{OUTPUT_KUNCI_PRIVATE}\" -outform PEM -algorithm RSA-PSS -verbose "
            OUTPUT_KUNCI_PUBLIK = simpan_file(title = "Pilih lokasi file kunci publik RSA-PSS (Rivest Shamir Addleman-Probabilistic Signature Scheme) disimpan", defaultextension = ".pem", initialfile = ".pem", confirmoverwrite = True, filetypes = [("Privacy Enhanced Mail", "*.pem")])
            if OUTPUT_KUNCI_PUBLIK:
                perintah += f"-outpubkey \"{OUTPUT_KUNCI_PUBLIK}\" "
            perintah += pilih_chiper()
            perintah += input_bit_rsa("RSA-PSS")
            perintah += input_prima_rsa("RSA-PSS")
            perintah += input_eksponent_publik_rsa("RSA-PSS")
            perintah += input_digest("RSA-PSS")
            perintah += input_digest("RSA-PSS untuk parameter MGF1")
            perintah = perintah.strip()
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Kunci private RSA-PSS gagal dibuat!{Fore.RESET}")
                if exists(OUTPUT_KUNCI_PRIVATE):
                    remove(OUTPUT_KUNCI_PRIVATE)
                if exists(OUTPUT_KUNCI_PUBLIK):
                    remove(OUTPUT_KUNCI_PUBLIK)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Kunci private RSA-PSS batal dibuat!{Fore.RESET}")
                if exists(OUTPUT_KUNCI_PRIVATE):
                    remove(OUTPUT_KUNCI_PRIVATE)
                if exists(OUTPUT_KUNCI_PUBLIK):
                    remove(OUTPUT_KUNCI_PUBLIK)
            else:
                print(f"{Fore.LIGHTGREEN_EX}Kunci private RSA-PSS berhasil dibuat!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File kunci private RSA-PSS tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C!\nProgram ditutup!{Fore.RESET}")
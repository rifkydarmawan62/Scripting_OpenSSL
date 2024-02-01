from modul import bersihkan_layar, Fore, pilih_chiper, exists, remove, run
from colorama import Back
from tkinter.filedialog import askopenfilename as pilih_file, asksaveasfilename as simpan_file
from subprocess import CalledProcessError

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        PARAMETER_DSA = pilih_file(title = "*Pilih file parameter DSA (Digital Signature Algorithm)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rule", "*.der"), ("Semua File", "*.*")])
        if PARAMETER_DSA:
            OUTPUT_KUNCI_PRIVATE = simpan_file(title = "*Pilih lokasi file kunci private DSA (Digital Signature Algorithm) disimpan", defaultextension = ".pem", initialfile = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], confirmoverwrite = True)
            if OUTPUT_KUNCI_PRIVATE:
                perintah = f"openssl gendsa -out \"{OUTPUT_KUNCI_PRIVATE}\" -verbose "
                perintah += pilih_chiper()
                perintah += f"\"{PARAMETER_DSA}\""
                print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
                try:
                    run(perintah, shell = True, check = True)
                except CalledProcessError:
                    print(f"{Fore.LIGHTRED_EX}Kunci private DSA gagal dibuat!{Fore.RESET}")
                    if exists(OUTPUT_KUNCI_PRIVATE):
                        remove(OUTPUT_KUNCI_PRIVATE)
                except KeyboardInterrupt:
                    print(f"{Fore.LIGHTRED_EX}Kunci private DSA batal dibuat!{Fore.RESET}")
                    if exists(OUTPUT_KUNCI_PRIVATE):
                        remove(OUTPUT_KUNCI_PRIVATE)
                else:
                    print(f"{Fore.LIGHTGREEN_EX}Kunci private DSA berhasil dibuat!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTRED_EX}Kunci private DSA tidak disimpan!{Fore.RESET}")
        else:
            print(f"{Fore.LIGHTRED_EX}File parameter DSA tidak dipilih!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C!\nProgram ditutup!{Fore.RESET}")
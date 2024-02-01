from modul import bersihkan_layar, Fore, exists, remove, run, pilih_group_parameter, input_kata_sandi_untuk, hapus_file_sementara
from subprocess import CalledProcessError
from colorama import Back
from tkinter.filedialog import asksaveasfilename as simpan_file, askopenfilename as pilih_file

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        OUTPUT_KUNCI_PRIVATE = simpan_file(title = "*Pilih lokasi file kunci private DH (Diffie Hellman) disimpan", defaultextension = ".pem", initialfile = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], confirmoverwrite = True)
        if OUTPUT_KUNCI_PRIVATE:
            perintah = f"openssl genpkey -out \"{OUTPUT_KUNCI_PRIVATE}\" -outform PEM -verbose "
            OUTPUT_KUNCI_PUBLIK = simpan_file(title = "Pilih lokasi file kunci publik DH (Diffie Hellman) disimpan", defaultextension = ".pem", initialfile = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], confirmoverwrite = True)
            if OUTPUT_KUNCI_PUBLIK:
                perintah += f"-outpubkey \"{OUTPUT_KUNCI_PUBLIK}\" "
            perintah_tambahan, file_sementara = input_kata_sandi_untuk("kunci private DH")
            perintah += perintah_tambahan; del perintah_tambahan
            PARAMETER_DH = pilih_file(title = "Pilih file parameter DH (Diffie Hellman)", filetypes = [("Privacy Enhanced Mail", "*.pem"), ("Distinguished Encoding Rule", "*.der"), ("Semua File", "*.*")])
            if PARAMETER_DH:
                perintah += f"-paramfile \"{PARAMETER_DH}\" "
            else:
                perintah += pilih_group_parameter()
            perintah = perintah.strip()
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Kunci private DH gagal dibuat!{Fore.RESET}")
                if exists(OUTPUT_KUNCI_PRIVATE):
                    remove(OUTPUT_KUNCI_PRIVATE)
                if exists(OUTPUT_KUNCI_PUBLIK):
                    remove(OUTPUT_KUNCI_PUBLIK)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Kunci private DH batal dibuat!{Fore.RESET}")
                if exists(OUTPUT_KUNCI_PRIVATE):
                    remove(OUTPUT_KUNCI_PRIVATE)
                if exists(OUTPUT_KUNCI_PUBLIK):
                    remove(OUTPUT_KUNCI_PUBLIK)
            else:
                print(f"{Fore.LIGHTGREEN_EX}Kunci private DH berhasil dibuat!{Fore.RESET}")
            hapus_file_sementara(file_sementara)
        else:
            print(f"{Fore.LIGHTRED_EX}Kunci private DH tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C!\nProgram ditutup!{Fore.RESET}")
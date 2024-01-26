from colorama import Fore
from subprocess import run, CalledProcessError
from platform import system, architecture
from tkinter.filedialog import askdirectory
from os.path import exists
from os import remove

if system().lower() == "windows":
    def bersihkan_layar(teks : str | None = None):
        run("cls", shell = True)
        if teks:
            print(teks)
    bersihkan_layar(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    DIREKTORI_FOLDER = askdirectory(title = "Pilih lokasi file unduhan OpenSSL disimpan").replace("/", "\\")
    if DIREKTORI_FOLDER:
        if architecture()[0] == "64bit":
            menu_tipe_unduhan : bool = True; unduhan_32_bit : bool | None = None
            while menu_tipe_unduhan:
                bersihkan_layar("Pilih Tipe Unduhan OpenSSL\n[-] keluar (Ctrl + C)\n[0] bersihkan layar\n[1] 32 bit\n[2] 64 bit")
                while True:
                    argumen = input("Pilih nomor : ")
                    match argumen.strip():
                        case "-":
                            menu_tipe_unduhan = False
                        case "0":
                            break
                        case "1":
                            menu_tipe_unduhan = False
                            unduhan_32_bit = True
                        case "2":
                            menu_tipe_unduhan = False
                            unduhan_32_bit = False
                        case _:
                            print(f"{Fore.LIGHTRED_EX}Input tidak valid!{Fore.RESET}")
                            continue
                    break
        else:
            unduhan_32_bit = True
        if (unduhan_32_bit == True) or (unduhan_32_bit == False):
            if unduhan_32_bit:
                URL = "https://slproweb.com/download/Win32OpenSSL-3_2_0.msi"
                LOKASI_UNDUHAN = f"{DIREKTORI_FOLDER}\\{URL.split("/")[-1]}"
                PERINTAH = f"bitsadmin /transfer \"Mengunduh_OpenSSL_32_bit\" /download \"{URL}\" \"{LOKASI_UNDUHAN}\""
            else:
                URL = "https://slproweb.com/download/Win64OpenSSL-3_2_0.msi"
                LOKASI_UNDUHAN = f"{DIREKTORI_FOLDER}\\{URL.split("/")[-1]}"
                PERINTAH = f"bitsadmin /transfer \"Mengunduh_OpenSSL_64_bit\" /download \"{URL}\" \"{LOKASI_UNDUHAN}\""
            print(f"Menjalankan perintah Windows Command Prompt [{PERINTAH}] ...")
            try:
                run(PERINTAH, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Gagal mengunduh OpenSSL!{Fore.RESET}")
                if exists(LOKASI_UNDUHAN):
                    remove(LOKASI_UNDUHAN)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Unduhan OpenSSL dihentikan!{Fore.RESET}")
                if exists(LOKASI_UNDUHAN):
                    remove(LOKASI_UNDUHAN)
            else:
                print("Menjalankan instalasi OpenSSL ...")
                run(f"\"{LOKASI_UNDUHAN}\"", shell = True)
    else:
        print(f"{Fore.LIGHTRED_EX}Unduhan instalasi OpenSSL tidak disimpan!{Fore.RESET}")
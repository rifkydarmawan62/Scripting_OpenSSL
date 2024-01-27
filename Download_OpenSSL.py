from colorama import Fore, Back
from subprocess import run, CalledProcessError
from platform import system, architecture
from tkinter.filedialog import askdirectory

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
            try:
                while menu_tipe_unduhan:
                    bersihkan_layar(f"{Fore.RESET}Pilih Tipe Unduhan OpenSSL\n[-] keluar (Ctrl + C)\n[0] bersihkan layar\n[1] 32 bit\n[2] 64 bit")
                    while True:
                        argumen = input(f"{Fore.RESET}Pilih nomor : ")
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
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Program ditutup!{Fore.RESET}")
        else:
            unduhan_32_bit = True
        if isinstance(unduhan_32_bit, bool):
            if unduhan_32_bit:
                URL = "https://slproweb.com/download/Win32OpenSSL-3_2_0.msi"
                LOKASI_UNDUHAN = f"{DIREKTORI_FOLDER}\\{URL.split("/")[-1]}"
                PERINTAH = f"bitsadmin /transfer \"Mengunduh_Instalasi_OpenSSL_32_bit\" /download /priority FOREGROUND \"{URL}\" \"{LOKASI_UNDUHAN}\" && \"{LOKASI_UNDUHAN}\""
            else:
                URL = "https://slproweb.com/download/Win64OpenSSL-3_2_0.msi"
                LOKASI_UNDUHAN = f"{DIREKTORI_FOLDER}\\{URL.split("/")[-1]}"
                PERINTAH = f"bitsadmin /transfer \"Mengunduh_Instalasi_OpenSSL_64_bit\" /download /priority FOREGROUND \"{URL}\" \"{LOKASI_UNDUHAN}\" && \"{LOKASI_UNDUHAN}\""
            print(f"{Fore.YELLOW}Menjalankan perintah Windows Command Prompt {Fore.BLACK}{Back.LIGHTBLUE_EX}{PERINTAH}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(PERINTAH, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Gagal mengunduh atau menjalankan instalasi OpenSSL!{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Unduhan atau instalasi OpenSSL dihentikan!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Berhasil menjalankan instalasi OpenSSL{Fore.RESET}")
    else:
        print(f"{Fore.LIGHTRED_EX}Unduhan instalasi OpenSSL tidak disimpan!{Fore.RESET}")
from getpass import getpass
from subprocess import run, CalledProcessError
from platform import system
from tkinter.filedialog import askopenfilename, asksaveasfilename
from colorama import Fore
from typing import Literal, Iterable

def __bersihkan_layar(__teks : str | None = None):
    run("cls" if system() == "Windows" else "clear", shell = True)
    if __teks:
        print(__teks)
def __enter_untuk_kembali(__pesan : str | None = None):
    if __pesan:
        print(__pesan)
    getpass(f"{Fore.RESET}Tekan enter untuk kembali")
def __tutup_program():
    print(f"{Fore.LIGHTRED_EX}Program ditutup{Fore.RESET}")
def __tekan_alt_tab_untuk_file(pilih_atau_simpan : Literal["pilih", "simpan"], judul : str | None = None, tipe_file : Iterable[tuple[str, str | list[str] | tuple[str, ...]]] | None = None, ekstensi_default : str | None = None, inisial_direktori : str | None = None, inisial_nama_file : str | None = None):
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru")
    if pilih_atau_simpan == "pilih":
        return askopenfilename(title = judul, filetypes = tipe_file, defaultextension = ekstensi_default, initialdir = inisial_direktori, initialfile = inisial_nama_file)
    else:
        return asksaveasfilename(title = judul, filetypes = tipe_file, defaultextension = ekstensi_default, initialdir = inisial_direktori, initialfile = inisial_nama_file, confirmoverwrite = True)
print(f"{Fore.LIGHTYELLOW_EX}Memeriksa Instalasi OpenSSL ...")
try:
    run("openssl version", shell = True, check = True, capture_output = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}OpenSSL belum diinstall")
    __tutup_program()
else:
    BERANDA = f"""{Fore.RESET}Buat Sertifikat SSL/TLS melalui perintah OpenSSL\n
Instagram : @rifkydarmawan62
GitHub : rifkydarmawan62\n
[-] {Fore.LIGHTRED_EX}keluar (Ctrl + C){Fore.RESET}
[0] bersihkan layar
[1] tampilkan bantuan
[2] tampilkan versi OpenSSL
[3] buat kunci private RSA (Rivest Shamir Adleman)"""
    __menu_beranda : bool = True
    try:
        while __menu_beranda:
            __bersihkan_layar(BERANDA)
            while True:
                argumen = input("Pilih nomor : ").strip()
                match argumen:
                    case "-":
                        __menu_beranda = False
                        __tutup_program()
                    case "0":
                        break
                    case "1":
                        run("openssl help", shell = True)
                        __enter_untuk_kembali()
                    case "2":
                        run("openssl version", shell = True)
                        continue
                    case "3":
                        alur = f"{Fore.RESET}beranda > buat kunci private RSA"
                        langkah = " > langkah 1\n\n"
                        __bersihkan_layar(alur + langkah)
                        direktori_output_file = __tekan_alt_tab_untuk_file("simpan", "*Pilih lokasi file kunci private RSA disimpan", [("File Biner", "*.bin"), ("Distinguished Encoding Rules", "*.der"), ("Privacy Enhanced Mail", "*.pem"),("Semua File", "*.*")], ".pem", inisial_nama_file = ".pem")
                        if direktori_output_file:
                            perintah_openssl = f"openssl genrsa -out \"{direktori_output_file}\""
                            langkah = " > langkah 2\n\n"
                            __bersihkan_layar(alur + langkah)
                            enkripsi_cipher = input("Pilih salah satu enkripsi cipher [aes128|aes192|aes256|aria128|aria192|aria256|camellia128|camellia192|camellia256|des|des3|idea] (Opsional | Enter untuk lanjut): ").lower().strip()
                            match enkripsi_cipher:
                                case "aes128"|"aes192"|"aes256"|"aria128"|"aria192"|"aria256"|"camellia128"|"camellia192"|"camellia256"|"des"|"des3"|"idea":
                                    perintah_openssl += f" -{enkripsi_cipher}"
                                case "":
                                    pass
                                case _:
                                    print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!\n")
                            langkah = " > langkah 3\n\n"
                            __bersihkan_layar(alur + langkah)
                            nomor_fermat_f4 = input("Gunakan nomor Fermat f4 [0|1] (default = 0) : ").strip()
                            if nomor_fermat_f4 == "1":
                                perintah_openssl += " -f4"
                            elif nomor_fermat_f4 == "0" or nomor_fermat_f4 == "":
                                pass
                            else:
                                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!\n{Fore.LIGHTBLUE_EX}defult = 0 digunakan")
                            langkah = " > langkah 4\n\n"
                            __bersihkan_layar(alur + langkah)
                            bilangan_prima = input("Masukkan bilangan prima untuk kunci RSA [1 - 15] (Opsional) : ").strip()
                            if bilangan_prima.isdigit():
                                bilangan_prima = int(bilangan_prima)
                                if bilangan_prima >= 1 and bilangan_prima <= 15:
                                    perintah_openssl += f" -primes {bilangan_prima}"
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Angka harus dalam jangkauan 1 sampai 15!")
                            elif bilangan_prima == "":
                                pass
                            else:
                                print(f"{Fore.LIGHTRED_EX}Input Harus Berupa Angka!")
                            langkah = " > langkah 5\n\n"
                            __bersihkan_layar(alur + langkah)
                            mode_tradisional = input("Gunakan kunci private RSA tradisional PKCS#1 [0|1] (default = 0) : ").strip()
                            if mode_tradisional == "1":
                                perintah_openssl += " -traditional"
                            elif mode_tradisional == "0" or mode_tradisional == "":
                                pass
                            else:
                                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid\n{Fore.LIGHTBLUE_EX}default = 0 digunakan")
                            langkah = " > langkah 6\n\n"
                            __bersihkan_layar(alur + langkah)
                            direktori_output_file_data_acak = __tekan_alt_tab_untuk_file("simpan", "Lokasi file untuk menyimpan data acak (Opsional)", [("File Biner", ".bin"), ("Semua File", "*.*")], ".bin", inisial_nama_file = ".bin")
                            if direktori_output_file_data_acak:
                                perintah_openssl += f" -writerand \"{direktori_output_file_data_acak}\""
                            perintah_openssl += " -verbose"
                            langkah = " > langkah 7\n\n"
                            __bersihkan_layar(alur + langkah)
                            ukuran_bit = input("Masukkan ukuran bit kunci RSA [>= 512] (Opsional) : ").strip()
                            if ukuran_bit.isdigit():
                                ukuran_bit = int(ukuran_bit)
                                if ukuran_bit >= 512:
                                    perintah_openssl += f" {ukuran_bit}"
                                else:
                                    print(f"{Fore.LIGHTRED_EX}Ukuran bit harus lebih dari atau sama dengan 512 (>= 512)!")
                            elif ukuran_bit == "":
                                pass
                            else:
                                print(f"{Fore.LIGHTRED_EX}Input Harus Berupa Angka!")
                            print(f"{Fore.LIGHTYELLOW_EX}Menjalankan perintah [{perintah_openssl}] ...{Fore.LIGHTBLUE_EX}")
                            run(perintah_openssl, shell = True)
                            __enter_untuk_kembali()
                        else:
                            __enter_untuk_kembali(f"{Fore.LIGHTRED_EX}File Tidak Disimpan!")
                    case _:
                        print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!")
                        continue
                break
    except KeyboardInterrupt:
        __tutup_program()
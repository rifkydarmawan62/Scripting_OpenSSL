from subprocess import run, CalledProcessError
from colorama import Fore, Back
from modul import bersihkan_layar, input_kata_sandi_untuk_parameter, input_digest, input_indeks_g, hapus_file_sementara
from tkinter.filedialog import asksaveasfilename as simpan_file
from tkinter.messagebox import askyesno
from os.path import exists
from os import remove
from platform import system as sistem_operasi

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = True, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        file_output = simpan_file(title = "*Pilih lokasi file parameter DSA (Digital Signature Algorithm) disimpan", defaultextension = ".pem", initialfile = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], confirmoverwrite = True)
        if sistem_operasi() == "Windows":
            file_output = file_output.replace("/", "\\")
        if file_output:
            perintah = f"openssl genpkey -out \"{file_output}\" -algorithm DSA -outform PEM -verbose -genparam "
            perintah_tambahan, file_sementara = input_kata_sandi_untuk_parameter("DSA")
            perintah += perintah_tambahan; del perintah_tambahan
            try:
                UKURAN_BIT_DSA = int(input("Masukkan ukuran bit DSA (default = 2048) [> 0] : ").strip())
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
            else:
                if UKURAN_BIT_DSA > 0:
                    perintah += f"-pkeyopt dsa_paramgen_bits:{UKURAN_BIT_DSA} "
                else:
                    print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
            UKURAN_BIT_PARAMETER_Q = input("Masukkan ukuran bit untuk parameter q (default = 224) [160 | 256] : ").strip()
            if UKURAN_BIT_PARAMETER_Q in ("160", "224", "256"):
                perintah += f"-pkeyopt dsa_paramgen_q_bits:{UKURAN_BIT_PARAMETER_Q} "
            elif UKURAN_BIT_PARAMETER_Q == "":
                pass
            else:
                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            perintah += input_digest()
            if askyesno(title = "Pilih tipe", message = "\"Ya\" untuk gunakan parameter generasi FIPS186-2\n\"Tidak\" untuk gunakan parameter generasi FIPS186-4"):
                perintah += "-pkeyopt type:1 "
            perintah += input_indeks_g()
            perintah = perintah.strip()
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = True, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Gagal membuat parameter DSA!{Fore.RESET}")
                if exists(file_output):
                    remove(file_output)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Parameter DSA batal dibuat!{Fore.RESET}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Parameter DSA berhasil dibuat!{Fore.RESET}")
            hapus_file_sementara(file_sementara)
        else:
            print(f"{Fore.LIGHTRED_EX}File paramater DSA tidak disimpan!{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")
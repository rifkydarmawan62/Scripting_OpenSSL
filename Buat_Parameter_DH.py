from subprocess import CalledProcessError
from colorama import Back
from modul import *
from tkinter.filedialog import asksaveasfilename as simpan_file

# Dokumentasi : https://www.openssl.org/docs/man3.2/man1/openssl-genpkey.html#DH-Parameter-Generation-Options

bersihkan_layar(f"{Fore.YELLOW}Memeriksa instalasi OpenSSL ...{Fore.RESET}")
try:
    run("openssl version", shell = False, check = True)
except CalledProcessError:
    print(f"{Fore.LIGHTRED_EX}Perintah OpenSSL tidak ditemukan!{Fore.RESET}")
else:
    print(f"{Fore.LIGHTBLUE_EX}Tekan Alt + Tab untuk membuka jendela baru{Fore.RESET}")
    try:
        file_output = simpan_file(title = "Pilih lokasi file parameter DH disimpan", defaultextension = ".pem", filetypes = [("Privacy Enhanced Mail", "*.pem")], initialfile = ".pem", confirmoverwrite = True)
        if sistem_operasi() == "Windows":
            file_output = file_output.replace("/", "\\")
        if file_output:
            perintah = f"openssl genpkey -out \"{file_output}\" -algorithm DH -outform PEM -genparam -verbose "
            perintah_tambahan, file_sementara = input_kata_sandi_untuk("parameter DH")
            perintah += perintah_tambahan; del perintah_tambahan
            perintah += pilih_group_parameter()
            perintah += input_parameter_prima_p()
            perintah += input_parameter_subprima_q()
            nilai_generator_g = input("Masukkan nilai generator g (default = 2) : ").strip()
            if nilai_generator_g == "":
                pass
            else:
                try:
                    nilai_generator_g = int(nilai_generator_g)
                except ValueError:
                    print(f"{Fore.LIGHTRED_EX}Input harus berupa angka!{Fore.RESET}")
                else:
                    if nilai_generator_g >= 0:
                        perintah += f"-pkeyopt dh_paramgen_generator:{nilai_generator_g} "
                    else:
                        print(f"{Fore.LIGHTRED_EX}Input tidak boleh bilangan negatif!{Fore.RESET}")
            TIPE = input("Pilih tipe parameter [generator | group | default] : ").lower().strip()
            if TIPE in ("generator", "group", "default"):
                perintah += f"-pkeyopt type:\"{TIPE}\" "
            elif TIPE == "":
                pass
            else:
                print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            TIPE_PARAMETER_DH = input("Pilih tipe parameter DH [generator | fips186_2 | fips186_4 | group] : ").strip().lower()
            match TIPE_PARAMETER_DH:
                case "generator":
                    perintah += "-pkeyopt dh_paramgen_type:0 "
                case "fips186_2":
                    perintah += "-pkeyopt dh_paramgen_type:1 "
                case "fips186_4":
                    perintah += "-pkeyopt dh_paramgen_type:2 "
                case "group":
                    perintah += "-pkeyopt dh_paramgen_type:3 "
                case "":
                    pass
                case _:
                    print(f"{Fore.LIGHTRED_EX}Input Tidak Valid!{Fore.RESET}")
            perintah += input_digest()
            perintah += input_indeks_g()
            perintah = perintah.strip()
            print(f"{Fore.YELLOW}Menjalankan perintah {Fore.LIGHTYELLOW_EX}{Back.BLUE}{perintah}{Fore.YELLOW}{Back.RESET} ...{Fore.RESET}")
            try:
                run(perintah, shell = False, check = True)
            except CalledProcessError:
                print(f"{Fore.LIGHTRED_EX}Gagal membuat parameter DH!{Fore.RESET}")
                if exists(file_output):
                    remove(file_output)
            except KeyboardInterrupt:
                print(f"{Fore.LIGHTRED_EX}Parameter DH batal dibuat!{Fore.RESET}")
                if exists(file_output):
                    remove(file_output)
            else:
                print(f"{Fore.LIGHTGREEN_EX}Parameter DH berhasil dibuat!{Fore.RESET}")
            hapus_file_sementara(file_sementara)
    except KeyboardInterrupt:
        print(f"{Fore.LIGHTRED_EX}Interupsi Ctrl + C\nProgram ditutup!{Fore.RESET}")
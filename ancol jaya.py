import csv
from prettytable import PrettyTable
import pwinput
from datetime import datetime

csv_users = "users.csv"
csv_wahana = "wahana.csv"
csv_tiket = "tiket.csv"
csv_pengunjung = "pengunjung.csv"

#======================= Autentikasi ======================
def muat_pengguna():
    pengguna = []
    try:
        with open(csv_users, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pengguna.append(row)
    except FileNotFoundError:
        with open(csv_users, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["username", "password", "role", "saldo"])
            writer.writeheader()
    return pengguna

def simpan_pengguna(pengguna):
    with open(csv_users, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["username", "password", "role", "saldo"])
        writer.writeheader()
        writer.writerows(pengguna)

def sign_up():
    pengguna = muat_pengguna()
    while True:
        username = input("Masukkan username baru (hanya huruf): ")
        if not username.isalpha():
            print("Username hanya boleh berisi huruf. Silahkan coba lagi.")
            continue      
        if any(user["username"] == username for user in pengguna):
            print("Username sudah terdaftar. Silakan gunakan username lain.")
            return False
        break
    password = pwinput.pwinput("Masukkan password: ")
    pengguna.append({"username": username, "password": password, "role": "user", "saldo": "0"})
    simpan_pengguna(pengguna)
    print("Registrasi berhasil! Silahkan login.")
    return True

def sign_in():
    pengguna = muat_pengguna()
    username = input("Masukkan username: ")
    password = pwinput.pwinput("Masukkan password: ")
    
    for user in pengguna:
        if user["username"] == username and user["password"] == password:
            print(f"Selamat datang, {username}!")
            return user["role"], username
    print("Username atau password salah.")
    return None, None

def menu_autentikasi():
    while True:
        tabel = PrettyTable()
        tabel.field_names = ["No", "Menu"]
        tabel.add_rows([
            ["1", "Sign In"],
            ["2", "Sign Up"],
            ["0", "Keluar"]
        ])
        print("\n" + str(tabel))
        pilihan = input("\nPilih opsi: ")
        if pilihan == "1":
            role, username = sign_in()
            if role:
                return role, username
            print("\nLogin gagal. Silakan coba lagi.")
        elif pilihan == "2":
            sign_up()
        elif pilihan == "0":
            print("\nTerima kasih! Sampai jumpa.")
            return None, None
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

#==================== Kelola Saldo ==================
def muat_saldo(username):
    pengguna = muat_pengguna()
    for user in pengguna:
        if user["username"] == username:
            return int(user.get("saldo", 0))
    return 0

def simpan_saldo(username, saldo):
    pengguna = muat_pengguna()
    for user in pengguna:
        if user["username"] == username:
            user["saldo"] = str(saldo)
    simpan_pengguna(pengguna)

def user_isi_saldo(username):
    saldo = muat_saldo(username)
    try:
        tambah = int(input("Masukkan jumlah saldo yang ingin diisi: "))
        if saldo + tambah > 2000000:
            print("Gagal mengisi saldo. Saldo tidak boleh melebihi 2,000,000.")
        else:
            saldo += tambah
            simpan_saldo(username, saldo)
            print(f"Saldo berhasil ditambahkan! Saldo saat ini: {saldo}")
    except ValueError:
        print("Input tidak valid. Masukkan jumlah saldo dalam angka.")
    except Exception as error:
        print(f"Gagal mengisi saldo: {error}")

#===================== Kelola Wahana ==================
def muat_wahana():
    wahana = []
    try:
        with open(csv_wahana, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            wahana = [row for row in reader if row]
    except FileNotFoundError:
        with open(csv_wahana, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Wahana"])
    return wahana

def simpan_wahana(wahana):
    with open(csv_wahana, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Wahana"])
        writer.writerows(wahana)

def read_wahana():
    wahana = muat_wahana()
    if not wahana or not isinstance(wahana, list):
        print("Belum ada wahana yang terdaftar atau format data tidak valid.")
        return
    else:
        print("\nMenampilkan semua wahana")
    table = PrettyTable()
    table.field_names = ["Nama Wahana"]
    for item in wahana:
        table.add_row(item)
    print(table)
    nama_wahana = input("Masukkan nama wahana untuk mencari (atau tekan enter untuk skip searching): ").strip().lower()
    if nama_wahana:
        wahana_list = [(item) for item in wahana if nama_wahana in str(item).lower()]
        if wahana_list:
            print(f"\nWahana dengan nama '{nama_wahana}' tersedia:")
            result_table = PrettyTable()
            result_table.field_names = ["Nama Wahana"]
            for item in wahana_list:
                result_table.add_row(item)
            print(result_table)
        else:
            print(f"Wahana dengan nama '{nama_wahana}' tidak ditemukan.")

def create_wahana():
    try:
        wahana = muat_wahana()
        nama_wahana = input("Masukkan wahana baru: ")
        if not all(kata.isalpha() for kata in nama_wahana.split()):
            print("Nama hanya boleh berisi huruf!")
            return
        if any(item[0] == nama_wahana for item in wahana):
            print("Wahana sudah ada!")
            return
        wahana.append([nama_wahana])
        simpan_wahana(wahana)
        print(f"Wahana {nama_wahana} berhasil ditambahkan.")
    except ValueError:
        print("wahana tidak valid")
        wahana_menu()

def update_wahana():
    try:
        wahana = muat_wahana()
        nama_lama = input("Masukkan nama wahana yang ingin diupdate: ")
        for index, item in enumerate(wahana):
            if item[0] == nama_lama:
                nama_baru = input("Masukkan nama wahana baru: ")
                if not all(kata.isalpha() for kata in nama_baru.split()):
                    print("Nama hanya berisi huruf!")
                    return
                wahana[index] = [nama_baru]
                simpan_wahana(wahana)
                print(f"Wahana {nama_lama} berhasil diupdate menjadi {nama_baru}.")
                return
        print("Wahana tidak ditemukan.")
    except ValueError:
        print("wahana tidak valid")
        wahana_menu()

def delete_wahana():
    try:
        wahana = muat_wahana()
        nama = input("Masukkan nama wahana yang ingin dihapus: ")
        wahana_baru = [item for item in wahana if item[0] != nama]
        if len(wahana_baru) < len(wahana):
            simpan_wahana(wahana_baru)
            print(f"Wahana {nama} berhasil dihapus.")
        else:
            print("Wahana tidak ditemukan.")
    except ValueError:
        print("wahana tidak valid")
        wahana_menu()

def wahana_menu():
    while True:
        print("\nMenu Wahana:")
        print("1. Create Wahana")
        print("2. Read Wahana")
        print("3. Update Wahana")
        print("4. Delete Wahana")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            create_wahana()
        elif pilihan == "2":
            read_wahana()
        elif pilihan == "3":
            update_wahana()
        elif pilihan == "4":
            delete_wahana()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid. Silahkan coba lagi.")

#====================== Kelola Tiket =================
def muat_tiket(csv_tiket):
    tiket_list = []
    try:
        with open(csv_tiket, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames is None or any(field not in reader.fieldnames for field in ["ID", "Nama Tiket", "Tipe", "Harga"]):
                with open(csv_tiket, "w", newline="") as csvfile_write:
                    writer = csv.DictWriter(csvfile_write, fieldnames=["ID", "Nama Tiket", "Tipe", "Harga"])
                    writer.writeheader()
                print("File tiket.csv tidak memiliki header. Menambahkan header.")
                return tiket_list
            
            for row in reader:
                tiket_list.append({
                    "ID": row["ID"],
                    "Nama Tiket": row["Nama Tiket"],
                    "Tipe": row["Tipe"],
                    "Harga": int(row["Harga"])
                })
    except FileNotFoundError:
        with open(csv_tiket, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["ID", "Nama Tiket", "Tipe", "Harga"])
            writer.writeheader()
        print("File tiket.csv belum ada. Membuat file baru dengan header.")
    return tiket_list

def simpan_tiket(tiket_list):
    with open(csv_tiket, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["ID", "Nama Tiket", "Tipe", "Harga"])
        writer.writeheader()
        writer.writerows(tiket_list)

def create_tiket():
    try:
        tiket_list = muat_tiket(csv_tiket)
        tiket_id = str(len(tiket_list) + 1)
        nama = input("Masukkan nama tiket: ")
        tipe = input("Masukkan tipe tiket: ")
        harga = int(input("Masukkan harga tiket: "))
        if not nama.isalpha():
            print("Pastikan nama dan tipe hanya berisi huruf!")
            return
        new_tiket = {"ID": tiket_id, "Nama Tiket": nama, "Tipe": tipe, "Harga": harga}
        tiket_list.append(new_tiket)
        simpan_tiket(tiket_list)
        print("Tiket berhasil ditambahkan.")
    except ValueError:
        print("Tiket tidak valid")
        tiket_menu()

def read_tiket():
    tiket_list = muat_tiket("tiket.csv")
    if not tiket_list:
        print("Belum ada tiket yang terdaftar.")
        return
    else:
        print("\nMenampilkan semua tiket:")
    table = PrettyTable()
    table.field_names = ["ID", "Nama Tiket", "Tipe", "Harga"]
    for tiket in tiket_list:
        table.add_row([tiket["ID"], tiket["Nama Tiket"], tiket["Tipe"], tiket["Harga"]])
    print(table)

    #Fitur searching
    nama_tiket = input("Masukkan nama tiket untuk mencari (atau tekan enter untuk skip searching): ").strip().lower()
    if nama_tiket:
        filtered_tiket = [tiket for tiket in tiket_list if nama_tiket in tiket["Nama Tiket"].lower()]
        if filtered_tiket:
            print(f"Tiket '{nama_tiket}' tersedia:")
            tiket_list = filtered_tiket
        else:
            print(f"Tiket {nama_tiket} tidak ditemukan.")
            return

    #Fitur sorting
    sort_option = input("Ingin mengurutkan tiket berdasarkan harga? (1: Ascending, 2: Descending, Enter: Lewati): ").strip()
    if sort_option == "1":
        tiket_list = sort_data_by_price(tiket_list, descending=False)
    elif sort_option == "2":
        tiket_list = sort_data_by_price(tiket_list, descending=True)

    table = PrettyTable()
    table.field_names = ["ID", "Nama Tiket", "Tipe", "Harga"]
    for tiket in tiket_list:
        table.add_row([tiket["ID"], tiket["Nama Tiket"], tiket["Tipe"], tiket["Harga"]])
    print(table)

    #Fitur searching
    nama_tiket = input("Masukkan nama tiket untuk mencari (atau tekan enter untuk skip searching): ").strip().lower()
    if nama_tiket:
        filtered_tiket = [tiket for tiket in tiket_list if nama_tiket in tiket["Nama Tiket"].lower()]
        if filtered_tiket:
            print(f"Tiket '{nama_tiket}' tersedia:")
            result_table = PrettyTable()
            result_table.field_names = ["ID", "Nama Tiket", "Tipe", "Harga"]
            for tiket in filtered_tiket:
                result_table.add_row([tiket["ID"], tiket["Nama Tiket"], tiket["Tipe"], tiket["Harga"]])
            print(result_table)
        else:
            print(f"Tiket {nama_tiket} tidak ditemukan.")
    
def sort_data_by_price(data, descending=False):
    return sorted(data, key=lambda x: x["Harga"], reverse=descending)

def read_data_berurut():    
    csv_tiket = "tiket.csv"
    data_tiket = muat_tiket(csv_tiket)
    if data_tiket:
        #Ascending
        data_sorted = sort_data_by_price(data_tiket)
        print("Data barang setelah diurutkan berdasarkan harga (ascending):")
        for item in data_sorted:
            print(f"{item['Nama Tiket']}: Rp {item['Harga']}")
        #Descending
        data_sorted_desc = sort_data_by_price(data_tiket, descending=True)
        print("\nData barang setelah diurutkan berdasarkan harga (descending):")
        for item in data_sorted_desc:
            print(f"{item['Nama Tiket']}: Rp {item['Harga']}")
    else:
        print("Tidak ada data tiket yang tersedia untuk ditampilkan.")

def update_tiket():
    try:
        tiket_list = muat_tiket(csv_tiket)
        read_tiket()
        tiket_id = input("Masukkan ID tiket yang ingin diubah: ")
        for tiket in tiket_list:
            while True:
                nama_tiket = input("Masukkan nama tiket baru: ")
                if nama_tiket.isalpha():
                    tiket["Nama tiket"] = nama_tiket
                    break
                else:
                    print("Nama tiket hanya berisi huruf!")
            
            while True:
                tipe_tiket = input("Masukkan tipe tiket yang baru: ")
                if tipe_tiket.isalpha():
                    tiket["Tipe tiket"] = tipe_tiket
                    break
                else:
                    print("Tipe tiket hanya berisi huruf!")
            tiket["Harga tiket"] = input(int("Masukkan harga tiket baru: "))
            simpan_tiket(tiket_list)
            print("Tiket berhasil diupdate.")
            return
        print("Tiket tidak ditemukan.")
    except ValueError:
        print("Tiket tidak valid")
        tiket_menu()

def delete_tiket():
    try:
        tiket_list = muat_tiket(csv_tiket)
        read_tiket()
        tiket_id = input("Masukkan ID tiket yang ingin dihapus: ")
        tiket_baru = [tiket for tiket in tiket_list if tiket["ID"] != tiket_id]
        if len(tiket_baru) < len(tiket_list):
            simpan_tiket(tiket_baru)
            print("Tiket berhasil dihapus.")
        else:
            print("ID tiket tidak ditemukan.")
    except ValueError:
        print("Tiket tidak valid")
        tiket_menu()

def buat_invoice(username, tiket_rincian, tiket_total_harga, saldo):
    table = PrettyTable()
    table.field_names = ["Keterangan", "Detail"]
    table.add_row(["Nama Pembeli", username])
    table.add_row(["Tanggal Pembelian", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    table.add_row(["Detail Tiket", " "])
    for tiket in tiket_rincian:
        total_harga = tiket['Harga'] * tiket['Jumlah']
        table.add_row([
            f"{tiket['Nama Tiket']} (Tipe: {tiket['Tipe']}, x{tiket['Jumlah']})",
            f"Rp {total_harga}"
        ])
    table.add_row(["Total Harga Tiket", f"Rp {tiket_total_harga}"])
    table.add_row(["Sisa Saldo", f"Rp {saldo}"])    
    print("\n===== INVOICE PEMBELIAN =====")
    print(table)
    print("=============================\n")

def tampilkan_tiket(tiket_list):
    table = PrettyTable(["ID", "Nama Tiket", "Tipe", "Harga"])
    for tiket in tiket_list:
        table.add_row([tiket["ID"], tiket["Nama Tiket"], tiket["Tipe"], f"Rp {tiket['Harga']}"])
    print("\nTiket yang tersedia:")
    print(table)

def beli_tiket(username):
    try:
        tiket_list = muat_tiket(csv_tiket)
        if not tiket_list:
            print("Belum ada tiket yang terdaftar.")
            return
        tampilkan_tiket(tiket_list)
        tiket_input = input("Masukkan ID tiket yang ingin dibeli (misal: 1, 2, 3): ")
        tiket_ids = tiket_input.split(", ")
        tiket_dict = {id: tiket_ids.count(id) for id in tiket_ids if id.isdigit()}
        if not tiket_dict:
            print("Input tidak valid, harus berupa ID angka.")
            return
        tiket_rincian, total_harga = [], 0
        for tiket_id, jumlah in tiket_dict.items():
            tiket_terpilih = next((t for t in tiket_list if t["ID"] == tiket_id), None)
            if tiket_terpilih:
                harga_total = tiket_terpilih["Harga"] * jumlah
                total_harga += harga_total
                tiket_rincian.append({
                    "Nama Tiket": tiket_terpilih["Nama Tiket"],
                    "Tipe": tiket_terpilih["Tipe"],
                    "Harga": tiket_terpilih["Harga"],
                    "Jumlah": jumlah
                })
            else:
                print(f"Tiket dengan ID {tiket_id} tidak ditemukan.")
                return
        saldo = muat_saldo(username)
        if saldo < total_harga:
            print("Saldo tidak mencukupi.")
            return
        saldo -= total_harga
        simpan_saldo(username, saldo)
        print("\nTiket berhasil dibeli! Berikut rincian pembelian:")
        for tiket in tiket_rincian:
            print(f"{tiket['Nama Tiket']} (Tipe: {tiket['Tipe']}) x{tiket['Jumlah']} - Rp {tiket['Harga'] * tiket['Jumlah']}")
        buat_invoice(username, tiket_rincian, total_harga, saldo)
        print(f"Sisa saldo Anda: Rp {saldo}")
    except Exception as e:
        print(f"Gagal membeli tiket: {e}")

def tiket_menu():
    while True:
        print("\nMenu Tiket:")
        print("1. Create Tiket")
        print("2. Read Tiket")
        print("3. Update Tiket")
        print("4. Delete Tiket")
        print("0. Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")
        if pilihan == "1":
            create_tiket()
        elif pilihan == "2":
            read_tiket()
        elif pilihan == "3":
            update_tiket()
        elif pilihan == "4":
            delete_tiket()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid. Silahkan coba lagi.")

#==================== Kelola Pengunjung ==================
def muat_pengunjung():
    pengunjung = []
    try:
        with open(csv_pengunjung, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pengunjung.append(row)
    except FileNotFoundError:
        with open(csv_pengunjung, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Nomor", "Nama"])
            writer.writeheader()
    return pengunjung

def simpan_pengunjung(pengunjung):
    with open(csv_pengunjung, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Nomor", "Nama"])
        writer.writeheader()
        writer.writerows(pengunjung)

def create_pengunjung():
    try:
        pengunjung = muat_pengunjung()
        nomor_pengunjung = str(len(pengunjung) + 1)
        nama_pengunjung = input("Masukkan nama pengunjung baru: ")
        if not nama_pengunjung.isalpha():
            print("Nama hanya berisi huruf!")
            return
        new_pengunjung = {"Nomor": nomor_pengunjung, "Nama": nama_pengunjung}
        pengunjung.append(new_pengunjung)
        simpan_pengunjung(pengunjung)
        print(f"Pengunjung {nama_pengunjung} berhasil ditambahkan.")
    except ValueError:
        print("Pengunjung tidak valid")
        pengunjung_menu()

def read_pengunjung():
    pengunjung = muat_pengunjung()
    if not pengunjung:
        print("Belum ada pengunjung yang terdaftar.")
        return
    table = PrettyTable()
    table.field_names = ["Nomor", "Nama"]
    for item in pengunjung:
        table.add_row([item["Nomor"], item["Nama"]])
    print(table)

def delete_pengunjung():
    try:
        pengunjung = muat_pengunjung()
        nama = input("Masukkan nama pengunjung yang ingin dihapus: ")
        pengunjung_baru = [item for item in pengunjung if item["Nama"] != nama]
        if len(pengunjung_baru) < len(pengunjung):
            simpan_pengunjung(pengunjung_baru)
            print(f"Pengunjung {nama} berhasil dihapus.")
        else:
            print("Pengunjung tidak ditemukan.")
    except ValueError:
        print("Pengunjung tidak valid")
        pengunjung_menu()

def pengunjung_menu():
    while True:
        print("\nMenu Pengunjung:")
        print("1. Create Pengunjung")
        print("2. Read Pengunjung")
        print("3. Delete Pengunjung")
        print("0. Keluar")
        
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            create_pengunjung()
        elif pilihan == "2":
            read_pengunjung()
        elif pilihan == "3":
            delete_pengunjung()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid. Silahkan coba lagi.")

#==================== Menu Admin ===================
def menu_admin():
    while True:
        print("\nMenu Admin:")
        print("1. Kelola Wahana")
        print("2. Kelola Tiket")
        print("3. Kelola Pengunjung")
        print("0. Keluar")
        
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            wahana_menu()
        elif pilihan == "2":
            tiket_menu()
        elif pilihan == "3":
            pengunjung_menu()
        elif pilihan == "0":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silahkan coba lagi.")

def read_menu():
    while True:
        print("\nMenu Read")
        print("1. Read wahana")
        print("2. Read tiket")
        print("0. Kembali ke menu utama")

        pilihan = input("Pilih opsi: ")
        if pilihan == "1":
            read_wahana()
        elif pilihan == "2":
            read_tiket()
        elif pilihan == "0":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silahkan coba lagi.")

#==================== Menu User ===================
def menu_user(username):
    while True:
        print("\nMenu User:")
        print("1. Read(wahana & tiket)")
        print("2. isi saldo")
        print("3. Beli tiket")
        print("0. Keluar")
        
        pilihan = input("Pilih opsi: ")
        if pilihan == "1":
            read_menu()
        elif pilihan == "2":
            user_isi_saldo(username)
        elif pilihan == "3":
            beli_tiket(username)
        elif pilihan == "0":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silahkan coba lagi.")

#==================== Menu Utama ===================
if __name__ == "__main__":
    role, username = menu_autentikasi()
    if role:
        if role == "admin":
            menu_admin()
        elif role == "user":
            menu_user(username)
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')

class HospitalManagementSystem:
    def __init__(self):
        """Initialize database connection"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='hospital_management',
                user='root',  # Ganti sesuai username MySQL Anda
                password=''   # Ganti sesuai password MySQL Anda
            )
            self.cursor = self.connection.cursor()
            print("✅ Koneksi database berhasil!")
        except mysql.connector.Error as e:
            print(f"❌ Error koneksi database: {e}")
            exit()

    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🏥 SISTEM MANAJEMEN DATA PASIEN RUMAH SAKIT")
        print("="*60)
        print("1. 📋 Tampilkan Data Pasien")
        print("2. 📊 Statistik Pasien")
        print("3. 📈 Visualisasi Data")
        print("4. ➕ Tambah Data Pasien Baru")
        print("5. 🔍 Cari Pasien")
        print("6. ✏️  Update Data Pasien")
        print("7. 🗑️  Hapus Data Pasien")
        print("0. 🚪 Keluar")
        print("="*60)

    # FITUR 1: READ TABLE (15%)
    def read_table(self):
        """Display all patient data in table format"""
        try:
            print("\n🔍 PILIHAN TAMPILAN DATA:")
            print("1. Semua Data Pasien")
            print("2. Filter berdasarkan Jenis Rawat")
            print("3. Filter berdasarkan Jenis Kelamin")
            print("4. Filter berdasarkan Rentang Umur")
            
            choice = input("\nPilih opsi (1-4): ")
            
            if choice == '1':
                query = "SELECT * FROM patients ORDER BY patient_id"
                self.cursor.execute(query)
                
            elif choice == '2':
                print("\nJenis Rawat:")
                print("1. Rawat Jalan")
                print("2. Rawat Inap")
                rawat_choice = input("Pilih (1-2): ")
                jenis_rawat = "Rawat Jalan" if rawat_choice == '1' else "Rawat Inap"
                
                query = "SELECT * FROM patients WHERE jenis_rawat = %s ORDER BY patient_id"
                self.cursor.execute(query, (jenis_rawat,))
                
            elif choice == '3':
                print("\nJenis Kelamin:")
                print("1. Laki-laki")
                print("2. Perempuan")
                gender_choice = input("Pilih (1-2): ")
                jenis_kelamin = "Laki-laki" if gender_choice == '1' else "Perempuan"
                
                query = "SELECT * FROM patients WHERE jenis_kelamin = %s ORDER BY patient_id"
                self.cursor.execute(query, (jenis_kelamin,))
                
            elif choice == '4':
                umur_min = int(input("Umur minimum: "))
                umur_max = int(input("Umur maksimum: "))
                
                query = "SELECT * FROM patients WHERE umur BETWEEN %s AND %s ORDER BY patient_id"
                self.cursor.execute(query, (umur_min, umur_max))
                
            else:
                print("❌ Pilihan tidak valid!")
                return

            results = self.cursor.fetchall()
            
            if results:
                headers = ['ID', 'Nama Pasien', 'Umur', 'Jenis Kelamin', 'Jenis Rawat', 'Biaya', 'Tanggal Masuk', 'Alamat', 'No. Telp']
                
                # Format data untuk tampilan yang lebih baik
                formatted_data = []
                for row in results:
                    formatted_row = list(row)
                    # Format biaya dengan separator ribuan
                    formatted_row[5] = f"Rp {formatted_row[5]:,.2f}"
                    formatted_data.append(formatted_row)
                
                print(f"\n📋 DATA PASIEN (Total: {len(results)} pasien)")
                print("="*150)
                print(tabulate(formatted_data, headers=headers, tablefmt='grid'))
            else:
                print("\n❌ Tidak ada data yang ditemukan!")
                
        except mysql.connector.Error as e:
            print(f"❌ Error saat mengambil data: {e}")
        except ValueError:
            print("❌ Input tidak valid! Masukkan angka yang benar.")

    # FITUR 2: SHOW STATISTIK (15%)
    def show_statistics(self):
        """Display descriptive statistics"""
        try:
            print("\n📊 STATISTIK DATA PASIEN")
            print("="*50)
            
            # Statistik Umur
            query_umur = """
            SELECT 
                AVG(umur) as rata_umur,
                MIN(umur) as umur_min,
                MAX(umur) as umur_max,
                COUNT(*) as total_pasien
            FROM patients
            """
            self.cursor.execute(query_umur)
            umur_stats = self.cursor.fetchone()
            
            # Statistik Biaya
            query_biaya = """
            SELECT 
                AVG(biaya_pengobatan) as rata_biaya,
                MIN(biaya_pengobatan) as biaya_min,
                MAX(biaya_pengobatan) as biaya_max,
                SUM(biaya_pengobatan) as total_biaya
            FROM patients
            """
            self.cursor.execute(query_biaya)
            biaya_stats = self.cursor.fetchone()
            
            # Statistik per kategori
            query_gender = """
            SELECT jenis_kelamin, COUNT(*) as jumlah, AVG(biaya_pengobatan) as rata_biaya
            FROM patients 
            GROUP BY jenis_kelamin
            """
            self.cursor.execute(query_gender)
            gender_stats = self.cursor.fetchall()
            
            query_rawat = """
            SELECT jenis_rawat, COUNT(*) as jumlah, AVG(biaya_pengobatan) as rata_biaya
            FROM patients 
            GROUP BY jenis_rawat
            """
            self.cursor.execute(query_rawat)
            rawat_stats = self.cursor.fetchall()
            
            # Display statistics
            print("\n👥 STATISTIK UMUR PASIEN:")
            print(f"   • Rata-rata umur: {umur_stats[0]:.1f} tahun")
            print(f"   • Umur termuda: {umur_stats[1]} tahun")
            print(f"   • Umur tertua: {umur_stats[2]} tahun")
            print(f"   • Total pasien: {umur_stats[3]} orang")
            
            print("\n💰 STATISTIK BIAYA PENGOBATAN:")
            print(f"   • Rata-rata biaya: Rp {biaya_stats[0]:,.2f}")
            print(f"   • Biaya terendah: Rp {biaya_stats[1]:,.2f}")
            print(f"   • Biaya tertinggi: Rp {biaya_stats[2]:,.2f}")
            print(f"   • Total biaya: Rp {biaya_stats[3]:,.2f}")
            
            print("\n👨‍👩‍👦 STATISTIK BERDASARKAN JENIS KELAMIN:")
            for stat in gender_stats:
                print(f"   • {stat[0]}: {stat[1]} orang (Rata-rata biaya: Rp {stat[2]:,.2f})")
            
            print("\n🏥 STATISTIK BERDASARKAN JENIS RAWAT:")
            for stat in rawat_stats:
                print(f"   • {stat[0]}: {stat[1]} orang (Rata-rata biaya: Rp {stat[2]:,.2f})")
                
        except mysql.connector.Error as e:
            print(f"❌ Error saat mengambil statistik: {e}")

    # FITUR 3: DATA VISUALIZATION (20%)
    def data_visualization(self):
        """Display data visualizations"""
        try:
            print("\n📈 PILIHAN VISUALISASI DATA:")
            print("1. Pie Chart - Proporsi Jenis Kelamin")
            print("2. Bar Chart - Proporsi Jenis Rawat")
            print("3. Histogram - Distribusi Umur")
            print("4. Histogram - Distribusi Biaya Pengobatan")
            print("5. Tampilkan Semua Visualisasi")
            
            choice = input("\nPilih visualisasi (1-5): ")
            
            if choice == '1' or choice == '5':
                self.plot_gender_pie()
            if choice == '2' or choice == '5':
                self.plot_rawat_bar()
            if choice == '3' or choice == '5':
                self.plot_age_histogram()
            if choice == '4' or choice == '5':
                self.plot_cost_histogram()
            
            if choice in ['1', '2', '3', '4', '5']:
                plt.show()
            else:
                print("❌ Pilihan tidak valid!")
                
        except Exception as e:
            print(f"❌ Error saat membuat visualisasi: {e}")

    def plot_gender_pie(self):
        """Create pie chart for gender distribution"""
        query = "SELECT jenis_kelamin, COUNT(*) FROM patients GROUP BY jenis_kelamin"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        labels = [row[0] for row in results]
        sizes = [row[1] for row in results]
        colors = ['lightblue', 'lightpink']
        
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Proporsi Pasien Berdasarkan Jenis Kelamin', fontsize=14, fontweight='bold')
        plt.axis('equal')

    def plot_rawat_bar(self):
        """Create bar chart for treatment type distribution"""
        query = "SELECT jenis_rawat, COUNT(*) FROM patients GROUP BY jenis_rawat"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        labels = [row[0] for row in results]
        counts = [row[1] for row in results]
        colors = ['skyblue', 'lightcoral']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, counts, color=colors)
        plt.title('Jumlah Pasien Berdasarkan Jenis Rawat', fontsize=14, fontweight='bold')
        plt.xlabel('Jenis Rawat', fontsize=12)
        plt.ylabel('Jumlah Pasien', fontsize=12)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')

    def plot_age_histogram(self):
        """Create histogram for age distribution"""
        query = "SELECT umur FROM patients"
        self.cursor.execute(query)
        ages = [row[0] for row in self.cursor.fetchall()]
        
        plt.figure(figsize=(10, 6))
        plt.hist(ages, bins=10, color='lightgreen', edgecolor='black', alpha=0.7)
        plt.title('Distribusi Umur Pasien', fontsize=14, fontweight='bold')
        plt.xlabel('Umur (tahun)', fontsize=12)
        plt.ylabel('Jumlah Pasien', fontsize=12)
        plt.grid(axis='y', alpha=0.3)

    def plot_cost_histogram(self):
        """Create histogram for cost distribution"""
        query = "SELECT biaya_pengobatan FROM patients"
        self.cursor.execute(query)
        costs = [float(row[0]) for row in self.cursor.fetchall()]
        
        plt.figure(figsize=(10, 6))
        plt.hist(costs, bins=10, color='gold', edgecolor='black', alpha=0.7)
        plt.title('Distribusi Biaya Pengobatan', fontsize=14, fontweight='bold')
        plt.xlabel('Biaya Pengobatan (Rp)', fontsize=12)
        plt.ylabel('Jumlah Pasien', fontsize=12)
        plt.ticklabel_format(style='plain', axis='x')
        plt.grid(axis='y', alpha=0.3)

    # FITUR 4: ADD DATA (15%)
    def add_patient(self):
        """Add new patient data"""
        try:
            print("\n➕ TAMBAH DATA PASIEN BARU")
            print("="*40)
            
            # Input validation
            nama = input("Nama Pasien: ").strip()
            if not nama:
                print("❌ Nama tidak boleh kosong!")
                return
            
            try:
                umur = int(input("Umur: "))
                if umur < 0 or umur > 150:
                    print("❌ Umur tidak valid! (0-150)")
                    return
            except ValueError:
                print("❌ Umur harus berupa angka!")
                return
            
            print("\nJenis Kelamin:")
            print("1. Laki-laki")
            print("2. Perempuan")
            gender_choice = input("Pilih (1-2): ")
            if gender_choice == '1':
                jenis_kelamin = 'Laki-laki'
            elif gender_choice == '2':
                jenis_kelamin = 'Perempuan'
            else:
                print("❌ Pilihan jenis kelamin tidak valid!")
                return
            
            print("\nJenis Rawat:")
            print("1. Rawat Jalan")
            print("2. Rawat Inap")
            rawat_choice = input("Pilih (1-2): ")
            if rawat_choice == '1':
                jenis_rawat = 'Rawat Jalan'
            elif rawat_choice == '2':
                jenis_rawat = 'Rawat Inap'
            else:
                print("❌ Pilihan jenis rawat tidak valid!")
                return
            
            try:
                biaya = float(input("Biaya Pengobatan (Rp): "))
                if biaya < 0:
                    print("❌ Biaya tidak boleh negatif!")
                    return
            except ValueError:
                print("❌ Biaya harus berupa angka!")
                return
            
            tanggal_masuk = input("Tanggal Masuk (YYYY-MM-DD): ")
            try:
                datetime.strptime(tanggal_masuk, '%Y-%m-%d')
            except ValueError:
                print("❌ Format tanggal salah! Gunakan YYYY-MM-DD")
                return
            
            alamat = input("Alamat: ").strip()
            nomor_telepon = input("Nomor Telepon: ").strip()
            
            # Confirmation
            print(f"\n📋 KONFIRMASI DATA BARU:")
            print(f"   Nama: {nama}")
            print(f"   Umur: {umur} tahun")
            print(f"   Jenis Kelamin: {jenis_kelamin}")
            print(f"   Jenis Rawat: {jenis_rawat}")
            print(f"   Biaya: Rp {biaya:,.2f}")
            print(f"   Tanggal Masuk: {tanggal_masuk}")
            print(f"   Alamat: {alamat}")
            print(f"   Nomor Telepon: {nomor_telepon}")
            
            confirm = input("\nSimpan data ini? (y/n): ").lower()
            if confirm == 'y':
                query = """
                INSERT INTO patients (nama_pasien, umur, jenis_kelamin, jenis_rawat, 
                                    biaya_pengobatan, tanggal_masuk, alamat, nomor_telepon)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (nama, umur, jenis_kelamin, jenis_rawat, biaya, tanggal_masuk, alamat, nomor_telepon)
                
                self.cursor.execute(query, values)
                self.connection.commit()
                
                print("✅ Data pasien berhasil ditambahkan!")
            else:
                print("❌ Data tidak disimpan.")
                
        except mysql.connector.Error as e:
            print(f"❌ Error saat menambah data: {e}")

    # FITUR TAMBAHAN untuk User Experience (10%)
    def search_patient(self):
        """Search patient by name or ID"""
        try:
            print("\n🔍 CARI PASIEN")
            print("="*30)
            print("1. Cari berdasarkan ID")
            print("2. Cari berdasarkan Nama")
            
            choice = input("Pilih opsi (1-2): ")
            
            if choice == '1':
                try:
                    patient_id = int(input("Masukkan ID Pasien: "))
                    query = "SELECT * FROM patients WHERE patient_id = %s"
                    self.cursor.execute(query, (patient_id,))
                except ValueError:
                    print("❌ ID harus berupa angka!")
                    return
                    
            elif choice == '2':
                nama = input("Masukkan nama pasien (atau sebagian nama): ")
                query = "SELECT * FROM patients WHERE nama_pasien LIKE %s"
                self.cursor.execute(query, (f"%{nama}%",))
            else:
                print("❌ Pilihan tidak valid!")
                return
            
            results = self.cursor.fetchall()
            
            if results:
                headers = ['ID', 'Nama Pasien', 'Umur', 'Jenis Kelamin', 'Jenis Rawat', 'Biaya', 'Tanggal Masuk', 'Alamat', 'No. Telp']
                
                formatted_data = []
                for row in results:
                    formatted_row = list(row)
                    formatted_row[5] = f"Rp {formatted_row[5]:,.2f}"
                    formatted_data.append(formatted_row)
                
                print(f"\n🔍 HASIL PENCARIAN ({len(results)} pasien ditemukan):")
                print("="*150)
                print(tabulate(formatted_data, headers=headers, tablefmt='grid'))
            else:
                print("❌ Data tidak ditemukan!")
                
        except mysql.connector.Error as e:
            print(f"❌ Error saat mencari data: {e}")

    def update_patient(self):
        """Update patient data"""
        try:
            patient_id = int(input("Masukkan ID pasien yang akan diupdate: "))
            
            # Check if patient exists
            query = "SELECT * FROM patients WHERE patient_id = %s"
            self.cursor.execute(query, (patient_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print("❌ Pasien dengan ID tersebut tidak ditemukan!")
                return
            
            print(f"\nData pasien saat ini:")
            headers = ['ID', 'Nama', 'Umur', 'Gender', 'Rawat', 'Biaya', 'Tanggal', 'Alamat', 'Telp']
            formatted_result = list(result)
            formatted_result[5] = f"Rp {formatted_result[5]:,.2f}"
            print(tabulate([formatted_result], headers=headers, tablefmt='grid'))
            
            print(f"\n✏️ UPDATE DATA PASIEN (kosongkan jika tidak ingin mengubah)")
            print("="*60)
            
            new_nama = input(f"Nama baru [{result[1]}]: ").strip() or result[1]
            
            umur_input = input(f"Umur baru [{result[2]}]: ").strip()
            new_umur = int(umur_input) if umur_input else result[2]
            
            biaya_input = input(f"Biaya baru [{result[5]}]: ").strip()
            new_biaya = float(biaya_input) if biaya_input else result[5]
            
            new_alamat = input(f"Alamat baru [{result[7]}]: ").strip() or result[7]
            new_telp = input(f"Telepon baru [{result[8]}]: ").strip() or result[8]
            
            # Update query
            update_query = """
            UPDATE patients 
            SET nama_pasien = %s, umur = %s, biaya_pengobatan = %s, alamat = %s, nomor_telepon = %s 
            WHERE patient_id = %s
            """
            
            self.cursor.execute(update_query, (new_nama, new_umur, new_biaya, new_alamat, new_telp, patient_id))
            self.connection.commit()
            
            print("✅ Data pasien berhasil diupdate!")
            
        except ValueError:
            print("❌ Input tidak valid!")
        except mysql.connector.Error as e:
            print(f"❌ Error saat mengupdate data: {e}")

    def delete_patient(self):
        """Delete patient data"""
        try:
            patient_id = int(input("Masukkan ID pasien yang akan dihapus: "))
            
            # Check if patient exists
            query = "SELECT * FROM patients WHERE patient_id = %s"
            self.cursor.execute(query, (patient_id,))
            result = self.cursor.fetchone()
            
            if not result:
                print("❌ Pasien dengan ID tersebut tidak ditemukan!")
                return
            
            print(f"\nData pasien yang akan dihapus:")
            headers = ['ID', 'Nama', 'Umur', 'Gender', 'Rawat', 'Biaya', 'Tanggal', 'Alamat', 'Telp']
            formatted_result = list(result)
            formatted_result[5] = f"Rp {formatted_result[5]:,.2f}"
            print(tabulate([formatted_result], headers=headers, tablefmt='grid'))
            
            confirm = input(f"\n⚠️ Yakin ingin menghapus data pasien '{result[1]}'? (ketik 'HAPUS' untuk konfirmasi): ")
            
            if confirm == 'HAPUS':
                delete_query = "DELETE FROM patients WHERE patient_id = %s"
                self.cursor.execute(delete_query, (patient_id,))
                self.connection.commit()
                print("✅ Data pasien berhasil dihapus!")
            else:
                print("❌ Penghapusan dibatalkan.")
                
        except ValueError:
            print("❌ ID harus berupa angka!")
        except mysql.connector.Error as e:
            print(f"❌ Error saat menghapus data: {e}")

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("✅ Koneksi database ditutup.")

    def run(self):
        """Main program loop"""
        print("🏥 Selamat datang di Sistem Manajemen Pasien Rumah Sakit!")
        
        while True:
            self.show_menu()
            choice = input("\nPilih menu (0-7): ").strip()
            
            if choice == '1':
                self.read_table()
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                self.data_visualization()
            elif choice == '4':
                self.add_patient()
            elif choice == '5':
                self.search_patient()
            elif choice == '6':
                self.update_patient()
            elif choice == '7':
                self.delete_patient()
            elif choice == '0':
                print("\n👋 Terima kasih telah menggunakan sistem kami!")
                break
            else:
                print("❌ Pilihan tidak valid! Silakan pilih 0-7.")
            
            input("\nTekan Enter untuk melanjutkan...")

# Main execution
if __name__ == "__main__":
    try:
        hospital_system = HospitalManagementSystem()
        hospital_system.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program dihentikan oleh user.")
    finally:
        try:
            hospital_system.close_connection()
        except:
            pass
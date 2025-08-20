-- Create Database
CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

-- Create patients table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    nama_pasien VARCHAR(100) NOT NULL,
    umur INT NOT NULL,
    jenis_kelamin ENUM('Laki-laki', 'Perempuan') NOT NULL,
    jenis_rawat ENUM('Rawat Jalan', 'Rawat Inap') NOT NULL,
    biaya_pengobatan DECIMAL(10,2) NOT NULL,
    tanggal_masuk DATE NOT NULL,
    alamat VARCHAR(200),
    nomor_telepon VARCHAR(15)
);

-- Insert sample data
INSERT INTO patients (nama_pasien, umur, jenis_kelamin, jenis_rawat, biaya_pengobatan, tanggal_masuk, alamat, nomor_telepon) VALUES
('Ahmad Wijaya', 45, 'Laki-laki', 'Rawat Inap', 2500000.00, '2024-01-15', 'Jl. Merdeka No. 123', '081234567890'),
('Siti Nurhaliza', 32, 'Perempuan', 'Rawat Jalan', 150000.00, '2024-01-20', 'Jl. Sudirman No. 45', '081298765432'),
('Budi Santoso', 28, 'Laki-laki', 'Rawat Jalan', 200000.00, '2024-01-22', 'Jl. Gatot Subroto No. 67', '081356789012'),
('Dewi Sartika', 55, 'Perempuan', 'Rawat Inap', 3200000.00, '2024-01-25', 'Jl. Diponegoro No. 89', '081445678901'),
('Eko Prasetyo', 38, 'Laki-laki', 'Rawat Jalan', 175000.00, '2024-02-01', 'Jl. Ahmad Yani No. 12', '081567890123'),
('Rina Kusuma', 42, 'Perempuan', 'Rawat Inap', 1800000.00, '2024-02-05', 'Jl. Veteran No. 34', '081678901234'),
('Joko Widodo', 50, 'Laki-laki', 'Rawat Inap', 2800000.00, '2024-02-08', 'Jl. Pancasila No. 56', '081789012345'),
('Maya Sari', 25, 'Perempuan', 'Rawat Jalan', 120000.00, '2024-02-10', 'Jl. Kartini No. 78', '081890123456'),
('Rudi Hartono', 60, 'Laki-laki', 'Rawat Inap', 4200000.00, '2024-02-12', 'Jl. Pahlawan No. 90', '081901234567'),
('Lisa Permata', 35, 'Perempuan', 'Rawat Jalan', 180000.00, '2024-02-15', 'Jl. Proklamasi No. 23', '081012345678'),
('Hendra Gunawan', 47, 'Laki-laki', 'Rawat Inap', 2100000.00, '2024-02-18', 'Jl. Kemerdekaan No. 45', '081123456789'),
('Indira Sari', 29, 'Perempuan', 'Rawat Jalan', 165000.00, '2024-02-20', 'Jl. Hayam Wuruk No. 67', '081234567801'),
('Bambang Sutrisno', 52, 'Laki-laki', 'Rawat Inap', 3500000.00, '2024-02-22', 'Jl. Gajah Mada No. 89', '081345678902'),
('Sri Wahyuni', 44, 'Perempuan', 'Rawat Jalan', 195000.00, '2024-02-25', 'Jl. Thamrin No. 12', '081456789013'),
('Agus Setiawan', 36, 'Laki-laki', 'Rawat Inap', 2200000.00, '2024-02-28', 'Jl. Rasuna Said No. 34', '081567890124');

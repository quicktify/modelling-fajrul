import json
import csv
import chardet
import os

# --- Konfigurasi Nama File ---
file_json = 'sources/slangwords.json'
file_csv = 'sources/slang_indo.csv'
file_csv2 = 'sources/slang-indo.csv'
file_txt_tab = 'sources/slangwords.txt'
file_txt_colon = 'sources/indo_slang_words_zeroid.txt'
output_json_file = 'merged_slang_dict.json'

# --- Inisialisasi Kamus Gabungan ---
merged_dict = {}
total_loaded_count = 0
skipped_lines = 0

print("Memulai proses penggabungan kamus slang...")

# --- Fungsi Helper untuk Deteksi Encoding ---
def detect_encoding(filepath):
    """Mendeteksi encoding file."""
    try:
        with open(filepath, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(10000)) # Baca 10KB untuk deteksi
        print(f"   Encoding terdeteksi untuk '{os.path.basename(filepath)}': {result['encoding']} (confidence: {result['confidence']:.2f})")
        return result['encoding']
    except FileNotFoundError:
        print(f"   PERINGATAN: File '{os.path.basename(filepath)}' tidak ditemukan.")
        return None
    except Exception as e:
        print(f"   ERROR saat mendeteksi encoding untuk '{os.path.basename(filepath)}': {e}")
        return None

# --- 1. Proses File JSON (slangwords.json) ---
print(f"\n1. Memproses '{file_json}'...")
try:
    with open(file_json, 'r', encoding='utf-8') as f:
        slang_dict_json = json.load(f)
        # Pastikan semua key dan value lowercase
        slang_dict_json_lower = {str(k).lower().strip(): str(v).lower().strip() for k, v in slang_dict_json.items()}
        count_before = len(merged_dict)
        merged_dict.update(slang_dict_json_lower)
        count_after = len(merged_dict)
        added_count = count_after - count_before
        total_loaded_count += len(slang_dict_json_lower)
        print(f"   Berhasil memuat {len(slang_dict_json_lower)} entri.")
        print(f"   Menambahkan {added_count} entri unik baru ke kamus gabungan.")
except FileNotFoundError:
    print(f"   PERINGATAN: File '{file_json}' tidak ditemukan.")
except json.JSONDecodeError as e:
    print(f"   ERROR: Gagal memproses JSON di '{file_json}': {e}")
except Exception as e:
    print(f"   ERROR saat memproses '{file_json}': {e}")

# --- 2. Proses File CSV (slang_indo.csv) ---
print(f"\n2. Memproses '{file_csv}'...")
loaded_csv_count = 0
try:
    # Coba buka dengan UTF-8, encoding umum untuk CSV
    with open(file_csv, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        temp_dict_csv = {}
        for i, row in enumerate(reader):
            if len(row) >= 2:
                slang = row[0].lower().strip()
                standard = row[1].lower().strip()
                if slang and standard: # Pastikan tidak kosong setelah strip
                    temp_dict_csv[slang] = standard
                    loaded_csv_count += 1
                else:
                    print(f"   PERINGATAN (Baris {i+1} CSV): Melewati baris karena slang atau standar kosong setelah strip: {row}")
                    skipped_lines += 1
            else:
                print(f"   PERINGATAN (Baris {i+1} CSV): Melewati baris karena tidak memiliki 2 kolom: {row}")
                skipped_lines += 1

        count_before = len(merged_dict)
        merged_dict.update(temp_dict_csv) # Update dengan data dari CSV
        count_after = len(merged_dict)
        added_count = count_after - count_before
        total_loaded_count += loaded_csv_count
        print(f"   Berhasil memuat {loaded_csv_count} entri valid.")
        print(f"   Menambahkan {added_count} entri unik baru ke kamus gabungan.")

except FileNotFoundError:
    print(f"   PERINGATAN: File '{file_csv}' tidak ditemukan.")
except UnicodeDecodeError:
    print(f"   ERROR: Gagal membaca '{file_csv}' dengan encoding UTF-8. Coba encoding lain jika perlu (misal: 'latin-1').")
except Exception as e:
    print(f"   ERROR saat memproses '{file_csv}': {e}")

# --- 3. Proses File CSV Ke-2 (slang-indo.csv) ---
print(f"\n3. Memproses '{file_csv2}'...")
loaded_csv_count = 0
try:
    # Coba buka dengan UTF-8, encoding umum untuk CSV
    with open(file_csv, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        temp_dict_csv = {}
        for i, row in enumerate(reader):
            if len(row) >= 2:
                slang = row[0].lower().strip()
                standard = row[1].lower().strip()
                if slang and standard: # Pastikan tidak kosong setelah strip
                    temp_dict_csv[slang] = standard
                    loaded_csv_count += 1
                else:
                    print(f"   PERINGATAN (Baris {i+1} CSV): Melewati baris karena slang atau standar kosong setelah strip: {row}")
                    skipped_lines += 1
            else:
                print(f"   PERINGATAN (Baris {i+1} CSV): Melewati baris karena tidak memiliki 2 kolom: {row}")
                skipped_lines += 1

        count_before = len(merged_dict)
        merged_dict.update(temp_dict_csv) # Update dengan data dari CSV
        count_after = len(merged_dict)
        added_count = count_after - count_before
        total_loaded_count += loaded_csv_count
        print(f"   Berhasil memuat {loaded_csv_count} entri valid.")
        print(f"   Menambahkan {added_count} entri unik baru ke kamus gabungan.")

except FileNotFoundError:
    print(f"   PERINGATAN: File '{file_csv}' tidak ditemukan.")
except UnicodeDecodeError:
    print(f"   ERROR: Gagal membaca '{file_csv}' dengan encoding UTF-8. Coba encoding lain jika perlu (misal: 'latin-1').")
except Exception as e:
    print(f"   ERROR saat memproses '{file_csv}': {e}")

# --- 4. Proses File TXT Tab (slangwords.txt) ---
print(f"\n4. Memproses '{file_txt_tab}'...")
loaded_txt_tab_count = 0
encoding_tab = detect_encoding(file_txt_tab)
if encoding_tab:
    try:
        with open(file_txt_tab, 'r', encoding=encoding_tab) as f:
            temp_dict_tab = {}
            for i, line in enumerate(f):
                parts = line.strip().split('\t') # Pisahkan berdasarkan Tab
                if len(parts) == 2:
                    slang = parts[0].lower().strip()
                    standard = parts[1].lower().strip()
                    if slang and standard:
                        temp_dict_tab[slang] = standard
                        loaded_txt_tab_count += 1
                    else:
                        print(f"   PERINGATAN (Baris {i+1} TXT Tab): Melewati baris karena slang atau standar kosong setelah strip: '{line.strip()}'")
                        skipped_lines += 1
                elif line.strip(): # Hanya beri peringatan jika baris tidak kosong tapi format salah
                    print(f"   PERINGATAN (Baris {i+1} TXT Tab): Melewati baris karena format tidak 'slang<TAB>standar': '{line.strip()}'")
                    skipped_lines += 1

            count_before = len(merged_dict)
            merged_dict.update(temp_dict_tab) # Update dengan data dari TXT Tab
            count_after = len(merged_dict)
            added_count = count_after - count_before
            total_loaded_count += loaded_txt_tab_count
            print(f"   Berhasil memuat {loaded_txt_tab_count} entri valid.")
            print(f"   Menambahkan {added_count} entri unik baru ke kamus gabungan.")

    except Exception as e:
        print(f"   ERROR saat memproses '{file_txt_tab}' dengan encoding {encoding_tab}: {e}")

# --- 5. Proses File TXT Colon (indo_slang_words_zeroid.txt) ---
print(f"\n5. Memproses '{file_txt_colon}'...")
loaded_txt_colon_count = 0
skipped_lines_colon = 0 # Gunakan variabel hitungan terpisah
temp_dict_colon = {} # Inisialisasi di luar try

encoding_colon = detect_encoding(file_txt_colon)
if encoding_colon:
    # Daftar encoding yang akan dicoba, prioritaskan UTF-8 jika ASCII terdeteksi
    encodings_to_try = []
    if encoding_colon.lower() == 'ascii':
        # Jika terdeteksi ASCII, kemungkinan salah, prioritaskan UTF-8
        encodings_to_try = ['utf-8', 'latin-1', encoding_colon]
    else:
        # Jika terdeteksi lain, coba itu dulu, lalu UTF-8/Latin-1
        encodings_to_try = [encoding_colon, 'utf-8', 'latin-1']

    file_processed = False
    for enc in encodings_to_try:
        if file_processed: # Jika sudah berhasil diproses, hentikan loop
            break
        print(f"   Mencoba membaca dengan encoding: '{enc}'...")
        try:
            with open(file_txt_colon, 'r', encoding=enc) as f:
                # Reset hitungan untuk percobaan encoding ini
                current_load_count = 0
                current_skip_count = 0
                temp_dict_colon.clear() # Kosongkan dict temporer

                for i, line in enumerate(f):
                    parts = line.strip().split(':', 1)
                    if len(parts) == 2:
                        slang = parts[0].lower().strip()
                        standard = parts[1].lower().strip()
                        if slang and standard:
                            temp_dict_colon[slang] = standard
                            current_load_count += 1
                        else:
                            # print(f"   PERINGATAN (Baris {i+1} TXT Colon, Enc: {enc}): Melewati baris karena slang atau standar kosong setelah strip: '{line.strip()}'")
                            current_skip_count += 1
                    elif line.strip():
                        # print(f"   PERINGATAN (Baris {i+1} TXT Colon, Enc: {enc}): Melewati baris karena format tidak 'slang:standar': '{line.strip()}'")
                        current_skip_count += 1

                # Jika berhasil membaca seluruh file tanpa error:
                loaded_txt_colon_count = current_load_count # Simpan hitungan yang berhasil
                skipped_lines_colon = current_skip_count
                file_processed = True # Tandai file sudah berhasil diproses
                print(f"   BERHASIL membaca dengan encoding '{enc}'.")

        except UnicodeDecodeError:
            print(f"   Gagal membaca dengan encoding '{enc}', mencoba selanjutnya...")
            continue # Coba encoding berikutnya
        except Exception as e:
            print(f"   ERROR tak terduga saat memproses '{file_txt_colon}' dengan encoding {enc}: {e}")
            break # Hentikan jika ada error selain encoding

    # Setelah mencoba semua encoding, update kamus jika file berhasil diproses
    if file_processed:
        count_before = len(merged_dict)
        merged_dict.update(temp_dict_colon) # Update dengan data dari TXT Colon
        count_after = len(merged_dict)
        added_count = count_after - count_before
        total_loaded_count += loaded_txt_colon_count
        skipped_lines += skipped_lines_colon # Tambahkan ke total skipped
        print(f"   Berhasil memuat {loaded_txt_colon_count} entri valid dari file ini.")
        print(f"   Menambahkan {added_count} entri unik baru ke kamus gabungan.")
    elif encoding_colon: # Jika file ada tapi semua encoding gagal
         print(f"   PERINGATAN: Tidak dapat memproses '{file_txt_colon}' dengan encoding yang dicoba: {encodings_to_try}. File dilewati.")


# --- Ringkasan dan Penyimpanan ---
print("\n--- Ringkasan Penggabungan ---")
print(f"Total entri yang berhasil dimuat dari semua file: {total_loaded_count}")
print(f"Total baris yang dilewati karena format salah/kosong: {skipped_lines}")
print(f"Jumlah entri unik dalam kamus gabungan akhir: {len(merged_dict)}")
print(f"Strategi duplikasi: Definisi dari file yang diproses terakhir akan menimpa definisi sebelumnya.")

# Menyimpan kamus gabungan ke file JSON
try:
    with open(output_json_file, 'w', encoding='utf-8') as f:
        # indent=2 membuat file JSON lebih mudah dibaca manusia
        # sort_keys=True mengurutkan kunci (slang) secara alfabetis
        # ensure_ascii=False penting untuk menyimpan karakter non-ASCII dengan benar
        json.dump(merged_dict, f, indent=2, sort_keys=True, ensure_ascii=False)
    print(f"\n✅ Kamus slang gabungan berhasil disimpan ke '{output_json_file}'")
except Exception as e:
    print(f"\n❌ ERROR saat menyimpan kamus gabungan ke JSON: {e}")

# Anda sekarang bisa menggunakan merged_dict di Python
# atau memuat 'merged_slang_dict.json' di lain waktu.
# Contoh akses: print(merged_dict.get("bgt"))
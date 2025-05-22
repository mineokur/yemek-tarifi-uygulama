import sqlite3
from PyQt6.QtWidgets import QMessageBox

class Veritabani:
    def __init__(self, db_adi="tarif_defteri.db"):
        self.db_adi = db_adi
        self.baglanti = None
        self.cursor = None
        self.baglan()
        self.tablo_olustur()

    def baglan(self):
        try:
            self.baglanti = sqlite3.connect(self.db_adi)
            self.cursor = self.baglanti.cursor()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Veritabanına bağlanırken bir hata oluştu: {e}")
            return False
        return True

    def baglantiyi_kes(self):
        if self.baglanti:
            self.baglanti.close()
            self.baglanti = None
            self.cursor = None

    def tablo_olustur(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarifler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                malzemeler TEXT NOT NULL,
                yapilis TEXT NOT NULL,
                tur TEXT NOT NULL,
                fotograf BLOB
            )
            """)
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                sifre TEXT NOT NULL
            )
            """)
            self.baglanti.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Tablo oluşturulurken bir hata oluştu: {e}")

    def tarif_ekle(self, ad, malzemeler, yapilis, tur, fotograf=None):
        try:
            self.cursor.execute("""
            INSERT INTO tarifler (ad, malzemeler, yapilis, tur, fotograf)
            VALUES (?, ?, ?, ?, ?)
            """, (ad, malzemeler, yapilis, tur, fotograf))
            self.baglanti.commit()
            return True
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Tarif eklenirken bir hata oluştu: {e}")
            return False

    def tum_tarifleri_getir(self):
        try:
            self.cursor.execute("SELECT id, ad FROM tarifler")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Tarifler getirilirken bir hata oluştu: {e}")
            return []

    def tur_gore_tarifleri_getir(self, tur):
        try:
            self.cursor.execute("SELECT id, ad FROM tarifler WHERE tur=?", (tur,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"{tur} tarifleri getirilirken bir hata oluştu: {e}")
            return []

    def tarif_getir(self, tarif_id):
        try:
            self.cursor.execute("SELECT ad, malzemeler, yapilis, fotograf FROM tarifler WHERE id=?", (tarif_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Tarif getirilirken bir hata oluştu: {e}")
            return None

    def kullanici_ekle(self, kullanici_adi, email, sifre):
        try:
            self.cursor.execute("""
            INSERT INTO kullanicilar (kullanici_adi, email, sifre)
            VALUES (?, ?, ?)
            """, (kullanici_adi, email, sifre))
            self.baglanti.commit()
            return True
        except sqlite3.IntegrityError:
            QMessageBox.warning(None, "Kayıt Hatası", "Bu kullanıcı adı veya e-posta adresi zaten kayıtlı.")
            return False
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Kullanıcı eklenirken bir hata oluştu: {e}")
            return False

    def kullanici_dogrula(self, email, sifre):
        try:
            self.cursor.execute("SELECT id, kullanici_adi FROM kullanicilar WHERE email=? AND sifre=?", (email, sifre))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Veritabanı Hatası", f"Kullanıcı doğrulanırken bir hata oluştu: {e}")
            return None
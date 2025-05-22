from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import os
from kullanici_islemleri import KullaniciOturumu

class TarifEkleSayfasi(QWidget):
    def __init__(self, parent, veritabani):
        super().__init__()
        self.parent = parent
        self.veritabani = veritabani
        self.setWindowTitle("Tarif Ekle")
        self.layout = QVBoxLayout()
        self.ust_kisim()
        self.form_alani()
        self.setLayout(self.layout)
        self.fotograf_yolu = None

    def ust_kisim(self):
        ust_layout = QHBoxLayout()
        dugmeler = [
            ("Anasayfa", self.parent.anasayfa_sayfasina_git),
            ("Tarif Ekle", lambda: self.parent.stacked_widget.setCurrentWidget(self)),  # Mevcut sayfa
            ("Yemekler", lambda: self.parent.tur_sayfasina_git("Yemek")),
            ("Tatlılar", lambda: self.parent.tur_sayfasina_git("Tatlı")),
            ("Çorbalar", lambda: self.parent.tur_sayfasina_git("Çorba")),
            ("İçecekler", lambda: self.parent.tur_sayfasina_git("İçecek")),
            ("Kayıt Ol", self.parent.kayit_ol_sayfasina_git),
            ("Giriş Yap", self.parent.giris_yap_sayfasina_git),
        ]
        for metin, hedef in dugmeler:
            dugme = QPushButton(metin)
            dugme.clicked.connect(hedef)
            ust_layout.addWidget(dugme)
        self.layout.addLayout(ust_layout)

    def form_alani(self):
        form_layout = QVBoxLayout()

        # Tarif Adı
        ad_etiketi = QLabel("Tarif Adı:")
        self.ad_alani = QLineEdit()
        form_layout.addWidget(ad_etiketi)
        form_layout.addWidget(self.ad_alani)

        # Malzemeler
        malzemeler_etiketi = QLabel("Malzemeler:")
        self.malzemeler_alani = QTextEdit()
        form_layout.addWidget(malzemeler_etiketi)
        form_layout.addWidget(self.malzemeler_alani)

        # Yapılış
        yapilis_etiketi = QLabel("Yapılış:")
        self.yapilis_alani = QTextEdit()
        form_layout.addWidget(yapilis_etiketi)
        form_layout.addWidget(self.yapilis_alani)

        # Tarif Türü
        tur_etiketi = QLabel("Tarif Türü:")
        self.tur_secimi = QComboBox()
        self.tur_secimi.addItems(["Yemek", "Tatlı", "Çorba", "İçecek"])
        form_layout.addWidget(tur_etiketi)
        form_layout.addWidget(self.tur_secimi)

        # Fotoğraf Ekleme
        fotograf_layout = QHBoxLayout()
        fotograf_etiketi = QLabel("Fotoğraf:")
        self.fotograf_onizleme = QLabel()
        self.fotograf_onizleme.setFixedSize(150, 200)
        self.fotograf_onizleme.setStyleSheet("border: 1px solid black;")
        fotograf_layout.addWidget(fotograf_etiketi)
        fotograf_layout.addWidget(self.fotograf_onizleme)

        fotograf_sec_dugmesi = QPushButton("Fotoğraf Seç")
        fotograf_sec_dugmesi.clicked.connect(self.fotograf_sec)
        fotograf_layout.addWidget(fotograf_sec_dugmesi)

        form_layout.addLayout(fotograf_layout)

        # Kaydet Düğmesi
        kaydet_dugmesi = QPushButton("Tarifi Kaydet")
        kaydet_dugmesi.clicked.connect(self.tarifi_kaydet)
        form_layout.addWidget(kaydet_dugmesi)

        self.layout.addLayout(form_layout)

    def fotograf_sec(self):
        dosya_adi, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
        if dosya_adi:
            self.fotograf_yolu = dosya_adi
            pixmap = QPixmap(dosya_adi).scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.fotograf_onizleme.setPixmap(pixmap)

    def tarifi_kaydet(self):
        if not KullaniciOturumu.oturum_acik_mi():
            QMessageBox.warning(self, "Uyarı", "Tarif kaydetmek için giriş yapmanız gerekmektedir.")
            self.parent.stacked_widget.setCurrentWidget(self.parent.giris_yap_sayfasi)
            self.parent.setWindowTitle("Tarif Defteri - Giriş Yap")
            return

        ad = self.ad_alani.text()
        malzemeler = self.malzemeler_alani.toPlainText()
        yapilis = self.yapilis_alani.toPlainText()
        tur = self.tur_secimi.currentText()
        fotograf_data = None
        if self.fotograf_yolu:
            with open(self.fotograf_yolu, "rb") as file:
                fotograf_data = file.read()

        if ad and malzemeler and yapilis and tur:
            if self.veritabani.tarif_ekle(ad, malzemeler, yapilis, tur, fotograf_data):
                QMessageBox.information(self, "Başarılı", "Tarif başarıyla kaydedildi.")
                # Kayıttan sonra ana sayfayı güncelle
                self.parent.anasayfa_sayfasi.alt_kisim()
                self.parent.stacked_widget.setCurrentWidget(self.parent.anasayfa_sayfasi)
                self.parent.setWindowTitle("Tarif Defteri - Ana Sayfa")
                self.temizle()
            else:
                QMessageBox.critical(self, "Hata", "Tarif kaydedilirken bir hata oluştu.")
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")

    def temizle(self):
        self.ad_alani.clear()
        self.malzemeler_alani.clear()
        self.yapilis_alani.clear()
        self.tur_secimi.setCurrentIndex(0)
        self.fotograf_yolu = None
        self.fotograf_onizleme.clear()
        self.fotograf_onizleme.setStyleSheet("border: 1px solid black;")

    # Sayfa geçiş metotları kaldırıldı.
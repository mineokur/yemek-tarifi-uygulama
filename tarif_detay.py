from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import io
from kullanici_islemleri import KullaniciOturumu

class TarifDetaySayfasi(QWidget):
    def __init__(self, parent, veritabani):
        super().__init__()
        self.parent = parent
        self.veritabani = veritabani
        self.setWindowTitle("Tarif Detayı")
        self.layout = QVBoxLayout()
        self.ust_kisim()
        self.detay_alani = QScrollArea()
        self.detay_icerik = QWidget()
        self.detay_layout = QVBoxLayout(self.detay_icerik)
        self.detay_alani.setWidgetResizable(True)
        self.detay_alani.setWidget(self.detay_icerik)
        self.layout.addWidget(self.detay_alani)
        self.setLayout(self.layout)

        self.mevcut_tarif = None

    def ust_kisim(self):
        ust_layout = QHBoxLayout()
        dugmeler = [
            ("Anasayfa", self.parent.anasayfa_sayfasina_git),
            ("Tarif Ekle", self.parent.tarif_ekle_sayfasina_git),
            ("Yemekler", lambda: self.parent.tur_sayfasina_git("Yemek")),
            ("Tatlılar", lambda: self.parent.tur_sayfasina_git("Tatlı")),
            ("Çorbalar", lambda: self.parent.tur_sayfasina_git("Çorba")),
            ("İçecekler", lambda: self.parent.tur_sayfasina_git("İçecek")),
            ("Kayıt Ol", self.parent.kayit_ol_sayfasina_git),
            ("Giriş Yap", self.parent.giris_yap_sayfasina_git),
        ]
        for metin, fonksiyon in dugmeler:
            dugme = QPushButton(metin)
            dugme.clicked.connect(fonksiyon)
            ust_layout.addWidget(dugme)
        self.layout.addLayout(ust_layout)

    def tarif_goster(self, tarif_bilgisi):
        self.mevcut_tarif = tarif_bilgisi

        # Önceki içerikleri temizle
        for i in reversed(range(self.detay_layout.count())):
            widget = self.detay_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        ad, malzemeler, yapilis, fotograf = tarif_bilgisi

        # Tarif Adı
        ad_etiketi = QLabel(f"<h2>{ad}</h2>")
        self.detay_layout.addWidget(ad_etiketi)

        # Fotoğraf
        if fotograf:
            image = QImage.fromData(fotograf)
            pixmap = QPixmap(image).scaled(300, 400, Qt.AspectRatioMode.KeepAspectRatio)
            fotograf_etiketi = QLabel()
            fotograf_etiketi.setPixmap(pixmap)
            self.detay_layout.addWidget(fotograf_etiketi)
        else:
            bos_fotograf_etiketi = QLabel("Fotoğraf Yok")
            self.detay_layout.addWidget(bos_fotograf_etiketi)

        # Malzemeler
        malzemeler_baslik = QLabel("<h3>Malzemeler</h3>")
        self.detay_layout.addWidget(malzemeler_baslik)
        malzemeler_etiketi = QLabel(malzemeler.replace('\n', '<br>'))
        malzemeler_etiketi.setWordWrap(True)
        malzemeler_etiketi.setTextFormat(Qt.TextFormat.RichText)
        self.detay_layout.addWidget(malzemeler_etiketi)

        # Yapılış
        yapilis_baslik = QLabel("<h3>Yapılış</h3>")
        self.detay_layout.addWidget(yapilis_baslik)
        yapilis_etiketi = QLabel(yapilis.replace('\n', '<br>'))
        yapilis_etiketi.setWordWrap(True)
        yapilis_etiketi.setTextFormat(Qt.TextFormat.RichText)
        self.detay_layout.addWidget(yapilis_etiketi)

        # Esneme payı ekle, böylece içerik yukarıda hizalanır
        self.detay_layout.addStretch(1)

    # Sayfa geçiş metotları kaldırıldı.
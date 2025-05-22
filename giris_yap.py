from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from kullanici_islemleri import KullaniciOturumu

class GirisYapSayfasi(QWidget):
    def __init__(self, parent, veritabani):
        super().__init__()
        self.parent = parent
        self.veritabani = veritabani
        self.setWindowTitle("Giriş Yap")
        self.layout = QVBoxLayout()
        self.ust_kisim()
        self.form_alani()
        self.setLayout(self.layout)

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
            ("Giriş Yap", lambda: self.parent.stacked_widget.setCurrentWidget(self)),  # Mevcut sayfa
        ]
        for metin, hedef in dugmeler:
            dugme = QPushButton(metin)
            dugme.clicked.connect(hedef)
            ust_layout.addWidget(dugme)
        self.layout.addLayout(ust_layout)

    def form_alani(self):
        form_layout = QVBoxLayout()

        # E-posta
        email_etiketi = QLabel("E-posta:")
        self.email_alani = QLineEdit()
        form_layout.addWidget(email_etiketi)
        form_layout.addWidget(self.email_alani)

        # Şifre
        sifre_etiketi = QLabel("Şifre:")
        self.sifre_alani = QLineEdit()
        self.sifre_alani.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(sifre_etiketi)
        form_layout.addWidget(self.sifre_alani)

        # Düğmeler
        dugme_layout = QHBoxLayout()
        giris_yap_dugmesi = QPushButton("Giriş Yap")
        giris_yap_dugmesi.clicked.connect(self.giris_yap)
        temizle_dugmesi = QPushButton("Temizle")
        temizle_dugmesi.clicked.connect(self.temizle)
        dugme_layout.addWidget(giris_yap_dugmesi)
        dugme_layout.addWidget(temizle_dugmesi)
        form_layout.addLayout(dugme_layout)

        self.layout.addLayout(form_layout)

    def giris_yap(self):
        email = self.email_alani.text()
        sifre = self.sifre_alani.text()

        if not email or not sifre:
            QMessageBox.warning(self, "Uyarı", "Lütfen e-posta ve şifrenizi girin.")
            return

        kullanici = self.veritabani.kullanici_dogrula(email, sifre)
        if kullanici:
            KullaniciOturumu.oturum_baslat(kullanici[0], kullanici[1])
            QMessageBox.information(self, "Başarılı", f"Hoş geldiniz, {KullaniciOturumu.mevcut_kullanici()}!")
            self.temizle()
            self.parent.anasayfa_sayfasi.alt_kisim() # Ana sayfayı güncelle
            self.parent.stacked_widget.setCurrentWidget(self.parent.anasayfa_sayfasi)
            self.parent.setWindowTitle("Tarif Defteri - Ana Sayfa")
        else:
            QMessageBox.warning(self, "Hata", "Yanlış e-posta veya şifre.")

    def temizle(self):
        self.email_alani.clear()
        self.sifre_alani.clear()

    # Sayfa geçiş metotları kaldırıldı.
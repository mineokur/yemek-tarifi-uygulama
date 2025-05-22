from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
from kullanici_islemleri import KullaniciOturumu

class KayitOlSayfasi(QWidget):
    def __init__(self, parent, veritabani):
        super().__init__()
        self.parent = parent
        self.veritabani = veritabani
        self.setWindowTitle("Kayıt Ol")
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
            ("Kayıt Ol", lambda: self.parent.stacked_widget.setCurrentWidget(self)),  # Mevcut sayfa
            ("Giriş Yap", self.parent.giris_yap_sayfasina_git),
        ]
        for metin, hedef in dugmeler:
            dugme = QPushButton(metin)
            dugme.clicked.connect(hedef)
            ust_layout.addWidget(dugme)
        self.layout.addLayout(ust_layout)

    def form_alani(self):
        form_layout = QVBoxLayout()

        # Kullanıcı Adı
        kullanici_adi_etiketi = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_alani = QLineEdit()
        form_layout.addWidget(kullanici_adi_etiketi)
        form_layout.addWidget(self.kullanici_adi_alani)

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
        kaydet_dugmesi = QPushButton("Kaydet")
        kaydet_dugmesi.clicked.connect(self.kaydet)
        temizle_dugmesi = QPushButton("Temizle")
        temizle_dugmesi.clicked.connect(self.temizle)
        dugme_layout.addWidget(kaydet_dugmesi)
        dugme_layout.addWidget(temizle_dugmesi)
        form_layout.addLayout(dugme_layout)

        self.layout.addLayout(form_layout)

    def kaydet(self):
        kullanici_adi = self.kullanici_adi_alani.text()
        email = self.email_alani.text()
        sifre = self.sifre_alani.text()

        if not kullanici_adi or not email or not sifre:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")
            return

        if self.veritabani.kullanici_ekle(kullanici_adi, email, sifre):
            QMessageBox.information(self, "Başarılı", "Kayıt başarıyla oluşturuldu. Giriş yapabilirsiniz.")
            self.temizle()
            self.parent.stacked_widget.setCurrentWidget(self.parent.giris_yap_sayfasi)
            self.parent.setWindowTitle("Tarif Defteri - Giriş Yap")
        else:
            # Hata mesajı zaten veritabanı sınıfında gösteriliyor.
            pass

    def temizle(self):
        self.kullanici_adi_alani.clear()
        self.email_alani.clear()
        self.sifre_alani.clear()

    # Sayfa geçiş metotları kaldırıldı.
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt
from kullanici_islemleri import KullaniciOturumu

class TatlilarSayfasi(QWidget):
    def __init__(self, parent, veritabani):
        super().__init__()
        self.parent = parent
        self.veritabani = veritabani
        self.setWindowTitle("Tarif Defteri - Tatlılar")
        self.layout = QVBoxLayout()
        self.ust_kisim()
        self.tarifler_alani = QWidget()
        self.tarifler_layout = QGridLayout(self.tarifler_alani)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.tarifler_alani)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        self.tarifleri_yukle()

    def ust_kisim(self):
        ust_layout = QHBoxLayout()
        dugmeler = [
            ("Anasayfa", self.parent.anasayfa_sayfasina_git),
            ("Tarif Ekle", self.parent.tarif_ekle_sayfasina_git),
            ("Yemekler", lambda: self.parent.tur_sayfasina_git("Yemek")),
            ("Tatlılar", lambda: self.parent.stacked_widget.setCurrentWidget(self)),  # Mevcut sayfa
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

    def tarifleri_yukle(self):
        # Önceki tarif etiketlerini temizle
        for i in reversed(range(self.tarifler_layout.count())):
            widget = self.tarifler_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        tatli_tarifleri = self.veritabani.tur_gore_tarifleri_getir("Tatlı")
        if not tatli_tarifleri:
            bos_etiket = QLabel("Henüz hiç tatlı tarifi eklenmedi.")
            bos_etiket.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tarifler_layout.addWidget(bos_etiket, 0, 0, 1, 3) # Tüm alanı kapla
            return

        satir = 0
        sutun = 0
        for tarif_id, tarif_adi in tatli_tarifleri:
            tarif_etiketi = QPushButton(tarif_adi)
            tarif_etiketi.setFixedSize(200, 100)
            tarif_etiketi.clicked.connect(lambda checked, id=tarif_id: self.parent.tarif_detay_sayfasina_git(id))
            self.tarifler_layout.addWidget(tarif_etiketi, satir, sutun)
            sutun += 1
            if sutun == 3:
                sutun = 0
                satir += 1

    # Sayfa geçiş metotları kaldırıldı.
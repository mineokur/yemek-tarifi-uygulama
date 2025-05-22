from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QScrollArea, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from kullanici_islemleri import KullaniciOturumu # Mutlak import

class AnaSayfa(QWidget):
    def __init__(self, parent, veritabani):
        super().__init__()
        self.parent = parent
        self.veritabani = veritabani
        self.setWindowTitle("Tarif Defteri - Ana Sayfa")
        self.layout = QVBoxLayout()
        self.ust_kisim()
        self.alt_kisim()
        self.setLayout(self.layout)

    def ust_kisim(self):
        ust_layout = QHBoxLayout()
        dugmeler = [
            ("Anasayfa", lambda: self.parent.stacked_widget.setCurrentWidget(self.parent.anasayfa_sayfasi)),
            ("Tarif Ekle", lambda: self.parent.tarif_ekle_sayfasina_git()),
            ("Yemekler", lambda: self.parent.tur_sayfasina_git("Yemek")),
            ("Tatlılar", lambda: self.parent.tur_sayfasina_git("Tatlı")),
            ("Çorbalar", lambda: self.parent.tur_sayfasina_git("Çorba")),
            ("İçecekler", lambda: self.parent.tur_sayfasina_git("İçecek")),
            ("Kayıt Ol", lambda: self.parent.kayit_ol_sayfasina_git()),
            ("Giriş Yap", lambda: self.parent.giris_yap_sayfasina_git()),
        ]
        for metin, fonksiyon in dugmeler:
            dugme = QPushButton(metin)
            dugme.clicked.connect(fonksiyon)
            ust_layout.addWidget(dugme)
        self.layout.addLayout(ust_layout)

    def alt_kisim(self):
        tarifler = self.veritabani.tum_tarifleri_getir()
        if not tarifler:
            bos_etiket = QLabel("Henüz hiç tarif eklenmedi.")
            bos_etiket.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(bos_etiket)
            return

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)

        satir = 0
        sutun = 0
        for tarif_id, tarif_adi in tarifler:
            tarif_etiketi = QPushButton(tarif_adi)
            tarif_etiketi.setFixedSize(200, 100)  # Dikdörtgen boyutları
            tarif_etiketi.clicked.connect(lambda checked, id=tarif_id: self.parent.tarif_detay_sayfasina_git(id))
            grid_layout.addWidget(tarif_etiketi, satir, sutun)
            sutun += 1
            if sutun == 3:
                sutun = 0
                satir += 1

        scroll_widget.setLayout(grid_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

    # Sayfa geçiş metotları kaldırıldı, MainWindow üzerinden erişiliyor.
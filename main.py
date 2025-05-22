import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from anasayfa import AnaSayfa
from tarif_ekle import TarifEkleSayfasi
from yemekler import YemeklerSayfasi
from tatlilar import TatlilarSayfasi
from corbalar import CorbalarSayfasi
from icecekler import IceceklerSayfasi
from kayit_ol import KayitOlSayfasi
from giris_yap import GirisYapSayfasi
from tarif_detay import TarifDetaySayfasi
from veritabani import Veritabani
from kullanici_islemleri import KullaniciOturumu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarif Defteri")
        self.setGeometry(100, 100, 800, 600)  # Pencere boyutları

        self.veritabani = Veritabani()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.anasayfa_sayfasi = AnaSayfa(self, self.veritabani)
        self.tarif_ekle_sayfasi = TarifEkleSayfasi(self, self.veritabani)
        self.yemekler_sayfasi = YemeklerSayfasi(self, self.veritabani)
        self.tatlilar_sayfasi = TatlilarSayfasi(self, self.veritabani)
        self.corbalar_sayfasi = CorbalarSayfasi(self, self.veritabani)
        self.icecekler_sayfasi = IceceklerSayfasi(self, self.veritabani)
        self.kayit_ol_sayfasi = KayitOlSayfasi(self, self.veritabani)
        self.giris_yap_sayfasi = GirisYapSayfasi(self, self.veritabani)
        self.tarif_detay_sayfasi = TarifDetaySayfasi(self, self.veritabani)

        self.stacked_widget.addWidget(self.anasayfa_sayfasi)
        self.stacked_widget.addWidget(self.tarif_ekle_sayfasi)
        self.stacked_widget.addWidget(self.yemekler_sayfasi)
        self.stacked_widget.addWidget(self.tatlilar_sayfasi)
        self.stacked_widget.addWidget(self.corbalar_sayfasi)
        self.stacked_widget.addWidget(self.icecekler_sayfasi)
        self.stacked_widget.addWidget(self.kayit_ol_sayfasi)
        self.stacked_widget.addWidget(self.giris_yap_sayfasi)
        self.stacked_widget.addWidget(self.tarif_detay_sayfasi)

        self.stacked_widget.setCurrentWidget(self.anasayfa_sayfasi)

    def anasayfa_sayfasina_git(self):
        self.stacked_widget.setCurrentWidget(self.anasayfa_sayfasi)
        self.setWindowTitle("Tarif Defteri - Ana Sayfa")

    def tarif_ekle_sayfasina_git(self):
        if KullaniciOturumu.oturum_acik_mi():
            self.stacked_widget.setCurrentWidget(self.tarif_ekle_sayfasi)
            self.setWindowTitle("Tarif Defteri - Tarif Ekle")
        else:
            QMessageBox.warning(self, "Uyarı", "Tarif eklemek için giriş yapmanız gerekmektedir.")
            self.stacked_widget.setCurrentWidget(self.giris_yap_sayfasi)
            self.setWindowTitle("Tarif Defteri - Giriş Yap")

    def tur_sayfasina_git(self, tur):
        if tur == "Yemek":
            self.yemekler_sayfasi.tarifleri_yukle()
            self.stacked_widget.setCurrentWidget(self.yemekler_sayfasi)
            self.setWindowTitle("Tarif Defteri - Yemekler")
        elif tur == "Tatlı":
            self.tatlilar_sayfasi.tarifleri_yukle()
            self.stacked_widget.setCurrentWidget(self.tatlilar_sayfasi)
            self.setWindowTitle("Tarif Defteri - Tatlılar")
        elif tur == "Çorba":
            self.corbalar_sayfasi.tarifleri_yukle()
            self.stacked_widget.setCurrentWidget(self.corbalar_sayfasi)
            self.setWindowTitle("Tarif Defteri - Çorbalar")
        elif tur == "İçecek":
            self.icecekler_sayfasi.tarifleri_yukle()
            self.stacked_widget.setCurrentWidget(self.icecekler_sayfasi)
            self.setWindowTitle("Tarif Defteri - İçecekler")

    def kayit_ol_sayfasina_git(self):
        self.stacked_widget.setCurrentWidget(self.kayit_ol_sayfasi)
        self.setWindowTitle("Tarif Defteri - Kayıt Ol")

    def giris_yap_sayfasina_git(self):
        self.stacked_widget.setCurrentWidget(self.giris_yap_sayfasi)
        self.setWindowTitle("Tarif Defteri - Giriş Yap")

    def tarif_detay_sayfasina_git(self, tarif_id):
        tarif_bilgisi = self.veritabani.tarif_getir(tarif_id)
        if tarif_bilgisi:
            self.tarif_detay_sayfasi.tarif_goster(tarif_bilgisi)
            self.stacked_widget.setCurrentWidget(self.tarif_detay_sayfasi)
            self.setWindowTitle(f"Tarif Defteri - {tarif_bilgisi[0]}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
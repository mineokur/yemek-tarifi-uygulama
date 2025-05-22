class KullaniciOturumu:
    kullanici_id = None
    kullanici_adi = None

    @classmethod
    def oturum_baslat(cls, kullanici_id, kullanici_adi):
        cls.kullanici_id = kullanici_id
        cls.kullanici_adi = kullanici_adi

    @classmethod
    def oturum_sonlandir(cls):
        cls.kullanici_id = None
        cls.kullanici_adi = None

    @classmethod
    def oturum_acik_mi(cls):
        return cls.kullanici_id is not None

    @classmethod
    def mevcut_kullanici(cls):
        return cls.kullanici_adi
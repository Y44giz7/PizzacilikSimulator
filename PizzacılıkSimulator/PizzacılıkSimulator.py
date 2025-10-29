import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class PizzaSimulator:
    def __init__(self):
        # Ana pencere ayarları
        self.root = tk.Tk()
        self.root.title("Pizzacılık Simulator")
        self.root.geometry("700x500")
        
        # Oyun verileri
        self.bakiye = 0
        self.hizli_eller = False
        self.super_firin = False
        self.current_musteri = None
        self.current_pizza = None
        self.tum_musteriler = {
            "Ahmet": "Karışık Pizza",
            "Mehmet": "Margarita", 
            "Ayşe": "Sucuklu Pizza",
            "Fatma": "Mantarlı Pizza",
            "Ali": "Vejeteryan Pizza",
            "Zeynep": "Akdeniz Pizza",
            "Can": "BBQ Pizza",
            "Elif": "Mantarlı Pizza"
        }
        
        # Veri dosyası yolu
        self.KAYIT_DOSYASI = "pizza_kayit.json"
        
        # Kayıtlı verileri yükle
        self.kayit_yukle()
        
        # Frame'leri oluştur
        self.giris_frame = tk.Frame(self.root)
        self.siparis_frame = tk.Frame(self.root)
        self.yukseltme_frame = tk.Frame(self.root)
        
        # Ekranları hazırla
        self.setup_giris_ekrani()
        self.setup_siparis_ekrani()
        self.setup_yukseltme_ekrani()
        
        # Giriş ekranını göster
        self.show_giris_ekrani()

    def setup_siparis_ekrani(self):
        # Üst kısım - Bakiye ve Geri butonu
        ust_frame = tk.Frame(self.siparis_frame)
        ust_frame.pack(fill="x", pady=10)
        
        self.geri_btn = tk.Button(ust_frame, text="← Geri", command=self.show_giris_ekrani)
        self.geri_btn.pack(side="left", padx=10)
        
        self.bakiye_label = tk.Label(ust_frame, text=f"Bakiye: {self.bakiye:,} ₺", font=("Bold", 16))
        self.bakiye_label.pack(side="right", padx=10)
        
        # Sipariş bilgileri
        self.musteri_label = tk.Label(self.siparis_frame, text="", font=("Arial", 14))
        self.musteri_label.pack(pady=20)
        
        self.pizza_label = tk.Label(self.siparis_frame, text="", font=("Arial", 14))
        self.pizza_label.pack(pady=10)
        
        self.progress_label = tk.Label(self.siparis_frame, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)
        
        self.timer_label = tk.Label(self.siparis_frame, text="", font=("Arial", 12))
        self.timer_label.pack(pady=5)
        
        self.hazirla_btn = tk.Button(
            self.siparis_frame,
            text="Siparişi Hazırla",
            command=self.baslat_siparis,
            bg="green",
            fg="white",
            font=("Arial", 12),
            state="disabled"
        )
        self.hazirla_btn.pack(pady=20)

    def setup_yukseltme_ekrani(self):
        # Üst kısım - Bakiye ve Geri butonu
        ust_frame = tk.Frame(self.yukseltme_frame)
        ust_frame.pack(fill="x", pady=10)
        
        self.geri_btn_yukseltme = tk.Button(ust_frame, text="← Geri", command=self.show_giris_ekrani)
        self.geri_btn_yukseltme.pack(side="left", padx=10)
        
        self.bakiye_label_yukseltme = tk.Label(ust_frame, text=f"Bakiye: {self.bakiye:,} ₺", font=("Bold", 16))
        self.bakiye_label_yukseltme.pack(side="right", padx=10)

        # Yükseltmeler başlığı
        tk.Label(self.yukseltme_frame, text="Yükseltmeler", font=("Bold", 24)).pack(pady=20)

        # Hızlı Eller yükseltmesi
        hizli_frame = tk.Frame(self.yukseltme_frame)
        hizli_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(hizli_frame, text="Hızlı Eller", font=("Bold", 16)).pack(anchor="w")
        tk.Label(hizli_frame, text="Hamur hazırlama ve malzeme ekleme süresi 5 saniyeye düşer").pack(anchor="w")
        self.hizli_btn = tk.Button(hizli_frame, text="Satın Al - 50000 TL", command=self.hizli_eller_al)
        self.hizli_btn.pack(anchor="w", pady=5)

        # 500 Derece Fırın yükseltmesi
        firin_frame = tk.Frame(self.yukseltme_frame)
        firin_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(firin_frame, text="500 Derece Fırın", font=("Bold", 16)).pack(anchor="w")
        tk.Label(firin_frame, text="Pişirme süresi yarıya iner").pack(anchor="w")
        self.firin_btn = tk.Button(firin_frame, text="Satın Al - 75000 TL", command=self.super_firin_al)
        self.firin_btn.pack(anchor="w", pady=5)

        self.guncelle_yukseltme_butonlari()

    def show_giris_ekrani(self):
        self.siparis_frame.pack_forget()
        self.yukseltme_frame.pack_forget()
        self.giris_frame.pack(expand=True, fill="both")
    
    def show_siparis_ekrani(self):
        self.giris_frame.pack_forget()
        self.yukseltme_frame.pack_forget()
        self.siparis_frame.pack(expand=True, fill="both")
        self.yeni_musteri()
    
    def show_yukseltme_ekrani(self):
        self.giris_frame.pack_forget()
        self.siparis_frame.pack_forget()
        self.yukseltme_frame.pack(expand=True, fill="both")
        self.guncelle_yukseltme_butonlari()

    def yeni_musteri(self):
        if len(self.tum_musteriler) > 0:
            self.current_musteri = random.choice(list(self.tum_musteriler.keys()))
            self.current_pizza = self.tum_musteriler[self.current_musteri]
            
            self.musteri_label.config(text=f"Müşteri: {self.current_musteri}")
            self.pizza_label.config(text=f"Sipariş: {self.current_pizza}")
            self.progress_label.config(text="")
            self.timer_label.config(text="")
            self.hazirla_btn.config(state="normal")
            self.geri_btn.config(state="normal")
        else:
            self.musteri_label.config(text="Günün son müşterisi!")
            self.pizza_label.config(text="")
            self.hazirla_btn.config(state="disabled")

    def baslat_siparis(self):
        sure = 5 if self.hizli_eller else 20
        self.baslat_asama("Hamur Hazırlanıyor...", sure)

    def baslat_asama(self, asama, sure):
        self.hazirla_btn.config(state="disabled")
        self.geri_btn.config(state="disabled")
        self.guncelle_zamanlayici(sure, asama)

    def guncelle_zamanlayici(self, kalan_sure, asama):
        if kalan_sure > 0:
            self.timer_label.config(text=f"Kalan süre: {kalan_sure} saniye")
            self.progress_label.config(text=f"Aşama: {asama}")
            self.root.after(1000, lambda: self.guncelle_zamanlayici(kalan_sure-1, asama))
        else:
            if asama == "Hamur Hazırlanıyor...":
                self.progress_label.config(text="Hamur Hazır!")
                sure = 5 if self.hizli_eller else 20
                self.root.after(1000, lambda: self.baslat_asama("Malzemeler Ekleniyor...", sure))
            elif asama == "Malzemeler Ekleniyor...":
                self.progress_label.config(text="Malzemeler Hazır!")
                sure = 10 if self.super_firin else 20
                self.root.after(1000, lambda: self.baslat_asama("Pişiriliyor...", sure))
            elif asama == "Pişiriliyor...":
                self.siparisi_tamamla()

    def siparisi_tamamla(self):
        self.bakiye += 200
        self.bakiye_label.config(text=f"Bakiye: {self.bakiye:,} ₺")
        
        del self.tum_musteriler[self.current_musteri]
        
        self.progress_label.config(text="Pizza Hazır!")
        self.timer_label.config(text="")
        self.geri_btn.config(state="normal")
        
        messagebox.showinfo("Başarılı!", 
                          f"{self.current_musteri} için {self.current_pizza} hazırlandı!\n+200 TL kazandınız!")
        
        self.kayit_kaydet()
        self.root.after(2000, self.yeni_musteri)

    def hizli_eller_al(self):
        if self.bakiye >= 50000:
            self.bakiye -= 50000
            self.hizli_eller = True
            self.guncelle_bakiye_gostergeleri()
            messagebox.showinfo("Başarılı", "Hızlı Eller yükseltmesi satın alındı!")

    def super_firin_al(self):
        if self.bakiye >= 75000:
            self.bakiye -= 75000
            self.super_firin = True
            self.guncelle_bakiye_gostergeleri()
            messagebox.showinfo("Başarılı", "500 Derece Fırın yükseltmesi satın alındı!")

    def guncelle_yukseltme_butonlari(self):
        if self.hizli_eller:
            self.hizli_btn.config(text="Satın Alındı", state="disabled", bg="gray")
        elif self.bakiye < 50000:
            self.hizli_btn.config(state="disabled")
        else:
            self.hizli_btn.config(state="normal")

        if self.super_firin:
            self.firin_btn.config(text="Satın Alındı", state="disabled", bg="gray")
        elif self.bakiye < 75000:
            self.firin_btn.config(state="disabled")
        else:
            self.firin_btn.config(state="normal")

# ...existing code...

    def kayit_yukle(self):
        """Kayıtlı oyun verilerini yükle"""
        try:
            if os.path.exists(self.KAYIT_DOSYASI):
                with open(self.KAYIT_DOSYASI, 'r', encoding='utf-8') as f:
                    veriler = json.load(f)
                    self.bakiye = veriler.get("bakiye", 0)
                    self.hizli_eller = veriler.get("hizli_eller", False)
                    self.super_firin = veriler.get("super_firin", False)
        except Exception as e:
            print(f"Kayıt yükleme hatası: {e}")

    def kayit_kaydet(self):
        """Oyun verilerini kaydet"""
        try:
            veriler = {
                "bakiye": self.bakiye,
                "hizli_eller": self.hizli_eller,
                "super_firin": self.super_firin
            }
            with open(self.KAYIT_DOSYASI, 'w', encoding='utf-8') as f:
                json.dump(veriler, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Kayıt kaydetme hatası: {e}")

    def setup_giris_ekrani(self):
        # Başlık
        baslik = tk.Label(self.giris_frame, 
                         text="Pizzacılık Simulator'a\nHoşgeldiniz!", 
                         font=("Arial", 24, "bold"))
        baslik.pack(pady=20)
        
        # Açıklama
        aciklama = tk.Label(self.giris_frame,
                           text="Kendi pizza dükkanınızı işletin ve para kazanın!",
                           font=("Arial", 12))
        aciklama.pack(pady=10)
        
        # Butonlar
        tk.Button(self.giris_frame, 
                 text="Oyuna Başla",
                 font=("Arial", 14),
                 bg="#4CAF50",
                 fg="white",
                 width=20,
                 command=self.show_siparis_ekrani).pack(pady=10)
        
        tk.Button(self.giris_frame,
                 text="Yükseltmeler",
                 font=("Arial", 14),
                 bg="#2196F3",
                 fg="white", 
                 width=20,
                 command=self.show_yukseltme_ekrani).pack(pady=10)

    def guncelle_bakiye_gostergeleri(self):
        """Tüm bakiye göstergelerini güncelle"""
        self.bakiye_label.config(text=f"Bakiye: {self.bakiye:,} ₺")
        self.bakiye_label_yukseltme.config(text=f"Bakiye: {self.bakiye:,} ₺")
        self.kayit_kaydet()

# Ana çalıştırma kodu
if __name__ == "__main__":
    oyun = PizzaSimulator()
    oyun.root.mainloop()

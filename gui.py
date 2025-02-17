import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tarama_motoru import hedef_belirle, cihaz_tara, port_tara
from sonuc_islemleri import sonuclari_goruntule, sonuclari_kaydet

def pencere_olustur():
  """
  Ana pencereyi ve GUI elemanlarını oluşturur.
  """
  global pencere, hedef_girdisi, port_araligi_girdisi
  
  pencere = tk.Tk()
  pencere.title("Ağ Tarayıcısı")

  # Hedef IP aralığı veya alt ağ maskesi için etiket ve girdi alanı
  tk.Label(pencere, text="Hedef:").grid(row=0, column=0, padx=5, pady=5)
  hedef_girdisi = tk.Entry(pencere)
  hedef_girdisi.grid(row=0, column=1, padx=5, pady=5)

  # Port aralığı için etiket ve girdi alanı
  tk.Label(pencere, text="Port Aralığı:").grid(row=1, column=0, padx=5, pady=5)
  port_araligi_girdisi = tk.Entry(pencere)
  port_araligi_girdisi.grid(row=1, column=1, padx=5, pady=5)
  port_araligi_girdisi.insert(0, "1-1024")  # Varsayılan port aralığı

  # Tarama başlatma butonu
  tarama_butonu = tk.Button(pencere, text="Tara", command=tarama_baslat)
  tarama_butonu.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

  # Sonuçları görüntülemek için bir ağaç yapısı
  global sonuclar_agaci
  sonuclar_agaci = ttk.Treeview(pencere, columns=("IP Adresi", "MAC Adresi", "Açık Portlar", "İşletim Sistemi"))
  sonuclar_agaci.heading("IP Adresi", text="IP Adresi")
  sonuclar_agaci.heading("MAC Adresi", text="MAC Adresi")
  sonuclar_agaci.heading("Açık Portlar", text="Açık Portlar")
  sonuclar_agaci.heading("İşletim Sistemi", text="İşletim Sistemi")
  sonuclar_agaci.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

  pencere.mainloop()

def tarama_baslat():
    """
    Tarama işlemini başlatır.
    """
    hedef = hedef_girdisi.get()
    port_araligi = port_araligi_girdisi.get()  # port_araligi değişkenini al

    # Hedef belirleme
    tarama_bilgileri = hedef_belirle(hedef)
    if isinstance(tarama_bilgileri, str):
        # Hata mesajını göster
        tk.messagebox.showerror("Hata", tarama_bilgileri)
        return

    # Cihaz tarama
    if tarama_bilgileri == "aralik":
        ip_adresleri = [str(ipaddress.ip_address(ip)) for ip in range(int(ipaddress.ip_address(tarama_bilgileri)), int(ipaddress.ip_address(tarama_bilgileri)) + 1)]
    else:
        ip_adresleri = [str(ip) for ip in tarama_bilgileri]
    aktif_cihazlar = cihaz_tara(ip_adresleri)

    # Port tarama
    tarama_sonuclari = list()
    for ip_adresi in aktif_cihazlar:
        try:
            baslangic_port, bitis_port = map(int, port_araligi.split("-"))
            acik_portlar = port_tara(ip_adresi, range(baslangic_port, bitis_port + 1))
            tarama_sonuclari.append({
                "ip_adresi": ip_adresi,
                "acik_portlar": list(acik_portlar)  # list(acik_portlar) olarak ayarla
            })
        except TypeError:  # TypeError hatası yakala
            tk.messagebox.showerror("Hata", "Geçersiz port aralığı.")
            return

    # Sonuçları işle
    sonuclari_goster(tarama_sonuclari)


def sonuclari_goster(tarama_sonuclari):
  """
  Tarama sonuçlarını GUI'de görüntüler.
  """
  # Önceki sonuçları temizle
  for i in sonuclar_agaci.get_children():
    sonuclar_agaci.delete(i)

  # Sonuçları ağaç yapısına ekle
  for cihaz in tarama_sonuclari:
    sonuclar_agaci.insert("", tk.END, values=(
        cihaz["ip_adresi"],
        cihaz.get("mac_adresi", "Bilinmiyor"),
        ", ".join(map(str, cihaz["acik_portlar"])),
        cihaz.get("isletim_sistemi", "Bilinmiyor")
    ))

if __name__ == "__main__":
  pencere_olustur()
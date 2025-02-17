from tabulate import tabulate
import csv
def sonuclari_goruntule(tarama_sonuclari):
  """
  Tarama sonuçlarını kullanıcı dostu bir şekilde konsola yazdırır.

  Args:
    tarama_sonuclari: Cihaz bilgileri listesi.
  """
  basliklar = ["IP Adresi", "MAC Adresi", "Açık Portlar", "İşletim Sistemi"]
  tablo_verileri = list()
  for cihaz in tarama_sonuclari:
    tablo_verileri.append([
        cihaz["ip_adresi"],
        cihaz.get("mac_adresi", "Bilinmiyor"),
        ", ".join(map(str, cihaz["acik_portlar"])),
        cihaz.get("isletim_sistemi", "Bilinmiyor")
    ])
  print(tabulate(tablo_verileri, headers=basliklar, tablefmt="grid"))

def sonuclari_kaydet(tarama_sonuclari, dosya_adi="tarama_sonuclari.csv"):
  """
  Tarama sonuçlarını bir dosyaya kaydeder.

  Args:
    tarama_sonuclari: Cihaz bilgileri listesi.
    dosya_adi: Kaydedilecek dosya adı (varsayılan: tarama_sonuclari.csv).
  """
  with open(dosya_adi, "w", newline="") as csvfile:
    alanlar = ["ip_adresi", "mac_adresi", "acik_portlar", "isletim_sistemi"]
    yazici = csv.DictWriter(csvfile, fieldnames=alanlar)
    yazici.writeheader()
    for cihaz in tarama_sonuclari:
      yazici.writerow(cihaz)
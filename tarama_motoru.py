import ipaddress
import subprocess
import socket
import platform 
def hedef_belirle(hedef):
    try:
        if "-" in hedef:
            baslangic_ip, bitis_ip = hedef.split("-")
            ipaddress.ip_address(baslangic_ip)
            ipaddress.ip_address(bitis_ip)
            return ("aralik", baslangic_ip, bitis_ip)
        else:
            ag = ipaddress.ip_network(hedef)
            return ("ag", ag)
    except ValueError:
        return "Geçersiz hedef. Lütfen geçerli bir IP adresi aralığı veya alt ağ maskesi girin"
# hedef_belirle fonksiyonunu çağır ve sonucu tarama_bilgileri değişkenine ata
hedef = "192.168.1.1-192.168.1.100"  # Örnek hedef
tarama_bilgileri = hedef_belirle(hedef)

# if bloğunu fonksiyonun dışına taşı
if isinstance(tarama_bilgileri, tuple):
    print("Hedef geçerli:", tarama_bilgileri)
else:
    print(tarama_bilgileri)

def cihaz_tara(ip_adresleri):
    """
    Belirtilen IP adreslerindeki aktif cihazları tespit eder.

    Args:
      ip_adresleri: Taranacak IP adreslerinin listesi.

    Returns:
      Aktif cihazların IP adreslerinin listesini içeren bir liste.
    """
    aktif_cihazlar = list()
    for ip_adresi in ip_adresleri:
        try:
            # İşletim sistemini kontrol et
            if platform.system().lower() == "windows":
                # ping komutunu kullanarak cihazın aktif olup olmadığını kontrol et (Windows)
                cikti = subprocess.check_output(["ping", "-n", "1", ip_adresi], stderr=subprocess.DEVNULL)
                if "TTL=" in cikti.decode():
                    aktif_cihazlar.append(ip_adresi)
            else:
                # ping komutunu kullanarak cihazın aktif olup olmadığını kontrol et (Linux/macOS)
                subprocess.check_output(["ping", "-c", "1", ip_adresi], stderr=subprocess.DEVNULL)
                aktif_cihazlar.append(ip_adresi)
        except subprocess.CalledProcessError:
            pass  # Cihaz aktif değilse, hiçbir şey yapma
    return aktif_cihazlar

def port_tara(ip_adresi, port_araligi):
    """
    Belirtilen IP adresindeki açık portları tarar.

    Args:
      ip_adresi: Hedef IP adresi.
      port_araligi: Taranacak port aralığı (liste veya tuple).

    Returns:
      Açık portların bir listesini.
    """
    acik_portlar = list()
    for port in port_araligi:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)  # Zaman aşımı süresi (saniye)
                s.connect((ip_adresi, port))
                acik_portlar.append(port)
        except:
            pass  # Port kapalı veya hata oluştuğunda hiçbir şey yapma
    return acik_portlar
 
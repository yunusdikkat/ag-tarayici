# Ağ Tarayıcısı

Bu proje, Python ile yazılmış basit bir ağ tarayıcısıdır. Belirli bir IP adresi aralığındaki veya ağdaki aktif cihazları ve bu cihazlardaki açık portları tespit etmek için kullanılabilir.

## Özellikler

* **Hedef Belirleme:** Belirli bir IP adresi, IP adresi aralığı veya alt ağ maskesi taranabilir. 
* **Aktif Cihaz Tespiti:**  ICMP Echo Request (ping) paketleri kullanarak aktif cihazları tespit eder. 
* **Port Taraması:** Her aktif cihaz için açık TCP portlarını belirler. 
* **Sonuç Görüntüleme:** Tarama sonuçlarını kullanıcı dostu bir tablo formatında görüntüler. 
* **Sonuç Kaydetme:**  Tarama sonuçlarını bir CSV dosyasına kaydedebilir.

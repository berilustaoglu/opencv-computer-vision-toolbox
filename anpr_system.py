import cv2
import numpy as np
import os
import sys
from datetime import datetime

# OCR için Tesseract kütüphanesini güvenli şekilde çağıralım
try:
    import pytesseract
except ImportError:
    print("[-] Hata: 'pytesseract' kütüphanesi bulunamadı.")
    print("[*] Lütfen terminale yazın: pip install pytesseract")
    sys.exit()

class SecureANPRSystem:
    def __init__(self, log_file="access_logs.txt"):
        self.log_file = log_file
        # 🛡️ SİBER GÜVENLİK BİLGİ TABANI: İzinli ve Yasaklı Araç Listeleri
        self.authorized_plates = ["34ABC123", "06XYZ999", "35FOO456"]
        self.blacklisted_plates = ["34DANGER34", "07BAD007"]

    def log_access(self, plate, status):
        """Giriş denemelerini tarih, saat ve güvenlik durumuyla dosyaya kaydeder."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Plate: {plate} | Status: {status}\n"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def process_license_plate(self, image_path):
        if not os.path.exists(image_path):
            print(f"[-] Hata: Görsel bulunamadı -> '{image_path}'")
            return

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Gürültü azaltma ve kenar tespiti
        temp = cv2.bilateralFilter(gray, 7, 250, 250)
        edged = cv2.Canny(temp, 50, 200)

        # Kontur tespiti
        contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        screen = None
        for cnt in cnts:
            epsilon = 0.018 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4: # Dikdörtgen plaka şekli arıyoruz
                screen = approx
                break

        if screen is None:
            print("[-] Hata: Görsel üzerinde plaka geometrisi tespit edilemedi.")
            return

        # Plaka bölgesini maskeleme ve kırpma
        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [screen], 0, 255, -1)
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (botx, boty) = (np.max(x), np.max(y))
        cropped = gray[topx:botx + 1, topy:boty + 1]

        # 🔍 OCR AŞAMASI: Resimdeki yazıyı metne çevir
        # Temizlik: Çıkan metindeki boşlukları ve gereksiz karakterleri temizleyelim
        raw_plate = pytesseract.image_to_string(cropped, lang="eng")
        detected_plate = "".join(raw_plate.split()).upper()

        if not detected_plate:
            detected_plate = "UNKNOWN_PLATE"

        # 🚨 SİBER GÜVENLİK VE ERİŞİM KONTROL MANTIĞI
        print("\n" + "=" * 50)
        print("          ANPR GÜVENLİK DENETİM RAPORU          ")
        print("=" * 50)
        print(f"[+] Okunan Araç Plakası: {detected_plate}")

        if detected_plate in self.blacklisted_plates:
            status = "CRITICAL - BLACKLISTED ENTRY DENIED 🔴"
            print(f"[🚨 ALARM] KARA LİSTEDEKİ ARAÇ TESPİT EDİLDİ: {detected_plate}")
            print("[❌] GİRİŞ ENGELLENDİ! GÜVENLİK EKİPLERİNE HABER VERİLDİ.")
        elif detected_plate in self.authorized_plates:
            status = "AUTHORIZED - ACCESS GRANTED 🟢"
            print(f"[🟢 ONAY] İzinli Güvenli Araç: {detected_plate}")
            print("[✔️] GİRİŞ BARİYERİ AÇILDI.")
        else:
            status = "SUSPICIOUS - UNKNOWN VEHICLE ⚠️"
            print(f"[⚠️ UYARI] Kayıtsız/Yabancı Araç Giriş Denemesi: {detected_plate}")
            print("[?] Ziyaretçi Kaydı Oluşturuluyor.")

        print("=" * 50 + "\n")

        # Log kaydını kaydet
        self.log_access(detected_plate, status)

        # Sonuçları ekranda görselleştir
        cv2.imshow("Security Monitor - Main", img)
        cv2.imshow("Security Monitor - Cropped Plate", cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    system = SecureANPRSystem()
    print("=== Otomatik Plaka Tanıma ve Akıllı Güvenlik Sistemi ===")
    test_file = input("Tarama yapılacak plaka resmi adını girin (Örn: license_plate.jpg): ").strip()
    system.process_license_plate(test_file)

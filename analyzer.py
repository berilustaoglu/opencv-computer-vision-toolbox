import cv2
import numpy as np
import os
import sys

class ImageForensicAnalyzer:
    def __init__(self):
        pass

    def analyze_difference(self, original_path, modified_path):
        """İki resim arasındaki pikselsel farkları analiz eder ve görselleştirir."""
        if not os.path.exists(original_path) or not os.path.exists(modified_path):
            print("[-] Error: One or both image paths do not exist.")
            return

        # Resimleri oku
        img1 = cv2.imread(original_path)
        img2 = cv2.imread(modified_path)

        # Boyut kontrolü
        if img1.shape != img2.shape:
            print("[-] Error: Images have different dimensions. Cannot perform subtraction.")
            return

        print("[*] Image dimensions match. Processing pixel-level forensics...")

        # 1. Adım: İki resim arasındaki mutlak farkı bul (Subtraction)
        diff = cv2.absdiff(img1, img2)
        
        # 2. Adım: Farkı gri tona çevir ve eşikleme (Threshold) uygula
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_diff, 10, 255, cv2.THRESH_BINARY)

        # 3. Adım: Farkların yüzdesel oranını hesapla
        total_pixels = thresh.size
        non_zero_pixels = cv2.countNonZero(thresh)
        difference_percentage = (non_zero_pixels / total_pixels) * 100
        similarity_percentage = 100 - difference_percentage

        # 4. Adım: Farklı olan bölgeleri kırmızı bir ısı haritası (Heatmap) gibi orijinal resme giydir
        heatmap = img1.copy()
        heatmap[thresh > 0] = [0, 0, 255] # Farklı pikselleri KIRMIZI yap

        # Raporlama Ekranı
        print("\n" + "=" * 50)
        print("          FORENSIC ANALYSIS REPORT          ")
        print("=" * 50)
        print(f"[+] Total Pixel Count   : {total_pixels}")
        print(f"[+] Altered Pixel Count : {non_zero_pixels}")
        print(f"[+] Similarity Score    : {similarity_percentage:.4f}%")
        
        if non_zero_pixels == 0:
            print("[🟢 STATUS] COMPLETELY EQUAL: No tampering or noise detected.")
        else:
            print(f"[🔴 STATUS] TAMPERED/CHANGED: Images differ by {difference_percentage:.4f}%.")
        print("=" * 50 + "\n")

        # Görselleri ekranda göster
        cv2.imshow("Original Image", img1)
        cv2.imshow("Pixel Difference (Raw)", diff)
        cv2.imshow("Tamper Detection Map (Red Areas)", heatmap)
        
        print("[*] Windows opened. Press any key on the image windows to exit.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzer = ImageForensicAnalyzer()
    
    # Kullanıcıdan iki resmi girmesini isteyelim
    # Test etmek için aynı resmi iki kere girebilirsiniz (0 fark için)
    # Veya birini photoshoplanmış/filtrelenmiş sürümü yapabilirsiniz
    path_a = input("Enter path for Image 1 (e.g., batman.jpg): ").strip()
    path_b = input("Enter path for Image 2 (or same image for test): ").strip()

    analyzer.analyze_difference(path_a, path_b)

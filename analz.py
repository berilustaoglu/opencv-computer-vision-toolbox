import cv2
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

class ImageExposureAnalyzer:
    def __init__(self):
        # Matplotlib grafik arka plan stilini modern yapalım
        plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    def analyze_image(self, image_path):
        """Resmin renk kanallarını ve pozlama durumunu analiz eder."""
        if not os.path.exists(image_path):
            print(f"[-] Error: Target image '{image_path}' not found.")
            return

        img = cv2.imread(image_path)
        if img is None:
            print("[-] Error: Image corrupted or format not supported.")
            return

        print("[*] Image loaded successfully. Generating analytical color histograms...")

        # Kanalları ayır (OpenCV varsayılan olarak BGR okur)
        channels = cv2.split(img)
        colors = ('b', 'g', 'r')
        color_names = ('Blue Channel', 'Green Channel', 'Red Channel')

        # Grafik ekranını hazırla
        plt.figure(num="Image Intensity Histogram", figsize=(10, 5))
        plt.title("Color Channel Intensity Distribution (0 - 255)")
        plt.xlabel("Pixel Intensity Value")
        plt.ylabel("Number of Pixels")

        # Her kanalı kendi gerçek rengiyle grafik üzerine çizdir
        for i, col in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=col, label=color_names[i], linewidth=2)
            plt.xlim([0, 256])

        plt.legend(loc='upper right')

        # --- Pozlama (Exposure) Analiz Algoritması ---
        # Resmi gri tona çevirerek genel parlaklık haritasını çıkarıyoruz
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean_intensity = np.mean(gray)

        print("\n" + "=" * 50)
        print("          EXPOSURE DIAGNOSTIC REPORT          ")
        print("=" * 50)
        print(f"[+] Mean Pixel Intensity : {mean_intensity:.2f}")

        # Sektörel parlaklık eşikleri (0-80: Karanlık, 81-175: Dengeli, 176-255: Parlak)
        if mean_intensity < 70:
            print("[⚠️ STATUS] UNDEREXPOSED (Too Dark / Shadow Heavy)")
        elif mean_intensity > 185:
            print("[⚠️ STATUS] OVEREXPOSED (Too Bright / Highlight Washed)")
        else:
            print("[🟢 STATUS] PERFECTLY BALANCED EXPOSURE")
        print("=" * 50 + "\n")

        # Pencereleri ekrana getir
        cv2.imshow("Source Image", img)
        plt.show() # Grafik penceresini açar (Engellemeyi kaldırmak için cv2'den önce çağrıldı)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    analyzer = ImageExposureAnalyzer()
    
    # Kullanıcıdan resmi alalım
    target_img = input("Enter image filename to analyze (e.g., test.jpg): ").strip()
    analyzer.analyze_image(target_img)

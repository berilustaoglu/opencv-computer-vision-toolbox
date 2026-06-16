import cv2
import numpy as np

def nothing(x):
    pass

def run_designer():
    # 512x600 boyutunda geniş bir çalışma alanı oluşturuyoruz (Alt kısmı metinler için ayırdık)
    canvas = np.zeros((600, 512, 3), np.uint8)
    
    # Profesyonel yapı için tek bir ana pencere tanımlıyoruz
    window_name = "Pro Color Palette Designer"
    cv2.namedWindow(window_name)

    # Sürgüleri (Trackbar) ana pencerenin üzerine ekliyoruz
    cv2.createTrackbar("R - Red", window_name, 0, 255, nothing)
    cv2.createTrackbar("G - Green", window_name, 0, 255, nothing)
    cv2.createTrackbar("B - Blue", window_name, 0, 255, nothing)

    print("[*] Pro Palette Designer başlatıldı.")
    print("[*] Kapatmak için 'q' tuşuna, HEX kodunu terminale yazdırmak için 'w' tuşuna basın.\n")

    while True:
        # Sürgülerden anlık RGB değerlerini oku
        r = cv2.getTrackbarPos("R - Red", window_name)
        g = cv2.getTrackbarPos("G - Green", window_name)
        b = cv2.getTrackbarPos("B - Blue", window_name)

        # Üst alanı (0-450 piksel arası) tamamen seçilen renkle boya
        canvas[0:450, :] = [b, g, r]

        # Alt bilgi panelini (450-600 piksel arası) koyu gri yap
        canvas[450:600, :] = [35, 35, 35]

        # RGB değerlerini HEX (Onaltılık) renk koduna dönüştür (Örn: #FF00AA)
        hex_code = f"#{r:02X}{g:02X}{b:02X}"

        # Ekranın alt paneline profesyonel metinleri yazdır
        cv2.putText(canvas, f"RGB: ({r}, {g}, {b})", (30, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(canvas, f"HEX: {hex_code}", (30, 540), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(canvas, "Press 'w' to print code | 'q' to quit", (30, 580), cv2.FONT_HERSHEY_PLAIN, 1.0, (180, 180, 180), 1)

        # Canlı görüntüyü ekrana yansıt
        cv2.imshow(window_name, canvas)

        # Klavye kontrolleri
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):  # Çıkış
            break
        elif key == ord("w"):  # Rengi kaydet/yazdır
            print(f"[🟢 COPIED] RGB({r},{g},{b}) -> HEX: {hex_code}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_designer():

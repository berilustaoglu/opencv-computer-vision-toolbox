import cv2
import os
import sys

class SmartImageResizer:
    def __init__(self, output_dir="output_images"):
        self.output_dir = output_dir
        # Çıktı klasörü yoksa otomatik oluştur
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def resize_aspect_ratio(self, img, width=None, height=None, inter=cv2.INTER_AREA):
        """Resmin en-boy oranını koruyarak boyutlandırma yapar."""
        (h, w) = img.shape[:2]
        
        if width is None and height is None:
            return img
        
        if width is None:
            # Yüksekliğe göre oranı hesapla
            r = height / float(h)
            dimension = (int(w * r), height)
        else:
            # Genişliğe göre oranı hesapla
            r = width / float(w)
            dimension = (width, int(h * r))
        
        return cv2.resize(img, dimension, interpolation=inter)

    def process_single_image(self, image_path, target_width=None, target_height=None):
        """Tek bir resmi güvenli bir şekilde işler ve kaydeder."""
        if not os.path.exists(image_path):
            print(f"[-] Error: Image '{image_path}' not found.")
            return False

        img = cv2.imread(image_path)
        if img is None:
            print(f"[-] Error: Could not read '{image_path}'. Corrupted file?")
            return False

        # Boyutlandırma fonksiyonunu çağır
        resized_img = self.resize_aspect_ratio(img, width=target_width, height=target_height)
        
        # Dosya adını ayıkla ve yeni klasöre kaydet
        base_name = os.path.basename(image_path)
        output_path = os.path.join(self.output_dir, f"resized_{base_name}")
        cv2.imwrite(output_path, resized_img)
        
        print(f"[🟢 SUCCESS] Processed: {image_path} -> Saved to: {output_path}")
        return True

if __name__ == "__main__":
    print("=" * 60)
    print("        SMART ASPECT-RATIO IMAGE RESIZER TOOL        ")
    print("=" * 60)

    resizer = SmartImageResizer()
    
    # Kullanıcıdan test etmek istediği dosya adını alalım
    test_image = input("Enter image filename to resize (e.g., deneme.jpg): ").strip()
    
    # Pro sürüm esnekliği: İster genişlik verin, ister yükseklik
    print("\nChoose resize mode:")
    print("1 - Set Target Height (Width calculates automatically)")
    print("2 - Set Target Width (Height calculates automatically)")
    choice = input("Choice (1/2): ").strip()

    if choice == "1":
        h_val = int(input("Enter target height (e.g., 450): "))
        resizer.process_single_image(test_image, target_height=h_val)
    elif choice == "2":
        w_val = int(input("Enter target width (e.g., 800): "))
        resizer.process_single_image(test_image, target_width=w_val)
    else:
        print("[-] Invalid choice. Exiting.")

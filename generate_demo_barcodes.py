import os
import cv2
import numpy as np

def draw_synthetic_qr_code(img, cx, cy, size=180, payload_text="ITEM-9842-MACBOOK-PRO"):
    """Draws a synthetic 2D QR Code graphic with 3 corner finder pattern targets."""
    half = size // 2
    x1, y1 = cx - half, cy - half
    x2, y2 = cx + half, cy + half
    
    # White QR background box
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), -1)
    cv2.rectangle(img, (x1, y1), (x2, y2), (20, 20, 20), 3)
    
    # 3 Corner Finder Pattern Targets (Top-Left, Top-Right, Bottom-Left)
    def draw_finder_pattern(px, py):
        cv2.rectangle(img, (px - 20, py - 20), (px + 20, py + 20), (0, 0, 0), -1)
        cv2.rectangle(img, (px - 14, py - 14), (px + 14, py + 14), (255, 255, 255), -1)
        cv2.rectangle(img, (px - 8, py - 8), (px + 8, py + 8), (0, 0, 0), -1)
        
    draw_finder_pattern(x1 + 35, y1 + 35) # Top-Left
    draw_finder_pattern(x2 - 35, y1 + 35) # Top-Right
    draw_finder_pattern(x1 + 35, y2 - 35) # Bottom-Left
    
    # Random Data Module Grid
    np.random.seed(42)
    grid_size = 12
    step = (size - 30) // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            if (i < 4 and j < 4) or (i < 4 and j > 7) or (i > 7 and j < 4):
                continue
            if np.random.rand() > 0.4:
                mx = x1 + 15 + i * step
                my = y1 + 15 + j * step
                cv2.rectangle(img, (mx, my), (mx + step - 1, my + step - 1), (0, 0, 0), -1)
                
    # Payload label below
    cv2.putText(img, payload_text, (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

def generate_synthetic_barcode_scene(output_path="input/sample_inventory_qr.jpg", width=800, height=600):
    """Generates a synthetic inventory scanner image with a QR Code and product label."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Desk / Warehouse Table Background
    bg = np.ones((height, width, 3), dtype=np.uint8) * 45
    
    # Shipping Box Container
    cv2.rectangle(bg, (100, 100), (width - 100, height - 100), (40, 90, 140), -1) # Cardboard brown
    cv2.rectangle(bg, (100, 100), (width - 100, height - 100), (20, 50, 90), 3)
    
    # Draw QR Code on Box Label
    draw_synthetic_qr_code(bg, cx=width // 2, cy=height // 2, size=220, payload_text="ITEM-9842-MACBOOK-PRO")
    
    # Header
    cv2.putText(bg, "AI INVENTORY SCANNER & QR AUDIT BENCHMARK", (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 255), 2)
                
    cv2.imwrite(output_path, bg)
    print(f"[OK] Synthetic QR inventory scene saved to '{output_path}'")
    return output_path

if __name__ == "__main__":
    generate_synthetic_barcode_scene()

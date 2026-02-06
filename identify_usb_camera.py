#!/usr/bin/env python3
"""
Identify which camera is your USB camera
Shows both cameras side by side
"""
import cv2
import numpy as np

def main():
    print("🎥 Camera Identification Tool")
    print("=" * 50)
    
    # Open both cameras
    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(2)
    
    if not cap0.isOpened():
        print("❌ Camera 0 not available")
        return
    
    if not cap1.isOpened():
        print("❌ Camera 1 not available")
        cap0.release()
        return
    
    print("✅ Both cameras opened successfully")
    print("\n📌 Instructions:")
    print("   - LEFT window = Camera 0")
    print("   - RIGHT window = Camera 1")
    print("   - Identify which one is your USB camera")
    print("   - Press 'q' to quit")
    print("\nShowing both cameras now...\n")
    
    while True:
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
        
        if not ret0 or not ret1:
            print("❌ Failed to read from cameras")
            break
        
        # Resize for display
        frame0 = cv2.resize(frame0, (640, 480))
        frame1 = cv2.resize(frame1, (640, 480))
        
        # Add labels
        cv2.putText(frame0, "CAMERA 0", (10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(frame1, "CAMERA 1", (10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        
        # Show both
        cv2.imshow("Camera 0 (LEFT)", frame0)
        cv2.imshow("Camera 1 (RIGHT)", frame1)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 50)
    print("Which camera is your USB camera?")
    choice = input("Enter 0 or 1: ").strip()
    
    if choice in ['0', '1']:
        print(f"\n✅ You identified Camera {choice} as your USB camera")
        print(f"\n📝 To use this camera in your face locking system:")
        print(f"   Update camera index to {choice} in:")
        print(f"   - src/camera.py")
        print(f"   - src/face_locking.py")
        print(f"   - src/enroll.py (if it uses camera)")
        return choice
    else:
        print("❌ Invalid choice")
        return None

if __name__ == "__main__":
    main()

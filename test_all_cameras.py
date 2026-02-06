#!/usr/bin/env python3
"""
Test all available camera indices to find your USB camera
"""
import cv2

def test_camera(index):
    """Test if a camera at given index works"""
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✅ Camera {index}: Working - Resolution: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
            return True
        else:
            print(f"⚠️ Camera {index}: Opened but can't read frames")
            cap.release()
            return False
    else:
        print(f"❌ Camera {index}: Not available")
        return False

def main():
    print("🔍 Scanning for available cameras...\n")
    
    available_cameras = []
    
    # Test indices 0-5 (covers most systems)
    for i in range(6):
        if test_camera(i):
            available_cameras.append(i)
    
    print(f"\n📊 Summary:")
    print(f"Found {len(available_cameras)} working camera(s): {available_cameras}")
    
    if len(available_cameras) > 0:
        print("\n🎥 Testing each camera with live preview...")
        print("Press any key to move to next camera, 'q' to quit\n")
        
        for idx in available_cameras:
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                print(f"Showing Camera {idx} - Press any key for next camera...")
                
                while True:
                    ret, frame = cap.read()
                    if ret:
                        # Add text overlay
                        cv2.putText(frame, f"Camera Index: {idx}", (10, 30), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(frame, "Press any key for next, 'q' to quit", (10, 70), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                        
                        cv2.imshow(f"Camera Test - Index {idx}", frame)
                        
                        key = cv2.waitKey(1) & 0xFF
                        if key != 255:  # Any key pressed
                            break
                    else:
                        print(f"Failed to read from camera {idx}")
                        break
                
                cap.release()
                cv2.destroyAllWindows()
                
                if key == ord('q'):
                    print("Quit by user")
                    break
    else:
        print("\n❌ No working cameras found!")

if __name__ == "__main__":
    main()

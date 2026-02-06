"""
Camera utility functions for automatic external camera detection
"""
import cv2
from typing import Optional, List, Tuple


def get_available_cameras(max_test: int = 5) -> List[int]:
    """
    Test camera indices and return list of working cameras.
    
    Args:
        max_test: Maximum number of camera indices to test
        
    Returns:
        List of working camera indices
    """
    available = []
    for i in range(max_test):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(i)
            cap.release()
    return available


def get_camera_info(index: int) -> Optional[Tuple[int, int, str]]:
    """
    Get camera information (width, height, backend).
    
    Args:
        index: Camera index
        
    Returns:
        Tuple of (width, height, backend_name) or None if camera not available
    """
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        return None
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    backend = cap.getBackendName()
    
    cap.release()
    return (width, height, backend)


def select_best_camera(prefer_external: bool = True) -> int:
    """
    Automatically select the best camera.
    
    Strategy:
    - If prefer_external=True and multiple cameras found, prefer higher index (usually external USB)
    - If only one camera, use it
    - If no cameras, raise error
    
    Args:
        prefer_external: If True, prefer external cameras over built-in
        
    Returns:
        Camera index to use
        
    Raises:
        RuntimeError: If no cameras are available
    """
    available = get_available_cameras()
    
    if not available:
        raise RuntimeError(
            "No cameras detected! Please connect a camera and try again."
        )
    
    if len(available) == 1:
        camera_idx = available[0]
        print(f"📷 Using camera {camera_idx} (only camera detected)")
        return camera_idx
    
    # Multiple cameras available
    if prefer_external:
        # Prefer higher index (usually external USB camera)
        camera_idx = available[-1]
        print(f"📷 Multiple cameras detected: {available}")
        print(f"📷 Auto-selected camera {camera_idx} (external USB camera)")
    else:
        # Prefer lower index (usually built-in camera)
        camera_idx = available[0]
        print(f"📷 Multiple cameras detected: {available}")
        print(f"📷 Auto-selected camera {camera_idx} (built-in camera)")
    
    return camera_idx


def open_camera(camera_index: Optional[int] = None, prefer_external: bool = True) -> cv2.VideoCapture:
    """
    Open camera with automatic selection if index not specified.
    
    Args:
        camera_index: Specific camera index to use, or None for auto-selection
        prefer_external: If True and camera_index is None, prefer external cameras
        
    Returns:
        Opened VideoCapture object
        
    Raises:
        RuntimeError: If camera cannot be opened
    """
    if camera_index is None:
        camera_index = select_best_camera(prefer_external=prefer_external)
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        raise RuntimeError(
            f"Failed to open camera {camera_index}. "
            f"Available cameras: {get_available_cameras()}"
        )
    
    info = get_camera_info(camera_index)
    if info:
        width, height, backend = info
        print(f"✅ Camera {camera_index} opened: {width}x{height} ({backend})")
    
    return cap


def list_cameras_interactive() -> int:
    """
    Show user all available cameras and let them choose.
    
    Returns:
        Selected camera index
    """
    available = get_available_cameras()
    
    if not available:
        raise RuntimeError("No cameras detected!")
    
    print("\n📷 Available Cameras:")
    print("=" * 50)
    
    for idx in available:
        info = get_camera_info(idx)
        if info:
            width, height, backend = info
            print(f"  Camera {idx}: {width}x{height} ({backend})")
        else:
            print(f"  Camera {idx}: Available")
    
    print("=" * 50)
    
    if len(available) == 1:
        print(f"\nOnly one camera available. Using camera {available[0]}")
        return available[0]
    
    while True:
        try:
            choice = input(f"\nSelect camera index {available} (or press Enter for auto): ").strip()
            
            if not choice:
                # Auto-select
                return select_best_camera(prefer_external=True)
            
            idx = int(choice)
            if idx in available:
                return idx
            else:
                print(f"❌ Camera {idx} not available. Choose from: {available}")
        except ValueError:
            print("❌ Invalid input. Enter a number.")
        except KeyboardInterrupt:
            print("\n\n👋 Cancelled")
            raise

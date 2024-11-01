# disp_btct_ctrl.py
# Python minimum required versions: 3.6

import argparse
from monitorcontrol import get_monitors
import win32api

def enumerate_active_displays():
    print("Connected Displays:")
    i = 0
    while True:
        try:
            display = win32api.EnumDisplayDevices(None, i)
            if display.StateFlags & 0x00000001:  # DISPLAY_DEVICE_ACTIVE
                print(f"- Device Name  : {display.DeviceName}")
                print(f"  Device String: {display.DeviceString}")
                if display.StateFlags & 0x00000004:  # DISPLAY_DEVICE_PRIMARY_DEVICE
                    print("  Primary Display: Yes")
                else:
                    print("  Primary Display: No")
                print()
            i += 1
        except Exception:
            break

def set_display_settings(target, brightness=None, contrast=None, blue_light_filter=None):
    # Convert / to \
    if target.startswith("/"):
        target = target.replace("/", "\\")

    # Create a list of names to identify the target display
    monitors = get_monitors()
    windows_displays = []
    i = 0
    while True:
        try:
            display = win32api.EnumDisplayDevices(None, i)
            if display.StateFlags & 0x00000001:  # DISPLAY_DEVICE_ACTIVE
                windows_displays.append(display.DeviceName)
            i += 1
        except Exception:
            break

    # Check if the target exists and access the matching monitorcontrol monitor by index
    if target not in windows_displays:
        print(f"Error: Display '{target}' not found.")
        return

    target_index = windows_displays.index(target)
    target_monitor = monitors[target_index] if target_index < len(monitors) else None

    if target_monitor is None:
        print(f"Error: Monitor matching '{target}' not found in monitorcontrol list.")
        return

    # Apply settings
    with target_monitor:
        if brightness is not None:
            target_monitor.set_luminance(brightness)
            print("brightness", brightness)
        if contrast is not None:
            target_monitor.set_contrast(contrast)
            print("contrast", contrast)
        if blue_light_filter is not None:
            print("blue_light_filter is not supported yet.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control LCD display settings.")
    parser.add_argument("-target", help="Target display device name (e.g., //./DISPLAY12).")
    parser.add_argument("-brightness", type=int, help="Set brightness level (0-100).")
    parser.add_argument("-contrast", type=int, help="Set contrast level (0-100).")
    parser.add_argument("-blfilter", type=int, help="Set blue light filter level (if supported).")

    args = parser.parse_args()

    if not any([args.target, args.brightness, args.contrast, args.blfilter]):
        print("No command-line parameters provided. Listing all active displays:\n")
        enumerate_active_displays()
        print("Usage:")
        print("  disp_btct_ctrl.py -target \"\\\\.\\DISPLAY1\" -brightness 10 -contrast 30")
        #print("  disp_btct_ctrl.py -target \"\\\\.\\DISPLAY1\" -brightness 10 -contrast 30 -blfilter 0")
        print("\nOptions:")
        print("  -target       Specify the display device name to control (required for settings).")
        #print("  -brightness   Set brightness level (0-100).")
        print("  -contrast     Set contrast level (0-100).")
        #print("  -blfilter     Set blue light filter level (if supported by the monitor).")
    else:
        if args.target:
            set_display_settings(args.target, args.brightness, args.contrast, args.blfilter)
        else:
            print("Error: '-target' is required when setting brightness, contrast, or blue light filter.")

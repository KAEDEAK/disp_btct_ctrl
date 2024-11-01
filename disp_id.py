import tkinter as tk
import win32api

def show_identifiers():
    # Retrieve all active display devices
    monitors = []
    i = 0
    while True:
        try:
            display = win32api.EnumDisplayDevices(None, i)
            if display.StateFlags & 0x00000001:  # DISPLAY_DEVICE_ACTIVE
                monitors.append(display)
            i += 1
        except Exception:
            break
    
    # Display an identification window for each monitor based on its Device ID
    for idx, monitor in enumerate(monitors):
        device_id = monitor.DeviceName
        print(f"Monitor {idx + 1}: {device_id}")  # Output Device ID to console
        
        # Get the position and size of each monitor
        monitor_info = win32api.EnumDisplayMonitors(None, None)
        left, top, right, bottom = win32api.GetMonitorInfo(monitor_info[idx][0])['Monitor']
        width = right - left
        height = bottom - top

        # Create an identification window for each monitor
        identifier_window = tk.Tk()  # Use Tk instance
        identifier_window.overrideredirect(True)  # Hide window borders
        identifier_window.attributes('-topmost', True)  # Display on top
        identifier_window.geometry(f"300x200+{left + width // 2 - 150}+{top + height // 2 - 100}")

        # Display the Device ID in a label
        label = tk.Label(identifier_window, text=device_id, font=("Helvetica", 24), fg="white", bg="black")
        label.pack(expand=True)

        # Automatically close the window after 2 seconds
        identifier_window.after(2000, identifier_window.destroy)  # Close after 2 seconds

    # Start the main loop
    identifier_window.mainloop()

if __name__ == "__main__":
    show_identifiers()

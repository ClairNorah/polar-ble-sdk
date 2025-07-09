import asyncio
import threading
from bleak import BleakScanner, BleakClient
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

class PolarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Polar Verity Sense RR Logger")
        self.device_address = None
        self.client = None
        self.recording = False
        self.csv_file = None
        self.csv_writer = None
        self.child_id = ""

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Child ID:").pack(pady=5)
        self.child_entry = tk.Entry(self.root)
        self.child_entry.pack(pady=5)

        self.start_btn = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

        self.status = tk.Label(self.root, text="Status: Idle", fg="white")
        self.status.pack(pady=10)

        # Event buttons
        self.event_frame = tk.Frame(self.root)
        self.event_frame.pack(pady=5)

        self.event_buttons = []
        events = ["Triage", "Waiting Room", "Examination Room", "Doctor's Examination"]
        for label in events:
            b = tk.Button(self.event_frame, text=label, width=20, command=lambda l=label: self.log_event(l))
            b.config(state=tk.DISABLED)
            b.pack(pady=2)
            self.event_buttons.append(b)

    def set_event_buttons_state(self, state):
        for b in self.event_buttons:
            b.config(state=state)

    def log_status(self, msg, color="white"):
        self.status.config(text=f"Status: {msg}", fg=color)
        self.root.update()

    def start_recording(self):
        self.child_id = self.child_entry.get().strip()
        if not self.child_id:
            messagebox.showerror("Error", "Please enter a child ID.")
            return

        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.set_event_buttons_state(tk.NORMAL)
        self.log_status("Scanning for Polar device...")

        threading.Thread(target=self.run_async_ble, daemon=True).start()

    def stop_recording(self):
        self.recording = False
        self.set_event_buttons_state(tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)
        self.log_status("Stopping...", "red")

    async def scan_and_connect(self):
        devices = await BleakScanner.discover(timeout=5.0)
        for d in devices:
            if "Polar" in d.name:
                self.device_address = d.address
                return d.address
        return None

    def run_async_ble(self):
        asyncio.run(self.record_ble_data())

    def handle_hr_notify(self, sender, data):
        flags = data[0]
        rr_present = flags & 0x10
        index = 1
        hr = data[index]
        index += 1

        rr_intervals = []
        if rr_present:
            while index + 1 < len(data):
                rr = int.from_bytes(data[index:index+2], byteorder='little') / 1024 * 1000
                rr_intervals.append(int(rr))
                index += 2

        now = datetime.utcnow().isoformat()
        for rr in rr_intervals:
            self.csv_writer.writerow([now, hr, rr, self.child_id, ""])
        print(f"[{now}] HR: {hr}, RR: {rr_intervals}")

    def log_event(self, label):
        if not self.csv_writer:
            return
        now = datetime.utcnow().isoformat()
        event_desc = f"Entered {label}"
        self.csv_writer.writerow([now, "", "", self.child_id, event_desc])
        print(f"[{now}] Event: {event_desc}")
        self.log_status(f"Event logged: {label}", "purple")

    async def record_ble_data(self):
        address = await self.scan_and_connect()
        if not address:
            self.log_status("Device not found", "red")
            return

        self.log_status("Device found. Connecting...")

        try:
            async with BleakClient(address) as client:
                self.client = client
                self.log_status("Connected. Recording...")

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"rr_log_{self.child_id}_{timestamp}.csv"
                self.csv_file = open(filename, mode='w', newline='')
                self.csv_writer = csv.writer(self.csv_file)
                self.csv_writer.writerow(["timestamp", "heart_rate_bpm", "rr_interval_ms", "child_id", "event"])

                self.recording = True
                await client.start_notify(HR_UUID, self.handle_hr_notify)

                while self.recording:
                    await asyncio.sleep(1)

                await client.stop_notify(HR_UUID)
                self.csv_file.close()
                self.log_status(f"Recording stopped. File: {filename}", "green")

        except Exception as e:
            self.log_status(f"Error: {str(e)}", "red")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.set_event_buttons_state(tk.DISABLED)

# Run the GUI
root = tk.Tk()
app = PolarApp(root)
root.mainloop()

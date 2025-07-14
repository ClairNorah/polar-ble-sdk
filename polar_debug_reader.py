import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import csv

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import csv
from collections import deque

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

async def main():
    print("🔍 Scanning for Polar devices...")
    devices = await BleakScanner.discover(timeout=5.0)

    target = None
    for d in devices:
        print(f"Found: {d.name} - {d.address}")
        if d.name and "Polar" in d.name:
            target = d
            break

    if not target:
        print("❌ No Polar device found.")
        return

    print(f"✅ Connecting to {target.name} ({target.address})...")

    async with BleakClient(target.address) as client:
        if not client.is_connected:
            print("❌ BLE client not connected.")
            return

        print("✅ Connected.")

        # Create CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"polar_output_{timestamp}.csv"
        csv_file = open(filename, mode='w', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["timestamp", "heart_rate_bpm", "rr_intervals_ms", "flags_hex", "energy_expended", "sensor_contact", "signal_stable"])

        # Stability tracking
        rr_window = deque(maxlen=5)
        signal_stable = False

        def handle_hr(sender, data):
            nonlocal signal_stable
            now = datetime.utcnow().isoformat()
            flags = data[0]

            hr_format = flags & 0x01
            sensor_contact = (flags >> 1) & 0x03
            energy_present = (flags >> 3) & 0x01
            rr_present = (flags >> 4) & 0x01

            index = 1
            hr = data[index] if hr_format == 0 else int.from_bytes(data[index:index+2], 'little')
            index += 1 if hr_format == 0 else 2

            energy = None
            if energy_present:
                energy = int.from_bytes(data[index:index+2], byteorder='little')
                index += 2

            rr_list = []
            if rr_present:
                while index + 1 < len(data):
                    rr = int.from_bytes(data[index:index+2], byteorder='little') / 1024 * 1000
                    rr_list.append(round(rr, 2))
                    index += 2

            # Signal stability tracking
            rr_window.append(bool(rr_list))
            current_stable = rr_window.count(True) >= 3

            if current_stable and not signal_stable:
                signal_stable = True
                print("✅ Signal is now STABLE (RR intervals detected reliably)")
            elif not current_stable and signal_stable:
                signal_stable = False
                print("⚠️ Signal is UNSTABLE (RR intervals missing)")

            print(f"[{now}] HR: {hr}, RR: {rr_list if rr_list else 'None'}")

            csv_writer.writerow([
                now,
                hr,
                str(rr_list) if rr_list else "",
                f"0x{flags:02x}",
                energy if energy is not None else "",
                "yes" if sensor_contact == 3 else "no",
                "yes" if signal_stable else "no"
            ])

        await client.start_notify(HR_UUID, handle_hr)

        print(f"📡 Logging to {filename} (Ctrl+C to stop)")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping...")
        finally:
            await client.stop_notify(HR_UUID)
            csv_file.close()
            print(f"✅ CSV file saved: {filename}")

# Run it
asyncio.run(main())

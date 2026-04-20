from backend.storage import compare_devices


def test_compare_devices_detects_added_and_removed_devices():
    old_devices = [
        {"ip": "192.168.1.2", "hostname": "old-device"},
        {"ip": "192.168.1.3", "hostname": "same-device"},
    ]

    new_devices = [
        {"ip": "192.168.1.3", "hostname": "same-device"},
        {"ip": "192.168.1.4", "hostname": "new-device"},
    ]

    added, removed = compare_devices(old_devices, new_devices)

    assert added == [{"ip": "192.168.1.4", "hostname": "new-device"}]
    assert removed == [{"ip": "192.168.1.2", "hostname": "old-device"}]

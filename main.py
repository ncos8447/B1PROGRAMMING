#iot device management system
from datetime import datetime

class Device:
    def __init__(self, device_id, device_type, owner, firmware_version="1.0.0"):
        self.device_id = device_id
        self.device_type = device_type
        self.owner = owner
        self.firmware_version = firmware_version
        self.compliance_status = "unknown"
        self.last_security_scan = None
        self.is_active = True
        self.access_log = []

    # log device activity
    def log_access(self, username, action):
        self.access_log.append(f"{datetime.now()}: {username} - {action}")

    # check if user can access device
    def authorise(self, user):
        if not self.is_active:
            self.log_access(user.get_username(), "Denied - inactive device")
            return False

        if not self.check_compliance():
            if not user.check_privileges("admin"):
                self.log_access(user.get_username(), "Denied - non-compliant device")
                return False

        if self.owner != user.get_username() and not user.check_privileges("admin"):
            self.log_access(user.get_username(), "Denied - not owner")
            return False

        self.log_access(user.get_username(), "Access granted")
        return True

    # run security scan
    def run_security_scan(self):
        self.last_security_scan = datetime.now()
        self.compliance_status = "compliant"
        self.log_access("SYSTEM", "Security scan completed")

    # check device compliance
    def check_compliance(self):
        if self.last_security_scan is None:
            self.compliance_status = "unknown"
            return False

        days_since_scan = (datetime.now() - self.last_security_scan).days
        if days_since_scan > 30:
            self.compliance_status = "non-compliant"
            return False

        return self.compliance_status == "compliant"

    # update firmware (admin only)
    def update_firmware(self, version, user):
        if not user.check_privileges("admin"):
            return False

        self.firmware_version = version
        self.log_access(user.get_username(), f"Firmware updated to {version}")
        return True

    # quarantine device (admin only)
    def quarantine(self, user):
        if not user.check_privileges("admin"):
            return False

        self.is_active = False
        self.log_access(user.get_username(), "Device quarantined")
        return True

    # return device info
    def get_device_info(self):
        return {
            "device_id": self.device_id,
            "device_type": self.device_type,
            "firmware_version": self.firmware_version,
            "compliance_status": self.compliance_status,
            "owner": self.owner,
            "is_active": self.is_active
        }

class DeviceManager:
    def __init__(self):
        self.devices = {}

    # add device
    def add_device(self, device):
        device_info = device.get_device_info()
        self.devices[device_info["device_id"]] = device

    # remove device (admin only)
    def remove_device(self, device_id, user):
        if not user.check_privileges("admin"):
            return False
        if device_id in self.devices:
            del self.devices[device_id]
            return True
        return False

    # generate security report (admin only)
    def generate_security_report(self, user):
        if not user.check_privileges("admin"):
            return None

        report = []
        for device_id, device in self.devices.items():
            device.check_compliance()
            info = device.get_device_info()
            report.append(info)
        return report

class User:
    def __init__(self, username, admin=False):
        self.username = username
        self.admin = admin

    # return username
    def get_username(self):
        return self.username

    # check privileges
    def check_privileges(self, privilege):
        if privilege == "admin":
            return self.admin
        return False
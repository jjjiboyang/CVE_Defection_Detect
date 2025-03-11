import hashlib
import uuid

def get_machine_id():
    return hashlib.sha256(uuid.getnode().to_bytes(6, 'big')).hexdigest()

license_key = "cec372e3696b03da1e958cbd01313e0bf2de7f58772e26178edfca7376e9532e"
machine_id = get_machine_id()

if machine_id != license_key:
    print("授权失败")
    exit()
else:
    print("授权成功")
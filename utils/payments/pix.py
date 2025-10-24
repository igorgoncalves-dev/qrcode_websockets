from pathlib import Path
from uuid import uuid4

import qrcode


class Pix:
    def __init__(self) -> None:
        pass

    def create_payment(self):
        # Create a payment in the financial instituation
        bank_payment_id = str(uuid4())

        # qr_code: generating a randomic hash
        hash_payment = f'hash_payment_{bank_payment_id}'

        # qr_code: creating the qrcode image
        qr_code_img = qrcode.make(hash_payment)

        # qr_code: saving the qrcode image
        qr_code_img.save(f"static\img\qr_code_{bank_payment_id}.png") #type: ignore

        return {
            "bank_payment_id": bank_payment_id,
            "qr_code_path": f"qr_code_{bank_payment_id}"
        }
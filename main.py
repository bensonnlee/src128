from datetime import datetime

from api.main import generate_id
from core.barcode_generator import BarcodeGenerator

if __name__ == "__main__":
    barcode_id = generate_id()  # "&380324664181&"
    barcode_generator = BarcodeGenerator()
    barcode_generator.generate_128(barcode_id)
    print(f"Generated barcode with the following data: {barcode_id}")

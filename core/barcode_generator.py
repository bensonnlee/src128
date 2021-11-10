import barcode


class BarcodeGenerator:
    def generate_128(self, data):
        code128 = barcode.get("code128", data)
        code128.save("src128")

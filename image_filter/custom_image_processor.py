import struct
from PIL import Image
import os

class CustomImageProcessor:
    def __init__(self, file_name=None):
        self.width = None
        self.height = None
        self.pixels = None
        self.file_name = file_name
	
	if file_name:
	    self.load(file_name)
    def load(self, file_name):
        """BMP 이미지 파일 로드 (24비트 BMP 형식)."""
        try:
            with open(file_name, "rb") as f:
                header = f.read(54)
                self.width, self.height = struct.unpack("<ii", header[18:26])
                print(f"Image loaded: {file_name} ({self.width}x{self.height})")

                self.pixels = []
                row_padded = (self.width * 3 + 3) & ~3
                for y in range(self.height):
                    row = []
                    for x in range(self.width):
                        b, g, r = struct.unpack("BBB", f.read(3))
                        row.append((r, g, b))
                    self.pixels.insert(0, row)
                    f.read(row_padded - self.width * 3)
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except Exception as e:
            print(f"Error loading image: {e}")

    def save(self, file_name):
        """BMP 이미지 파일로 저장."""
        if self.pixels is None:
            print("No image loaded to save.")
            return

        try:
            with open(file_name, "wb") as f:
                row_padded = (self.width * 3 + 3) & ~3
                file_size = 54 + row_padded * self.height
                header = struct.pack(
                    "<2sIHHIIIIHHIIIIII",
                    b"BM",
                    file_size,
                    0, 0,
                    54,
                    40,
                    self.width, self.height,
                    1, 24,
                    0, row_padded * self.height,
                    2835, 2835,
                    0, 0
                )
                f.write(header)

                for row in reversed(self.pixels):
                    for r, g, b in row:
                        f.write(struct.pack("BBB", b, g, r))
                    f.write(b"\x00" * (row_padded - self.width * 3))
                print(f"Image saved as: {file_name}")
        except Exception as e:
            print(f"Error saving image: {e}")

    def save_with_suffix(self, suffix):
        """현재 파일 경로에 suffix를 붙여 저장."""
        if self.file_name is None:
            print("No file loaded to save.")
            return

        base, ext = os.path.splitext(self.file_name)
        output_file = f"{base}_{suffix}{ext}"
        self.save(output_file)

    def apply_grayscale(self, output_file):
        """흑백 이미지 생성."""
        if self.pixels is None:
            print("No image loaded to process.")
            return

        original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = original_pixels[y][x]
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                self.pixels[y][x] = (gray, gray, gray)
        self.save(output_file)

    def apply_invert_colors(self, output_file):
        """색상 반전."""
        if self.pixels is None:
            print("No image loaded to process.")
            return

        original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = original_pixels[y][x]
                self.pixels[y][x] = (255 - r, 255 - g, 255 - b)
        self.save(output_file)

    def apply_pixelation(self, pixel_size, output_file):
        """픽셀화."""
        if self.pixels is None:
            print("No image loaded to process.")
            return

        original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
        for y in range(0, self.height, pixel_size):
            for x in range(0, self.width, pixel_size):
                block_colors = []
                for yy in range(y, min(y + pixel_size, self.height)):
                    for xx in range(x, min(x + pixel_size, self.width)):
                        block_colors.append(original_pixels[yy][xx])

                avg_color = tuple(
                    sum(color[i] for color in block_colors) // len(block_colors)
                    for i in range(3)
                )

                for yy in range(y, min(y + pixel_size, self.height)):
                    for xx in range(x, min(x + pixel_size, self.width)):
                        self.pixels[yy][xx] = avg_color
        self.save(output_file)

    def convert_to_24bit(self, input_file, output_file):
        """32비트 BMP 파일을 24비트 BMP로 변환."""
        try:
            image = Image.open(input_file)
            image = image.convert("RGB")
            image.save(output_file, "BMP")
            print(f"Converted {input_file} to 24-bit BMP as {output_file}")
        except Exception as e:
            print(f"Error converting image: {e}")

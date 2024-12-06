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

    def convert_jpg_to_bmp(self, jpg_file, bmp_file):
        """JPG 파일을 24비트 BMP 파일로 변환."""
        try:
            image = Image.open(jpg_file)
            image = image.convert("RGB")  # RGB로 변환 (24비트 BMP 지원)
            image.save(bmp_file, "BMP")
            print(f"Converted {jpg_file} to 24-bit BMP as {bmp_file}")
        except Exception as e:
            print(f"Error converting JPG to BMP: {e}")

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

    def apply_flip_horizontal(self, output_file):
        """이미지를 좌우 반전."""
        if self.pixels is None:
            print("No image loaded to process.")
            return

        try:
            original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
            for y in range(self.height):
                # 행의 픽셀 순서를 반전
                self.pixels[y] = list(reversed(original_pixels[y]))

            # 반전된 이미지를 저장
            self.save(output_file)
            print(f"Image flipped horizontally and saved as: {output_file}")
        except Exception as e:
            print(f"Error flipping image horizontally: {e}")

    def apply_skin_brightness(self, brightness_factor=1.2, soften_intensity=20, output_file="output_brightness.bmp"):
        """
        밝기 증가와 피부 개선 필터
        - brightness_factor: 밝기를 증가시키는 비율 (기본값 1.2)
        - soften_intensity: 부드러움을 추가하는 강도 (기본값 20)
        - output_file: 처리된 이미지를 저장할 파일 경로
        """
        if self.pixels is None:
            print("No image loaded to process.")
            return

        # 원본 픽셀 데이터를 복사
        original_pixels = [row[:] for row in self.pixels]

        for y in range(self.height):
            for x in range(self.width):
                r, g, b = original_pixels[y][x]

                # 밝기 조정
                new_r = min(255, int(r * brightness_factor))
                new_g = min(255, int(g * brightness_factor))
                new_b = min(255, int(b * brightness_factor))

                # 부드러운 효과 추가
                softened_r = min(255, new_r + soften_intensity)
                softened_g = min(255, new_g + soften_intensity)
                softened_b = min(255, new_b + soften_intensity)

                # 결과 픽셀 업데이트
                self.pixels[y][x] = (softened_r, softened_g, softened_b)

        # 결과 이미지를 저장
        self.save(output_file)
        print(f"Skin brightness filter applied and saved to {output_file}")



    def convert_to_24bit(self, input_file, output_file):
        """32비트 BMP 파일을 24비트 BMP로 변환."""
        try:
            image = Image.open(input_file)
            image = image.convert("RGB")
            image.save(output_file, "BMP")
            print(f"Converted {input_file} to 24-bit BMP as {output_file}")
        except Exception as e:
            print(f"Error converting image: {e}")
        
    def apply_neon_filter(self, output_file, intensity=1.5):
        """네온 필터 적용."""
        if self.pixels is None:
            print("No image loaded to process.")
            return

        try:
            original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = original_pixels[y][x]

                    # 네온 효과: 색상을 강조하고 높은 대비를 적용
                    nr = min(255, int((r ** 2 / 255) * intensity))
                    ng = min(255, int((g ** 2 / 255) * intensity))
                    nb = min(255, int((b ** 2 / 255) * intensity))

                    self.pixels[y][x] = (nr, ng, nb)

            self.save(output_file)
            print(f"Neon filter applied and saved as: {output_file}")
        except Exception as e:
            print(f"Error applying neon filter: {e}")
    
    def apply_sepia_tone(self, output_file):
        """세피아 톤 필터 적용."""
        if self.pixels is None:
            print("No image loaded to process.")
            return

        try:
            original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = original_pixels[y][x]
                    # 세피아 톤 계산
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                    # 값이 255를 넘지 않도록 조정
                    tr, tg, tb = min(255, tr), min(255, tg), min(255, tb)

                    self.pixels[y][x] = (tr, tg, tb)

            self.save(output_file)
            print(f"Sepia tone filter applied and saved as: {output_file}")
        except Exception as e:
            print(f"Error applying sepia tone filter: {e}")

    def apply_blur(self, output_file, radius=1):
        """
        블러 필터 적용.
        - radius: 블러 효과의 강도 (1 이상 정수)
        """
        if self.pixels is None:
            print("No image loaded to process.")
            return

        try:
            original_pixels = [row[:] for row in self.pixels]  # 원본 픽셀 복사
            new_pixels = [row[:] for row in self.pixels]  # 변경된 픽셀 저장용

            for y in range(self.height):
                for x in range(self.width):
                    r_sum, g_sum, b_sum = 0, 0, 0
                    count = 0

                    # 주변 픽셀의 평균 계산
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                r, g, b = original_pixels[ny][nx]
                                r_sum += r
                                g_sum += g
                                b_sum += b
                                count += 1

                    # 평균 값으로 현재 픽셀 설정
                    new_pixels[y][x] = (
                        r_sum // count,
                        g_sum // count,
                        b_sum // count,
                    )

            self.pixels = new_pixels
            self.save(output_file)
            print(f"Blur filter applied with radius {radius} and saved as: {output_file}")
        except Exception as e:
            print(f"Error applying blur filter: {e}")

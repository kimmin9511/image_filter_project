import struct
from PIL import Image
import os

class CustomImageProcessor:
    def __init__(self):
        self.width = None
        self.height = None
        self.pixels = None

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
            raise
        except Exception as e:
            print(f"Error loading image: {e}")
            raise

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
            raise

    def convert_jpg_to_bmp(self, jpg_file, bmp_file):
        """JPG 파일을 24비트 BMP 파일로 변환."""
        try:
            image = Image.open(jpg_file)
            image = image.convert("RGB")  # RGB로 변환 (24비트 BMP 지원)
            image.save(bmp_file, "BMP")
            print(f"Converted {jpg_file} to 24-bit BMP as {bmp_file}")
        except Exception as e:
            print(f"Error converting JPG to BMP: {e}")

    def convert_png_to_bmp(self, png_file, bmp_file):
        """
        PNG 파일을 24비트 BMP 파일로 변환.
        """
        try:
            image = Image.open(png_file)
            image = image.convert("RGB")  # RGB로 변환
            image.save(bmp_file, "BMP")
            print(f"Converted {png_file} to 24-bit BMP as {bmp_file}")
        except Exception as e:
          print(f"Error converting PNG to BMP: {e}")

    def auto_convert_to_24bit_bmp(self, input_file, output_file):
        """
        파일 형식을 자동으로 인식하여 24비트 BMP로 변환.
        - input_file: 입력 파일 경로
        - output_file: 출력 파일 경로
        """
        try:
            # 파일 확장자 추출
            _, ext = os.path.splitext(input_file)
            ext = ext.lower()
    
            if ext == ".jpg" or ext == ".jpeg":
                print(f"Detected format: JPG")
                self.convert_jpg_to_bmp(input_file, output_file)
            elif ext == ".png":
                print(f"Detected format: PNG")
                self.convert_png_to_bmp(input_file, output_file)
            elif ext == ".bmp":
                # BMP 파일 확인
                with open(input_file, "rb") as f:
                    f.seek(28)  # BMP의 비트 수 정보 위치로 이동
                    bit_depth = struct.unpack("<H", f.read(2))[0]
                if bit_depth == 32:
                    print(f"Detected format: 32-bit BMP")
                    self.convert_to_24bit(input_file, output_file)
                elif bit_depth == 24:
                    print(f"Detected format: 24-bit BMP (no conversion needed)")
                    os.rename(input_file, output_file)
                else:
                    print(f"Unsupported BMP bit depth: {bit_depth}")
            else:
                print(f"Unsupported file format: {ext}")
        except Exception as e:
            print(f"Error during auto conversion: {e}")




    def apply_grayscale(self, input_file, output_file):
        """흑백 필터."""
        self.load(input_file)
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[y][x]
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                self.pixels[y][x] = (gray, gray, gray)
        self.save(output_file)

    def apply_invert_colors(self, input_file, output_file):
        """색상 반전 필터."""
        self.load(input_file)
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[y][x]
                self.pixels[y][x] = (255 - r, 255 - g, 255 - b)
        self.save(output_file)

    def apply_pixelation(self, input_file, output_file, pixel_size=10):
        """픽셀화 필터."""
        self.load(input_file)
        for y in range(0, self.height, pixel_size):
            for x in range(0, self.width, pixel_size):
                block_colors = []
                for yy in range(y, min(y + pixel_size, self.height)):
                    for xx in range(x, min(x + pixel_size, self.width)):
                        block_colors.append(self.pixels[yy][xx])

                avg_color = tuple(
                    sum(color[i] for color in block_colors) // len(block_colors)
                    for i in range(3)
                )

                for yy in range(y, min(y + pixel_size, self.height)):
                    for xx in range(x, min(x + pixel_size, self.width)):
                        self.pixels[yy][xx] = avg_color
        self.save(output_file)

    def apply_flip_horizontal(self, input_file, output_file):
        """좌우 반전 필터."""
        self.load(input_file)
        for y in range(self.height):
            self.pixels[y] = list(reversed(self.pixels[y]))
        self.save(output_file)
        
    def apply_skin_brightness(self, input_file, output_file, brightness_factor=1.2, soften_intensity=20):
        """
        밝기 증가와 피부 개선 필터.
        - input_file: 입력 파일 경로.
        - output_file: 출력 파일 경로.
        - brightness_factor: 밝기를 증가시키는 비율 (기본값 1.2).
        - soften_intensity: 부드러움을 추가하는 강도 (기본값 20).
        """
        self.load(input_file)  # 이미지를 로드
        try:
            # 원본 픽셀 데이터를 복사
            for y in range(self.height):
                for x in range(self.width):
                    r, g, b = self.pixels[y][x]

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
        except Exception as e:
            print(f"Error applying skin brightness filter: {e}")




    def convert_to_24bit(self, input_file, output_file):
        """32비트 BMP 파일을 24비트 BMP로 변환."""
        try:
            image = Image.open(input_file)
            image = image.convert("RGB")
            image.save(output_file, "BMP")
            print(f"Converted {input_file} to 24-bit BMP as {output_file}")
        except Exception as e:
            print(f"Error converting image: {e}")
        
    def apply_neon_filter(self, input_file, output_file, intensity=1.5):
        """네온 필터."""
        self.load(input_file)
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[y][x]
                nr = min(255, int((r ** 2 / 255) * intensity))
                ng = min(255, int((g ** 2 / 255) * intensity))
                nb = min(255, int((b ** 2 / 255) * intensity))
                self.pixels[y][x] = (nr, ng, nb)
        self.save(output_file)
    
    def apply_sepia_tone(self, input_file, output_file):
        """세피아 톤 필터."""
        self.load(input_file)
        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[y][x]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                self.pixels[y][x] = (min(255, tr), min(255, tg), min(255, tb))
        self.save(output_file)

    def apply_blur(self, input_file, output_file, radius=1):
        """블러 필터."""
        self.load(input_file)
        try:
            original_pixels = [row[:] for row in self.pixels]
            new_pixels = [row[:] for row in self.pixels]

            for y in range(self.height):
                for x in range(self.width):
                    r_sum, g_sum, b_sum = 0, 0, 0
                    count = 0

                    # 주변 픽셀 평균 계산
                    for dy in range(-radius, radius + 1):
                        for dx in range(-radius, radius + 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                r, g, b = original_pixels[ny][nx]
                                r_sum += r
                                g_sum += g
                                b_sum += b
                                count += 1

                    # 평균값으로 현재 픽셀 설정
                    new_pixels[y][x] = (
                        r_sum // count,
                        g_sum // count,
                        b_sum // count,
                    )

            self.pixels = new_pixels
            self.save(output_file)
        except Exception as e:
            print(f"Error applying blur filter: {e}")

    def apply_text_sticker(self, input_file, output_file, user_text="Text Sticker"):
        """
        이미지에서 얼굴을 인식하고 입력된 문자열을 스티커처럼 얼굴에 덮어씌웁니다.
        - input_file: 입력 이미지 파일 경로
        - output_file: 출력 이미지 파일 경로
        - user_text: 얼굴에 추가할 텍스트
        """
        self.load(input_file)

        try:
            from PIL import Image, ImageDraw, ImageFont
            import numpy as np
            import cv2

        # 픽셀 데이터를 numpy 배열로 변환
            image_array = np.array([pixel for row in self.pixels for pixel in row], dtype=np.uint8)
            image_array = image_array.reshape((self.height, self.width, 3))

        # PIL 이미지 생성
            pil_image = Image.fromarray(image_array)

        # OpenCV를 사용하여 얼굴 검출
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # ImageDraw로 텍스트 추가
            draw = ImageDraw.Draw(pil_image)
            try:
                font = ImageFont.truetype("arial.ttf", size=max(10, min(self.width, self.height) // 15))
            except IOError:
                font = ImageFont.load_default()

            for (x, y, w, h) in faces:
                text_bbox = draw.textbbox((0, 0), user_text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # 텍스트 배경 그리기
                draw.rectangle([(x, y), (x + w, y + h)], fill=(0, 0, 0))

                # 텍스트 중앙 배치
                text_x = x + (w - text_width) // 2
                text_y = y + (h - text_height) // 2
                draw.text((text_x, text_y), user_text, font=font, fill=(255, 255, 255))

            # 변환된 이미지를 다시 저장
            pil_image.save(output_file)
            print(f"Text sticker applied and saved to {output_file}")

        except Exception as e:
            print(f"Error applying text sticker: {e}")


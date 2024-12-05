import struct

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
                header = f.read(54)  # BMP 헤더 읽기
                self.width, self.height = struct.unpack("ii", header[18:26])
                print(f"Image loaded: {file_name} ({self.width}x{self.height})")

                # 픽셀 데이터 읽기
                f.seek(54)  # 픽셀 데이터 시작 위치로 이동
                self.pixels = []
                row_padded = (self.width * 3 + 3) & ~3  # BMP는 행 패딩이 필요
                for y in range(self.height):
                    row = []
                    for x in range(self.width):
                        b, g, r = struct.unpack("BBB", f.read(3))  # 픽셀(BGR 순서)
                        row.append((r, g, b))  # RGB 순서로 저장
                    self.pixels.append(row)
                    f.read(row_padded - self.width * 3)  # 패딩 건너뛰기
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
                # BMP 헤더 작성
                row_padded = (self.width * 3 + 3) & ~3
                file_size = 54 + row_padded * self.height
                header = struct.pack(
                    "<2sIHHIIIIHHIIIIII",
                    b"BM",  # 파일 타입
                    file_size,  # 파일 크기
                    0, 0,  # 예약 필드
                    54,  # 픽셀 데이터 시작 위치
                    40,  # DIB 헤더 크기
                    self.width, self.height,  # 너비와 높이
                    1, 24,  # 색상 평면과 비트당 색상
                    0, row_padded * self.height,  # 압축 방식과 이미지 크기
                    2835, 2835,  # 해상도 (픽셀/미터)
                    0, 0  # 색상 팔레트 정보
                )
                f.write(header)

                # 픽셀 데이터 저장
                for row in reversed(self.pixels):  # BMP는 아래에서 위로 저장
                    for r, g, b in row:
                        f.write(struct.pack("BBB", b, g, r))  # BGR 순서로 저장
                    f.write(b"\x00" * (row_padded - self.width * 3))  # 패딩 추가
                print(f"Image saved as: {file_name}")
        except Exception as e:
            print(f"Error saving image: {e}")

    def invert_colors(self):
        """이미지의 색상을 반전."""
        if self.pixels is None:
            print("No image loaded to invert.")
            return

        for y in range(self.height):
            for x in range(self.width):
                r, g, b = self.pixels[y][x]
                self.pixels[y][x] = (255 - r, 255 - g, 255 - b)  # 색상 반전
        print("Colors inverted.")

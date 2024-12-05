from image_filter.custom_image_processor import CustomImageProcessor

# 1. 32비트 BMP를 24비트 BMP로 변환
processor = CustomImageProcessor()
processor.convert_to_24bit("example_32bit.bmp", "example_24bit.bmp")

# 2. 24비트 BMP 로드
processor.load("example_24bit.bmp")

# 3. 흑백 변환
processor.apply_grayscale("example_24bit_grayscale.bmp")

# 4. 색상 반전
processor.load("example_24bit.bmp")  # 원본 다시 로드
processor.apply_invert_colors("example_24bit_inverted.bmp")

# 5. 픽셀화
processor.load("example_24bit.bmp")  # 원본 다시 로드
processor.apply_pixelation(pixel_size=20, output_file="example_24bit_pixelated.bmp")

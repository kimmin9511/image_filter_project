from image_filter.custom_image_processor import CustomImageProcessor

# JPG 파일 경로
jpg_file = "example.jpg"

# 1. JPG 파일을 24비트 BMP로 변환
processor = CustomImageProcessor()
bmp_file = "example_jpg_to_bmp24.bmp"  # 변환된 BMP 파일 이름
processor.convert_jpg_to_bmp(jpg_file, bmp_file)

# 2. 24비트 BMP 로드
processor.load(bmp_file)

# 3. 흑백 변환
processor.apply_grayscale("example_grayscale.bmp")

# 4. 색상 반전
processor.load(bmp_file)
processor.apply_invert_colors("example_inverted.bmp")

# 5. 픽셀화
processor.load(bmp_file)
processor.apply_pixelation(pixel_size=20, output_file="example_pixelated.bmp")

# 6. 좌우반전
processor.load(bmp_file)
processor.apply_flip_horizontal("example_flipped.bmp")


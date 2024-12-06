from image_filter.custom_image_processor import CustomImageProcessor

# 1. 32비트 BMP를 24비트 BMP로 변환
processor = CustomImageProcessor()
processor.convert_to_24bit("32bit_example.bmp", "example_24bit.bmp")

# 2. 24비트 BMP 로드
processor.load("example_24bit.bmp")

# 3. 흑백 변환
processor.apply_grayscale("example_32_to_24_grayscale.bmp")

# 4. 색상 반전
processor.load("example_24bit.bmp")  # 원본 다시 로드
processor.apply_invert_colors("example_32_to_24_inverted.bmp")

# 5. 픽셀화
processor.load("example_24bit.bmp")  # 원본 다시 로드
processor.apply_pixelation(pixel_size=20, output_file="example_32_to_24_pixelated.bmp")

# 6. 좌우반전
processor.load("example_24bit.bmp")  # 원본 다시 로드
processor.apply_flip_horizontal("example_32_to_24_flipped.bmp")

#7. 밝기 올리기
processor.load("example_24bit.bmp")  # 원본 다시 로드
processor.apply_skin_brightness(
    brightness_factor=1.3,  # 밝기 증가 비율
    soften_intensity=25,    # 부드러움 추가 강도
    output_file="example_32_to_24_brightness.bmp"  # 결과 저장 파일
)


processor.load("example_24bit.bmp")
processor.apply_text_sticker("얼간이", "example_24bit_multiple_faces.bmp")

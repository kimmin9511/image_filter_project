from image_filter.custom_image_processor import CustomImageProcessor

# 파일 경로
input_file = input()

# 1. 파일을 24비트 BMP로 변환
processor = CustomImageProcessor()
bmp_file = "example_24bmp.bmp"
processor.auto_convert_to_24bit_bmp(input_file, bmp_file)

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

#7. 밝기 올리기
processor.load(bmp_file)
processor.apply_skin_brightness(
    brightness_factor=1.3,  # 밝기 증가 비율
    soften_intensity=25,    # 부드러움 추가 강도
    output_file="example_brightness.bmp"  # 결과 저장 파일
)

#8. 세피아 필터
processor.load(bmp_file)
processor.apply_sepia_tone("example_sepia.bmp")

#9. 네온 필터
processor.load(bmp_file)
processor.apply_neon_filter("example_neon.bmp", intensity=1.8)

#10. 블러 처리
processor.load(bmp_file)
processor.apply_blur("example_blur.bmp", radius=2)


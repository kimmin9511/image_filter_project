from image_filter.custom_image_processor import CustomImageProcessor

# 파일 경로
input_file = input()

# 1. 파일을 24비트 BMP로 변환
processor = CustomImageProcessor()
bmp_file = "example_24bmp.bmp"
processor.auto_convert_to_24bit_bmp(input_file, bmp_file)

# 2. 흑백 변환
processor.apply_grayscale(bmp_file, "example_grayscale.bmp")

# 3. 색상 반전
processor.apply_invert_colors(bmp_file, "example_inverted.bmp")

# 4. 픽셀화
processor.apply_pixelation(bmp_file, "example_pixelated.bmp", pixel_size=20)

# 5. 좌우반전
processor.apply_flip_horizontal(bmp_file, "example_flipped.bmp")

#6. 밝기 올리기
processor.apply_skin_brightness(
    bmp_file,
    "example_brightness.bmp",  # 결과 저장 파일
    brightness_factor=1.3,  # 밝기 증가 비율
    soften_intensity=25,    # 부드러움 추가 강도
)

#7. 세피아 필터
processor.apply_sepia_tone(bmp_file, "example_sepia.bmp")

#8. 네온 필터
processor.apply_neon_filter(bmp_file,"example_neon.bmp", intensity=1.8)

#9. 블러 처리
processor.apply_blur(bmp_file, "example_blur.bmp", radius=2)

#10. 얼굴 인식
processor.apply_text_sticker(bmp_file, "example_face.bmp", user_text="Hello World")

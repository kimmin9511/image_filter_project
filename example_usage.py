from image_filter.custom_image_processor import CustomImageProcessor

# 이미지 로드
processor = CustomImageProcessor("example.bmp")

# 색상 반전 적용
processor.apply_grayscale()

# 결과 저장
processor.save("inverted_example.bmp")

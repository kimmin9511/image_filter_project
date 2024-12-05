from image_filter import CustomImageProcessor

# 이미지 로드
processor = CustomImageProcessor("example.bmp")

# 색상 반전 적용
processor.invert_colors()

# 결과 저장
processor.save("inverted_example.bmp")

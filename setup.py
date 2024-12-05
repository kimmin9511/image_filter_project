from setuptools import setup, find_packages

setup(
    name="custom_image_processor",  # 패키지 이름
    version="1.0.0",                # 버전
    description="A custom image processing library for BMP files",  # 설명
    author="Your Name",             # 작성자 이름
    author_email="your_email@example.com",  # 작성자 이메일
    url="https://github.com/yourusername/custom_image_processor",  # 저장소 URL
    packages=find_packages(),       # `image_filter` 디렉토리와 하위 모듈 포함
    python_requires=">=3.6",        # Python 3.6 이상 요구
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],  # 추가 라이브러리 필요 없다면 빈 리스트
    long_description=open("README.md").read(),  # 프로젝트 설명 (README.md 읽기)
    long_description_content_type="text/markdown",  # README 파일의 형식 (마크다운)
)


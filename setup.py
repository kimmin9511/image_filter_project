from setuptools import setup, find_packages

setup(
    name="image_filter_library",
    version="1.0.0",
    description="A library for processing BMP images",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/image_filter_project",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["pillow"],
    long_description=open("README.md", encoding="utf-8").read(),  # 인코딩 추가
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)

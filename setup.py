from setuptools import setup, find_packages

setup(
    name="image_filter_library_oss",
    version="1.1.1",
    description="A library for processing BMP images",
    author="kimmin9511",
    author_email="gimm50655@gmail.com",
    url="https://github.com/kimmin9511/image_filter_project",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["pillow",
                      "numpy",
                      "opencv-python",
                      "sphinx",
                      "sphinx-autodoc-typehints"],
    long_description=open("README.md", encoding="utf-8").read(),  # 인코딩 추가
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)

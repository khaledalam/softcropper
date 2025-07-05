
from setuptools import setup, find_packages

setup(
    name="softcropper",
    version="0.1.8",
    url="https://github.com/khaledalam/softcropper",
    project_urls={
        "Source": "https://github.com/khaledalam/softcropper",
        "Tracker": "https://github.com/khaledalam/softcropper/issues",
    },
    packages=find_packages(),
    install_requires=["opencv-python", "numpy"],
    entry_points={
        "console_scripts": [
            "softcropper=softcropper.cli:main",
        ],
    },
    author="Khaled Alam",
    description="Resize and blur-pad photos to square format for photos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

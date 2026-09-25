from setuptools import setup, find_packages

setup(
    name="keyshield",
    version="1.0.0",
    author="Cioponea Alexandru (Shenny)",
    description="Acoustic Keystroke Defense & Neural Voice Gatekeeper",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="Personal-Use License (Cioponea Alexandru)",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "keyshield": ["models/*.onnx"],
    },
    install_requires=[
        "numpy>=1.24.0",
        "onnxruntime>=1.16.0",
        "sounddevice>=0.4.6",
        "PyQt6>=6.5.0",
    ],
    entry_points={
        "console_scripts": [
            "keyshield=keyshield.main:main",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)

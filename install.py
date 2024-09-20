import subprocess

def install_dependencies():
    dependencies = [
        "torch",
        "torchvision",
        "opencv-python-headless",
        "scikit-image",
        "numpy",
        "Pillow"
    ]

    for dep in dependencies:
        subprocess.check_call(["pip", "install", dep])

if __name__ == "__main__":
    install_dependencies()
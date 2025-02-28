import subprocess
import sys

def install_packages():
    packages = ["pandas", "sqlalchemy", "pymysql"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("Instalação concluída.")

if __name__ == "__main__":
    install_packages()

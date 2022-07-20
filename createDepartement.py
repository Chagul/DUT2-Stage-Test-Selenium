import subprocess
from setting import LINK_SCODOC_SERVER, NOM_DPT


def main():
    cmdProcess = ["./scriptCreationDepartement.sh", LINK_SCODOC_SERVER, NOM_DPT]
    process = subprocess.Popen(cmdProcess)
    process.wait()
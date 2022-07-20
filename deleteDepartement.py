import subprocess
from setting import LINK_SCODOC_SERVER, NOM_DPT


def main():
    cmdProcess = ["./scriptDeleteDepartement.sh", LINK_SCODOC_SERVER, NOM_DPT]
    process = subprocess.Popen(cmdProcess)
    process.wait()
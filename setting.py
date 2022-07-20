import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BASE_URL = os.environ.get("BASE_URL")
NOM_DPT = os.environ.get("NOM_DPT")
SCODOC_ADMIN_ID = os.environ.get("SCODOC_ADMIN_ID")
SCODOC_ADMIN_PASS = os.environ.get("SCODOC_ADMIN_PASS")
SCODOC_ENS_ID = os.environ.get("SCODOC_ENS_ID")
SCODOC_ENS_PASS = os.environ.get("SCODOC_ENS_PASS")
SCODOC_CHEF_ID = os.environ.get("SCODOC_CHEF_ID")
SCODOC_CHEF_PASS = os.environ.get("SCODOC_CHEF_PASS")
LINK_SCODOC_SERVER = os.environ.get("LINK_SCODOC_SERVER")
BASE_NOT_SECURED_URL = os.environ.get("BASE_NOT_SECURED_URL")
NAVIGATEUR = os.environ.get("NAVIGATEUR")
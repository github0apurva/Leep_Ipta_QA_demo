
import setuptools


__version__ = "0.0.0"

REPO_NAME = "Leep_Ipta_QA_demo"
AUTHOR_USER_NAME = "github0apurva"
AUTHOR_EMAIL = "apurva.c27@gmail.com"

setuptools.setup(
    name = REPO_NAME,
    version = __version__,
    author = AUTHOR_USER_NAME,
    author_email= AUTHOR_EMAIL,
    description = "A small package for CNN app",
    long_description="A small package for CNN app",
    url = f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls = {"Bug Tracker" : f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
                    },
    package_dir = {"":"src"},
    packages = setuptools.find_packages(where = "src")
)
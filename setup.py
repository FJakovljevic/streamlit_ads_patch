from setuptools import setup
import importlib
import pathlib
import os
from setuptools.command.install import install
from bs4 import BeautifulSoup

# Function to patch Streamlit for ads
def patch_streamlit_for_ads():
    print("Patching streamlit for ads")
    # Loading Streamlit index.html
    streamlit_path = importlib.util.find_spec("streamlit").origin
    index_path = pathlib.Path(streamlit_path).parent / "static" / "index.html"
    with open(index_path, "r") as file:
        html_content = file.read()
    index_html = BeautifulSoup(html_content, "lxml")

    # Creating ads HTML
    ads_html = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9139235018955761" crossorigin="anonymous"></script>"""
    ads_tag = BeautifulSoup(ads_html, "html.parser")

    # If tag doesn't exist, add it to the header and save the file
    if not index_html.find("script", src=ads_tag.script.get("src")):
        index_html.head.append(ads_tag)
        index_html_with_ads = index_html.prettify()
        
        os.chmod(index_path, 0o644)
        index_path.write_text(index_html_with_ads)
        print("Streamlit patched successfully.")
    else:
        print("Ads script already exists in Streamlit index.html.")

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        patch_streamlit_for_ads()

setup(
    name="streamlit_ads",
    version="0.1",
    packages=["streamlit_ads"],
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "streamlit"
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)

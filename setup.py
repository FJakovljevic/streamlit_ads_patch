from setuptools import setup
import importlib
import pathlib
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
    script_tag = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9139235018955761" crossorigin="anonymous"></script>"""
    script_tag = BeautifulSoup(ads_html, "html.parser")
    meta_tag = """<meta name="google-adsense-account" content="ca-pub-9139235018955761">"""
    meta_tag = BeautifulSoup(ads_html, "html.parser")

    # adding tags to the header and save the file
    index_html.head.append(script_tag)
    index_html.head.append(meta_tag)
    index_html_with_ads = index_html.prettify()
    index_path.write_text(index_html_with_ads)
    
    print("Streamlit patched successfully.")

class CustomInstallCommand(install):
    def run(self):
        print("Installing streamlit_ads_patch")
        install.run(self)
        patch_streamlit_for_ads()

setup(
    name="streamlit_ads_patch",
    version="0.1",
    packages=["streamlit_ads_patch"],
    install_requires=[
        "beautifulsoup4",
        "lxml",
        "streamlit"
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
)

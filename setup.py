from setuptools import setup

setup(
  name="tenis",
  version="0.0.1",
  packages=["tenis"],
  entry_points={
    "console_scripts": [
      "tenis = tenis.__main__:main"
    ],
  },
  install_requires=["pygame"]
)
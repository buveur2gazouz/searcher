from setuptools import setup

setup(
    name="multi-tools-by-ys",
    version="3.0",
    py_modules=["multi_tools"],
    install_requires=[
        "requests",
        "phonenumbers",
        "dnspython",
    ],
)

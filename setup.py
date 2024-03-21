"""
Setup script for the src Genta Customer Service folder
"""

from setuptools import setup, find_packages

setup(
    name="genta_customer_service",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
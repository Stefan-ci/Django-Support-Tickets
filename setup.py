import os, django_support_tickets
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-support-tickets",
    version=django_support_tickets.__version__,
    description="More advanced reusable django application providing a generic support ticket system.",
    long_description=read("README.md"),
    license="MIT License",
    author="Stéphane Claver DIBY",
    author_email="s.diby@waliye.com",
    url="https://github.com/Stefan-ci/Django-Support-Tickets",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django",
    ],
    keywords = ["support", "ticket", "django-ticket", "django-support-tickets"],
    classifiers = [
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

setuptools.setup(
    name="mailog",
    version="0.1.1",
    author="Hive Solutions Lda.",
    author_email="development@hive.pt",
    description="SMTP relay activity dashboard",
    license="Apache License, Version 2.0",
    keywords="smtp relay activity dashboard admin",
    url="http://mailog.bemisc.com",
    zip_safe=False,
    packages=[
        "mailog",
        "mailog.controllers",
        "mailog.controllers.api",
        "mailog.controllers.web",
        "mailog.models",
    ],
    package_dir={"": os.path.normpath("src")},
    package_data={"mailog": ["templates/*.tpl"]},
    install_requires=["appier", "appier-extras"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
)

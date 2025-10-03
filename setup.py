from setuptools import setup, find_packages

setup(
    name="taskmaster",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PyQt6>=6.4.0',
        'qtawesome>=1.3.1',
        'matplotlib>=3.7.0',
        'pandas>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'taskmaster=taskmaster.main:main',
        ],
    },
    author="evilshxt",
    author_email="",
    description="A modern, offline-first task and productivity manager",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/evilshxt/taskmaster",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)

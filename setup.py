from setuptools import setup, find_packages


extras_require = {
    "astropy": ["astropy"],
    "tests": ["pytest"],
}

extras_require["all"] = list({
    dep for extra in extras_require.values()
    for dep in extra
})

setup(
    name="config",
    packages=find_packages(),
    python_requires=">=3.6",
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
    ],
    zip_safe=False,
)

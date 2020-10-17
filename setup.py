from setuptools import setup, find_packages


tests_require = [
    "pytest",
]
extras_require = {
    "astropy": ["astropy"],
}

extras_require["all"] = list({
    dep for extra in extras_require.values()
    for dep in extra
})

setup(
    name="config",
    packages=find_packages(),
    version='0.1.0.dev1',
    python_requires=">=3.6",
    extras_require=extras_require,
    tests_require=tests_require,
    setup_requires=["pytest_runner"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
    ],
    zip_safe=False,
)

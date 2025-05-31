from setuptools import setup, find_packages

setup(
    name="multi_agent_ai_router",
    version="0.1.0",
    description="Multi-Agent AI Document Router: Classifies, routes, and processes business documents with memory and logging.",
    author="Sujal Kamble",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "torch",
        "pdfplumber",
        "pydantic",
        "redis",
        "email-validator",
        "fastapi",
        "uvicorn"
    ],
    entry_points={
        "console_scripts": [
            "ai-router=cli:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.10"
)

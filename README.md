# Aws Ecs FastAPI Service Template


## Requirements

- AWS CDK
- AWS cli
- AWS User with permissions
- Docker / Docker-compose
- Python3.7


## Initial setup

### Deploy Cloudformation stack using CDK (initial setup only)
- The `ServiceStack` creates the following resources:
    - ECR Repository (empty)
    - SQS Queue and Dead-Letter-Queue
    - CloudWatch Alarm
    - ECS Task Definition (with QUEUE_NAME as environment variable)
    - ECS Service, with AutoScalling
    - Task Definition and Task role and policies
    - Log Group


## Using `pre-commit`, `black` and `flake8` for style and consistency

- Downlaod config files`

    ```bash
    wget https://s3.amazonaws.com/lexter.nlp.public/python_style_guide_files.zip
    unzip python_style_guide_files.zip
    rm python_style_guide_files.zip
    ```

    - This zip file contains the following files:
        - `.pre-commit-config.yaml`
        - `pylintrc`
        - `pyproject.toml`
        - `setup.cfg`

- Install and configure packages

    - Don't forget to source your virtualenv `venv`

        ```bash
        pip install black flake8 pylint pre-commit
        pre-commit install
        pre-commit install --hook-type commit-msg
        pre-commit autoupdate
        ```

- Using `pre-commit`

    - Once installed, pre-commit works automatically in every commit you make.

    - If you forgot to run black and flake8 and there are inconsistencies, it will remind you

    - Also, it enforces a standard way to write commit messages.

    - To run it:

        ```bash
        pre-commit run --all-files

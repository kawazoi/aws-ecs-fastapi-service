![](https://github.com/kawazoi/aws-ecs-fastapi-service/workflows/CI/badge.svg?branch=staging&event=push)

# Aws Ecs FastAPI Service Template

A template to create python microservies with:

- CI/CD using Github Actions:
    - Built, Test and Release workflow:
        - requirements [caching](https://github.com/actions/cache/blob/main/examples.md#python---pip)
        - testing with [pytest](https://docs.pytest.org/en/stable/)
        - coverage report uploaded as [artifact](https://github.com/actions/upload-artifact)
        - coverage report uploaded to [codecov](https://docs.codecov.io/docs/python)
        - [semantic-release](https://github.com/semantic-release/semantic-release)
        - build and deploy docker image to AWS ECR Staging and Production
        - deploy to AWS ECS Cluster Staging and Production
        - notifications on relases via [slack](https://api.slack.com/apps)
        - notifications on issues
    - Lint workflow:
        - [black](https://github.com/psf/black) formatter
        - [flake8](https://flake8.pycqa.org/en/latest/) linter

- [pre-commit](https://pre-commit.com/) with:
    - [bandit](https://github.com/PyCQA/bandit) security linter
    - [black](https://github.com/ambv/black) formatter
    - [commitizen](https://github.com/commitizen-tools/commitizen)
    - [flake8](https://gitlab.com/pycqa/flake8) linter
    - [isort](https://github.com/PyCQA/isort) to sort imports
    - [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
    - [pylint](https://github.com/PyCQA/pylint) linter


## How to create your own microservice using this template

1. Create Github Repository
    Repository template: `lexter-ai/nlp-template-aws-ecs-fastapi-service`
    Repository name: `your-api`
    Description: `Your service description.`

    After creating your repository, don't forget to add `Topics` to help organize your packages:
    - `api`
    - `nlp` (if applicable)

2. Clone the repository

3. Follow the [tutorial](./docs/TUTORIAL_RUNNING_LOCALLY.md) to check if the microservice is working.

    Great! Your package is running locally

4. Create and push `develop` branch

    ```bash
    git checkout -b develop
    git push --set-upstream origin develop
    ```

5. Invite `lexter-nlp` Team to project (When ready)

6. Configure Branches protection rules:

    - Branches `develop` and `master`
    - Check boxes:
        - `Require pull request reviews before merging`
            - `Dismiss stale pull request approvals when new commits are pushed`
            - `Require review from Code Owners`
            - `Restrict who can dismiss pull request reviews`: default
        - `Require status checks to pass before merging`
            - `Require branches to be up to date before merging`
                - `ci (x.x)`
                - `lint`


7. Now you can edit the names in the entire folder to match your package

    Hint1: If you use VSCode, use `Ctrl + Shift + F` to search and substitute the following expressions:

    - `nlp-template-package`
    - `my_package`
    - `my_module`
    - `my_submodule`

    Also, you can use `Ctrl + P` to search and edit file names.

8. Set up CodeCov to centralize Tests Coverage:

    - Go to https://codecov.io/gh/lexter-ai and `Add new repository`

    - Choose your repository
        - If needed, update list with `Sync team repository list`

    - Add the CODECOV_TOKEN to your Github repository Secrets
        - Github repo > Settings > Secrets > Add secret
        - `CODECOV_TOKEN`

9. Install virtualenv and configure `pre-commit`

    Make sure you are in the base project folder with no env activated
    ```
    cd ..
    deactivate
    ```

    Create your project `venv` with `pre-commit`
    ```bash
    virtualenv --python=python3.7 venv
    source venv/bin/activate
    python setup.py install
    pip install black flake8 pylint pre-commit
    pre-commit install
    pre-commit install --hook-type commit-msg
    pre-commit autoupdate
    ```

10. Use `pre-commit`

    - Once installed, pre-commit works automatically in every commit you make.

    - If you forgot to run black and flake8 and there are inconsistencies, it will remind you

    - Also, it enforces a standard way to write commit messages.

    - To run it:

        ```bash
        pre-commit run --all-files
        ```

11. Create your first_commit branch, add make your first commit

    ```bash
    git checkout -b first_commit
    git add .
    git commit -m "fix: my first commit"
    git push --set-upstream origin first_commit
    ```

12. Your tests should start now.

13. Then, go to Github and open a pull request `first_commit` to `develop`

14. After those tests are completed, merge the PR and open a new pull request from `develop` to `master`

15. Finally, merge this last PR to `master`. This last step should trigger a release process and a message to Slack!


## How to make pull requests to this project

1. Install virtualenv and configure `pre-commit`

    ```bash
    virtualenv --python=python3.7 venv
    source venv/bin/activate
    python setup.py install
    pre-commit install
    pre-commit install --hook-type commit-msg
    ```

2. Create new branch

    ```
    git branch -b my_branch_name
    ```

3. Push changes and create pull request to branch `develop` (no direct pushes to `master`)

    ```
    git add ...
    git commit -m "..."
    git push --set-upstream origin my_branch_name
    ```


## How to install and use the package

1. Create and activate virtualenv

    ```bash
    cd tutorial/
    virtualenv --python=python3.7 venv
    source venv/bin/activate
    ```

2. Install using pip - latest version

    Latest stable version:

    ```bash
    pip install git+ssh://git@github.com/lexter-ai/nlp-template-package.git
    ```

    Specific version:

    ```bash
    pip install git+ssh://git@github.com/lexter-ai/nlp-template-package.git@v1.0.0
    ```

    Building from source:

    ```bash
    git clone git@github.com:lexter-ai/nlp-template-package.git
    cd my_package
    python setup.py install
    ```


## Coverage report

- https://codecov.io/gh/lexter-ai/nlp-template-package


----------------------------------------------------------------
_This repository is heavilly inspired by this [course](https://www.udemy.com/course/github-actions/)_

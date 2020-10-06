# Tutorial - How to run this microservice locally

## Initial setup

0. Go to the root of your project

1. Create and activate virtualenv

    ```bash
    virtualenv --python=python3.7 venv
    source venv/bin/activate
    ```

2. Install requirements

    ```bash
    pip install -r requirements.txt
    ```

3. Create and edit `.env` file

    ```bash
    cp .env.example .env
    code .env
    ```

4. Set current path as PYTHONPATH and run app:

    ```bash
    export PYTHONPATH=$PWD
    python src/main.py
    ```

5. Check if the endpoint is running

    - healthcheck

        http://0.0.0.0:$API_PORT/

    - docs

        http://0.0.0.0:$API_PORT/docs


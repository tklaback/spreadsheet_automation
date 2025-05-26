# Devcontainer & AWS SAM Local Setup Guide

## Opening the Project in Devcontainer

Once the repository is pulled:

1. Open the project in **VS Code**.
2. VS Code will detect the `.devcontainer` folder.
3. Click **“Reopen in Container”** when prompted.

---

## Testing Using `aws-sam-cli` Locally

> **Note**: Ensure [`aws-sam-cli`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) is installed **on your local machine**, not inside the devcontainer.

Running `sam local invoke <function>` doesn't work directly from inside the devcontainer, since SAM itself spins up its own Docker containers. Instead:

1. **Return to your local machine (outside the devcontainer)**.
2. Create a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies into the Lambda layer directory:

    ```bash
    pip install -r requirements.txt -t ./layers/dependencies/python
    ```

4. Invoke the function using:

    ```bash
    DOCKER_HOST=unix://$HOME/.docker/run/docker.sock sam local invoke <function-name>
    ```

> 💡 **Tip**: VS Code's **AWS Toolkit Extension** allows setting breakpoints for Lambda functions when debugging.

---

## Dependency Management

- The `pyproject.toml` file is the **source of truth** for dependencies.
- The `requirements.txt` file is a **generated artifact** used for:
  - **Local testing** with AWS SAM CLI
  - **Deploying** to AWS Lambda layers

> ❗ `requirements.txt` does **not** support dev-dependencies, which is why `pyproject.toml` is preferred for full development configuration.

---

## Running Tests

To run tests:

```bash
python3 -m pytest
```


## How to get account_id and location_id:

- GET this endpoint  
  `https://mybusinessbusinessinformation.googleapis.com/v1/accounts`  
  ^^ then copy the number (i.e. `12345`) from the response: (i.e. `account/12345`)

- Then get the location id(s):  
  `https://mybusinessbusinessinformation.googleapis.com/v1/accounts/<account_number_from_above>/locations?readMask=name`

- Then, finally:  
  `https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/reviews`

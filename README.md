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


## 1. Service Account Setup

1. In the Google Cloud Console, go to **APIs & Services → Credentials**.
2. If you don’t already have one, **Create a Service Account**:
   - Click **+ CREATE CREDENTIALS → Service account**.
   - Give it a name and (optionally) a description.
3. Under the **Keys** tab of your new service account, click **ADD KEY → Create new key**, choose **JSON**, and download the file.
4. In your target Google Sheet, share it with the service account’s **client_email** (found in the downloaded JSON).

---

## 2. Required Environment Variables

Set the following environment variables before running the tool:

| Variable                     | Description                                                                                                                                           |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `CLIENT_ID`                  | OAuth 2.0 **Client ID** from **APIs & Services → Credentials** in GCP.                                                                               |
| `CLIENT_SECRET`              | OAuth 2.0 **Client Secret** (from the same credentials page).                                                                                         |
| `SHEET_ID`                   | The ID of your Google Sheet (the long identifier in the sheet’s URL).                                                                                 |
| `SHEET_NAME`                 | The sheet tab and range where reviews will be written, e.g.:<br>```Sheet1!A2```                                                                         |
| `REFRESH_TOKEN`              | A long-lived OAuth token to authorize the Sheets API. See steps below to generate.                                                                    |
| `GOOGLE_CREDENTIALS_BASE64`  | Base64-encoded JSON key for your service account.                                                                                                     |

---

### 2.1. Generating the `REFRESH_TOKEN`

1. Open the [OAuth 2.0 Playground](https://developers.google.com/oauthplayground).
2. Click the **⚙️ (settings)** icon in the top-right, enable **Use your own OAuth credentials**, and paste in your `CLIENT_ID` and `CLIENT_SECRET`.
3. In the left panel under **Select & authorize APIs**, enter: `https://www.googleapis.com/auth/business.manage` then click **Authorize APIs**.
4. Choose the Google account that has access to your GCP project.
- If you get an “unauthorized” error, add your email as a **test user** under **APIs & Services → OAuth consent screen** in GCP.
5. Click **Exchange authorization code for tokens**, then copy the **Refresh Token** value and set it as the `REFRESH_TOKEN` env var.

---

### 2.2. Generating `GOOGLE_CREDENTIALS_BASE64`

1. Locate the JSON key file you downloaded when creating the service account.
2. In your terminal, run:
```bash
base64 -i /path/to/your-service-account.json
```
3. Copy the base64‐encoded output and set it as the GOOGLE_CREDENTIALS_BASE64 env var.

### 3. Example .env File
```bash
CLIENT_ID=123456789012-abcdefg.apps.googleusercontent.com
CLIENT_SECRET=ABCdEFGhIJKlMnOpQrStUv
SHEET_ID=1A2b3C4d5E6f7G8h9I0jKlmNoPqRsTuV
SHEET_NAME=Sheet1!A2
REFRESH_TOKEN=1//04iI0f-EXAMPLE_REFRESHTOKEN_HERE
GOOGLE_CREDENTIALS_BASE64=ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgImNkciI6ICIxMjM0NTY3ODkw...
```

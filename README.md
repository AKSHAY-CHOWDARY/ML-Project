# Student Exam Performance Prediction

This project trains a machine-learning model to predict a student's **maths score** from demographic information, lunch type, test-preparation status, and reading and writing scores. A Flask web application provides the prediction form.

## Run locally

### Requirements

- Python 3.11 (the version used by the Docker image)
- Git

### Setup and start

Run these commands in PowerShell, Command Prompt, or a VS Code terminal:

```powershell
git clone https://github.com/AKSHAY-CHOWDARY/ML-Project.git
cd ML-Project
code .
```

There is no `MLproject` file in this repository; open the cloned `ML-Project` folder in VS Code.

Create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Generate the training artifacts by running data ingestion from the repository root:

```powershell
python src/components/data_ingestion.py
```

This reads `notebook/data/stud.csv`, creates train/test data, runs the transformation and training steps, and writes model artifacts under `artifacts/`.

Start the Flask application:

```powershell
python application.py
```

Open [http://127.0.0.1:8080/predictdata](http://127.0.0.1:8080/predictdata), choose the input values, and submit the form to predict the maths score. The application also serves its landing page at [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

Stop the local server with `Ctrl+C`.

## Deploy to AWS

The GitHub Actions workflow in `.github/workflows/main.yaml` builds a Docker image, pushes it to Amazon ECR, and then deploys it to a self-hosted runner. The deployment job runs the container with port `8080` exposed.

### Before configuring GitHub

1. Create an ECR repository in the AWS account and region you will use.
2. Set up a Linux EC2 instance as a GitHub Actions **self-hosted runner** for this repository. It must be online when the workflow reaches the deployment job and have Docker installed and usable by the runner.
3. Ensure the instance's network rules allow access to the application on port `8080` from the clients that need it.
4. Create AWS credentials with the permissions needed to authenticate, push and pull images in the target ECR repository, and run the deployment commands. Use least-privilege permissions.

### Add repository secrets

In GitHub, open **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret name | Value |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | Access key ID for the AWS IAM identity used by the workflow |
| `AWS_SECRET_ACCESS_KEY` | Secret access key for that identity |
| `AWS_REGION` | AWS region containing the ECR repository, such as `us-east-1` |
| `ECR_REPOSITORY_NAME` | Name of the existing ECR repository (not its full URI) |
| `AWS_ECR_LOGIN_URI` | ECR registry URI, if needed for other workflow configuration |

**Note:** The current workflow does not read `AWS_ECR_LOGIN_URI`; it obtains the registry URI from the Amazon ECR login action. The four other listed secrets are referenced by the workflow. Never put AWS credentials in the repository source code or commit them.

### Trigger and access the deployment

The workflow runs on pushes to the `main` branch, except for changes limited to `README.md`. After a successful deployment, access the EC2 instance using its reachable host name or IP on port `8080`, for example `http://<EC2-host-or-IP>:8080/predictdata`. Configure DNS and HTTPS separately if needed.

The current integration job contains placeholder lint and test commands; it prints status messages but does not run an actual linter or test suite.

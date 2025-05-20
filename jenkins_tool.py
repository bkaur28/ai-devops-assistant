from langchain.tools import BaseTool
from typing import Optional
import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

class JenkinsPipelineStatusTool(BaseTool):
    name: str = "jenkins_pipeline_status"
    description: str = "Get the status of the latest Jenkins pipeline build."

    def _run(self, pipeline_name: str) -> str:
        jenkins_url = os.getenv("JENKINS_URL")
        user = os.getenv("JENKINS_USER")
        token = os.getenv("JENKINS_TOKEN")

        if not jenkins_url or not user or not token:
            return "Missing Jenkins environment variables."

        api_url = f"{jenkins_url}/job/{pipeline_name}/lastBuild/api/json"

        try:
            response = requests.get(api_url, auth=HTTPBasicAuth(user, token))
            response.raise_for_status()
            data = response.json()
            status = data.get("result")
            if status is None:
                status = "IN PROGRESS"
            return f"The latest build status of '{pipeline_name}' is: {status}"
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except Exception as e:
            return f"Error getting Jenkins status: {str(e)}"

    async def _arun(self, pipeline_name: str) -> str:
        # Keep it simple fallback to sync version
        return self._run(pipeline_name)
JENKINS_URL = os.getenv("JENKINS_URL")
USERNAME = os.getenv("JENKINS_USER")
API_TOKEN = os.getenv("JENKINS_TOKEN")
JOB_NAME = "ai-devops-pipeline"  # Or parametrize if needed

def get_last_build_status():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    response.raise_for_status()
    return response.json().get("result")

def trigger_jenkins_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    response.raise_for_status()
    return "Build triggered"
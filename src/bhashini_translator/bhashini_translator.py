import requests, os
import json
from .config import ulcaEndPoint
from .payloads import Payloads


class Bhashini(Payloads):
    ulcaUserId: str
    ulcaApiKey: str
    sourceLanguage: str
    targetLanguage: str
    pipeLineData: dict
    pipeLineId: str
    ulcaEndPoint: str

    def __init__(self, sourceLanguage=None, targetLanguage=None) -> None:
        self.ulcaUserId = os.environ.get("userID")
        self.ulcaApiKey = os.environ.get("ulcaApiKey")
        self.pipeLineId = os.environ.get("DefaultPipeLineId")
        self.ulcaEndPoint = ulcaEndPoint
        if not self.ulcaUserId or not self.ulcaApiKey:
            raise ("Invalid Credentials!")
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage

    def translate(self, text) -> json:
        self.nmt_payload()

        if not self.pipeLineData:
            raise "Pipe Line data is not available"

        callbackUrl = self.pipeLineData.get("pipelineInferenceAPIEndPoint").get(
            "callbackUrl"
        )
        inferenceApiKey = (
            self.pipeLineData.get("pipelineInferenceAPIEndPoint")
            .get("inferenceApiKey")
            .get("value")
        )
        serviceId = (
            self.pipeLineData.get("pipelineResponseConfig")[0]
            .get("config")[0]
            .get("serviceId")
        )

        headers = {
            "Authorization": inferenceApiKey,
            "Content-Type": "application/json",
        }
        requestPayload = json.dumps(
            {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": self.sourceLanguage,
                                "targetLanguage": self.targetLanguage,
                            },
                            "serviceId": serviceId,
                        },
                    },
                ],
                "inputData": {"input": [{"source": text}]},
            }
        )
        try:
            response = requests.post(callbackUrl, data=requestPayload, headers=headers)
        except Exception as e:
            raise e
        return response.json().get("pipelineResponse")[0]["output"][0]["target"]

    def getTTSPipeLine(self) -> None:
        requestPayload = self.tts_payload()
        headers = {
            "ulcaApiKey": self.ulcaApiKey,
            "userID": self.ulcaUserId,
            "Content-Type": "application/json",
        }
        response = requests.post(
            ulcaEndPoint,
            data=requestPayload,
            headers=headers,
        )

        self.pipeLineData = response.json()

    def tts(self, text) -> str:
        self.getTTSPipeLine()

        if not self.pipeLineData:
            raise "Pipe Line data is not available"

        callbackUrl = self.pipeLineData.get("pipelineInferenceAPIEndPoint").get(
            "callbackUrl"
        )
        inferenceApiKey = (
            self.pipeLineData.get("pipelineInferenceAPIEndPoint")
            .get("inferenceApiKey")
            .get("value")
        )
        serviceId = (
            self.pipeLineData.get("pipelineResponseConfig")[0]
            .get("config")[0]
            .get("serviceId")
        )

        headers = {
            "Authorization": inferenceApiKey,
            "Content-Type": "application/json",
        }

        requestPayload = json.dumps(
            {
                "pipelineTasks": [
                    {
                        "taskType": "tts",
                        "config": {
                            "language": {
                                "sourceLanguage": self.sourceLanguage,
                            },
                            "serviceId": serviceId,
                            "gender": "female",
                        },
                    },
                ],
                "inputData": {
                    "input": [{"source": text}],
                    "audio": [{"audioContent": None}],
                },
            }
        )

        try:
            response = requests.post(callbackUrl, data=requestPayload, headers=headers)
        except Exception as e:
            raise e

        if response.status_code != 200:
            raise "TTS Callback failed!"

        return response.json()["pipelineResponse"][0]["audio"][0]["audioContent"]

    def asr_nmt(self, base64String: str) -> json:
        """Automatic Speech recongnition, translation and conversion to text."""
        """Multi-lingual speech to text conversion happens here."""
        requestPayload = self.asr_nmt_payload(base64String)

        if not self.pipeLineData:
            raise "Pipe Line data is not available"

        callbackUrl = self.pipeLineData.get("pipelineInferenceAPIEndPoint").get(
            "callbackUrl"
        )

        inferenceApiKey = (
            self.pipeLineData.get("pipelineInferenceAPIEndPoint")
            .get("inferenceApiKey")
            .get("value")
        )

        headers = {
            "Authorization": inferenceApiKey,
            "Content-Type": "application/json",
        }
        response = requests.post(
            callbackUrl,
            data=requestPayload,
            headers=headers,
        )

        if response.status_code != 200:
            raise ValueError("Something went wrong!")

        return response.json().get("pipelineResponse")[1].get("output")[0].get("target")

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
        if not self.pipeLineId:
            self.pipeLineId = "64392f96daac500b55c543cd"
        self.ulcaEndPoint = ulcaEndPoint
        if not self.ulcaUserId or not self.ulcaApiKey:
            raise ValueError("Invalid Credentials!")
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage

    def translate(self, text) -> json:
        requestPayload = self.nmt_payload(text)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[0].get("output")[0].get("target")
        )

    def tts(self, text) -> str:
        requestPayload = self.tts_payload(text)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[0]
            .get("audio")[0]
            .get("audioContent")
        )

    def asr_nmt(self, base64String: str) -> json:
        """Automatic Speech recongnition, translation and conversion to text."""
        """Multi-lingual speech to text conversion happens here."""
        requestPayload = self.asr_nmt_payload(base64String)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[1].get("output")[0].get("target")
        )

    def asr(self, base64String: str) -> json:
        """Automatic Speech recongnition and conversion to text."""
        """Multi-lingual speech to text conversion happens here."""
        requestPayload = self.asr_payload(base64String)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[0].get("output")[0].get("source")
        )

    def compute_response(self, requestPayload: json) -> json:
        if not self.pipeLineData:
            raise ValueError("Intitialize pipe line data first!")

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

        try:
            response = requests.post(callbackUrl, data=requestPayload, headers=headers)
        except Exception as e:
            raise e

        if response.status_code != 200:
            raise ValueError("Something went wrong")
        return response.json()

import requests, os
import json
from bhashini_translator.config import ulcaEndPoint
from bhashini_translator.payloads import Payloads


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
        """
        TTS (Text-to-Speech) - generates speech from text.
        Generates speech from text in a specific source language.
        """
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
        """
        ASR-NMT (Automatic Speech Recognition - Neural Machine Translation)
        Automatic Speech recongnition, translation and conversion to text.
        Performs ASR and NMT on the audio data (base64) and translates it to the target language.
        """
        requestPayload = self.asr_nmt_payload(base64String)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[1].get("output")[0].get("target")
        )

    def asr(self, base64String: str) -> json:
        """Automatic Speech recognition for processing audio data."""
        """Sends audio data (base64) to the server for speech recognition."""
        requestPayload = self.asr_payload(base64String)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[0].get("output")[0].get("source")
        )

    def nmt_tts(self, text: str) -> str:
        # TODO: Fix use of 'gender' in pipeline
        requestPayload = self.nmt_tts_payload(text)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[1]
            .get("audio")[0]
            .get("audioContent")
        )

    def asr_nmt_tts(self, base64String: str) -> str:
        requestPayload = self.asr_nmt_tts_payload(base64String)

        if not self.pipeLineData:
            raise ValueError("Pipe Line data is not available")

        pipelineResponse = self.compute_response(requestPayload)
        return (
            pipelineResponse.get("pipelineResponse")[2]
            .get("audio")[0]
            .get("audioContent")
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

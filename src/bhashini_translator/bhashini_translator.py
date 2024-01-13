import requests, os
import json
import base64


class Bhashini:
    ulcaUserId: str
    ulcaApiKey: str
    sourceLanguage: str
    targetLanguage: str
    pipeLineData: dict
    pipeLineId: str

    def __init__(self, sourceLanguage=None, targetLanguage=None) -> None:
        self.ulcaUserId = os.environ.get("userID")
        self.ulcaApiKey = os.environ.get("ulcaApiKey")
        self.pipeLineId = os.environ.get("DefaultPipeLineId")
        if not self.ulcaUserId or not self.ulcaApiKey:
            raise ("Invalid Credentials!")
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage

    def getTranslatorPipeLine(self) -> None:
        ulcaEndPoint = (
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        )
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
                        },
                    },
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
            }
        )
        response = requests.post(
            ulcaEndPoint,
            data=requestPayload,
            headers={
                "ulcaApiKey": self.ulcaApiKey,
                "userID": self.ulcaUserId,
                "Content-Type": "application/json",
            },
        )

        self.pipeLineData = response.json()

    def translate(self, text) -> json:
        self.getTranslatorPipeLine()

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
        ulcaEndPoint = (
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        )
        requestPayload = json.dumps(
            {
                "pipelineTasks": [
                    {
                        "taskType": "tts",
                        "config": {"language": {"sourceLanguage": self.sourceLanguage}},
                    },
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
            }
        )
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

    def tts(self, text):
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

        b4audio = response.json()["pipelineResponse"][0]["audio"][0]["audioContent"]
        decodedData = base64.b64decode(b4audio)
        wav_file = "/tmp/tts.wav"
        with open(wav_file, "wb") as wavFh:
            wavFh.write(decodedData)

        return wav_file

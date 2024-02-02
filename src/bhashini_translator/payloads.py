import json
from bhashini_translator.pipeline_config import PipelineConfig


class Payloads(PipelineConfig):
    def nmt_payload(self, text: str) -> json:
        return json.dumps(
            {
                "pipelineTasks": [
                    self.getPipeLineConfig("translation"),
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
                "inputData": {"input": [{"source": text}]},
            }
        )

    def tts_payload(self, text: str) -> json:
        return json.dumps(
            {
                "pipelineTasks": [self.getPipeLineConfig("tts")],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
                "inputData": {"input": [{"source": text}]},
            }
        )

    def asr_nmt_payload(self, base64String) -> json:
        payload = {
            "pipelineTasks": [
                self.getPipeLineConfig("asr"),
                self.getPipeLineConfig("translation"),
            ],
            "pipelineRequestConfig": {
                "pipelineId": self.pipeLineId,
            },
            "inputData": {"audio": [{"audioContent": base64String}]},
        }
        return json.dumps(payload)

    def asr_payload(self, base64String) -> json:
        payload = {
            "pipelineTasks": [
                self.getPipeLineConfig("asr"),
            ],
            "pipelineRequestConfig": {
                "pipelineId": self.pipeLineId,
            },
            "inputData": {"audio": [{"audioContent": base64String}]},
        }
        return json.dumps(payload)

    def nmt_tts_payload(self, text: str) -> json:
        return json.dumps(
            {
                "pipelineTasks": [
                    self.getPipeLineConfig("translation"),
                    self.getPipeLineConfig("tts"),
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
                "inputData": {"input": [{"source": text}]},
            }
        )

    def asr_nmt_tts_payload(self, base64String: str) -> json:
        return json.dumps(
            {
                "pipelineTasks": [
                    self.getPipeLineConfig("asr"),
                    self.getPipeLineConfig("translation"),
                    self.getPipeLineConfig("tts"),
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
                "inputData": {"audio": [{"audioContent": base64String}]},
            }
        )

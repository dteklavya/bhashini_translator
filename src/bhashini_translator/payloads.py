import json
from .pipeline_config import PipelineConfig


class Payloads(PipelineConfig):
    def nmt_payload(self) -> json:
        return json.dumps(
            {
                "pipelineTasks": [
                    self.getPipeLineConfig("translation"),
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
            }
        )

    def tts_payload(self) -> json:
        return json.dumps(
            {
                "pipelineTasks": [self.getPipeLineConfig("tts")],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
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

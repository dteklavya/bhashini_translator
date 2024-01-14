import json
from .pipeline_config import PipelineConfig


class Payloads(PipelineConfig):
    def nmt_payload(self) -> json:
        return json.dumps(
            {
                "pipelineTasks": [
                    self.getTaskTypeConfig("translation"),
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
            }
        )

    def tts_payload(self) -> json:
        return json.dumps(
            {
                "pipelineTasks": [self.getTaskTypeConfig("tts")],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
            }
        )

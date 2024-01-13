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

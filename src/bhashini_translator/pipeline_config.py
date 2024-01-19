import requests
import json


class PipelineConfig:
    def getTaskTypeConfig(self, taskType):
        taskTypeConfig = {
            "translation": {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": self.sourceLanguage,
                        "targetLanguage": self.targetLanguage,
                    },
                },
            },
            "tts": {
                "taskType": "tts",
                "config": {
                    "language": {"sourceLanguage": self.sourceLanguage},
                    "gender": "female",
                },
            },
            "asr": {
                "taskType": "asr",
                "config": {"language": {"sourceLanguage": self.sourceLanguage}},
            },
        }
        try:
            return taskTypeConfig[taskType]
        except KeyError:
            raise KeyError("Invalid task type.")

    def getPipeLineConfig(self, taskType):
        taskTypeConfig = self.getTaskTypeConfig(taskType)
        payload = json.dumps(
            {
                "pipelineTasks": [taskTypeConfig],
                "pipelineRequestConfig": {
                    "pipelineId": self.pipeLineId,
                },
            }
        )
        response = requests.post(
            self.ulcaEndPoint,
            data=payload,
            headers={
                "ulcaApiKey": self.ulcaApiKey,
                "userID": self.ulcaUserId,
                "Content-Type": "application/json",
            },
        )

        if response.status_code != 200:
            raise ValueError("Something went wrong!")

        serviceId = (
            response.json()["pipelineResponseConfig"][0]
            .get("config")[0]
            .get("serviceId")
        )
        taskTypeConfig["config"]["serviceId"] = serviceId
        self.pipeLineData = response.json()

        return taskTypeConfig

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
            }
        }
        try:
            return taskTypeConfig[taskType]
        except KeyError:
            raise "Invalid task type."

    def getPipeLineConfig(self, taskType):
        if taskType == "translation":
            return self.getTaskTypeConfig(taskType)

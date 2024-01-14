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
                "config": {"language": {"sourceLanguage": self.sourceLanguage}},
            },
        }
        try:
            return taskTypeConfig[taskType]
        except KeyError:
            raise "Invalid task type."

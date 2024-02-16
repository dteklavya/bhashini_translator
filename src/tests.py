from unittest import TestCase, mock, main
import os
import json
from bhashini_translator import Bhashini


class TestTranslation(TestCase):
    """
    Test the translation functionality
    """

    def setUp(self) -> None:
        os.environ["userID"] = "test"
        os.environ["ulcaApiKey"] = "mock_key"
        os.environ["DefaultPipeLineId"] = "mock_id"
        return super().setUp()

    def test_nmt_payload(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {"pipelineResponseConfig": [{"config": [{"serviceId": 111}]}]}

        with mock.patch("bhashini_translator.pipeline_config.requests") as mock_request:
            mock_request.post.return_value.json.return_value = pl_config
            mock_request.post().status_code = 200
            json_payload = json.loads(bhashini.nmt_payload("Some text"))
            conf_payload = json_payload.get("pipelineTasks")[0].get("config")
            tasks_payload = json_payload.get("pipelineTasks")[0]

            self.assertTrue(mock_request.post.called)
            self.assertEqual(
                conf_payload.get("serviceId"),
                pl_config.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )

            self.assertEqual(tasks_payload.get("taskType"), "translation")
            self.assertEqual(conf_payload.get("language").get("sourceLanguage"), "en")
            self.assertEqual(conf_payload.get("language").get("targetLanguage"), "hi")

            self.assertEqual(
                json_payload.get("pipelineRequestConfig").get("pipelineId"), "mock_id"
            )
            self.assertEqual(
                json_payload.get("inputData").get("input")[0].get("source"),
                "Some text",
            )

    def test_tts_payload(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {"pipelineResponseConfig": [{"config": [{"serviceId": 123}]}]}

        with mock.patch("bhashini_translator.pipeline_config.requests") as mock_request:
            mock_request.post.return_value.json.return_value = pl_config
            mock_request.post().status_code = 200
            json_payload = json.loads(bhashini.tts_payload("Some text"))
            conf_payload = json_payload.get("pipelineTasks")[0].get("config")
            tasks_payload = json_payload.get("pipelineTasks")[0]

            self.assertTrue(mock_request.post.called)
            self.assertEqual(tasks_payload.get("taskType"), "tts")
            self.assertEqual(conf_payload.get("language").get("sourceLanguage"), "en")
            self.assertEqual(conf_payload.get("gender"), "female")
            self.assertEqual(conf_payload.get("serviceId"), 123)
            self.assertEqual(
                json_payload.get("pipelineRequestConfig").get("pipelineId"), "mock_id"
            )
            self.assertEqual(
                json_payload.get("inputData").get("input")[0].get("source"),
                "Some text",
            )

    def test_asr_nmt_payload(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {"pipelineResponseConfig": [{"config": [{"serviceId": 124}]}]}

        with mock.patch("bhashini_translator.pipeline_config.requests") as mock_request:
            mock_request.post.return_value.json.return_value = pl_config
            mock_request.post().status_code = 200
            json_payload = json.loads(bhashini.asr_nmt_payload("mock base64 string"))
            tasks_payload = json_payload.get("pipelineTasks")

            self.assertTrue(mock_request.post.called)
            self.assertEqual(tasks_payload[0].get("taskType"), "asr")
            self.assertEqual(
                tasks_payload[0].get("config").get("language").get("sourceLanguage"),
                "en",
            )
            self.assertEqual(tasks_payload[0].get("config").get("serviceId"), 124)

            self.assertEqual(tasks_payload[1].get("taskType"), "translation")
            self.assertEqual(
                tasks_payload[1].get("config").get("language").get("targetLanguage"),
                "hi",
            )
            self.assertEqual(tasks_payload[1].get("config").get("serviceId"), 124)

            self.assertEqual(
                json_payload.get("pipelineRequestConfig").get("pipelineId"), "mock_id"
            )

            self.assertEqual(
                json_payload.get("inputData").get("audio")[0].get("audioContent"),
                "mock base64 string",
            )

    def test_asr_payload(self):
        bhashini = Bhashini(targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {"pipelineResponseConfig": [{"config": [{"serviceId": 125}]}]}

        with mock.patch("bhashini_translator.pipeline_config.requests") as mock_request:
            mock_request.post.return_value.json.return_value = pl_config
            mock_request.post().status_code = 200
            json_payload = json.loads(bhashini.asr_payload("mock base64 string"))
            tasks_payload = json_payload.get("pipelineTasks")

            self.assertTrue(mock_request.post.called)

            self.assertEqual(tasks_payload[0].get("taskType"), "asr")
            self.assertIsNone(
                tasks_payload[0].get("config").get("language").get("sourceLanguage")
            )
            self.assertEqual(tasks_payload[0].get("config").get("serviceId"), 125)

            self.assertEqual(
                json_payload.get("pipelineRequestConfig").get("pipelineId"), "mock_id"
            )

            self.assertEqual(
                json_payload.get("inputData").get("audio")[0].get("audioContent"),
                "mock base64 string",
            )

    def test_nmt_tts_payload(self):
        bhashini = Bhashini(targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {"pipelineResponseConfig": [{"config": [{"serviceId": 126}]}]}

        with mock.patch("bhashini_translator.pipeline_config.requests") as mock_request:
            mock_request.post.return_value.json.return_value = pl_config
            mock_request.post().status_code = 200
            json_payload = json.loads(bhashini.nmt_tts_payload("mock string"))
            tasks_payload = json_payload.get("pipelineTasks")

            self.assertTrue(mock_request.post.called)

            self.assertEqual(tasks_payload[0].get("taskType"), "translation")
            self.assertIsNone(
                tasks_payload[0].get("config").get("language").get("sourceLanguage")
            )
            self.assertEqual(
                tasks_payload[0].get("config").get("language").get("targetLanguage"),
                "hi",
            )
            self.assertEqual(tasks_payload[0].get("config").get("serviceId"), 126)

            self.assertEqual(tasks_payload[1].get("taskType"), "tts")
            self.assertIsNone(
                tasks_payload[1].get("config").get("language").get("targetLanguage")
            )
            self.assertEqual(tasks_payload[1].get("config").get("serviceId"), 126)
            self.assertEqual(tasks_payload[1].get("config").get("gender"), "female")

            self.assertEqual(
                json_payload.get("pipelineRequestConfig").get("pipelineId"), "mock_id"
            )
            self.assertEqual(
                json_payload.get("inputData").get("input")[0].get("source"),
                "mock string",
            )

    def test_asr_nmt_tts_payload(self):
        bhashini = Bhashini(targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {"pipelineResponseConfig": [{"config": [{"serviceId": 127}]}]}

        with mock.patch("bhashini_translator.pipeline_config.requests") as mock_request:
            mock_request.post.return_value.json.return_value = pl_config
            mock_request.post().status_code = 200
            json_payload = json.loads(bhashini.nmt_tts_payload("mock string"))
            tasks_payload = json_payload.get("pipelineTasks")

            self.assertTrue(mock_request.post.called)

            self.assertEqual(tasks_payload[0].get("taskType"), "translation")
            self.assertIsNone(
                tasks_payload[0].get("config").get("language").get("sourceLanguage")
            )
            self.assertEqual(
                tasks_payload[0].get("config").get("language").get("targetLanguage"),
                "hi",
            )
            self.assertEqual(tasks_payload[0].get("config").get("serviceId"), 127)

            self.assertEqual(tasks_payload[1].get("taskType"), "tts")
            self.assertIsNone(
                tasks_payload[1].get("config").get("language").get("sourceLanguage")
            )
            self.assertEqual(tasks_payload[1].get("config").get("serviceId"), 127)
            self.assertEqual(tasks_payload[1].get("config").get("gender"), "female")


if __name__ == "__main__":
    main(exit=False)

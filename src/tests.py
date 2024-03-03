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

            self.assertEqual(
                json_payload.get("pipelineRequestConfig").get("pipelineId"), "mock_id"
            )
            self.assertEqual(
                json_payload.get("inputData").get("input")[0].get("source"),
                "mock string",
            )

    def test_translate(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "translation",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "sourceScriptCode": "Latn",
                                "targetLanguage": "hi",
                                "targetScriptCode": "Deva",
                            },
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.requests"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200
            json_payload = json.loads(bhashini.nmt_payload("Some text"))

            self.assertTrue(mock_pl_request.post.called)

            self.assertIsNotNone(bhashini.pipeLineData)
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                "ai4bharat/indictrans-v2",
            )

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200
            response = bhashini.compute_response(json_payload)

            self.assertTrue(mock_main.post.called)

            self.assertEqual(response.get("languages")[0].get("sourceLanguage"), "en")
            self.assertEqual(
                response.get("languages")[0].get("targetLanguageList")[0], "hi"
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                response.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("modelId"),
                "641d1d6",
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("language")
                .get("sourceScriptCode"),
                "Latn",
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("language")
                .get("targetScriptCode"),
                "Deva",
            )

            # Checks for pipelineInferenceAPIEndPoint
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint").get("callbackUrl"),
                "https://google.com/services/inference/pipeline",
            )
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint")
                .get("inferenceApiKey")
                .get("value"),
                "J|*wM4/ycjXv",
            )

    def test_tts(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "tts",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "targetLanguage": "hi",
                            },
                            "supportedVoices": ["male", "female"],
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.requests"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200
            json_payload = json.loads(bhashini.tts_payload("Some text"))

            self.assertTrue(mock_pl_request.post.called)

            self.assertIsNotNone(bhashini.pipeLineData)
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                "ai4bharat/indictrans-v2",
            )

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200
            response = bhashini.compute_response(json_payload)

            self.assertTrue(mock_main.post.called)

            self.assertEqual(response.get("languages")[0].get("sourceLanguage"), "en")
            self.assertEqual(
                response.get("languages")[0].get("targetLanguageList")[0], "hi"
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                response.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("modelId"),
                "641d1d6",
            )
            self.assertIsNotNone(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("supportedVoices")
            )

            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint").get("callbackUrl"),
                "https://google.com/services/inference/pipeline",
            )
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint")
                .get("inferenceApiKey")
                .get("value"),
                "J|*wM4/ycjXv",
            )

    def test_asr_nmt(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "tts",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "targetLanguage": "hi",
                            },
                            "supportedVoices": ["male", "female"],
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.requests"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200
            json_payload = json.loads(bhashini.asr_nmt_payload("mock base64 string"))

            self.assertTrue(mock_pl_request.post.called)

            self.assertIsNotNone(bhashini.pipeLineData)
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                "ai4bharat/indictrans-v2",
            )

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200
            response = bhashini.compute_response(json_payload)

            self.assertTrue(mock_main.post.called)

            response = bhashini.compute_response(json_payload)

            self.assertTrue(mock_main.post.called)

            self.assertEqual(response.get("languages")[0].get("sourceLanguage"), "en")
            self.assertEqual(
                response.get("languages")[0].get("targetLanguageList")[0], "hi"
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                response.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("modelId"),
                "641d1d6",
            )
            self.assertIsNotNone(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("supportedVoices")
            )

            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint").get("callbackUrl"),
                "https://google.com/services/inference/pipeline",
            )
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint")
                .get("inferenceApiKey")
                .get("value"),
                "J|*wM4/ycjXv",
            )

    def test_asr(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "tts",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "targetLanguage": "hi",
                            },
                            "supportedVoices": ["male", "female"],
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.requests"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200
            asr_payload = json.loads(bhashini.asr_payload("mock base64 string"))

            self.assertTrue(mock_pl_request.post.called)

            self.assertIsNotNone(bhashini.pipeLineData)
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                "ai4bharat/indictrans-v2",
            )

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200
            response = bhashini.compute_response(asr_payload)

            self.assertTrue(mock_main.post.called)

            self.assertEqual(response.get("languages")[0].get("sourceLanguage"), "en")
            self.assertEqual(
                response.get("languages")[0].get("targetLanguageList")[0], "hi"
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                response.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("modelId"),
                "641d1d6",
            )
            self.assertIsNotNone(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("supportedVoices")
            )

            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint").get("callbackUrl"),
                "https://google.com/services/inference/pipeline",
            )
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint")
                .get("inferenceApiKey")
                .get("value"),
                "J|*wM4/ycjXv",
            )

    def test_nmt_tts(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "tts",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "targetLanguage": "hi",
                            },
                            "supportedVoices": ["male", "female"],
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.requests"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200
            asr_payload = json.loads(bhashini.nmt_tts_payload("mock string"))

            self.assertTrue(mock_pl_request.post.called)

            self.assertIsNotNone(bhashini.pipeLineData)
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                "ai4bharat/indictrans-v2",
            )

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200
            response = bhashini.compute_response(asr_payload)

            self.assertTrue(mock_main.post.called)

            self.assertEqual(response.get("languages")[0].get("sourceLanguage"), "en")
            self.assertEqual(
                response.get("languages")[0].get("targetLanguageList")[0], "hi"
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                response.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("modelId"),
                "641d1d6",
            )
            self.assertIsNotNone(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("supportedVoices")
            )

            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint").get("callbackUrl"),
                "https://google.com/services/inference/pipeline",
            )
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint")
                .get("inferenceApiKey")
                .get("value"),
                "J|*wM4/ycjXv",
            )

    def test_asr_nmt_tts(self):
        bhashini = Bhashini(sourceLanguage="en", targetLanguage="hi")
        self.assertIsNotNone(bhashini)

        pl_config = {
            "languages": [{"sourceLanguage": "en", "targetLanguageList": ["hi"]}],
            "pipelineResponseConfig": [
                {
                    "taskType": "tts",
                    "config": [
                        {
                            "serviceId": "ai4bharat/indictrans-v2",
                            "modelId": "641d1d6",
                            "language": {
                                "sourceLanguage": "en",
                                "targetLanguage": "hi",
                            },
                            "supportedVoices": ["male", "female"],
                        }
                    ],
                }
            ],
            "feedbackUrl": "https://google.com/services/feedback/submit",
            "pipelineInferenceAPIEndPoint": {
                "callbackUrl": "https://google.com/services/inference/pipeline",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
            "pipelineInferenceSocketEndPoint": {
                "callbackUrl": "wss://dhruva-api.bhashini.gov.in",
                "inferenceApiKey": {
                    "name": "Authorization",
                    "value": "J|*wM4/ycjXv",
                },
                "isMultilingualEnabled": True,
                "isSyncApi": True,
            },
        }

        with mock.patch(
            "bhashini_translator.pipeline_config.requests"
        ) as mock_pl_request, mock.patch(
            "bhashini_translator.bhashini_translator.requests"
        ) as mock_main:
            mock_pl_request.post.return_value.json.return_value = pl_config
            mock_pl_request.post().status_code = 200
            asr_payload = json.loads(bhashini.asr_nmt_tts_payload("mock string"))

            self.assertTrue(mock_pl_request.post.called)

            self.assertIsNotNone(bhashini.pipeLineData)
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                "ai4bharat/indictrans-v2",
            )

            mock_main.post.return_value.json.return_value = pl_config
            mock_main.post().status_code = 200
            response = bhashini.compute_response(asr_payload)

            self.assertTrue(mock_main.post.called)

            self.assertEqual(response.get("languages")[0].get("sourceLanguage"), "en")
            self.assertEqual(
                response.get("languages")[0].get("targetLanguageList")[0], "hi"
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
                response.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertEqual(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("modelId"),
                "641d1d6",
            )
            self.assertIsNotNone(
                bhashini.pipeLineData.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("supportedVoices")
            )

            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint").get("callbackUrl"),
                "https://google.com/services/inference/pipeline",
            )
            self.assertEqual(
                response.get("pipelineInferenceAPIEndPoint")
                .get("inferenceApiKey")
                .get("value"),
                "J|*wM4/ycjXv",
            )


if __name__ == "__main__":
    main(exit=False)

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
            json_payload = bhashini.nmt_payload("Some text")
            payload = json.loads(json_payload).get("pipelineTasks")[0]

            self.assertEqual(
                payload.get("config").get("serviceId"),
                pl_config.get("pipelineResponseConfig")[0]
                .get("config")[0]
                .get("serviceId"),
            )
            self.assertTrue(mock_request.post.called)


if __name__ == "__main__":
    main(exit=False)

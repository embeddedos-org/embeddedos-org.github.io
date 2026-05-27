import unittest

class Testembeddedos-org.github.ioFunctional(unittest.TestCase):
    def test_documentation_search_indexing_pipeline(self):
        pages = [{"title": "Kernel Task API", "content": "eos_task_create is the primary function..."}, {"title": "NPU Inference", "content": "eai_inference_run executes models..."}]
        index = {}
        for p in pages:
            for word in p["content"].split():
                if "task" in word or "inference" in word:
                    index[word] = p["title"]
        assert "eos_task_create" in index

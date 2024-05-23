import pytest
import os 

documentation_folder = "documentation"

class MarkdownWritter:
    cariage_return:str
    data:str = ""

    def __init__(self, carriage_return = "\n\n") -> None:
        self.cariage_return = carriage_return

    def log(self, content, cariage_return=None):
        self.data += f"{self.cariage_return if cariage_return is None else cariage_return}{content}"

    def dump(self):
        return self.data
    
    def dump_in_file(self, path):
        with open(path, mode="w") as file:
            file.write(self.dump())

    @staticmethod
    def img(image_url, alt="todo"):
        return f'<img src="{image_url}" alt="{alt}" height="150px">'
    

@pytest.fixture(scope="module")
def doc_module(request):
    if not os.path.exists(documentation_folder):
        os.makedirs(documentation_folder)
    doc = MarkdownWritter()
    yield doc
    doc.dump_in_file(f"{documentation_folder}/{request.module.__name__}.md")


@pytest.fixture(scope="function")
def doc(doc_module, request):
    doc_module.log(f"##### {request.function.__name__.capitalize()}:".replace("_", " "))
    yield doc_module


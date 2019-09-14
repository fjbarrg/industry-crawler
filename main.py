import logging
import json
import fire

from model.industry import SIC
from difflib import SequenceMatcher


URL = "https://www.osha.gov/pls/imis/sic_manual.html"
INDUSTRY_FILE = "industries.json"


class Main(object):

    def _recursive_search(self, node, search_string, exact):
        title = node["title"].lower()
        new_children = []
        for child in node["children"]:
            is_valid_child = self._recursive_search(child, search_string, exact)
            if is_valid_child:
                new_children.append(child)
        successful_search = len(new_children) or self.similarity(search_string, title, exact)
        node["children"] = new_children
        return successful_search

    @staticmethod
    def download(filename=INDUSTRY_FILE):
        sic = SIC.from_url(URL)
        with open(filename, "w") as file:
            file.write(sic.jsonify())

    @staticmethod
    def similarity(a, b, exact=False, threshold=0.5):
        if exact:
            return a in b
        return SequenceMatcher(None, a, b).ratio() > threshold

    def search(self, title, exact=False, filename=INDUSTRY_FILE):
        sic_industries = SIC.load_json(filename)
        search_results = [node for node in sic_industries["children"] if self._recursive_search(node, title.lower(), exact)]
        print(json.dumps(search_results, indent=4))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(Main)

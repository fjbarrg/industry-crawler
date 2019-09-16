import logging
import fire

from model.industry import SIC
from util import StringWrapper, pretty_print, timeit


URL = "https://www.osha.gov/pls/imis/sic_manual.html"
DEFAULT_INDUSTRY_FILE = "industries.json"

logger = logging.getLogger(__name__)


class Main(object):

    def _recursive_search(self, node, string_wrapper, exact):
        title = node["title"].lower()
        new_children = []
        for child in node["children"]:
            is_valid_child = self._recursive_search(child, string_wrapper, exact)
            if is_valid_child:
                new_children.append(child)
        successful_search = len(new_children) or string_wrapper.boolean_search(pattern=title, exact=exact, reverse=True)
        node["children"] = new_children
        return successful_search

    @staticmethod
    @timeit(logger)
    def download(filename=DEFAULT_INDUSTRY_FILE):
        logging.info("Starting download procedure.")
        sic = SIC.from_url(URL)
        with open(filename, "w") as file:
            file.write(sic.jsonify())

    @timeit(logger)
    @pretty_print(logger)
    def search(self, title, exact=False, filename=DEFAULT_INDUSTRY_FILE):
        target_title = StringWrapper(value=title)
        sic_industries = SIC.load_json(filename)
        return [node for node in sic_industries["children"] if self._recursive_search(node, target_title, exact)]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    fire.Fire(Main)

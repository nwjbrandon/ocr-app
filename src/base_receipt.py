import re
from abc import ABC, abstractmethod


class BaseReceipt(ABC):
    def __init__(self, data):
        self.blocks = data["Blocks"]
        self.price_re = "^(?:\d+[\,\s])?\d+\.\d+$"
        self.count_re = "^(?:\d+)?X"
        super().__init__()

    @abstractmethod
    def run(self):
        pass

    def extract_price(self, data):
        parser = re.compile(self.price_re)
        matches = [match for match in parser.findall(data)]
        return matches

    def extract_no_of_items(self, data):
        parser = re.compile(self.count_re)
        matches = [match for match in parser.findall(data)]
        return matches

    def parse_blocks(self):
        root_block = self.blocks[0]
        relationships = root_block["Relationships"][0]["Ids"]

        items = []
        for block in self.blocks:
            # remove items that are centralized on the receipt
            left = block["Geometry"]["BoundingBox"]["Left"]
            width = block["Geometry"]["BoundingBox"]["Width"]
            center = left + width / 2
            is_centered = center > 0.45 and center < 0.55

            if block["Id"] not in relationships or is_centered:
                continue

            items.append(block)

        return items

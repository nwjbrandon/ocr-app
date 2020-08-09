import re


class ReceiptContentExtractor:
    def __init__(self, data):
        self.blocks = data["Blocks"]
        self.price_re = r"^\d+\.\d\d$"
        self.count_re = r"^\d+X"
        self.item_re = r"[a-zA-Z\d\s/.]+"
        self.item_ignore_list_re = [r"\d+\.\d+", r"(KG|SGD|CARD)"]

    def run(self):
        items = self.parse_blocks()
        items = self.get_content(items=items)
        items = self.format_output(items=items)
        return items

    def extract_item(self, data):
        if any(re.search(r, data) for r in self.item_ignore_list_re):
            return None
        pattern = re.compile(self.item_re)
        matches = [match for match in pattern.findall(data)]
        if len(matches) > 0:
            return matches[0]
        else:
            return None

    def extract_count(self, data):
        pattern = re.compile(self.count_re)
        matches = [match for match in pattern.findall(data)]
        if len(matches) > 0:
            return int(matches[0][:-1]) if matches[0][:-1].isdigit() else None
        else:
            return None

    def extract_price(self, data):
        pattern = re.compile(self.price_re)
        matches = [match for match in pattern.findall(data)]
        if len(matches) > 0:
            return float(matches[0])
        else:
            return None

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

            terminating_flags = ["total", "discount"]
            text = block["Text"].lower()
            if any([True for flag in terminating_flags if flag in text]):
                break

            items.append(block)

        return items

    def get_content(self, items):
        content = list()
        for i, item in enumerate(items):
            print()
            text = item["Text"]
            print(text)

            price = self.extract_price(data=text)
            count = self.extract_count(data=text)
            if price is None and count is None:
                item = self.extract_item(data=text)
            else:
                item = None

            if item is None and count is None and price is None:
                continue

            output = {
                "price": price,
                "item": item,
                "count": count,
            }

            print(output)
            content.append(output)

        return content

    def format_output(self, items):
        total = len(items)
        no_of_items = sum([1 for item in items if not item["item"] is None])
        no_of_items_to_right = total // no_of_items + 1

        results = list()
        for i, item in enumerate(items):
            if item["item"] is None:
                continue

            items_to_right = items[i : i + no_of_items_to_right]

            price = None
            for element in items_to_right:
                if not element["price"] is None:
                    price = element["price"]
                    break

            count = 1
            for element in items_to_right:
                if not element["count"] is None:
                    count = element["count"]
                    break

            results.append(
                {"item": item["item"], "count": count, "price": price,}
            )

        return results

from base_receipt import BaseReceipt


class FairPriceReceipt(BaseReceipt):
    def __init__(self, data):
        super().__init__(data=data)

    def run(self):
        items = self.parse_blocks()
        items = self.get_items(items=items)
        return items

    def get_items(self, items):
        results = []
        for i, item in enumerate(items):
            price = self.extract_price(item["Text"])
            if len(price) > 0:
                no_of_items, item_name = self.get_item(i, items)
                results.append(
                    {"no_of_items": no_of_items, "item_name": item_name,}
                )
        return results

    def get_item(self, current_index, items):
        count_value, count_pos = self.get_counts(current_index, items)
        name = self.get_name(current_index, items, count_pos)
        return count_value, name

    def get_counts(self, current_index, items):
        # -1 for left, 1 for right, 0 for absent
        if current_index + 1 >= len(items):
            return 0, 0

        left_counts = self.get_count(current_index, items, -1)
        right_counts = self.get_count(current_index, items, 1)

        if len(left_counts) > 0:
            return self.format_count(left_counts[0][:-1], -1)
        if len(right_counts) > 0:
            return self.format_count(right_counts[0][:-1], 1)

        return 0, 0

    def format_count(self, value, offset):
        if value.isdigit():
            return int(value), offset
        else:
            return 0, offset

    def get_count(self, current_index, items, offset):
        count = items[current_index + offset]["Text"]
        return self.extract_no_of_items(count)

    def get_name(self, current_index, items, offset):
        name_pos = -1
        if offset == -1:
            name_pos = -2
        return items[current_index + name_pos]["Text"]

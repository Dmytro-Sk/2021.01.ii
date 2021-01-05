import csv


class Converter:

    def __init__(self, args):
        self.args = args

    def open_file(self, column) -> list:
        with open(f"../req_data.csv") as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            headers = []
            for line in csv_reader:
                headers += [line[column]]
        return headers

    def get_items(self, column) -> list:
        converted_items_list = []
        for parse_items in self.open_file(column):
            if parse_items != '':
                converted_items = f"{parse_items.replace(' ', '_').lower()} = scrapy.Field()"
                converted_items_list.append(converted_items)
        return converted_items_list

    def get_parse_items_elements(self, column) -> list:
        converted_parse_items_elements_list = []
        for parse_items_element in self.open_file(column):
            if parse_items_element != '':
                converted_parse_items_element = f"items[\'{parse_items_element.replace(' ', '_').lower()}\'] = {parse_items_element.replace(' ', '_').lower()}"
                converted_parse_items_elements_list.append(converted_parse_items_element)
        return converted_parse_items_elements_list

    def get_parse_elements(self, column) -> list:
        converted_parse_elements_list = []
        for parse_element in self.open_file(column):
            if parse_element != '':
                converted_parse_element = f"{parse_element.replace(' ', '_').lower()} = response.xpath(Locators.{parse_element.replace(' ', '_').upper()}).get()"
                converted_parse_elements_list.append(converted_parse_element)
        return converted_parse_elements_list

    def get_custom_settings(self, column, spider_name) -> list:
        converted_custom_settings_list = [
            "\tcustom_settings = {",
            "\t\t'FEED_EXPORT_BATCH_ITEM_COUNT': 100,",
            "\t\t'FEED_FORMAT': 'csv',",
            f"\t\t'FEED_URI': '../../iii_results/{spider_name.split('_')[-1]}/%(batch_id)02d-{spider_name}.csv',",
            "\t\t'FEED_EXPORT_FIELDS': [",
        ]
        for custom_setting in self.open_file(column):
            if custom_setting != '':
                converted_custom_settings_name = f"\t\t\t\'{custom_setting.replace(' ', '_').lower()}\',"
                converted_custom_settings_list.append(converted_custom_settings_name)
        converted_custom_settings_list.append('\t\t]' + '\n' + '\t}')
        return converted_custom_settings_list

    def get_locators(self, column) -> list:
        converted_locators_list = []
        for locator in self.open_file(column):
            if locator != '':
                converted_locator = f"{locator.replace(' ', '_').upper()} = \'\'"
                converted_locators_list.append(converted_locator)
        return converted_locators_list

    @staticmethod
    def conv_def_name(func_name) -> str:
        conv_def_name = f' {func_name.replace("_", " ").upper()} '.center(50, "-") + '\n' * 2
        return conv_def_name

    def write_column(self) -> None:
        for column, spider_name in enumerate(self.args['spiders_names']):
            with open(f"./{spider_name}.txt", 'a') as f:
                f.write(self.conv_def_name(self.get_locators.__name__))
                f.writelines('\n'.join(self.get_locators(column)) + '\n' * 3)
                f.write(self.conv_def_name(self.get_custom_settings.__name__))
                f.writelines('\n'.join(self.get_custom_settings(column, spider_name)) + '\n' * 3)
                f.write(self.conv_def_name(self.get_parse_elements.__name__))
                f.writelines('\n'.join(self.get_parse_elements(column)) + '\n' * 3)
                f.write(self.conv_def_name(self.get_parse_items_elements.__name__))
                f.writelines('\n'.join(self.get_parse_items_elements(column)) + '\n' * 3)
                f.write(self.conv_def_name(self.get_items.__name__))
                f.writelines('\n'.join(self.get_items(column)) + '\n' * 3)


"""Put and initial data"""

data = {
    'spiders_names': ['vrisko_gr_companies', 'vrisko_gr_urls'],
}

con = Converter(data)


"""Create converted_data file"""

con.write_column()

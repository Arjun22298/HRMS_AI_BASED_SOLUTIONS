class ConvertNullToNone:
    def convert_null_to_none(self, data):
        if isinstance(data, dict):
            return {key: self.convert_null_to_none(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_null_to_none(item) for item in data]
        elif isinstance(data, str) and data.lower() == "null":
            return None
        else:
            return data

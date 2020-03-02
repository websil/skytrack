class BaseForm:

    errors = []

    safe_attributes = []

    def __init__(self):
        self.clear_errors()

    def load(self, data):
        for key in data:
            if isinstance(self, BaseForm) and hasattr(self, key):
                if key in self.safe_attributes:
                    setattr(self, key, data[key])

    def validate(self):
        return not self.has_error()

    def add_error(self, attribute, code, message):
        self.errors.append({'attribute': attribute, 'code': code, 'message': message})

    # проверяем наличие ошибок
    def has_error(self):
        if len(self.errors) > 0:
            return True
        return False

    def clear_errors(self):
        self.errors = []

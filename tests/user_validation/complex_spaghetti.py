class DataProcessor:
    """Handles data transformation (Wisdom)."""

    def process(self, data):
        # Wisdom: Logic/Transform
        return [d.strip().lower() for d in data if d]


class DataValidator:
    """Enforces data integrity (Justice)."""

    def validate(self, data):
        # Justice: Validation
        if not data:
            raise ValueError("Empty data")
        return True


class Application:
    """Orchestrates the flow (Power/Love)."""

    def __init__(self):
        self.processor = DataProcessor()
        self.validator = DataValidator()
        self.state = []

    def run(self, raw_input):
        # Power: Execution
        try:
            if self.validator.validate(raw_input):
                self.state = self.processor.process(raw_input)
                print("Processing complete")
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

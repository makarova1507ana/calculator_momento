class Calculator:
    def __init__(self):
        self.result = 0
        self.last_operation = None
        self.operand1 = None
        self.operand2 = None

    def add(self, operand1, operand2):
        self.result = operand1 + operand2
        self.last_operation = 'add'
        self.operand1 = operand1
        self.operand2 = operand2

    def subtract(self, operand1, operand2):
        self.result = operand1 - operand2
        self.last_operation = 'subtract'
        self.operand1 = operand1
        self.operand2 = operand2

    def multiply(self, operand1, operand2):
        self.result = operand1 * operand2
        self.last_operation = 'multiply'
        self.operand1 = operand1
        self.operand2 = operand2

    def divide(self, operand1, operand2):
        if operand2 != 0:
            self.result = operand1 / operand2
            self.last_operation = 'divide'
            self.operand1 = operand1
            self.operand2 = operand2
        else:
            raise ValueError("Division by zero is not allowed")

    def get_result(self):
        return self.result

    def get_last_operation(self):
        return self.last_operation

    def get_operands(self):
        return self.operand1, self.operand2

    def set_operands(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

class Memento:
    def __init__(self, result, last_operation, operand1, operand2):
        self.result = result
        self.last_operation = last_operation
        self.operand1 = operand1
        self.operand2 = operand2

    def get_state(self):
        return self.result, self.last_operation, self.operand1, self.operand2

class Caretaker:
    def __init__(self):
        self._mementos = []

    def save_state(self, memento):
        self._mementos.append(memento)

    def restore_state(self):
        if self._mementos:
            return self._mementos.pop()
        return None

class Mediator:
    def __init__(self, calculator, caretaker):
        self.calculator = calculator
        self.caretaker = caretaker

    def execute(self, operation, operand1, operand2):
        try:
            if operation == 'add':
                self.calculator.add(operand1, operand2)
            elif operation == 'subtract':
                self.calculator.subtract(operand1, operand2)
            elif operation == 'multiply':
                self.calculator.multiply(operand1, operand2)
            elif operation == 'divide':
                self.calculator.divide(operand1, operand2)
            else:
                raise ValueError("Unsupported operation")

            self.save_state()

        except ValueError as e:
            print(e)

    def save_state(self):
        result = self.calculator.get_result()
        last_operation = self.calculator.get_last_operation()
        operand1, operand2 = self.calculator.get_operands()
        memento = Memento(result, last_operation, operand1, operand2)
        self.caretaker.save_state(memento)

    def restore_state(self):
        memento = self.caretaker.restore_state()
        if memento:
            result, last_operation, operand1, operand2 = memento.get_state()
            self.calculator.result = result
            self.calculator.last_operation = last_operation
            self.calculator.set_operands(operand1, operand2)
        else:
            raise ValueError("No states to restore")

def main():
    calculator = Calculator()
    caretaker = Caretaker()
    mediator = Mediator(calculator, caretaker)

    while True:
        print(f"Current result: {calculator.get_result()}")

        operation = input("Enter operation (add, subtract, multiply, divide, undo, redo, exit): ")

        if operation == 'exit':
            break
        elif operation == 'undo':
            try:
                mediator.restore_state()
            except ValueError as e:
                print(e)
        elif operation == 'redo':
            try:
                mediator.execute(calculator.get_last_operation(), *calculator.get_operands())
            except ValueError as e:
                print(e)
        else:
            try:
                operand1 = float(input("Enter operand 1: "))
                operand2 = float(input("Enter operand 2: "))
                calculator.set_operands(operand1, operand2)
                mediator.execute(operation, operand1, operand2)
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    main()

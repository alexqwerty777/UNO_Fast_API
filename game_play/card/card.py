

class Card:

    usual_colors = ['r', 'g', 'b', 'y']
    flip_colors = ['o', 'c', 'm', 'p']
    num_values = [str(i) for i in range(1,10)]
    taking_values = ['+1', '+2', '+5']
    action_values = [
        'choose_color', 'repeat', 'find_color',
        'flip', 'passed', 'revert',
    ]

    def __init__(self, value: str, color: str, flip_value: str, flip_color: str):
        self.value = value
        self.color = color
        self.flip_value = flip_value
        self.flip_color = flip_color

    def __repr__(self):
        return f'{self.value}"{self.color}"/{self.flip_value}"{self.flip_color}"'

    def get_value(self, flip: bool = False) -> int:
        value_point = {
            'flip': 25,
            'repeat': 25,
            'revert': 25,
            'passed': 25,
            'choose_color': 50,
            'find_color': 50,
            '+1': 25,
            '+2': 50,
            '+5': 50,
        }
        if flip:
            if self.flip_value in self.num_values:
                return int(self.flip_value)
            return value_point.get(self.flip_value)
        else:
            if self.value in self.num_values:
                return int(self.value)
            return value_point.get(self.value)

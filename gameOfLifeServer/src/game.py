

class GameOfLife:
    """
    Класс, реализующий игру.
    """
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []
        self.old_states = []

    def resurrection(self):
        """
        Метод установки состояний клеткам (живая/мертвая).
        """
        new_state = []
        for i in range(len(self.cells)):
            new_state.append([0] * len(self.cells[0]))
        self.old_states.append(self.cells)
        for row_index, row in enumerate(self.cells):
            for column_index, element in enumerate(row):
                neighbors = self.count_living_neighbors(row_index, column_index)
                if self.cells[row_index][column_index] == 1 and (neighbors == 2 or neighbors == 3):
                    new_state[row_index][column_index] = 1
                elif self.cells[row_index][column_index] == 0 and neighbors == 3:
                    new_state[row_index][column_index] = 1
        self.cells = new_state

    def count_living_neighbors(self, cell_row, cell_col):
        """
        Метод подсчёта количества соседей клетки.
        :param cell_row: x координата клетки
        :param cell_col: y координата клетки
        :return: количество соседей клетки
        """
        if cell_row == 0 and cell_col == 0:
            x_shift = [0, 1, 1]
            y_shift = [1, 0, 1]
        elif cell_row == 0 and cell_col == len(self.cells[0]) - 1:
            x_shift = [0, 1, 1]
            y_shift = [-1, -1, 0]
        elif cell_row == len(self.cells) - 1 and cell_col == 0:
            x_shift = [-1, -1, 0]
            y_shift = [0, 1, 1]
        elif cell_row == len(self.cells) - 1 and cell_col == len(self.cells[0]) - 1:
            x_shift = [-1, -1, 0]
            y_shift = [-1, 0, -1]
        elif cell_row == 0:
            x_shift = [0, 0, 1, 1, 1]
            y_shift = [-1, 1, -1, 0, 1]
        elif cell_col == 0:
            x_shift = [-1, -1, 0, 1, 1]
            y_shift = [0, 1, 1, 0, 1]
        elif cell_col == len(self.cells[0]) - 1:
            x_shift = [-1, -1, 0, 1, 1]
            y_shift = [-1, 0, -1, -1, 0]
        elif cell_row == len(self.cells) - 1:
            x_shift = [-1, -1, -1, 0, 0]
            y_shift = [-1, 0, 1, -1, 1]
        else:
            x_shift = [-1, -1, -1, 0, 0, 1, 1, 1]
            y_shift = [-1, 0, 1, -1, 1, -1, 0, 1]
        i = 0
        neighbor_sum = 0
        while i < len(x_shift):
            neighbor_sum += self.cells[cell_row + x_shift[i]][cell_col + y_shift[i]]
            i += 1
        return neighbor_sum

    def count_living_cells(self):
        """
        Метод подсчёта количества живых клеток на поле.
        :return: количество живых клеток
        """
        sum_living_cells = 0
        for row in self.cells:
            for cell in row:
                if cell:
                    sum_living_cells += 1

        return sum_living_cells

    def view_stat(self, state):
        """
        Метод сравнения старого состояния клеток с текущим.
        :param state: старое состояние
        :return: результат сравнения
        """
        for row_index, state_row in enumerate(state):
            for column_index, state_cell in enumerate(state_row):
                if self.cells[row_index][column_index] != state_cell:
                    return False
        return True

    def state_comparison(self):
        """
        Метод сравнения всех старых состояний с текущим.
        :return: результат совпадения с хотя бы одним состоянием
        """
        for state in self.old_states:
            if self.view_stat(state):
                return True

        return False

    def game(self, user_data):
        """
        Метод, реализующий игру.
        """
        for row in list(user_data.form.lists()):
            row_list = []
            if row[0] != 'token':
                for element in row[1]:
                    row_list.append(int(element))
                self.cells.append(row_list)

        i = 0
        for row in self.cells:
            some = []
            for element in row:
                some.append(str(element))

        states = []
        while not self.state_comparison() and self.count_living_cells() > 0:
            self.resurrection()
            i += 1
            state = []
            j = 0
            for row in self.cells:
                some = []
                for element in row:
                    some.append(element)
                state.append(some)
                j += 1
            states.append(state)

        print("The game is over.")
        return states

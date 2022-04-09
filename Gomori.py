import math
from fractions import Fraction
from accessify import private
from SimplexTable import SimplexTable


class Gomori(SimplexTable):
    def __init__(self, table: list, rows_caption: list, columns_caption: list, is_maximize: bool):
        self.is_maximize = is_maximize
        for i in range(len(table[0])):
            table[len(table) - 1][i] = - table[len(table) - 1][i]
        super().__init__(table, len(table), len(table[0]), rows_caption, columns_caption)

    @staticmethod
    def no_integer_values(vector: list):
        for value in vector:
            if value.denominator != 1:
                return True
        return False

    def can_be_iterated(self):
        for value in self.get_vector_answer():
            if value.denominator != 1:
                return True
        return False

    @private
    def find_row(self):
        value = Fraction(-1)
        index = -1
        for i in range(self.rows - 1):
            b = self.table[i][self.columns - 1]
            b_part = b - math.floor(b)
            if b_part > value or value < 0:
                value = b_part
                index = i
        return index

    @private
    def print_new_equation(self, q: list):
        print('Added new equation: {}'.format(-q[len(q) - 1]), end='')
        for i in range(len(q) - 1):
            if q[i] == -1:
                print('-x{}'.format(i + 1), end='')
            elif q[i] == 0:
                continue
            else:
                print('{}x{}'.format(q[i], i + 1), end='')
        print('<=0')

    @private
    def add_basis(self, index_from: int):
        row = []
        for i in range(self.columns):
            element = self.table[index_from][i]
            q = element - math.floor(element)
            row.append(-q)
        self.print_new_equation(row)
        self.table.insert(self.rows - 1, row.copy())
        new_basis_index = Gomori.get_basis_index(self.columns_caption[self.columns - 2]) + 1
        self.rows_caption.insert(self.rows - 1, 'x' + str(new_basis_index))
        self.rows += 1
        for i in range(self.rows):
            if i == self.rows - 2:
                self.table[i].insert(self.columns - 1, Fraction(1))
            else:
                self.table[i].insert(self.columns - 1, Fraction(0))
        self.columns_caption.insert(self.columns - 1, 'x' + str(new_basis_index))
        self.columns += 1

    @private
    def find_column(self):
        value = Fraction(-1)
        index = -1
        for i in range(self.columns - 2):
            a = self.table[self.rows - 2][i]
            c = self.table[self.rows - 1][i]
            if a == 0:
                continue
            if c / a < value or value < 0:
                value = c / a
                index = i
        return index

    def iterate(self):
        row = self.find_row()
        self.add_basis(row)
        self.print()
        column = self.find_column()
        print('Element: {} ({}, {})'.format(str(self.table[self.rows - 2][column]), self.rows - 1, column + 1))
        self.recalculate(self.rows - 2, column)

    def get_function_answer(self):
        return -self.table[self.rows - 1][self.columns - 1]

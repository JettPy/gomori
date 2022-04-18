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
            if value.denominator != 1 or value < 0:
                return True
        return False

    @private
    def find_max_fraction(self):
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
    def find_row(self):
        value = Fraction(0)
        index = -1
        for i in range(self.rows - 1):
            b = self.table[i][self.columns - 1]
            if b < value or index < 0:
                value = b
                index = i
        return index

    @private
    def new_equation(self, q: list):
        equation = 'Added new equation: {}'.format(-q[len(q) - 1])
        for i in range(len(q) - 1):
            if q[i] == -1:
                equation += '-x{}'.format(i + 1)
            elif q[i] == 0:
                continue
            else:
                equation += '{}x{}'.format(q[i], i + 1)
        equation += '<=0'
        return equation

    @private
    def add_basis(self, index_from: int):
        row = []
        for i in range(self.columns):
            element = self.table[index_from][i]
            q = element - math.floor(element)
            row.append(-q)
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
        return self.new_equation(row) + ' from {}'.format(self.rows_caption[index_from])

    @private
    def find_column(self, row: int):
        value = Fraction(-1)
        index = -1
        for i in range(self.columns - 1):
            a = self.table[row][i]
            c = self.table[self.rows - 1][i]
            if a >= 0 or c >= 0:
                continue
            if c / a < value or value < 0:
                value = c / a
                index = i
        return index

    def iterate_first(self):
        row = self.find_max_fraction()
        return self.add_basis(row)

    def iterate_last(self):
        row = self.find_row()
        column = self.find_column(row)
        element = 'Element: {} ({}, {})'.format(str(self.table[self.rows - 2][column]), self.rows - 1, column + 1)
        self.recalculate(row, column)
        return element

    def get_function_answer(self):
        return -self.table[self.rows - 1][self.columns - 1]

    def last_iteration(self):
        for value in self.get_vector_answer():
            if value.denominator == 1 and value < 0:
                return True
        return False

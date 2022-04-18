from accessify import private
from ArtificialBasis import ArtificialBasis
from Gomori import Gomori


class App:
    def __init__(self):
        self.variables_count = 0
        self.equations_count = 0
        self.matrix_a = []
        self.matrix_b = []
        self.matrix_c = []
        self.signs = []
        self.is_maximize = None

    def enter_from_console(self):
        while True:
            print('Enter count of variables:')
            buffer = input()
            try:
                self.variables_count = int(buffer)
                if self.variables_count < 1:
                    raise ValueError
                break
            except ValueError:
                print('Enter natural integer')
                continue
        while True:
            print('Enter count of equations:')
            buffer = input()
            try:
                self.equations_count = int(buffer)
                if self.equations_count < 1:
                    raise ValueError
                break
            except ValueError:
                print('Enter natural integer')
                continue
        k = 1
        while k <= self.equations_count:
            print('Enter {} coefficients, equality sign and free term for the equation {}:'.format(self.variables_count,
                                                                                                   k))
            buffer = input()
            equation = buffer.split()
            if len(equation) < self.variables_count + 2:
                print('Too few arguments')
                continue
            elif len(equation) > self.variables_count + 2:
                print('Too many arguments')
                continue
            matrix_a_row = []
            try:
                for i in range(self.variables_count):
                    a = int(equation[i])
                    matrix_a_row.append(a)
            except ValueError:
                print('Enter integers for coefficients')
                continue
            self.matrix_a.append(matrix_a_row.copy())
            sign = equation[self.variables_count]
            if sign != '>=' and sign != '==' and sign != '<=':
                print('Enter ">=", "<=", or "==" for sign')
                self.matrix_a.pop()
                continue
            else:
                self.signs.append(sign)
            try:
                b = int(equation[self.variables_count + 1])
                self.matrix_b.append(b)
            except ValueError:
                print('Enter integer for free term')
                self.matrix_a.pop()
                self.signs.pop()
                continue
            k += 1
        while True:
            print('Enter {} coefficients for object function:'.format(self.variables_count))
            buffer = input()
            equation = buffer.split()
            if len(equation) < self.variables_count:
                print('Too few arguments')
                continue
            elif len(equation) > self.variables_count:
                print('Too many arguments')
                continue
            try:
                for i in range(self.variables_count):
                    c = int(equation[i])
                    self.matrix_c.append(c)
            except ValueError:
                print('Enter integers for coefficients')
                self.matrix_c.clear()
                continue
            break
        while True:
            print('Maximize? (y/n)')
            buffer = input()
            if buffer != 'y' and buffer != 'n':
                print('Enter "y" for "yes" or "n" for "no"')
                continue
            elif buffer == 'y':
                self.is_maximize = True
            else:
                self.is_maximize = False
            break

    def enter_from_message(self, buffer: str):
        try:
            self.variables_count = int(buffer[0])
            if self.variables_count < 1:
                raise ValueError
            self.equations_count = int(buffer[1])
            if self.equations_count < 1:
                raise ValueError
            for i in range(1, self.equations_count + 1):
                equation = buffer[1 + i].split()
                if len(equation) != self.variables_count + 2:
                    raise ValueError
                matrix_a_row = []
                for j in range(self.variables_count):
                    a = int(equation[j])
                    matrix_a_row.append(a)
                self.matrix_a.append(matrix_a_row.copy())
                sign = equation[self.variables_count]
                self.signs.append(sign)
                b = int(equation[self.variables_count + 1])
                self.matrix_b.append(b)
            equation = buffer[self.equations_count + 2].split()
            if len(equation) != self.variables_count:
                raise ValueError
            for i in range(self.variables_count):
                c = int(equation[i])
                self.matrix_c.append(c)
            if buffer[self.equations_count + 3] != 'y' and buffer[self.equations_count + 3] != 'n':
                raise ValueError
            elif buffer[self.equations_count + 3] == 'y':
                self.is_maximize = True
            else:
                self.is_maximize = False
        except Exception:
            self.variables_count = 0
            self.equations_count = 0
            self.matrix_a.clear()
            self.matrix_b.clear()
            self.matrix_c.clear()
            self.signs.clear()
            self.is_maximize = None
            return False
        return True

    def print_enter(self, file=None):
        print('Your enter:', file=file)
        for i in range(self.equations_count):
            for j in range(self.variables_count):
                if j == 0 or self.matrix_a[i][j] < 0:
                    if self.matrix_a[i][j] == -1:
                        print('-x{}'.format(j + 1), file=file, end='')
                    elif self.matrix_a[i][j] == 1:
                        print('x{}'.format(j + 1), file=file, end='')
                    else:
                        print('{}x{}'.format(self.matrix_a[i][j], j + 1), file=file, end='')
                else:
                    if self.matrix_a[i][j] == 1:
                        print('+x{}'.format(j + 1), file=file, end='')
                    else:
                        print('+{}x{}'.format(self.matrix_a[i][j], j + 1), file=file, end='')
            print('{}{}'.format(self.signs[i], self.matrix_b[i]), file=file)
        print('Z(x)=', file=file, end='')
        for i in range(self.variables_count):
            if i == 0 or self.matrix_c[i] < 0:
                if self.matrix_c[i] == -1:
                    print('-x{}'.format(i + 1), file=file, end='')
                elif self.matrix_c[i] == 1:
                    print('x{}'.format(i + 1), file=file, end='')
                else:
                    print('{}x{}'.format(self.matrix_c[i], i + 1), file=file, end='')
            else:
                if self.matrix_c[i] == 1:
                    print('+x{}'.format(i + 1), file=file, end='')
                else:
                    print('+{}x{}'.format(self.matrix_c[i], i + 1), file=file, end='')
        if self.is_maximize:
            print(' -> max', file=file)
        else:
            print(' -> min', file=file)

    def print_dual_system(self, file=None):
        print('Dual system:', file=file)
        for i in range(len(self.matrix_a)):
            for j in range(len(self.matrix_a[0])):
                if j == 0 or self.matrix_a[i][j] < 0:
                    if self.matrix_a[i][j] == -1:
                        print('-y{}'.format(j + 1), file=file, end='')
                    elif self.matrix_a[i][j] == 1:
                        print('y{}'.format(j + 1), file=file, end='')
                    else:
                        print('{}y{}'.format(self.matrix_a[i][j], j + 1), file=file, end='')
                else:
                    if self.matrix_a[i][j] == 1:
                        print('+y{}'.format(j + 1), file=file, end='')
                    else:
                        print('+{}y{}'.format(self.matrix_a[i][j], j + 1), file=file, end='')
            print('{}{}'.format(self.signs[i], self.matrix_b[i]), file=file)
        print('Z(y)=', file=file, end='')
        for i in range(len(self.matrix_c)):
            if i == 0 or self.matrix_c[i] < 0:
                if self.matrix_c[i] == -1:
                    print('-y{}'.format(i + 1), file=file, end='')
                elif self.matrix_c[i] == 1:
                    print('y{}'.format(i + 1), file=file, end='')
                else:
                    print('{}y{}'.format(self.matrix_c[i], i + 1), file=file, end='')
            else:
                if self.matrix_c[i] == 1:
                    print('+y{}'.format(i + 1), file=file, end='')
                else:
                    print('+{}y{}'.format(self.matrix_c[i], i + 1), file=file, end='')
        if self.is_maximize:
            print(' -> max', file=file)
        else:
            print(' -> min', file=file)

    @private
    def transform_to_positive_b(self):
        for i in range(len(self.matrix_a)):
            if self.matrix_b[i] < 0:
                for j in range(len(self.matrix_c)):
                    self.matrix_a[i][j] = -self.matrix_a[i][j]
                self.matrix_b[i] = -self.matrix_b[i]
                if self.signs[i] == '>=':
                    self.signs[i] = '<='
                elif self.signs[i] == '<=':
                    self.signs[i] = '>='

    @private
    def transform_for_dual_task(self):
        for i in range(self.equations_count):
            if self.is_maximize and self.signs[i] == '>=' or not self.is_maximize and self.signs[i] == '<=':
                for j in range(self.variables_count):
                    self.matrix_a[i][j] = -self.matrix_a[i][j]
                self.matrix_b[i] = -self.matrix_b[i]
                if self.signs[i] == '>=':
                    self.signs[i] = '<='
                elif self.signs[i] == '<=':
                    self.signs[i] = '>='

    @private
    def transpose_data(self):
        matrix_a_t = []
        for i in range(len(self.matrix_a[0])):
            row_a = []
            for j in range(len(self.matrix_a)):
                row_a.append(self.matrix_a[j][i])
            matrix_a_t.append(row_a.copy())
            row_a.clear()
        dual_signs = []
        for i in range(len(self.matrix_c)):
            if not self.is_maximize:
                dual_signs.append('<=')
            else:
                dual_signs.append('>=')
        return matrix_a_t, dual_signs

    def do_artificial_basis(self, file=None):
        self.print_enter(file)
        self.transform_to_positive_b()
        table = ArtificialBasis(self.matrix_a, self.matrix_b, self.matrix_c, self.signs, self.is_maximize)
        print('Initial:', file=file)
        for row in table.get_table_to_print():
            for element in row:
                print('{:>6}'.format(element), file=file, end=' ')
            print(file=file)
        count = 1
        while table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            comment = table.iterate()
            print(comment, file=file)
            if comment == 'No solution':
                return
            for row in table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('Drop G:', file=file)
        table.drop_artificial_function()
        for row in table.get_table_to_print():
            for element in row:
                print('{:>6}'.format(element), file=file, end=' ')
            print(file=file)
        while table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            comment = table.iterate()
            print(comment, file=file)
            if comment == 'No solution':
                return
            for row in table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('X vector:', file=file)
        for element in table.get_vector_answer():
            print('{:>6}'.format(str(element)), file=file, end=' ')
        print(file=file)
        if self.is_maximize:
            print('Max Z: {}'.format(str(table.get_function_answer())), file=file)
        else:
            print('Min Z: {}'.format(str(table.get_function_answer())), file=file)

    def do_dual_task(self, file=None):
        self.print_enter(file)
        self.transform_for_dual_task()
        matrix_a_t, dual_signs = self.transpose_data()
        self.matrix_a = matrix_a_t
        self.matrix_b, self.matrix_c = self.matrix_c, self.matrix_b
        self.signs = dual_signs
        self.is_maximize = not self.is_maximize
        self.print_dual_system(file)
        self.transform_to_positive_b()
        self.print_dual_system(file)
        table = ArtificialBasis(self.matrix_a, self.matrix_b, self.matrix_c, self.signs, self.is_maximize, 'y')
        print('Initial:', file=file)
        for row in table.get_table_to_print():
            for element in row:
                print('{:>6}'.format(element), file=file, end=' ')
            print(file=file)
        count = 1
        while table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            comment = table.iterate()
            print(comment, file=file)
            if comment == 'No solution':
                return
            for row in table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('Drop G:', file=file)
        table.drop_artificial_function()
        for row in table.get_table_to_print():
            for element in row:
                print('{:>6}'.format(element), file=file, end=' ')
            print(file=file)
        while table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            comment = table.iterate()
            print(comment, file=file)
            if comment == 'No solution':
                return
            for row in table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('Y vector:', file=file)
        for element in table.get_vector_answer():
            print('{:>6}'.format(str(element)), file=file, end=' ')
        print(file=file)
        if self.is_maximize:
            print('Max Z: {}'.format(str(table.get_function_answer())), file=file)
        else:
            print('Min Z: {}'.format(str(table.get_function_answer())), file=file)

    def do_gomori(self, file=None):
        self.print_enter(file)
        self.transform_to_positive_b()
        table = ArtificialBasis(self.matrix_a, self.matrix_b, self.matrix_c, self.signs, self.is_maximize)
        print('Initial:', file=file)
        for row in table.get_table_to_print():
            for element in row:
                print('{:>6}'.format(element), file=file, end=' ')
            print(file=file)
        count = 1
        while table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            comment = table.iterate()
            print(comment, file=file)
            if comment == 'No solution':
                return
            for row in table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('Drop G:', file=file)
        table.drop_artificial_function()
        for row in table.get_table_to_print():
            for element in row:
                print('{:>6}'.format(element), file=file, end=' ')
            print(file=file)
        while table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            comment = table.iterate()
            print(comment, file=file)
            if comment == 'No solution':
                return
            for row in table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('Using Gomori method:', file=file)
        table_data, rows_data, columns_data, task = table.get_data()
        gomori_table = Gomori(table_data, rows_data, columns_data, task)
        while gomori_table.can_be_iterated():
            print('Step {}:'.format(count), file=file)
            if not gomori_table.last_iteration():
                print(gomori_table.iterate_first(), file=file)
                for row in gomori_table.get_table_to_print():
                    for element in row:
                        print('{:>6}'.format(element), file=file, end=' ')
                    print(file=file)
            print(gomori_table.iterate_last(), file=file)
            for row in gomori_table.get_table_to_print():
                for element in row:
                    print('{:>6}'.format(element), file=file, end=' ')
                print(file=file)
            count += 1
        print('X vector:', file=file)
        for element in gomori_table.get_vector_answer():
            print('{:>6}'.format(str(element)), file=file, end=' ')
        print(file=file)
        if self.is_maximize:
            print('Max Z: {}'.format(str(gomori_table.get_function_answer())), file=file)
        else:
            print('Min Z: {}'.format(str(gomori_table.get_function_answer())), file=file)

from accessify import private
from ArtificialBasis import ArtificialBasis
from DualTask import DualTask
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
            print('Enter {} coefficients (1 for constant) for object function:'.format(self.variables_count + 1))
            buffer = input()
            equation = buffer.split()
            if len(equation) < self.variables_count + 1:
                print('Too few arguments')
                continue
            elif len(equation) > self.variables_count + 1:
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

    def enter_from_message(self, message: str):
        try:
            buffer = message.split('\n')
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

    def print_to_console(self):
        print('Your enter:')
        for i in range(self.equations_count):
            for j in range(self.variables_count):
                if j == 0 or self.matrix_a[i][j] < 0:
                    if self.matrix_a[i][j] == -1:
                        print('-x{}'.format(j + 1), end='')
                    elif self.matrix_a[i][j] == 1:
                        print('x{}'.format(j + 1), end='')
                    else:
                        print('{}x{}'.format(self.matrix_a[i][j], j + 1), end='')
                else:
                    if self.matrix_a[i][j] == 1:
                        print('+x{}'.format(j + 1), end='')
                    else:
                        print('+{}x{}'.format(self.matrix_a[i][j], j + 1), end='')
            print('{}{}'.format(self.signs[i], self.matrix_b[i]))
        print('Z(x)=', end='')
        for i in range(self.variables_count):
            if i == 0 or self.matrix_c[i] < 0:
                if self.matrix_c[i] == -1:
                    print('-x{}'.format(i + 1), end='')
                elif self.matrix_c[i] == 1:
                    print('x{}'.format(i + 1), end='')
                else:
                    print('{}x{}'.format(self.matrix_c[i], i + 1), end='')
            else:
                if self.matrix_c[i] == 1:
                    print('+x{}'.format(i + 1), end='')
                else:
                    print('+{}x{}'.format(self.matrix_c[i], i + 1), end='')
        if self.is_maximize:
            print(' -> max')
        else:
            print(' -> min')

    def print_to_file(self):
        file = open('answer.txt', 'w')
        file.write('Your enter:' + '\n')
        for i in range(self.equations_count):
            for j in range(self.variables_count):
                if j == 0 or self.matrix_a[i][j] < 0:
                    if self.matrix_a[i][j] == -1:
                        file.write('-x{}'.format(j + 1))
                    elif self.matrix_a[i][j] == 1:
                        file.write('x{}'.format(j + 1))
                    else:
                        file.write('{}x{}'.format(self.matrix_a[i][j], j + 1))
                else:
                    if self.matrix_a[i][j] == 1:
                        file.write('+x{}'.format(j + 1))
                    else:
                        file.write('+{}x{}'.format(self.matrix_a[i][j], j + 1))
            file.write('{}{}'.format(self.signs[i], self.matrix_b[i]) + '\n')
        file.write('Z(x)=')
        for i in range(self.variables_count):
            if i == 0 or self.matrix_c[i] < 0:
                if self.matrix_c[i] == -1:
                    file.write('-x{}'.format(i + 1))
                elif self.matrix_c[i] == 1:
                    file.write('x{}'.format(i + 1))
                else:
                    file.write('{}x{}'.format(self.matrix_c[i], i + 1))
            else:
                if self.matrix_c[i] == 1:
                    file.write('+x{}'.format(i + 1))
                else:
                    file.write('+{}x{}'.format(self.matrix_c[i], i + 1))
        if self.is_maximize:
            file.write(' -> max\n')
        else:
            file.write(' -> min\n')
        file.close()

    @private
    def transform_to_positive_b(self):
        for i in range(self.equations_count):
            if self.matrix_b[i] < 0:
                for j in range(self.variables_count):
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

    def do_artificial_basis(self, is_to_console: bool):
        self.transform_to_positive_b()
        file = None
        if not is_to_console:
            file = open('answer.txt', 'a')
        table = ArtificialBasis(self.matrix_a, self.matrix_b, self.matrix_c, self.signs, self.is_maximize)
        if is_to_console:
            print('Initial:')
            table.print()
        else:
            file.write('Initial:\n')
            tmp_table = table.get_table_to_print()
            for row in tmp_table:
                for element in row:
                    file.write('{:>6} '.format(element))
                file.write('\n')
        count = 1
        while table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            element = table.iterate()
            if is_to_console:
                print(element)
                table.print()
            else:
                file.write(element + '\n')
                tmp_table = table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('Drop G:')
        else:
            file.write('Drop G:\n')
        table.drop_artificial_function()
        if is_to_console:
            table.print()
        else:
            tmp_table = table.get_table_to_print()
            for row in tmp_table:
                for element in row:
                    file.write('{:>6} '.format(element))
                file.write('\n')
        while table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            element = table.iterate()
            if is_to_console:
                print(element)
                table.print()
            else:
                file.write(element + '\n')
                tmp_table = table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('X vector:')
            for element in table.get_vector_answer():
                print('{:>6}'.format(str(element)), end=' ')
            print()
            if self.is_maximize:
                print('Max Z: {}'.format(str(table.get_function_answer())))
            else:
                print('Min Z: {}'.format(str(table.get_function_answer())))
        else:
            file.write('X vector:\n')
            for element in table.get_vector_answer():
                file.write('{:>6} '.format(str(element)))
            file.write('\n')
            if self.is_maximize:
                file.write('Max Z: {}\n'.format(str(table.get_function_answer())))
            else:
                file.write('Min Z: {}\n'.format(str(table.get_function_answer())))
        if not is_to_console:
            file.close()

    def do_dual_task(self, is_to_console: bool):
        self.transform_for_dual_task()
        file = None
        table = None
        if is_to_console:
            table = DualTask(self.matrix_a, self.matrix_b, self.matrix_c, self.is_maximize)
            print('Initial:')
            table.print()
        else:
            table = DualTask(self.matrix_a, self.matrix_b, self.matrix_c, self.is_maximize, False)
            file = open('answer.txt', 'a')
            file.write('Initial:\n')
            tmp_table = table.get_table_to_print()
            for row in tmp_table:
                for element in row:
                    file.write('{:>6} '.format(element))
                file.write('\n')
        count = 1
        while table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            element = table.iterate()
            if is_to_console:
                print(element)
                table.print()
            else:
                file.write(element + '\n')
                tmp_table = table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('Drop G:')
        else:
            file.write('Drop G:\n')
        table.drop_artificial_function()
        if is_to_console:
            table.print()
        else:
            tmp_table = table.get_table_to_print()
            for row in tmp_table:
                for element in row:
                    file.write('{:>6} '.format(element))
                file.write('\n')
        while table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            element = table.iterate()
            if is_to_console:
                print(element)
                table.print()
            else:
                file.write(element + '\n')
                tmp_table = table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('Y vector:')
            for element in table.get_vector_answer():
                print('{:>6}'.format(str(element)), end=' ')
            print()
            if self.is_maximize:
                print('Max Z: {}'.format(str(table.get_function_answer())))
            else:
                print('Min Z: {}'.format(str(table.get_function_answer())))
        else:
            file.write('Y vector:\n')
            for element in table.get_vector_answer():
                file.write('{:>6} '.format(str(element)))
            file.write('\n')
            if self.is_maximize:
                file.write('Max Z: {}\n'.format(str(table.get_function_answer())))
            else:
                file.write('Min Z: {}\n'.format(str(table.get_function_answer())))
        if not is_to_console:
            file.close()

    def do_gomori(self, is_to_console: bool):
        self.transform_to_positive_b()
        file = None
        if not is_to_console:
            file = open('answer.txt', 'a')
        table = ArtificialBasis(self.matrix_a, self.matrix_b, self.matrix_c, self.signs, self.is_maximize)
        if is_to_console:
            print('Initial:')
            table.print()
        else:
            file.write('Initial:\n')
            tmp_table = table.get_table_to_print()
            for row in tmp_table:
                for element in row:
                    file.write('{:>6} '.format(element))
                file.write('\n')
        count = 1
        while table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            element = table.iterate()
            if is_to_console:
                print(element)
                table.print()
            else:
                file.write(element + '\n')
                tmp_table = table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('Drop G:')
        else:
            file.write('Drop G:\n')
        table.drop_artificial_function()
        if is_to_console:
            table.print()
        else:
            tmp_table = table.get_table_to_print()
            for row in tmp_table:
                for element in row:
                    file.write('{:>6} '.format(element))
                file.write('\n')
        while table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            element = table.iterate()
            if is_to_console:
                print(element)
                table.print()
            else:
                file.write(element + '\n')
                tmp_table = table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('Using Gomori method:')
        else:
            file.write('Using Gomori method:\n')
        table_data, rows_data, columns_data, task = table.get_data()
        gomori_table = Gomori(table_data, rows_data, columns_data, task)
        while gomori_table.can_be_iterated():
            if is_to_console:
                print('Step {}:'.format(count))
            else:
                file.write('Step {}:\n'.format(count))
            if is_to_console:
                element = gomori_table.iterate()
                print(element)
                gomori_table.print()
            else:
                file.close()
                element = gomori_table.iterate(False)
                file = open('answer.txt', 'a')
                file.write(element + '\n')
                tmp_table = gomori_table.get_table_to_print()
                for row in tmp_table:
                    for element in row:
                        file.write('{:>6} '.format(element))
                    file.write('\n')
            count += 1
        if is_to_console:
            print('X vector:')
            for element in gomori_table.get_vector_answer():
                print('{:>6}'.format(str(element)), end=' ')
            print()
            if self.is_maximize:
                print('Max Z: {}'.format(str(gomori_table.get_function_answer())))
            else:
                print('Min Z: {}'.format(str(gomori_table.get_function_answer())))
        else:
            file.write('X vector:\n')
            for element in gomori_table.get_vector_answer():
                file.write('{:>6} '.format(str(element)))
            file.write('\n')
            if self.is_maximize:
                file.write('Max Z: {}\n'.format(str(gomori_table.get_function_answer())))
            else:
                file.write('Min Z: {}\n'.format(str(gomori_table.get_function_answer())))
        if not is_to_console:
            file.close()

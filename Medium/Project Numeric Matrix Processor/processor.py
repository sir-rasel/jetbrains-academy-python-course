class MatrixCalc:    
    def __init__(self):
        self.main_acts = {
            '1':['. Add matrices', self.add_matrix],
            '2':['. Multiply matrix by a constant', self.const_mult_matrix],
            '3':['. Multiply matrices', self.mult_matrix],
            '4':['. Transpose matrix', self.init_transpose],
            '5':['. Calculate a determinant', self.det_matrix],
            '6':['. Inverse matrix', self.inv_matrix],
            '0':['. Exit', False]}

        self.transpose_acts = {
            '1':['. Main diagonal', self.transpose_main_diagonal],
            '2':['. Side diagonal', self.transpose_side_diagonal],
            '3':['. Vertical line', self.transpose_vertical_line],
            '4':['. Horizontal line', self.transpose_horizontal_line]}
        

    def start(self):
        self.print_acts(self.main_acts)

        action = input('Your choice: ')
        while self.main_acts[action][1]:
            self.main_acts[action][1]()
            print()
            self.print_acts(self.main_acts)
            action = input('Your choice: ')

    def print_acts(self, acts):
        for key in acts.keys():
            print(key, acts[key][0], sep='')

    def input_data(self, order=['first', 'second'], is_const=False):
        data = []
        
        for i in order:
            size = input(f'Enter size of {i} matrix: ').split()
            print(f'Enter {i} matrix: ')
            M = [list(map(float, input().split())) for _ in range(int(size[0]))]
            data.append(M)
        
        if is_const:
            const = float(input('Enter constant: '))
            data.append(const)
        
        return data

    def add_matrix(self):
        M1, M2 = self.input_data()
        
        size_1 = [len(M1), len(M1[0])]
        size_2 = [len(M2), len(M2[0])]
        
        if size_1 == size_2:
            print('The result is:')
            for rows in zip(M1, M2):
                print(*[sum(x) for x in zip(*rows)])
        else:
            print('The operation cannot be performed.')


    def const_mult_matrix(self):
        M, const = self.input_data(order=[''], is_const=True)
        
        print('The result is:')
        for row in M:
            print(*[cell * const for cell in row])

    def mult_matrix(self):
        M1, M2 = self.input_data()
        
        if len(M1[0]) == len(M2):
            M2 = list(zip(*M2))
            
            print('The result is:')
            for row1 in M1:
                print(*[sum(list(map(lambda x, y: x * y, row1, row2))) for row2 in M2])
        else:
            print('The operation cannot be performed.')

    def init_transpose(self):
        self.print_acts(self.transpose_acts)
        
        action = input('Your choice: ')
        self.transpose_acts[action][1]()
    
    def transpose_main_diagonal(self):
        M = self.input_data([''])[0]
        
        M = list(zip(*M))
        print('The result is:')
        for row in M:
            print(*[cell for cell in row])

    def transpose_side_diagonal(self):
        M = self.input_data([''])[0]
        
        M = list(zip(*M))
        print('The result is:')
        for row in reversed(M):
            print(*[cell for cell in reversed(row)])

    def transpose_vertical_line(self):
        M = self.input_data([''])[0]
        
        print('The result is:')
        for row in M:
            print(*[cell for cell in reversed(row)])

    def transpose_horizontal_line(self):
        M = self.input_data([''])[0]
        
        print('The result is:')
        for row in reversed(M):
            print(*[cell for cell in row])

    def det_matrix(self):
        M = self.input_data([''])[0]

        print('The result is:')
        print(self.determinant(M, 1))

    def determinant(self, matrix, mul):
        width = len(matrix)
        if width == 1:
            return mul * matrix[0][0]
        else:
            sign = -1
            sum = 0
            for i in range(width):
                m = []
                for j in range(1, width):
                    buff = []
                    for k in range(width):
                        if k != i:
                            buff.append(matrix[j][k])
                    m.append(buff)
                sign *= -1
                sum += mul * self.determinant(m, sign * matrix[0][i])
            return sum

    def transposeMatrix(self, m):
        return list(map(list,zip(*m)))

    def getMatrixMinor(self, m,i,j):
        return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

    def getMatrixDeternminant(self, m):
        #base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0]*m[1][1]-m[0][1]*m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1)**c)*m[0][c] * self.getMatrixDeternminant(self.getMatrixMinor(m,0,c))
        return determinant

    def getMatrixInverse(self, m):
        determinant = self.getMatrixDeternminant(m)
        #special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                    [-1*m[1][0]/determinant, m[0][0]/determinant]]

        #find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m,r,c)
                cofactorRow.append(((-1)**(r+c)) * self.getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c]/determinant
        return cofactors


    def inv_matrix(self):
        M = self.input_data([''])[0]

        det = self.determinant(M,1)
        if det == 0:
            print('The operation cannot be performed.')
        else:
            print('The result is:')
            M = self.getMatrixInverse(M)
            for row in M:
                print(*[cell for cell in row])


if __name__ == '__main__':
    matrix_calc = MatrixCalc()
    matrix_calc.start()

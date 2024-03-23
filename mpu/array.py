import random

EPSILON = 1e-9

class array():
    def __init__(self, values: list) -> None:
        self.values = values
        self.n = len(values)
        self.m = len(values[0])
    
    def __iadd__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        for i in range(self.n):
            for j in range(self.m):
                self.values[i][j] += other.values[i][j]
        return self
    
    def __add__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        
        return [[self.values[i][j] + other.values[i][j] for j in range(self.m)] for i in range(self.n)]

    def __sub__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        
        return [[self.values[i][j] - other.values[i][j] for j in range(self.m)] for i in range(self.n)]
    
    def __isub__(self, other):
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        for i in range(self.n):
            for j in range(self.m):
                self.values[i][j] -= other.values[i][j]
        return self

    def __mul__(self, other):
        if isinstance(other, array):
            if self.m != other.n:
                raise ValueError("Array dimensions must agree")
            else:
                return [[sum([self.values[i][k] * other.values[k][j] for k in range(self.m)]) for j in range(other.m)] for i in range(self.n)]
        else:  
            for i in range(self.n):
                for j in range(self.m):
                    print(self.values[i][j], type(self.values[i][j]), other, type(other), self.values[i][j] * other)
                    self.values[i][j] *= other
        return self
        
    
    def __truediv__(self, other):
        return self * (1 / other)
    
    def __str__(self):
        return "".join([str(self.values[i]) + "\n" for i in range(self.n)])
                   
    def __abs__(self):
        return sum([sum([abs(self.values[i][j]) for j in range(self.m)]) for i in range(self.n)])
    
    def __pow__(self, other):
        result = [[0 for _ in range(self.m)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                result[i][j] = self.values[i][j] ** other
        return array(result)

    def __eq__(self, other):
        for i in range(self.n):
            for j in range(self.m):
                if abs(self.values[i][j] - other.values[i][j]) > EPSILON:
                    return False
        return True
    
    def T(self):
        return array([[self.values[j][i] for j in range(self.n)] for i in range(self.m)])
    
    def __getitem__(self, key):
        return self.values[key]
    
    def round(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.values[i][j] < EPSILON:
                    self.values[i][j] = 0
                elif abs(self.values[i][j] - 1) < EPSILON:
                    self.values[i][j] = 1
        
        return self

def Id(n):
    return array([[1 if i == j else 0 for j in range(n)] for i in range(n)])

def diag(values):
    n = len(values)
    return array([[values[i] if i == j else 0 for j in range(n)] for i in range(n)])

def cofactor_matrix(A, i, j):
    return array([[A.values[x][y] for y in range(A.m) if y != j] for x in range(A.n) if x != i])

def det(A):
    if A.n == 1:
        return A.values[0][0]
    elif A.n == 2:
        return A.values[0][0] * A.values[1][1] - A.values[0][1] * A.values[1][0]
    else:
        return sum([(-1) ** i * A.values[i][0] * det(cofactor_matrix(A, i, 0)) for i in range(A.m)])

def cofactor_det_matrix(A):
    return array([[(-1) ** (i + j) * det(cofactor_matrix(A, j, i)) for i in range(A.n)] for j in range(A.m)])

def inv(A):
    return (cofactor_det_matrix(A).T() / det(A))

def random_matrix(n = 0, m = 0):
    if n == 0 and m == 0:
        return random.random()
    else:
        return array([[random.random() for _ in range(m)] for _ in range(n)])

if __name__ == "__main__":
    a = array([[1, 2, 3], 
               [4, 10, 6],
               [7, 8, 9]])
    
    print(inv(a) * a == Id(3))
    print(random_matrix(10, 10))
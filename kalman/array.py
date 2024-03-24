EPSILON = 1e-9

class array():
    def __init__(self, values: list) -> None:
        self.values = values
        self.n = len(values)
        self.m = len(values[0])
    
    def __iadd__(self, other: "array") -> "array":
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        for i in range(self.n):
            for j in range(self.m):
                self.values[i][j] += other.values[i][j]
        return self
    
    def __add__(self, other: "array") -> "array":
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        
        return array([[self.values[i][j] + other.values[i][j] for j in range(self.m)] for i in range(self.n)])

    def __sub__(self, other: "array") -> "array":
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        
        return array([[self.values[i][j] - other.values[i][j] for j in range(self.m)] for i in range(self.n)])
    
    def __isub__(self, other) -> "array":
        if self.n != other.n or self.m != other.m:
            raise ValueError("Array dimensions must agree")
        for i in range(self.n):
            for j in range(self.m):
                self.values[i][j] -= other.values[i][j]
        return self

    def __imul__(self, other) -> "array":
        if isinstance(other, array):
            if self.m != other.n:
                raise ValueError("Array dimensions must agree")
            else:
                self.values = [[sum([self.values[i][k] * other.values[k][j] for k in range(self.m)]) for j in range(other.m)] for i in range(self.n)]
                self.n = len(self.values)
                self.m = len(self.values[0])
        else:  
            for i in range(self.n):
                for j in range(self.m):
                    self.values[i][j] *= other
        
        return self
    
    def __mul__(self, other) -> "array":
        if isinstance(other, array):
            if self.m != other.n:
                raise ValueError("Array dimensions must agree")
            else:
                return array([[sum([self.values[i][k] * other.values[k][j] for k in range(self.m)]) for j in range(other.m)] for i in range(self.n)])
        else:
            return array([[self.values[i][j] * other for j in range(self.m)] for i in range(self.n)])
        
    def copy(self) -> "array":
        return array([self.values[i].copy() for i in range(self.n)])
    
    def __truediv__(self, other) -> "array":
        return self * (1 / other)
    
    def __str__(self) -> str:
        return "".join([str(self.values[i]) + "\n" for i in range(self.n)])
                   
    def __abs__(self):
        if self.n != 1 and self.m != 1:
            raise ValueError("Array must be a vector")
        if self.n == 1:
            return sum([(self.values[0][i]) ** 2 for i in range(self.m)]) ** .5
        if self.m == 1:
            return sum([(self.values[i][0]) ** 2 for i in range(self.n)]) ** .5
    
    def __eq__(self, other) -> bool:
        for i in range(self.n):
            for j in range(self.m):
                if abs(self.values[i][j] - other.values[i][j]) > EPSILON:
                    return False
        return True
    
    @property
    def dim(self) -> tuple:
        return (len(self.values), len(self.values[0]))

    @property
    def T(self) -> "array":
        return array([[self.values[j][i] for j in range(self.n)] for i in range(self.m)])
    
    def __getitem__(self, key) -> list:
        return self.values[key]
    
    def round(self) -> "array":
        for i in range(self.n):
            for j in range(self.m):
                if self.values[i][j] < EPSILON:
                    self.values[i][j] = 0
                elif abs(self.values[i][j] - 1) < EPSILON:
                    self.values[i][j] = 1
        
        return self

def new_array(n: int, m: int) -> array:
    return array([[0 for _ in range(m)] for _ in range(n)])

def Id(n: int) -> array:
    return array([[1 if i == j else 0 for j in range(n)] for i in range(n)])

def diag(values: list) -> array:
    n = len(values)
    return array([[values[i] if i == j else 0 for j in range(n)] for i in range(n)])

def cofactor_matrix(A: array, i: int, j: int) -> array:
    return array([[A.values[x][y] for y in range(A.m) if y != j] for x in range(A.n) if x != i])

def det(A: array) -> float:
    if A.n == 1:
        return A.values[0][0]
    elif A.n == 2:
        return A.values[0][0] * A.values[1][1] - A.values[0][1] * A.values[1][0]
    else:
        return sum([(-1) ** i * A.values[i][0] * det(cofactor_matrix(A, i, 0)) for i in range(A.m)])

def cofactor_det_matrix(A: array) -> array:
    return array([[(-1) ** (i + j) * det(cofactor_matrix(A, j, i)) for i in range(A.n)] for j in range(A.m)])

def inv(A: array) -> array:
    if A.n == 1:
        return array([[1 / A.values[0][0]]])
    return (cofactor_det_matrix(A).T / det(A))

import random

def random_matrix(n: int = 0, m: int = 0):
    if n == 0 and m == 0:
        return random.random()
    else:
        return array([[random.random() for _ in range(m)] for _ in range(n)])

if __name__ == "__main__":
    a = array([[1, 2, 3], 
               [4, 10, 6],
               [7, 8, 9]])

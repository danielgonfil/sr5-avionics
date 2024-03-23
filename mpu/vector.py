class mat2x2():
    def __init__(self) -> None:
        self.

class mat1x2():
    def __init__(self) -> None:
        pass

class mat2x1():
    def __init__(self) -> None:
        pass

class vec3d():
    def __init__(self, x = 0.0, y = 0.0, z = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self
    
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self
    
    def __add__(self, other):
        return vec(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):    
        return vec(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return vec(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float):
        return vec(self.x / other, self.y / other, self.z / other)

    def __pow__(self, other):
        return vec(self.x ** other, self.y ** other, self.z ** other)

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

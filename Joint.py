# class represent skeleton joint


class Joint(object):

    def __init__(self, type, x, y, z):
        self.type = type
        self.x = x
        self.y = y
        self.z = z
        self.visible = 0 if x == y == z == 0 else 1

    def __str__(self):
        return self.type+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)

    def joint_to_array(self):
        arr = [self.type, self.x, self.y, self.z]
        return arr

    def is_joint_all_zeros(self):
        if self.x == 0 and self.y == 0 and self.z == 0:
            return True
        else:
            return False


import os
import sys
import platform

PYTHONPATH = os.path.dirname(os.path.dirname(os.__file__))
print(PYTHONPATH)
print(platform.python_version())

# Where am I
Directory = os.path.dirname(sys._getframe().f_code.co_filename)

os.chdir(Directory)

if not os.path.isdir(Directory + '\\venv'):
   os.system('python -m venv venv')

os.system('venv\\Scripts\\activate')  # <-- for Windows

os.system('python.exe -m pip install --upgrade pip')
os.system('python -m pip install -r requirements.txt')
os.system('python -m pip install -r requirements.extra.txt')
os.system('python -m pip install -Ue .')
os.system('python -m pip install numba==0.48')

print("")
input('Installed Requirements. Press Enter to exit . . . ')

"""
def shape_broadcast(shape1, shape2):
    """
    Broadcast two shapes to create a new union shape.

    Args:
        shape1 (tuple) : first shape
        shape2 (tuple) : second shape

    Returns:
        tuple : broadcasted shape

    Raises:
        IndexingError : if cannot broadcast
    """

    # TODO: Implement for Task 2.4.

    if shape1 == shape2:
        # Nothing to do
        return shape1

    Broadcast_Shape = []

    if len(shape1) < len(shape2):

        s1 = list(shape1)
        s2 = list(shape2)

        shape1 = tuple(([1] * (len(s2) - len(s1))) + s1)

        for i in range(-len(shape2), 0)[::-1]:
            if shape1[i] == shape2[i] or shape1[i] == 1 or shape2[i] == 1:
                Broadcast_Shape.insert(0, max(shape1[i], shape2[i]))
            else:
                print('shape1 == shape2', shape1, shape2, Broadcast_Shape)
                # assert shape1 == shape2
                raise IndexError  # ("Incompatible Broadcast")

        return tuple(Broadcast_Shape)

    elif len(shape1) > len(shape2):

        s1 = list(shape1)
        s2 = list(shape2)

        shape2 = tuple(([1] * (len(s1) - len(s2))) + s2)

        for i in range(-len(shape1), 0)[::-1]:
            if shape1[i] == shape2[i] or shape1[i] == 1 or shape2[i] == 1:
                Broadcast_Shape.insert(0, max(shape1[i], shape2[i]))
            else:
                print('shape1 == shape2', shape1, shape2, Broadcast_Shape)
                # assert shape1 == shape2
                raise IndexError  # ("Incompatible Broadcast")

        return tuple(Broadcast_Shape)

    else:

        for i in range(-len(shape1), 0)[::-1]:
            if shape1[i] == shape2[i] or shape1[i] == 1 or shape2[i] == 1:
                Broadcast_Shape.insert(0, max(shape1[i], shape2[i]))
            else:
                print('shape1 == shape2', shape1, shape2, Broadcast_Shape)
                # assert shape1 == shape2
                raise IndexError  # ("Incompatible Broadcast")

        return tuple(Broadcast_Shape)
        
        
        
    ####################################################################

    #ret = [0]
    #max_length = max(len(shape1), len(shape2))

    #if len(shape1) == max_length:
        #shape = shape1
    #else:
        #shape = shape2

    #shape_diff = max(max_length - len(shape1), max_length - len(shape2))

    #for i in range(-1, -1 * max_length - 1 + shape_diff, -1):
        #if shape1[i] == shape2[i] or shape1[i] == 1 or shape2[i] == 1:
            #ret.insert(0, max(shape1[i], shape2[i]))
        #else:
            #raise IndexError("Incompatible Broadcast")

    #for i in range(-1 * max_length - 1 + shape_diff, -1 * max_length - 1, -1):
        #ret.insert(0, shape[i])

    #ret = tuple(*[ret[0:-1]])

    #return ret
    ####################################################################

"""

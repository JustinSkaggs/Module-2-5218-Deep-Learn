import numpy as np
import minitorch
from .tensor_data import (
    count,
    index_to_position,
    broadcast_index,
    shape_broadcast,
    # MAX_DIMS,
)


def tensor_map(fn):
    """
    Higher-order tensor map function ::

      fn_map = tensor_map(fn)
      fn_map(out, ... )

    Args:
        fn: function from float-to-float to apply
        out (array): storage for out tensor
        out_shape (array): shape for out tensor
        out_strides (array): strides for out tensor
        in_storage (array): storage for in tensor
        in_shape (array): shape for in tensor
        in_strides (array): strides for in tensor

    Returns:
        None : Fills in `out`

    """

    def _map(out, out_shape, out_strides, in_storage, in_shape, in_strides):

        # TODO: Implement for Task 2.2.

        if all(out_shape == in_shape):

            for idx, val in enumerate(in_storage):
                out[idx] = fn(val)
        else:

            for i in range(len(out)):

                index = [0] * len(out_shape)
                count(i, out_shape, index)

                # Broadcast tensor in_shape
                in_index = [0] * len(in_shape)
                broadcast_index(index, out_shape, in_shape, in_index)

                in_pos = index_to_position(in_index, in_strides)

                out[i] = fn(in_storage[in_pos])

    return _map


def map(fn):
    """
    Higher-order tensor map function ::

      fn_map = map(fn)
      b = fn_map(a)


    Args:
        fn: function from float-to-float to apply.
        a (:class:`TensorData`): tensor to map over
        out (:class:`TensorData`): optional, tensor data to fill in,
               should broadcast with `a`

    Returns:
        :class:`TensorData` : new tensor data
    """

    f = tensor_map(fn)

    def ret(a, out=None):
        if out is None:
            out = a.zeros(a.shape)
        f(*out.tuple(), *a.tuple())
        return out

    return ret


def tensor_zip(fn):
    """
    Higher-order tensor zipWith (or map2) function. ::

      fn_zip = tensor_zip(fn)
      fn_zip(out, ...)


    Args:
        fn: function mapping two floats to float to apply
        out (array): storage for `out` tensor
        out_shape (array): shape for `out` tensor
        out_strides (array): strides for `out` tensor
        a_storage (array): storage for `a` tensor
        a_shape (array): shape for `a` tensor
        a_strides (array): strides for `a` tensor
        b_storage (array): storage for `b` tensor
        b_shape (array): shape for `b` tensor
        b_strides (array): strides for `b` tensor

    Returns:
        None : Fills in `out`
    """

    def _zip(
        out,
        out_shape,
        out_strides,
        a_storage,
        a_shape,
        a_strides,
        b_storage,
        b_shape,
        b_strides,
    ):
        # TODO: Implement for Task 2.2.

        out_a = []
        out_b = []

        for i in range(len(out)):

            # Use count(…) to go from i to index according to out_shape
            index = [0] * len(out_shape)
            count(i, out_shape, index)

            # Broadcast tensor a
            a_index = [0] * len(a_shape)
            broadcast_index(index, out_shape, a_shape, a_index)
            a_pos = index_to_position(a_index, a_strides)
            out_a.append(a_storage[a_pos])

            # Broadcast tensor b
            b_index = [0] * len(b_shape)
            broadcast_index(index, out_shape, b_shape, b_index)
            b_pos = index_to_position(b_index, b_strides)
            out_b.append(b_storage[b_pos])

        out_storage = [fn(out_a[j], out_b[j]) for j in range(len(out_a))]

        for idx, val in enumerate(out_storage):
            out[idx] = val

    return _zip


def zip(fn):
    """
    Higher-order tensor zip function ::

      fn_zip = zip(fn)
      c = fn_zip(a, b)

    Args:
        fn: function from two floats-to-float to apply
        a (:class:`TensorData`): tensor to zip over
        b (:class:`TensorData`): tensor to zip over

    Returns:
        :class:`TensorData` : new tensor data
    """

    f = tensor_zip(fn)

    def ret(a, b):
        if a.shape != b.shape:
            c_shape = shape_broadcast(a.shape, b.shape)
        else:
            c_shape = a.shape
        out = a.zeros(c_shape)
        f(*out.tuple(), *a.tuple(), *b.tuple())
        return out

    return ret


def tensor_reduce(fn):
    """
    Higher-order tensor reduce function. ::

      fn_reduce = tensor_reduce(fn)
      c = fn_reduce(out, ...)

    Args:
        fn: reduction function mapping two floats to float
        out (array): storage for `out` tensor
        out_shape (array): shape for `out` tensor
        out_strides (array): strides for `out` tensor
        a_storage (array): storage for `a` tensor
        a_shape (array): shape for `a` tensor
        a_strides (array): strides for `a` tensor
        reduce_shape (array): shape of reduction (1 for dimension kept, shape value for dimensions summed out)
        reduce_size (int): size of reduce shape

    Returns:
        None : Fills in `out`

    """

    def _reduce(
        out,
        out_shape,
        out_strides,
        a_storage,
        a_shape,
        a_strides,
        reduce_shape,
        reduce_size,
    ):
        """
            # Broadcast tensor in_shape
            in_index = [0] * len(in_shape)
            broadcast_index(index, out_shape, in_shape, in_index)

            in_pos = index_to_position(in_index, in_strides)

            out[i] = fn(in_storage[in_pos])


                def my_reduce(ls):

        ls = [start] + list(ls)

        x = ls[0]

        for i in range(1, len(ls)):

            x = fn(x, ls[i])

        return x

    return my_reduce

        [fn(x, a_storage[i])  for i in range(len(a_storage))]

        """
        # TODO: Implement for Task 2.2.

        if len(out) == 1:

            out[0] = minitorch.operators.reduce(fn, 0.0)(a_storage)

        else:

            for i in range(len(out)):

                out_storage = []

                for j in range(reduce_size):

                    out_index = list(np.zeros(len(out_shape)))
                    count(i, out_shape, out_index)

                    reduce_index = list(np.zeros(len(reduce_shape)))
                    count(j, reduce_shape, reduce_index)

                    for idx, val in enumerate(reduce_index):
                        out_index[idx] += val

                    idx_to_pos = index_to_position(out_index, a_strides)
                    out_storage.append(a_storage[idx_to_pos])

                out[i] = minitorch.operators.reduce(fn, 0.0)(list(out_storage))

    return _reduce


def reduce(fn, start=0.0):
    """
    Higher-order tensor reduce function. ::

      fn_reduce = reduce(fn)
      reduced = fn_reduce(a, dims)


    Args:
        fn: function from two floats-to-float to apply
        a (:class:`TensorData`): tensor to reduce over
        dims (list, optional): list of dims to reduce
        out (:class:`TensorData`, optional): tensor to reduce into

    Returns:
        :class:`TensorData` : new tensor data
    """

    f = tensor_reduce(fn)

    # START Code Update
    def ret(a, dims=None, out=None):
        old_shape = None
        if out is None:
            out_shape = list(a.shape)
            for d in dims:
                out_shape[d] = 1
            # Other values when not sum.
            out = a.zeros(tuple(out_shape))
            out._tensor._storage[:] = start
        else:
            old_shape = out.shape
            diff = len(a.shape) - len(out.shape)
            out = out.view(*([1] * diff + list(old_shape)))

        # Assume they are the same dim
        assert len(out.shape) == len(a.shape)

        # Create a reduce shape / reduce size
        reduce_shape = []
        reduce_size = 1
        for i, s in enumerate(a.shape):
            if out.shape[i] == 1:
                reduce_shape.append(s)
                reduce_size *= s
            else:
                reduce_shape.append(1)

        # Apply
        f(*out.tuple(), *a.tuple(), reduce_shape, reduce_size)

        if old_shape is not None:
            out = out.view(*old_shape)
        return out

    return ret
    # END Code Update


class TensorOps:
    map = map
    zip = zip
    reduce = reduce

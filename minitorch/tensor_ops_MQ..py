from .tensor_data import (
    count,
    index_to_position,
    broadcast_index,
    shape_broadcast,
    # MAX_DIMS,
    # TensorData
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
        if (out_shape == in_shape).all() and len(out_shape) == len(in_shape):
            for i, tmp in enumerate(in_storage):
                out[i] = fn(tmp)
        elif (out_shape == shape_broadcast(out_shape, in_shape)).all():
            out_index = [0] * len(out_shape)
            position = 0
            for i, tmp in enumerate(out):
                count(position, out_shape, out_index)

                in_index = [0] * len(in_shape)
                broadcast_index(out_index, out_shape, in_shape, in_index)
                out[i] = fn(in_storage[index_to_position(in_index, in_strides)])

                position = 1
        else:
            raise NotImplementedError('Not implemented map operator between these shapes')
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
        if isinstance((a_shape == b_shape), bool):
            if a_shape == b_shape:
                for i, tmp in enumerate(out):
                    out[i] = fn(a_storage[i], b_storage[i])
            else:
                tmp_out = [0] * len(out_shape)
                position = 0
                for i, tmp in enumerate(out):
                    count(position, out_shape, tmp_out)

                    a_out = [0] * len(a_shape)
                    broadcast_index(tmp_out, out_shape, a_shape, a_out)
                    b_out = [0] * len(b_shape)
                    broadcast_index(tmp_out, out_shape, b_shape, b_out)
                    a_position = index_to_position(a_out, a_strides)
                    b_position = index_to_position(b_out, b_strides)
                    out[i] = fn(a_storage[a_position], b_storage[b_position])

                    position = 1
        elif (a_shape == b_shape).all() and len(a_shape) == len(b_shape):
            for i, tmp in enumerate(out):
                out[i] = fn(a_storage[i], b_storage[i])
        else:
            tmp_out = [0] * len(out_shape)
            position = 0
            for i, tmp in enumerate(out):
                count(position, out_shape, tmp_out)

                a_out = [0] * len(a_shape)
                broadcast_index(tmp_out, out_shape, a_shape, a_out)
                b_out = [0] * len(b_shape)
                broadcast_index(tmp_out, out_shape, b_shape, b_out)
                a_position = index_to_position(a_out, a_strides)
                b_position = index_to_position(b_out, b_strides)
                out[i] = fn(a_storage[a_position], b_storage[b_position])
                position = 1
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
        if len(out) == 1:
            for tmp in a_storage:
                out[0] = fn(tmp, out[0])
        elif len(out) <= len(a_storage):
            for i in range(len(out)):
                index = [0] * len(out_shape)
                count(i, out_shape, index)
                r_index = [0] * len(reduce_shape)
                position = 0
                for j in range(reduce_size):
                    count(position, reduce_shape, r_index)
                    for h, k in enumerate(r_index):
                        index[h] += k
                    out[i] = fn(out[i], a_storage[index_to_position(index, a_strides)])
                    for h, k in enumerate(r_index):
                        index[h] -= k
                    position = 1
        else:
            raise NotImplementedError('Not implemented reducing to a bigger set se Tensor->expand(),  chose to use map')
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
            # print(out.tuple())
        return out

    return ret
    # END Code Update


class TensorOps:
    map = map
    zip = zip
    reduce = reduce

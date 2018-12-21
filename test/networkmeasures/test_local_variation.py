
import teneto
import numpy as np
import pytest


def test_bursty():
    t1 = np.arange(0, 60, 2)
    t2 = [1, 8, 9, 32, 33, 34, 39, 40, 50, 51, 52, 55]

    G = np.zeros([3, 3, 60])
    G[0, 1, t1] = 1
    G[1, 2, t2] = 1
    ict = teneto.networkmeasures.intercontacttimes(G)
    B1 = teneto.networkmeasures.local_variation(ict)
    B2 = teneto.networkmeasures.local_variation(G)

    assert B1[0, 1] == B2[0, 1]
    assert B1[1, 2] == B2[1, 2]
    assert B1[0, 1] == -1
    assert B1[0, 1] == B3[0, 1]
    assert np.isnan(B3[1, 2]) == 1
    assert B1[1, 2] == (np.std(np.diff(t2))-np.mean(np.diff(t2))) / \
        (np.mean(np.diff(t2))+np.std(np.diff(t2)))

    with pytest.raises(ValueError):
        teneto.networkmeasures.local_variation(G, calc='communities')

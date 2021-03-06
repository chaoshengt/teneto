
import teneto
import numpy as np


def test_volatility():
    # Test volatility
    G = np.zeros([3, 3, 3])
    G[0, 1, [0, 1, 2]] = 1
    G[0, 2, 1] = 1
    G[1, 2, 2] = 1
    G = G + G.transpose([1, 0, 2])
    # global volatility
    v_global = teneto.networkmeasures.volatility(G)
    # v volatility per time point
    v_time = teneto.networkmeasures.volatility(G, calc='pertime')
    v_tr = np.array([2/6, 4/6])
    if not v_global == np.mean(v_tr):
        raise AssertionError()
    if not all(v_time == v_tr):
        raise AssertionError()
    # event displacement
    v_er_tr = np.array([0, 2/6, 2/6])
    v_er = teneto.networkmeasures.volatility(
        G, calc='event_displacement', event_displacement=0)
    if not all(v_er == v_er_tr):
        raise AssertionError()
    # vol per node
    v_edge = teneto.networkmeasures.volatility(G, calc='edge')
    if not np.all(v_edge == np.mean(np.abs(np.diff(G)), axis=-1)):
        raise AssertionError()
    v_node = teneto.networkmeasures.volatility(G, calc='node')
    if not np.all(v_node == np.mean(
        np.mean(np.abs(np.diff(G)), axis=-1), axis=-1)):
        raise AssertionError()


def test_volatility_communities():
    # Test volatility
    G = np.zeros([4, 4, 3])
    G[0, 1, [0, 2]] = 1
    G[2, 3, [0, 1]] = 1
    G[1, 2, [1, 2]] = 1
    G = G + G.transpose([1, 0, 2])
    communities = [0, 0, 1, 1]
    # global volatility
    v_bet = teneto.networkmeasures.volatility(
        G, calc='betweencommunities', communities=communities)
    v_within = teneto.networkmeasures.volatility(
        G, calc='withincommunities', communities=communities)
    v_communities = teneto.networkmeasures.volatility(
        G, calc='communities', communities=communities)
    if not len(v_bet) == G.shape[-1] - 1:
        raise AssertionError()
    if not len(v_within) == G.shape[-1] - 1:
        raise AssertionError()
    if not np.all(v_communities.shape == (
        len(np.unique(communities)), len(np.unique(communities)), G.shape[-1] - 1)):
        raise AssertionError()
    # Hardcode answer due to hamming distance and predefined matrix
    if not np.all(v_within == [0.5, 1]):
        raise AssertionError()
    if not np.all(v_bet == [0.25, 0]):
        raise AssertionError()
    if not np.all(v_communities[:, :, 0] == np.array([[1, 0.25], [0.25, 0]])):
        raise AssertionError()
    if not np.all(v_communities[:, :, 1] == np.array([[1, 0], [0, 1]])):
        raise AssertionError()

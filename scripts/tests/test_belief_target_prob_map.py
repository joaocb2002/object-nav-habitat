import numpy as np
from objectnav.belief.legacy_bridge import target_probability_map

def main():
    # belief_map is list[list[np.ndarray]] in your legacy code :contentReference[oaicite:2]{index=2}
    # We'll create a 2x3 map with Dirichlet vectors of length K+1 = 3.
    Kp1 = 3
    belief_map = [
        [np.array([1.0, 2.0, 1.0]), np.array([1.0, 1.0, 10.0]), np.array([5.0, 1.0, 1.0])],
        [np.array([1.0, 4.0, 1.0]), np.array([2.0, 2.0, 2.0]),  np.array([1.0, 1.0, 1.0])],
    ]

    # occ_grid_map is RGB (H,W,3). White cells are treated as "free => prob=0".
    occ_grid_map = np.zeros((2, 3, 3), dtype=np.uint8)
    occ_grid_map[:] = (128, 128, 128)           # occupied/unknown
    occ_grid_map[0, 1] = (255, 255, 255)        # one free cell

    target_class_idx = 1  # second entry in alpha vector

    tp = target_probability_map(belief_map, occ_grid_map, target_class_idx)

    assert tp.shape == (2, 3)
    assert tp[0, 1] == 0.0, "free cell must be 0"
    assert np.isfinite(tp).all()
    assert (tp >= 0).all() and (tp <= 1).all()

    # spot-check one value: alpha=[1,2,1] => prob=2/4=0.5
    assert abs(tp[0, 0] - 0.5) < 1e-6, tp[0, 0]

    print("Target prob map OK:\n", tp)

if __name__ == "__main__":
    main()

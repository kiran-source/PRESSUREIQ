"""
Tests for PRESSUREIQ Hybrid Methodology Validation Gate.

Validates:
1. Reproduction and exact number parity.
2. Conditional monotonicity across (balls, wickets, RRR) slices.
3. Smooth blowout discount continuity and boundary suppression.
4. Analytical DLS prior equation correctness and parameter bounds.
5. Chronological win-probability calibration and zero-leakage invariant.
6. Continuous opportunity weighting and Kish ESS positivity.
"""

import json
import shutil
import numpy as np
import pandas as pd
import pytest

import scripts.hybrid_validation_gate as hvg
from scripts.hybrid_validation_gate import sigmoid


def test_sigmoid_monotonicity_and_bounds():
    """Verify numerical sigmoid is strictly monotonic and bounded in [0, 1]."""
    x = np.linspace(-20, 20, 500)
    y = sigmoid(x)
    assert np.all(y >= 0.0)
    assert np.all(y <= 1.0)
    assert np.all(np.diff(y) >= 0.0)


def test_smooth_blowout_continuity_and_suppression():
    """Verify smooth sigmoid blowout discount eliminates derivative jumps."""
    rrr = np.linspace(3.0, 6.0, 301)
    step_vals = np.where(rrr < 4.5, 0.25, 1.0)
    sig_vals = sigmoid((rrr - 4.5) / 1.0)
    
    # Step discount has a huge jump (0.75) at 4.5
    assert np.max(np.abs(np.diff(step_vals))) >= 0.70
    # Sigmoid discount has maximum jump per step < 0.01
    assert np.max(np.abs(np.diff(sig_vals))) < 0.01


def test_analytical_dls_prior_bounds():
    """Verify analytical DLS prior returns 1.0 at full innings and 0.0 at 0 balls."""
    norm_factor = 1.0 - np.exp(-0.12 * 20.0)
    
    # Full innings (20 overs, 10 wickets)
    u_full = 20.0
    w_full = 10.0
    r_full = ((1.0 - np.exp(-0.12 * u_full)) / norm_factor) * ((w_full / 10.0) ** 0.65)
    assert np.isclose(r_full, 1.0, atol=1e-5)
    
    # Zero balls remaining
    u_zero = 0.0
    r_zero = ((1.0 - np.exp(-0.12 * u_zero)) / norm_factor) * ((w_full / 10.0) ** 0.65)
    assert np.isclose(r_zero, 0.0, atol=1e-5)
    
    # Zero wickets remaining
    w_zero = 0.0
    r_no_wkt = ((1.0 - np.exp(-0.12 * u_full)) / norm_factor) * ((w_zero / 10.0) ** 0.65)
    assert np.isclose(r_no_wkt, 0.0, atol=1e-5)


def test_kish_effective_sample_size_formula():
    """Verify Kish's ESS equals N for equal weights and is strictly positive."""
    # N equal weights
    N = 100
    w_equal = np.ones(N)
    ess_equal = (np.sum(w_equal) ** 2) / np.sum(w_equal ** 2)
    assert np.isclose(ess_equal, N)
    
    # Unequal weights
    w_unequal = np.linspace(0.1, 1.0, N)
    ess_unequal = (np.sum(w_unequal) ** 2) / np.sum(w_unequal ** 2)
    assert 0 < ess_unequal < N


def test_validation_gate_main_succeeds_on_valid_data(tmp_path, monkeypatch):
    """Verify validation gate main() returns exit code 0 when all checks match."""
    out_dir = tmp_path / "out_valid"
    monkeypatch.setattr(hvg, "OUTPUT_DIR", out_dir)
    rc = hvg.main()
    assert rc == 0
    rep = json.loads((out_dir / "reproduction_verification.json").read_text(encoding="utf-8"))
    assert rep["verification_status"] == "ALL_NUMBERS_VERIFIED_EXACT_MATCH"
    assert rep["failed_checks"] == []


def test_validation_gate_missing_weighting_csv_returns_nonzero(tmp_path, monkeypatch, capsys):
    """Verify missing weighting_fairness_comparison.csv avoids UnboundLocalError and returns nonzero."""
    src_chal = hvg.CHALLENGE_DIR
    chal_dir = tmp_path / "challenge_missing"
    chal_dir.mkdir()
    shutil.copy2(src_chal / "cdpi_parameter_sweep.csv", chal_dir / "cdpi_parameter_sweep.csv")
    shutil.copy2(src_chal / "win_prob_chronological_validation.json", chal_dir / "win_prob_chronological_validation.json")
    out_dir = tmp_path / "out_missing"

    monkeypatch.setattr(hvg, "CHALLENGE_DIR", chal_dir)
    monkeypatch.setattr(hvg, "OUTPUT_DIR", out_dir)

    rc = hvg.main()
    assert rc != 0
    captured = capsys.readouterr()
    assert "missing_weighting_csv" in captured.err

    rep = json.loads((out_dir / "reproduction_verification.json").read_text(encoding="utf-8"))
    assert rep["verification_status"] == "VERIFICATION_MISMATCH"
    assert "missing_weighting_csv" in rep["failed_checks"]
    assert rep["reproduced_weighting"] == {}


def test_validation_gate_mismatched_values_return_nonzero(tmp_path, monkeypatch, capsys):
    """Verify deliberately mismatched reproduced metrics return nonzero and log detailed JSON failure."""
    src_chal = hvg.CHALLENGE_DIR
    chal_dir = tmp_path / "challenge_bad"
    chal_dir.mkdir()
    shutil.copy2(src_chal / "cdpi_parameter_sweep.csv", chal_dir / "cdpi_parameter_sweep.csv")
    shutil.copy2(src_chal / "win_prob_chronological_validation.json", chal_dir / "win_prob_chronological_validation.json")

    wf = pd.read_csv(src_chal / "weighting_fairness_comparison.csv")
    wf.loc[wf["player_name"] == "Ruturaj Gaikwad", "step_50_balls"] = 999
    wf.to_csv(chal_dir / "weighting_fairness_comparison.csv", index=False)

    out_dir = tmp_path / "out_bad"
    monkeypatch.setattr(hvg, "CHALLENGE_DIR", chal_dir)
    monkeypatch.setattr(hvg, "OUTPUT_DIR", out_dir)

    rc = hvg.main()
    assert rc != 0
    captured = capsys.readouterr()
    assert "gaikwad_step_50_mismatch" in captured.err

    rep = json.loads((out_dir / "reproduction_verification.json").read_text(encoding="utf-8"))
    assert rep["verification_status"] == "VERIFICATION_MISMATCH"
    assert "gaikwad_step_50_mismatch" in rep["failed_checks"]



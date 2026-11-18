"""
Comprehensive test of all 13 navigation views using Streamlit AppTest.
Tests session state and rendering for every view.
"""
import sys
from pathlib import Path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from streamlit.testing.v1 import AppTest
from src.dashboard.design_tokens import NAV_LABELS

def test_all_views():
    print(f"Testing all {len(NAV_LABELS)} navigation views...")
    results = {}
    
    for i, label in enumerate(NAV_LABELS, 1):
        print(f"\n[{i}/{len(NAV_LABELS)}] Testing view: '{label}'")
        at = AppTest.from_file("streamlit_app.py", default_timeout=30)
        at.run()
        
        # Set active page in session state and rerun
        at.session_state["active_page"] = label
        at.run()
        
        exceptions = list(at.exception)
        if exceptions:
            print(f"  FAILED with {len(exceptions)} exception(s):")
            for ex in exceptions:
                print(f"    {ex.value}")
            results[label] = False
        else:
            print(f"  PASSED with 0 exceptions! (Rendered {len(at.markdown)} markdowns, {len(at.dataframe)} dataframes)")
            results[label] = True

    print("\n" + "=" * 60)
    print("ALL 13 NAVIGATION VIEWS TEST RESULTS:")
    print("=" * 60)
    all_passed = True
    for label, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {label}")
        if not passed:
            all_passed = False

    return all_passed

if __name__ == "__main__":
    ok = test_all_views()
    sys.exit(0 if ok else 1)

from client import LongevityBiomarkerEstimatorClient
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

def main():
    estimator = LongevityBiomarkerEstimatorClient()
    print("=== LONGEVITY PHENOTYPIC BIOLOGICAL AGE ESTIMATOR ===")

    # Profile: 40-year-old individual with healthy biomarker panel
    healthy_panel = {
        "albumin_g_dl": 4.6,
        "creatinine_mg_dl": 0.85,
        "glucose_mg_dl": 88.0,
        "crp_mg_l": 0.45,
        "lymphocyte_pct": 34.0,
        "mcv_fl": 86.0,
        "rdw_pct": 12.1,
        "alp_u_l": 62.0,
        "wbc_10e3_ul": 5.2
    }

    res = estimator.calculate_biological_age(40.0, healthy_panel)
    print()
    print(f"Chronological Age: {res['chronological_age']} yrs")
    print(f"Phenotypic Biological Age: {res['estimated_biological_age']} yrs (Delta: {res['age_acceleration_delta']:+0.1f} yrs)")
    print(f"Pace of Aging: {res['hazard_profile']} (Hazard Ratio: {res['mortality_hazard_ratio']}x)")

if __name__ == "__main__":
    main()

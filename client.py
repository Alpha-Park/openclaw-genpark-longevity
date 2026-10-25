import sys, math
sys.stdout.reconfigure(encoding='utf-8')

class LongevityBiomarkerEstimatorClient:
    """
    Phenotypic Biological Age Estimator based on Morgan Levine's mortality hazard model.
    Evaluates key blood biomarkers (Albumin, Creatinine, Glucose, hs-CRP, Lymphocyte %, MCV, RDW, ALP, WBC)
    to compute biological age acceleration and mortality hazard ratios.
    """
    def __init__(self):
        pass

    def calculate_biological_age(self, chronological_age, biomarkers):
        """
        biomarkers: dict with albumin_g_dl, creatinine_mg_dl, glucose_mg_dl,
        crp_mg_l, lymphocyte_pct, mcv_fl, rdw_pct, alp_u_l, wbc_10e3_ul
        """
        # Linear biomarker hazard coefficient approximation
        alb = float(biomarkers.get("albumin_g_dl", 4.5))
        creat = float(biomarkers.get("creatinine_mg_dl", 0.9))
        glu = float(biomarkers.get("glucose_mg_dl", 90.0))
        crp = float(biomarkers.get("crp_mg_l", 1.0))
        lymp = float(biomarkers.get("lymphocyte_pct", 32.0))
        mcv = float(biomarkers.get("mcv_fl", 88.0))
        rdw = float(biomarkers.get("rdw_pct", 12.5))
        alp = float(biomarkers.get("alp_u_l", 65.0))
        wbc = float(biomarkers.get("wbc_10e3_ul", 6.0))

        # Hazard mortality index score
        xb = (
            -1.99
            + (0.0804 * chronological_age)
            - (0.0336 * alb)
            + (0.0095 * creat)
            + (0.0019 * glu)
            + (0.0954 * math.log(max(0.1, crp)))
            - (0.0120 * lymp)
            + (0.0268 * mcv)
            + (0.3306 * rdw)
            + (0.0019 * alp)
            + (0.0554 * wbc)
        )

        mortality_score = 1.0 - math.exp(-math.exp(xb))
        # Derive phenotypic age
        phenotypic_age = 141.50 + (math.log(-0.00553 * math.log(max(1e-6, 1.0 - mortality_score))) / 0.090165)
        phenotypic_age = max(18.0, min(100.0, phenotypic_age))

        age_acceleration = phenotypic_age - chronological_age
        hazard_profile = "OPTIMAL_LONGEVITY" if age_acceleration <= -3.0 else ("NORMAL_PACE" if age_acceleration <= 2.0 else "ACCELERATED_AGING")

        return {
            "status": "success",
            "chronological_age": chronological_age,
            "estimated_biological_age": round(phenotypic_age, 1),
            "age_acceleration_delta": round(age_acceleration, 1),
            "hazard_profile": hazard_profile,
            "mortality_hazard_ratio": round(math.exp(max(-1.0, min(2.0, age_acceleration * 0.08))), 2)
        }

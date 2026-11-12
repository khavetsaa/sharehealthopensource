# Model card: SHARE PPH risk score (v0.1, placeholder)

- **Purpose:** classify PPH risk during labour as green, amber or red, with reasons.
- **Current version:** transparent logistic score with illustrative weights (`share/risk.py`). Not trained on patient data. Not validated. Not for clinical use.
- **Inputs:** EHG fatigue index (median frequency drop), oxytocin hours, haemoglobin, previous PPH, labour duration.
- **Planned training data:** consented, pseudonymised recordings from SHARE's silent study in Kenyan hospitals (target 300 women), stored in Kenya.
- **Planned evaluation:** sensitivity, specificity and calibration for PPH; subgroup checks by anaemia, body mass index and skin tone; false alarm rate per shift.
- **Change control:** the model is locked after validation; any update goes through documented re-validation (IEC 62304, Good Machine Learning Practice).

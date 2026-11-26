# v9 FGSM-only adversarial training -- final summary (auto-generated from this run)

**Verdict:** SUCCEEDED against FGSM on the main seed (C1-C7 met; C8 multi-seed pending Cell 18)

Training epsilon 4/255, target epsilon 2/255, selected epoch 13, test videos 400.

| epsilon (/255) | clean-trained acc | FGSM-trained acc | clean-trained AUC | FGSM-trained AUC |
|---|---|---|---|---|
| 0 | 0.907 | 0.920 | 0.975 | 0.973 |
| 0.25 | 0.907 | 0.920 | 0.975 | 0.973 |
| 0.5 | 0.285 | 0.863 | 0.117 | 0.937 |
| 1 | 0.228 | 0.845 | 0.088 | 0.937 |
| 1.5 | 0.190 | 0.830 | 0.066 | 0.923 |
| 2 | 0.147 | 0.825 | 0.046 | 0.911 |
| 4 | 0.055 | 0.797 | 0.018 | 0.889 |
| 8 | 0.190 | 0.723 | 0.073 | 0.829 |
| 12 | 0.328 | 0.657 | 0.206 | 0.726 |
| 16 | 0.417 | 0.585 | 0.337 | 0.637 |

Criteria:
- C1: met -- clean test AUC FGSM-trained 0.9727 vs clean-trained 0.9745 (ratio 0.998, need >= 0.97)
- C2: met -- validation FGSM AUC @target = 0.9047
- C3: met -- validation FGSM AUC gain over clean-trained = +0.8884
- C4: met -- FGSM accuracy above clean accuracy + margin at: no epsilon
- C5: met -- AUC delta @2/255 = +0.8641 [+0.8261, +0.8959]; @4/255 = +0.8714 [+0.8354, +0.9040]
- C6: met -- eval zero-grad 0, eval non-finite grads 0, training NaN-skipped steps 0
- C7: met -- @2/255, attack-aware threshold 0.597: fake recall 166/200 = 0.830, real specificity 162/200 = 0.810 (need both >= 0.35)

Scope: FGSM only. PGD was deliberately excluded; nothing here supports a claim of general adversarial robustness.


**C8 (multi-seed):** met -- gate passed in 2/2 seeds {42: True, 1: True}; skipped: [(2, "'fgsm_only' needs ~1.37 h, only 0.04 h left after the reserve")]

**Final verdict:** SUCCEEDED against FGSM (C1-C8 met, 2 seed(s))

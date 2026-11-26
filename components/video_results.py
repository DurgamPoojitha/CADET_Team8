"""
components/video_results.py
Full video Results content extracted from pages/results.py.
Call render() from the Video tab in pages/results.py.
"""
import streamlit as st
import json
import csv
import re
import html
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_RESULTS_DIR = _ROOT / "models" / "results"
_FIGURES_DIR = _RESULTS_DIR / "figures"


def clean_text(value) -> str:
    """Strips any HTML tags and trims whitespace."""
    if value is None:
        return ""
    text = re.sub(r"<[^>]+>", "", str(value))
    return text.strip()


@st.cache_data(ttl=3600)
def _load_json(path: Path):
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_data(ttl=3600)
def _load_csv(path: Path):
    if not path.exists():
        return None
    rows = []
    try:
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned_row = {clean_text(k): clean_text(v) for k, v in row.items()}
                rows.append(cleaned_row)
        return rows
    except Exception:
        return None


def _na(val, fmt=None) -> str:
    cleaned = clean_text(val)
    if cleaned == "" or cleaned.lower() == "none":
        return "not available"
    if fmt:
        try:
            return fmt.format(float(cleaned))
        except (ValueError, TypeError):
            return cleaned
    return cleaned


def _format_eps(val) -> str:
    cleaned = clean_text(val)
    try:
        fval = float(cleaned)
        eps_str = f"{fval:.2f}".rstrip("0").rstrip(".")
        if eps_str == "":
            eps_str = "0"
        return f"{eps_str}/255"
    except (ValueError, TypeError):
        return f"{cleaned}/255" if cleaned else "not available"


def _format_pct_1dec(val) -> str:
    cleaned = clean_text(val)
    try:
        return f"{float(cleaned):.1%}"
    except (ValueError, TypeError):
        return _na(cleaned)


def _format_4dec(val) -> str:
    cleaned = clean_text(val)
    try:
        return f"{float(cleaned):.4f}"
    except (ValueError, TypeError):
        return _na(cleaned)


def _format_delta_4dec(val) -> str:
    cleaned = clean_text(val)
    try:
        return f"{float(cleaned):+.4f}"
    except (ValueError, TypeError):
        return _na(cleaned)


def _render_chip(status_text: str) -> str:
    """Returns an HTML badge using the project CSS classes."""
    norm = status_text.strip().upper()
    if norm == "MET":
        return '<span class="chip-met">MET</span>'
    elif norm == "NOT MET":
        return '<span class="chip-not-met">NOT MET</span>'
    return f'<span style="font-family:var(--mono);color:var(--ink-muted)">{html.escape(status_text)}</span>'


def render():
    st.caption(
        "All numbers are read directly from the model output files in `models/results/`. "
        "Nothing is hardcoded or estimated."
    )

    # ── Load data ────────────────────────────────────────────────────────────
    summary     = _load_json(_RESULTS_DIR / "fgsm_v9_results_summary.json")
    criteria    = _load_json(_RESULTS_DIR / "acceptance_criteria.json")
    multiseed   = _load_csv(_RESULTS_DIR / "fgsm_v9_multiseed.csv")
    per_method  = _load_csv(_RESULTS_DIR / "fgsm_v9_per_method.csv")
    paired_csv  = _load_csv(_RESULTS_DIR / "fgsm_v9_paired_comparison.csv")

    # ── 1. Clean Test Performance ─────────────────────────────────────────────
    st.markdown("### Clean test performance")
    kn = summary.get("key_numbers", {}) if summary else {}
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Clean-trained model**")
        st.metric("Clean test AUC",      _na(kn.get("clean_test_auc_clean_trained"), "{:.4f}"))
        st.metric("Clean test accuracy", _na(kn.get("Clean-trained_acc_eps0"),        "{:.1%}"))
    with c2:
        st.markdown("**FGSM-trained model**")
        st.metric("Clean test AUC",      _na(kn.get("clean_test_auc_fgsm_trained"),  "{:.4f}"))
        st.metric("Clean test accuracy", _na(kn.get("FGSM-trained_acc_eps0"),        "{:.1%}"))

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── 2. Accuracy & AUC vs FGSM epsilon ─────────────────────────────────────
    st.markdown("### Accuracy and AUC vs FGSM epsilon")
    if paired_csv:
        try:
            import pandas as pd
            import altair as alt

            df_paired = pd.DataFrame(paired_csv)
            df_paired["eps_255"]          = pd.to_numeric(df_paired["eps_255"], errors="coerce")
            df_paired["acc_clean_trained"] = pd.to_numeric(df_paired["acc_clean_trained"], errors="coerce")
            df_paired["acc_fgsm_trained"]  = pd.to_numeric(df_paired["acc_fgsm_trained"], errors="coerce")
            df_paired["auc_clean_trained"] = pd.to_numeric(df_paired["auc_clean_trained"], errors="coerce")
            df_paired["auc_fgsm_trained"]  = pd.to_numeric(df_paired["auc_fgsm_trained"], errors="coerce")
            df_paired = df_paired.dropna(subset=["eps_255"]).sort_values("eps_255")

            ch_col1, ch_col2 = st.columns(2)
            with ch_col1:
                st.markdown("**Accuracy vs FGSM ε (/255)**")
                df_acc = df_paired.melt(
                    id_vars=["eps_255"],
                    value_vars=["acc_clean_trained", "acc_fgsm_trained"],
                    var_name="model", value_name="accuracy"
                )
                df_acc["Model"] = df_acc["model"].map({
                    "acc_clean_trained": "Clean-trained",
                    "acc_fgsm_trained":  "FGSM-trained"
                })
                chart_acc = alt.Chart(df_acc).mark_line(point=True).encode(
                    x=alt.X("eps_255:Q", title="ε (/255)"),
                    y=alt.Y("accuracy:Q", title="Accuracy", scale=alt.Scale(domain=[0, 1])),
                    color=alt.Color("Model:N", scale=alt.Scale(
                        domain=["Clean-trained", "FGSM-trained"],
                        range=["#C45A00", "#3D6B4F"]
                    )),
                    tooltip=["eps_255", "Model", alt.Tooltip("accuracy:Q", format=".3f")]
                ).properties(height=260)
                st.altair_chart(chart_acc, use_container_width=True)

            with ch_col2:
                st.markdown("**ROC-AUC vs FGSM ε (/255)**")
                df_auc = df_paired.melt(
                    id_vars=["eps_255"],
                    value_vars=["auc_clean_trained", "auc_fgsm_trained"],
                    var_name="model", value_name="auc"
                )
                df_auc["Model"] = df_auc["model"].map({
                    "auc_clean_trained": "Clean-trained",
                    "auc_fgsm_trained":  "FGSM-trained"
                })
                chart_auc = alt.Chart(df_auc).mark_line(point=True).encode(
                    x=alt.X("eps_255:Q", title="ε (/255)"),
                    y=alt.Y("auc:Q", title="ROC-AUC", scale=alt.Scale(domain=[0, 1])),
                    color=alt.Color("Model:N", scale=alt.Scale(
                        domain=["Clean-trained", "FGSM-trained"],
                        range=["#C45A00", "#3D6B4F"]
                    )),
                    tooltip=["eps_255", "Model", alt.Tooltip("auc:Q", format=".3f")]
                ).properties(height=260)
                st.altair_chart(chart_auc, use_container_width=True)

            # Tabular breakdown with right-aligned numeric columns
            thead = (
                "<table><thead><tr>"
                "<th>Epsilon</th>"
                "<th style='text-align:right'>Clean-trained Acc</th>"
                "<th style='text-align:right'>Clean-trained AUC</th>"
                "<th style='text-align:right'>FGSM-trained Acc</th>"
                "<th style='text-align:right'>FGSM-trained AUC</th>"
                "<th style='text-align:right'>AUC Delta</th>"
                "</tr></thead><tbody>"
            )
            tbody = ""
            for _, r in df_paired.iterrows():
                eps_str = _format_eps(r["eps_255"])
                c_acc = _format_pct_1dec(r["acc_clean_trained"])
                c_auc = _format_4dec(r["auc_clean_trained"])
                f_acc = _format_pct_1dec(r["acc_fgsm_trained"])
                f_auc = _format_4dec(r["auc_fgsm_trained"])
                d_auc = _format_delta_4dec(r.get("auc_delta"))
                tbody += (
                    f"<tr>"
                    f"<td style='font-family:var(--mono)'>{html.escape(eps_str)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(c_acc)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(c_auc)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(f_acc)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(f_auc)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(d_auc)}</td>"
                    f"</tr>"
                )
            st.markdown(thead + tbody + "</tbody></table>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not render chart: {e}")
    else:
        st.warning("Robustness metrics not available.")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── 3. Per-manipulation breakdown ─────────────────────────────────────────
    st.markdown("### Per-manipulation breakdown (clean, ε = 0)")
    if per_method:
        filtered = [r for r in per_method if clean_text(r.get("eps_255", "")) in ("0.0", "0", "0.00")]
        if filtered:
            thead = (
                "<table><thead><tr>"
                "<th>Model</th>"
                "<th>Method</th>"
                "<th style='text-align:right'>Videos</th>"
                "<th style='text-align:right'>Detection Rate</th>"
                "<th style='text-align:right'>95 % CI</th>"
                "<th style='text-align:right'>Mean P(fake)</th>"
                "</tr></thead><tbody>"
            )
            tbody = ""
            for r in filtered:
                m_model  = clean_text(r.get("model", "not available"))
                m_method = clean_text(r.get("method", "not available"))
                n_vids   = clean_text(r.get("n_videos", "not available"))
                rate_str = _format_pct_1dec(r.get("rate"))
                ci_lo    = _format_4dec(r.get("ci_lo"))
                ci_hi    = _format_4dec(r.get("ci_hi"))
                mean_p   = _format_4dec(r.get("mean_p_fake"))
                ci_str   = f"[{ci_lo}, {ci_hi}]"

                tbody += (
                    f"<tr>"
                    f"<td>{html.escape(m_model)}</td>"
                    f"<td>{html.escape(m_method)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(n_vids)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(rate_str)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(ci_str)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(mean_p)}</td>"
                    f"</tr>"
                )
            st.markdown(thead + tbody + "</tbody></table>", unsafe_allow_html=True)
        else:
            st.info("No clean-condition rows found in per-method CSV.")
    else:
        st.warning("Per-manipulation breakdown not available.")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── 4. Acceptance criteria C1–C8 ─────────────────────────────────────────
    st.markdown("### Acceptance criteria (C1–C8)")
    crit_source = summary.get("criteria", {}) if (summary and "criteria" in summary) else (criteria if criteria else {})
    if crit_source:
        criteria_defs = {
            "C1": "C1 — Clean AUC retained (FGSM ≥ 0.97× clean)",
            "C2": "C2 — Validation FGSM AUC @ target ε ≥ 0.75",
            "C3": "C3 — Validation FGSM AUC gain over clean ≥ 0.1",
            "C4": "C4 — No label leak (FGSM acc ≤ clean acc + 2%)",
            "C5": "C5 — Paired bootstrap CI lower bound > 0",
            "C6": "C6 — No NaN/Inf; zero-gradient = 0",
            "C7": "C7 — Attack-aware: recall & specificity ≥ 35%",
            "C8": "C8 — Multi-seed gate passes in ≥ 2 seeds",
        }
        thead = (
            "<table><thead><tr>"
            "<th>ID</th><th>Criterion</th><th style='text-align:center'>Status</th><th>Evidence</th>"
            "</tr></thead><tbody>"
        )
        tbody = ""
        for key, label in criteria_defs.items():
            crit_data = crit_source.get(key, {})
            if isinstance(crit_data, dict):
                met_val = crit_data.get("met")
                raw_ev  = crit_data.get("evidence", "not available")
            else:
                met_val = None
                raw_ev  = str(crit_data) if crit_data else "not available"

            # Plain text status
            if met_val is True or str(met_val).lower() == "true":
                status_text = "MET"
            elif met_val is False or str(met_val).lower() == "false":
                status_text = "NOT MET"
            else:
                status_text = "not available"

            chip_html = _render_chip(status_text)
            evidence_clean = clean_text(raw_ev)

            tbody += (
                f"<tr><td style='font-family:var(--mono);font-size:.8rem'>{html.escape(key)}</td>"
                f"<td style='font-size:.82rem'>{html.escape(label)}</td>"
                f"<td style='text-align:center'>{chip_html}</td>"
                f"<td style='font-family:var(--mono);font-size:.72rem'>{html.escape(evidence_clean)}</td></tr>"
            )
        st.markdown(thead + tbody + "</tbody></table>", unsafe_allow_html=True)
    else:
        st.warning("Acceptance criteria not available.")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── 5. Multi-seed Results ────────────────────────────────────────────────
    st.markdown("### Multi-seed verification results")
    if multiseed:
        thead = (
            "<table><thead><tr>"
            "<th>Seed</th><th>Mode</th><th>Model</th>"
            "<th style='text-align:center'>Gate Passed</th>"
            "<th style='text-align:right'>Epsilon</th>"
            "<th style='text-align:right'>Accuracy</th>"
            "<th style='text-align:right'>ROC-AUC</th>"
            "<th style='text-align:right'>F1 Score</th>"
            "</tr></thead><tbody>"
        )
        tbody = ""
        for r in multiseed:
            eps_clean = clean_text(r.get("eps_255", ""))
            if eps_clean in ("0.0", "0", "2.0", "2", "4.0", "4"):
                gate_val = clean_text(r.get("gate_passed", ""))
                if gate_val.lower() == "true":
                    status_text = "MET"
                elif gate_val.lower() == "false":
                    status_text = "NOT MET"
                else:
                    status_text = gate_val if gate_val else "not available"

                chip_html = _render_chip(status_text)
                seed_str  = clean_text(r.get("seed", "not available"))
                mode_str  = clean_text(r.get("mode", "not available"))
                model_str = clean_text(r.get("model", "not available"))
                eps_str   = _format_eps(eps_clean)
                acc_str   = _format_pct_1dec(r.get("accuracy"))
                auc_str   = _format_4dec(r.get("roc_auc"))
                f1_str    = _format_4dec(r.get("f1"))

                tbody += (
                    f"<tr>"
                    f"<td style='font-family:var(--mono)'>{html.escape(seed_str)}</td>"
                    f"<td>{html.escape(mode_str)}</td>"
                    f"<td>{html.escape(model_str)}</td>"
                    f"<td style='text-align:center'>{chip_html}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(eps_str)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(acc_str)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(auc_str)}</td>"
                    f"<td style='font-family:var(--mono);text-align:right'>{html.escape(f1_str)}</td>"
                    f"</tr>"
                )
        st.markdown(thead + tbody + "</tbody></table>", unsafe_allow_html=True)
    else:
        st.warning("Multi-seed results not available.")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── 6. Saved Figures ─────────────────────────────────────────────────────
    st.markdown("### Training figures")
    if _FIGURES_DIR.exists():
        fig_files = sorted(_FIGURES_DIR.glob("*.png"))
        if fig_files:
            key_figs = {
                "fig06_accuracy_vs_eps.png":        "Figure 6: Accuracy vs FGSM Epsilon",
                "fig07_auc_vs_eps.png":             "Figure 7: ROC-AUC vs FGSM Epsilon",
                "fig10_clean_vs_fgsm_trained.png":  "Figure 10: Clean-trained vs FGSM-trained Comparison",
                "fig12_per_manipulation.png":       "Figure 12: Detection Rate by Manipulation Method",
                "fig11_confusion_matrices.png":     "Figure 11: Confusion Matrices under Clean Input",
            }
            for fname, caption in key_figs.items():
                fig_path = _FIGURES_DIR / fname
                if fig_path.exists():
                    st.image(str(fig_path), caption=caption, use_container_width=True)
                    st.markdown('<div style="margin:.6rem 0"></div>', unsafe_allow_html=True)
            remaining = [f for f in fig_files if f.name not in key_figs]
            if remaining:
                with st.expander(f"All saved figures ({len(fig_files)} total)"):
                    for fig_path in fig_files:
                        st.image(str(fig_path), caption=fig_path.stem.replace("_", " ").title(),
                                 use_container_width=True)
        else:
            st.info("No figures found in models/results/figures/.")
    else:
        st.warning("Figures directory not available.")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

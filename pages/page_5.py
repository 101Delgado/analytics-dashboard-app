# IMPORTS
import streamlit as st 
from utils.math_utils import SimularTeoremaRaoBlackwell

# display code on screen 
st.title("Rao–Blackwell Theorem")

st.write(r"""Consider the geometric distribution with probability mass function:"""
)

st.latex(r"""f(x; \theta) = (1 - p)^{x-1} p, \quad x = 1, 2, 3, \ldots.""")

st.write(r"""Consider the following estimators:"""
)

st.write(r"""Initial estimator: $\hat{\theta}_1 = X_1$.""")

st.write(r"""Sufficient statistic: $U = \sum_{i=1}^{n} X_i$.""")

st.write(r"""Improved estimator: $\hat{\theta}_2 = \frac{1}{n} \sum_{i=1}^{n} X_i$.""")

st.subheader("Python code for the simulation")

codigo = """
    import numpy as np
    import pandas as pd
    import streamlit as st

    # Experiment setup
    np.random.seed(42)
    theta = 4.0
    p = 1.0 / theta
    n = 20
    M = 10000

    # 1. Generate M = 10,000 samples of size n = 20 from a geometric distribution
    muestras = np.random.geometric(p=p, size=(M, n))

    # 2. Initial estimator: X_1 (first element of each sample)
    theta_1 = muestras[:, 0]

    # 3. Sufficient statistic U = sum of elements in each sample
    U = np.sum(muestras, axis=1)

    # 4. Rao-Blackwell improved estimator: E(X_1 | U) = U / n = X_bar
    theta_star = U / n

    # 5. Compute empirical variances
    var_theta_1 = np.var(theta_1, ddof=1)
    var_theta_star = np.var(theta_star, ddof=1)
    reduccion_porcentual = ((var_theta_1 - var_theta_star) / var_theta_1) * 100

    # Show results in a Streamlit table
    st.title("Rao–Blackwell Theorem Results (Exercise 5)")

    data_e5 = {
        "Estimator": ["Initial Estimator (X₁)", "Improved Estimator (Rao-Blackwell)"],
        "Expression": ["\\hat{\\theta}_1 = X_1", "\\hat{\\theta}^* = \\overline{X} = \\frac{U}{n}"],
        "Empirical Variance": [f"{var_theta_1:.4f}", f"{var_theta_star:.4f}"],
        "Efficiency": ["Low efficiency (uses 1 data point)", f"High efficiency (variance reduction of {reduccion_porcentual:.1f}% )"]
    }

    df_e5 = pd.DataFrame(data_e5)
    st.dataframe(df_e5, use_container_width=True)
"""

st.code(codigo, language='python')

st.subheader("Purpose of the Rao–Blackwell Theorem:")

st.write(r"""This theorem states that if you have an unbiased estimator for a parameter
    and condition it on a sufficient statistic ($U$), the resulting estimator remains
    unbiased and has variance less than or equal to the original estimator
    ($\text{Var}(\hat{\theta}^*) \le \text{Var}(\hat{\theta}_1)$).""")

st.write(r"""The initial estimator $\hat{\theta}_1 = X_1$ uses only the first observation
    of the sample, wasting information from the rest of the data and resulting in
    a high variance.""")

st.write(r"""Conditioning on the sufficient statistic $U = \sum X_i$ yields the sample mean
    $\overline{X}$, which leverages all available sample information.""")

tabla_de_resultados = SimularTeoremaRaoBlackwell(theta=4.0, n=20, M=10000, seed=42)

st.subheader("Simulation results")

st.table(tabla_de_resultados)

st.subheader("Conclusion on the improvement")

st.write(r"""The simulation clearly shows that the empirical variance of the sample mean
    ($\text{Var}(\overline{X}) \approx 0.5956$) is substantially lower than the variance
    of the initial estimator ($\text{Var}(X_1) \approx 11.9141$). This represents about a 95%
    variance reduction, empirically confirming the Rao–Blackwell Theorem.""")

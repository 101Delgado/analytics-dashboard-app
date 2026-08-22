# IMPORTS 
import streamlit as st

# display code on screen 
st.title("Cramér–Rao")

st.subheader("Code to compute bias and empirical variance")

codigo = """
    import numpy as np

    # Experiment setup
    np.random.seed(42)  # For reproducibility
    theta = 4.0
    p = 1.0 / theta
    n = 30
    M = 10000

    # 1. Simulate M = 10,000 samples of size n = 30 from a geometric distribution
    # Note: np.random.geometric uses p as the success parameter.
    muestras = np.random.geometric(p=p, size=(M, n))

    # 2. Compute the sample mean X_bar for each of the M samples
    x_bar = np.mean(muestras, axis=1)
    theta_hat = x_bar

    # 3. Estimate the bias of theta_hat
    esperanza_estimador = np.mean(theta_hat)
    sesgo = esperanza_estimador - theta

    # 4. Compute the empirical variance of the estimator
    varianza_empirica = np.var(theta_hat, ddof=1)

    # 5. Compute the theoretical Cramér-Rao lower bound: [theta * (theta - 1)] / n
    cramer_rao_bound = (theta * (theta - 1)) / n
"""

st.code(codigo, language='python')

st.subheader("Simulation results")

# Markdown table using st.markdown
tabla_markdown = """
| Variable or Metric | Symbol / Expression | Obtained / Theoretical Value | Description and Interpretation |
| :--- | :---: | :---: | :--- |
| **True Parameter** | $\\theta$ | $4.0000$ | Fixed value used for the population parameter of interest. |
| **Success Parameter** | $p = \\frac{1}{\\theta}$ | $0.2500$ | Success probability for the simulated geometric distribution. |
| **Number of Simulations** | $M$ | $10\\,000$ | Number of Monte Carlo repetitions. |
| **Sample Size** | $n$ | $30$ | Number of observations per sample. |
| **Theoretical Mean** | $\\mathbb{E}(X)$ | $4.0000$ | Theoretical mean of a geometric variable with $\\theta = 4$. |
| **Empirical Mean (Estimator)** | $\\mathbb{E}(\\hat{\\theta}) = \\overline{X}$ | $4.0037$ | Average of sample means across the $10\\,000$ simulations. |
| **Estimated Bias** | $\\text{Bias}(\\hat{\\theta})$ | $0.0037$ | Difference between empirical mean and true $\\theta$. Being close to zero confirms $\\overline{X}$ is an unbiased estimator. |
"""

st.markdown(tabla_markdown)

st.write(r"""Consider a random variable $X$ with a geometric distribution where
    the parameter is $p = \frac{1}{\theta}$. For this distribution, the expected value is:""")

st.latex(r'''
    E[X] = \frac{1}{p} = \theta''')

st.write(r"""Therefore, the sample mean $\overline{X}$ is an unbiased estimator
    of $\theta$, since $\mathbb{E}(\overline{X}) = \theta$.""")

st.subheader("Bias estimation")

st.write(r"""The bias of an estimator $\hat{\theta} = \overline{X}$ is defined as:"""
)

st.latex(r'''
    \text{Bias}(\hat{\theta}) = \mathbb{E}(\hat{\theta}) - \theta''')

st.write(r"""Since $\hat{\theta}$ is theoretically unbiased, the expected bias is 0.
    In the simulation results with $M = 10\,000$ samples, the empirical bias
    is very small (around 0.0036), which empirically confirms the estimator's
    unbiased property.""")

st.subheader("Empirical Variance vs Cramér–Rao Lower Bound")

st.write(r"""Empirical variance obtained in the simulation $\approx 0.4079$""")

st.write("""The theoretical Cramér–Rao lower bound:""")

st.latex(r'''\text{CRLB} = \frac{\theta(\theta - 1)}{n} = \frac{4(4 - 1)}{30} = \frac{12}{30} = 0.40''')

st.write(r"""Because the estimator's empirical variance ($\approx 0.4079$) is
     very close to the Cramér–Rao lower bound (0.40), we conclude that the
     sample mean $\overline{X}$ is an efficient estimator for parameter $\theta$
     of the geometric distribution under the evaluated sample size conditions.""")

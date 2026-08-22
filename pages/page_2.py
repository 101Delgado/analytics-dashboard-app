# IMPORTS
import streamlit as st
from utils.math_utils import CalcularIntervalo

# Data
n = 64
x_bar = 42
sigma = 8

# display code on screen
st.title("Confidence intervals for the population mean")

st.write("Recalling the formula for the confidence interval for the population mean with known sigma:")
st.latex(r'''
    \bar{x} \pm Z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}
''')

st.subheader("Code to compute the confidence interval")

codigo = """
    import scipy.stats as stats
    import numpy as np

    # Data
    n = 64
    x_bar = 42
    sigma = 8

    # function to compute the confidence interval
    def CalcularIntervalo(confianza, n, x_bar, sigma):
        alpha = 1 - confianza
        z = stats.norm.ppf(1 - alpha / 2)
        error = z * (sigma / np.sqrt(n))
        return (x_bar - error, x_bar + error)
"""

st.code(codigo, language='python')

st.write("""This code defines the function `CalcularIntervalo` in
         `utils/math_utils.py`, which is imported at the top of this file
         to be used below.
""")

# Results
inter_1 = CalcularIntervalo(0.95, n, x_bar, sigma)
inter_2 = CalcularIntervalo(0.99, n, x_bar, sigma)

st.subheader("Interpretation of results")
st.write(rf"""There is a 95% confidence level that the true population
         mean delivery time is between {inter_1[0]:.2f} and {inter_1[1]:.2f} minutes.
         This means that if we repeated sampling many times, 95% of the
         calculated intervals would contain the true mean delivery time.
""")

st.write(rf"""When increasing the confidence level to 99%, the critical Z value
         increases (from ~1.96 to ~2.58). This increases the margin of error,
         producing the 99% interval: {inter_2[0]:.2f} to {inter_2[1]:.2f} minutes.
""")

st.write(r"""The 99% interval is wider than the 95% interval. This is consistent
         with statistical theory: to be more certain (99% vs 95%) that the
         population parameter lies inside our interval, we must cover a larger
         range of values, sacrificing precision for greater confidence.
""")
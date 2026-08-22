# IMPORTS
import streamlit as st
from utils.math_utils import CalcularIntervaloProporcion

# Data
n = 400
exitos = 280
confianza = 0.95

# display code on screen
st.title("Confidence intervals for a population proportion")

st.write("Recalling the formula for the confidence interval for a population proportion:")
st.latex(r'''
    \hat{p} \pm Z_{\alpha/2} \cdot \frac{\sqrt{\hat{p}(1-\hat{p})}}{\sqrt{n}}
''')

st.subheader("Code to compute the confidence interval")

codigo = """
    import scipy.stats as stats
    import numpy as np

    # Data
    n = 400
    exitos = 280
    confianza = 0.95

    # Sample proportion
    p_hat = exitos / n

    # Confidence interval
    z = stats.norm.ppf(1 - (1 - confianza) / 2)
    error = z * np.sqrt((p_hat * (1 - p_hat)) / n)
    intervalo = (p_hat - error, p_hat + error)
"""

st.code(codigo, language='python')

st.write("""This code defines the function `CalcularIntervaloProporcion` in
         `utils/math_utils.py`, which is imported at the top of this file
         to be used below.
""")

# Results
inter_1 = CalcularIntervaloProporcion(0.95, n, exitos)
inter_2 = CalcularIntervaloProporcion(0.95, n, exitos)

st.subheader("Interpretation of results")
st.write(rf"""We have a sample proportion of {exitos/n:.2f} ({exitos/n*100:.2f}%)
         and a 95% confidence level that the true population proportion
         of students using AI tools lies between {inter_1[0]:.4f} and {inter_1[1]:.4f}.
""")
st.write(rf"""Since the entire confidence interval [{inter_1[0]:.4f}, {inter_1[1]:.4f}]
         is above 0.60 (60%), there is sufficient statistical evidence at the 95%
         confidence level to conclude that the proportion of students using AI
         tools is greater than 60%.
""")


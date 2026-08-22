#IMPORTS 
import streamlit as st
import matplotlib.pyplot as plt
from utils.math_utils import SimularMaximaVerosimilitud
import io

# Variables used in exercise 6
n = 100
theta_real = 2.0
M = 5000
seed = 42

resultados_simulacion = SimularMaximaVerosimilitud(n, theta_real, M, seed)

st.title("Simulation and Maximum Likelihood Estimation")

st.write("""Considering the following density function:""" )

st.latex(r"""f(x;\theta) = (1+\theta)x^\theta, \quad 0 \le x \le 1, \quad \theta > -1""")

st.write(r"""We will use the inverse transform method to generate observations from
    this distribution. If $U \sim \text{Uniform}(0,1)$, then $X = U^{\frac{1}{1+\theta}}$.""")

st.write(r"""We consider $n = 100$ and $\theta = 2$. A random sample of size $n$ is generated.""")

st.write("""Using the estimator:""")

st.latex(r"""\hat{\theta}_{MV} = -\frac{n}{\sum_{i=1}^{n} \ln(X_i)} - 1""")

st.subheader("Code for simulation and estimation")

codigo = """
    import numpy as np
    import pandas as pd

    # Experiment parameters
    np.random.seed(42)
    n = 100
    theta_real = 2.0
    M = 5000

    # 1. Generate data via inverse transform
    # X = U^(1 / (1 + theta))
    U = np.random.uniform(0, 1, size=(M, n))
    X = U ** (1.0 / (1.0 + theta_real))

    # 2. Compute the MLE for each of the M samples
    # theta_hat_mv = -n / sum(ln(X_i)) - 1
    suma_ln_x = np.sum(np.log(X), axis=1)
    theta_mv = -n / suma_ln_x - 1.0

    # 3. Empirical probability that |X_bar - E[X]| > 0.5
    E_X = (theta_real + 1.0) / (theta_real + 2.0)  # Should be 0.75 for theta = 2
    x_bar_muestras = np.mean(X, axis=1)
    desviaciones = np.abs(x_bar_muestras - E_X)
    probabilidad_empirica = np.mean(desviaciones > 0.5)
"""
st.code(codigo, language='python')

st.subheader("Key numerical results")
col1, col2, col3 = st.columns(3)
col1.metric("Empirical mean ($\hat{\theta}_{MV}$)", f"{resultados_simulacion['media_theta_mv']:.4f}")
col2.metric("Theoretical expectation $\mathbb{E}[X]$", f"{resultados_simulacion['E_X_teorico']:.4f}")
col3.metric("Empirical probability", f"{resultados_simulacion['probabilidad_empirica']:.4f}")

st.write(f"**Empirical standard deviation of the MLEs:** {resultados_simulacion['desviacion_theta_mv']:.4f}")

st.subheader("Empirical distribution of the Maximum Likelihood Estimator")

# Create plot with transparent background
fig, ax = plt.subplots(figsize=(8, 4))

# Configure transparent backgrounds so they inherit Streamlit's color
fig.patch.set_facecolor('none')
ax.patch.set_facecolor('none')

# Histogram and reference line
ax.hist(resultados_simulacion["theta_mv"], bins=50, density=True, alpha=0.6, color='#bf00ff', edgecolor='white')
ax.axvline(resultados_simulacion["theta_real"], color='red', linestyle='--', linewidth=2, label=f'Real value $\\theta$ = {resultados_simulacion["theta_real"]}')

text_color = 'white'

ax.set_title(f"Empirical distribution of $\hat{{\theta}}_{{MV}}$ ($M = {M}$, $n = {n}$)", color=text_color)
ax.set_xlabel("Values of $\hat{\theta}_{MV}$", color=text_color)
ax.set_ylabel("Density", color=text_color)
ax.tick_params(axis='x', colors=text_color)
ax.tick_params(axis='y', colors=text_color)
for spine in ax.spines.values():
    spine.set_color(text_color)
legend = ax.legend()
for text in legend.get_texts():
    text.set_color("black")  # Dark text inside the legend for contrast with white background

# Render the figure with transparency
buf = io.BytesIO()
fig.savefig(buf, format="png", transparent=True, bbox_inches="tight")
st.image(buf)

st.write(r"""The inverse transform method generates random samples from a continuous
    distribution using a uniform variable $U(0,1)$ by equating the cumulative
    distribution function $F(x)$ to $U$. For this density, integrating gives
    $F(x) = x^{\theta+1}$, and solving for $X$ yields $X = U^{\frac{1}{1+\theta}}$.""")

st.write(r"""According to statistical inference theory and the Central Limit Theorem,
    Maximum Likelihood Estimators have desirable properties for large samples
    ($n = 100$), such as asymptotic unbiasedness and normality. Therefore,
    the empirical distribution of $\hat{\theta}_{MV}$ over $M = 5,000$ simulations
    tends to a bell-shaped (normal) form centered near the true value $\theta = 2$.""")

st.write(r"""Evaluating the sample mean $\overline{X}$ against its theoretical expectation
    ($\mathbb{E}[X] = 0.75$), the empirical probability quantifies how often
    large deviations greater than 0.5 occur in the simulated samples.""")

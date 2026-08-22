# LIBRARY IMPORTS
import pandas as pd 
import scipy.stats as stats
import numpy as np

# HELPER FUNCTIONS

def CalcularMedidasDescriptivasEstacion(df):

    df = df.drop('PromAnual', axis=1) # remove the average column
    
    df_aux = pd.DataFrame()

    # axis=1 computes the statistic across each row
    df_aux['Mean'] = df.select_dtypes(include=['number']).mean(axis=1)
    df_aux['Median'] = df.select_dtypes(include=['number']).median(axis=1)
    df_aux['Sample Variance'] = df.select_dtypes(include=['number']).var(axis=1)
    df_aux['Sample StdDev'] = df.select_dtypes(include=['number']).std(axis=1)
    df_aux['Min'] = df.select_dtypes(include=['number']).min(axis=1)
    df_aux['Max'] = df.select_dtypes(include=['number']).max(axis=1)
    df_aux['Range'] = df_aux['Max'] - df_aux['Min']

    df_final = pd.concat([df, df_aux], axis=1) # coloca las nuevas columnas al lado del df original
    
    return df_final

def CalcularMedidasDescriptivasMes(df):
    
    df = df.drop('PromAnual', axis=1) # remove the average column

    df_aux = pd.DataFrame()

    # axis=0 computes the statistic across each column
    df_aux['Mean'] = df.select_dtypes(include=['number']).mean(axis=0)
    df_aux['Median'] = df.select_dtypes(include=['number']).median(axis=0)
    df_aux['Sample Variance'] = df.select_dtypes(include=['number']).var(axis=0)
    df_aux['Sample StdDev'] = df.select_dtypes(include=['number']).std(axis=0)
    df_aux['Min'] = df.select_dtypes(include=['number']).min(axis=0)
    df_aux['Max'] = df.select_dtypes(include=['number']).max(axis=0)
    df_aux['Range'] = df_aux['Max'] - df_aux['Min']

    return df_aux

def CalcularIntervalo(confianza, n, x_bar, sigma):
    alpha = 1 - confianza
    z = stats.norm.ppf(1 - alpha / 2)
    error = z * (sigma / np.sqrt(n))
    return (x_bar - error, x_bar + error)

def CalcularIntervaloProporcion(confianza, n, exitos):
    alpha = 1 - confianza
    z = stats.norm.ppf(1 - alpha / 2)
    p_hat = exitos / n
    error = z * np.sqrt((p_hat * (1 - p_hat)) / n)
    return (p_hat - error, p_hat + error)

def GenerarTalloHojas(datos):

    datos = sorted(datos)
    tallo_hojas = {}
    
    for num in datos:
        tallo = num // 10
        hoja = num % 10
        if tallo not in tallo_hojas:
            tallo_hojas[tallo] = []
        tallo_hojas[tallo].append(str(hoja))
    
    resultado = "Stem | Leaves\n"
    resultado += "-------------\n"
    for tallo in sorted(tallo_hojas.keys()):
        resultado += f"{tallo:5} | {' '.join(tallo_hojas[tallo])}\n"
    return resultado

def SimularTeoremaRaoBlackwell(theta, n, M, seed):
    # Set random seed
    np.random.seed(seed)

    # Success parameter for the geometric distribution (p = 1 / theta)
    p = 1.0 / theta

    # 1. Generate M samples of size n
    muestras = np.random.geometric(p=p, size=(M, n))

    # 2. Initial estimator: X_1 (first element of each sample)
    theta_1 = muestras[:, 0]

    # 3. Sufficient statistic U = sum of observations in each sample
    U = np.sum(muestras, axis=1)

    # 4. Rao-Blackwell improved estimator: E(X_1 | U) = U / n = X_bar
    theta_star = U / n

    # 5. Compute empirical variances
    var_theta_1 = np.var(theta_1, ddof=1)
    var_theta_star = np.var(theta_star, ddof=1)

    # Percentage reduction in variance
    reduction = ((var_theta_1 - var_theta_star) / var_theta_1) * 100

    # Structure results into a dictionary for a table (user-facing labels in English)
    resultados_tabla = {
        "Estimator": [
            "Initial Estimator", 
            "Improved Estimator (Rao–Blackwell)"
        ],
        "Empirical Variance": [
            f"{var_theta_1:.4f}", 
            f"{var_theta_star:.4f}"
        ],
        "Description and Efficiency": [
            "High dispersion when based on a single observation.",
            f"Variance drastically reduced (reduction of {reduction:.2f}%) when conditioning on the sufficient statistic."
        ]
    }

    # Convert and return as a Pandas DataFrame
    return pd.DataFrame(resultados_tabla)

def SimularMaximaVerosimilitud(n, theta_real, M, seed):
    """
    Perform Monte Carlo simulation and Maximum Likelihood Estimation
    for Exercise 6. Graphics are omitted from this function.

    Parameters:
    - n (int): Sample size for each random sample.
    - theta_real (float): True value of the parameter theta.
    - M (int): Number of simulation repetitions.
    - seed (int): Seed for reproducible randomness.

    Returns:
    - dict: Dictionary with generated samples, estimates and summary statistics.
    """
    # 1. Seed for reproducibility
    np.random.seed(seed)

    # 2. Generate data via inverse transform: X = U^(1 / (1 + theta))
    U = np.random.uniform(0, 1, size=(M, n))
    X = U ** (1.0 / (1.0 + theta_real))

    # 3. Compute the MLE for each of the M samples
    suma_ln_x = np.sum(np.log(X), axis=1)
    theta_mv = -n / suma_ln_x - 1.0

    # 4. Analytical and statistical calculations
    media_theta_mv = np.mean(theta_mv)
    desviacion_theta_mv = np.std(theta_mv, ddof=1)

    # Theoretical expectation E[X] = (theta + 1) / (theta + 2)
    E_X_teorico = (theta_real + 1.0) / (theta_real + 2.0)

    # Empirical probability that |X_bar - E[X]| > 0.5
    x_bar_muestras = np.mean(X, axis=1)
    desviaciones = np.abs(x_bar_muestras - E_X_teorico)
    probabilidad_empirica = np.mean(desviaciones > 0.5)

    # Package results in an organized dictionary
    resultados = {
        "n": n,
        "theta_real": theta_real,
        "M": M,
        "X_muestras": X,             # Generated data matrix (useful for plotting)
        "theta_mv": theta_mv,         # Vector with the M estimates (useful for histograms)
        "media_theta_mv": media_theta_mv,
        "desviacion_theta_mv": desviacion_theta_mv,
        "E_X_teorico": E_X_teorico,
        "probabilidad_empirica": probabilidad_empirica
    }

    return resultados
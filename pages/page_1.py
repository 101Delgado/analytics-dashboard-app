# IMPORTS
import pandas as pd
import streamlit as st
import plotly.express as px
import utils.math_utils as math_utils

# DataFrames to display
if 'datos_cargados' in st.session_state:
    df_original = st.session_state['datos_cargados']
    st.write("Data received successfully:")
    df_por_mes = math_utils.CalcularMedidasDescriptivasMes(df_original)
    df_por_estacion = math_utils.CalcularMedidasDescriptivasEstacion(df_original)

    tab1, tab2, tab3 = st.tabs(["PART 1", "PART 2", "PART 3"])

    with tab1:
        # QUESTION 1
        st.title("Part 1")
        # part 1.1
        st.write("Part 1.1")
        st.dataframe(df_por_estacion, use_container_width=True)
        # part 1.2
        st.write("Part 1.2")
        st.dataframe(df_por_mes, use_container_width=True)
        st.write("""
                The data show a marked seasonal thermal variability. For example, in January,
                 the standard deviation is 15.78 °F (indicating large differences between stations),
                 while in July it decreases to 7.48 °F, suggesting that temperatures are relatively
                 more homogeneous among stations during the summer months.
        """)

    with tab2:
        # QUESTION 2
        st.title("Part 2")
        # part a
        st.write("part 2.1")
        st.write("""
                The boxplot for the variable PromAnual shows a positive skew (right-tailed).
                 This is evidenced by a skewness coefficient of 0.518 and by the median's
                 position inside the box shifted towards lower values, while the upper whisker
                 and box extend further toward higher temperatures. This suggests that some
                 stations have notably higher annual average temperatures that pull the mean
                 to the right, away from the center of the distribution.
        """)
        fig_caja = px.box(df_original, y='PromAnual', title="PromAnual distribution")
        st.plotly_chart(fig_caja, use_container_width=True)
        # part b
        st.write("part 2.2")
        colores = []
        max_val = df_original['PromAnual'].max()
        min_val = df_original['PromAnual'].min()

        for val in df_original['PromAnual']:
            if val == max_val:
                colores.append('red')    # Color for the maximum
            elif val == min_val:
                colores.append('blue')   # Color for the minimum
            else:
                colores.append('lightgray') # Color for the rest

        fig_barras = px.bar(
            df_original,
            x='Estacion',
            y='PromAnual',
            title="Comparison of average temperatures"
        )
        fig_barras.update_traces(marker_color=colores)
        st.plotly_chart(fig_barras, use_container_width=True)
        # part c
        st.write("part 2.3")

        col1, col2, col3 = st.columns([0.2, 7, 0.2])

        with col2:
            st.subheader("Stem-and-Leaf Diagram")
            st.code(math_utils.GenerarTalloHojas(df_original['PromAnual'].tolist()), language=None)
        
        st.write("""
                The stem-and-leaf plot reveals a concentration of annual average temperatures
                 in the 50 to 70 °F range, with a main stem at 6 (60-69 °F) that contains the
                 majority of the data. There is also a secondary stem at 5 (50-59 °F) with fewer
                 values, and some outliers in stem 7 (70-79 °F), suggesting some stations have
                 significantly higher annual averages than the rest.
        """)
        st.write("""
                Overall, the descriptive statistics, the boxplot and the stem-and-leaf plot
                 indicate that annual average temperatures have a right-skewed distribution
                 concentrated around 60 °F, with some outliers that raise the mean.
        """)
        st.write("""
                 The data show a high concentration between 30 °F and 50 °F. In contrast,
                 values in the 60 °F and 70 °F ranges are scarce, representing particular
                 stations with annual average temperatures higher than most of the dataset.
        """)

    with tab3:
        # QUESTION 3
        st.title("Part 3")
        st.subheader("Part 3.1")
        st.write("""
                Comparing the mean (46.11 °F) with the median shows proximity that
                 suggests a relatively symmetric distribution, although a visual check
                 with the histogram is recommended to confirm any slight skew.
        """)

        st.subheader("Part 3.2")
        st.latex(r"""
                Q_1 = 39.30 \quad ; \quad Q_3 = 51.65 \\
                RIC = Q_3 - Q_1 = 12.35 \\
                \text{Lower bound: } Q_1 - 1.5 \times RIC = 20.77 \\
                \text{Upper bound: } Q_3 + 1.5 \times RIC = 70.18
        """)
        st.write("""
                Using Tukey's rule, lower and upper bounds were set to identify
                 outliers. The lower bound is 20.77 °F and the upper bound is 70.18 °F.
        """)
        st.write("""
                Applying these limits to PromAnual, no outliers were identified in
                 the dataset, since all observations fall within the defined range.
                 Therefore, the distribution of annual average temperatures appears
                 consistent and does not contain extreme stations that significantly
                 distort the behavior of the dataset.
        """)
        st.subheader("Part 3.3")
        st.write("""
                With a standard deviation of 10.11 °F around a mean of 46.11 °F,
                variability is considered moderate-high, indicating significant
                climatic differences among the analyzed stations.
        """)
        st.subheader("Part 3.4")
        st.write("""
                The station with the highest annual average temperature is Honolulu.🔥         
        """)
        st.subheader("Part 3.5")
        st.write("""
                The station with the lowest annual average temperature is Duluth.❄️         
        """)
        st.subheader("Part 3.6")
        st.write("""
                Based on the descriptive analysis of temperatures, the evaluated
                 meteorological stations show heterogeneous thermal behavior
                 throughout the year. Monthly dispersion measures such as the
                 standard deviation reach significant values (up to 15.78 °F in winter),
                 evidencing marked differences across regions. While all stations
                 follow a common seasonal cycle, the magnitude of temperature
                 fluctuation between the warmest and coldest months varies by location,
                 demonstrating diverse thermal regimes rather than a uniform climate
                 pattern across the dataset.
        """)
        st.subheader("Part 3.7")
        st.write("""
                The station with the highest annual thermal variability is Minneapolis.
                 This station shows the most extreme temperature fluctuation in the dataset.
                 A range of 60.3 °F and a monthly standard deviation of 21.13 °F indicate
                 drastic seasonal variations consistent with a continental climate.
        """)
else:   
    st.warning("No data uploaded. Please return to the Home page and upload the temperaturas.txt file.")

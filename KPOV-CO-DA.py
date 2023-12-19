import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly

# https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Automate Data Analysis for Shrincon Machine",
                   page_icon="📈",
                   layout="wide"
)

uploaded_file = st.file_uploader("Upload an Exel File", type=["xlsx"])

# file_source = r"\\172.25.70.18\PE-  Budo Urgent Normal Item\Boat18\COATING\Excursion\20231213 TA304 Potsu\20231213 TA304 Potsu NG.xlsx"

if uploaded_file is not None:
    df = pd.read_excel(
        io = uploaded_file,
        engine='openpyxl',
        sheet_name=None,
        # skiprows=0,
        usecols='A:AZ',
        nrows=1000000
    )

    sheet_name = st.selectbox("Select Sheet", list(df.keys()))
    df = df[sheet_name]

    date_coat = st.sidebar.multiselect(
        "Select the Coated Date:",
        options=df["Date_Coat"].unique(),
        default=df["Date_Coat"].unique(),
    )

    # coated_time = st.sidebar.multiselect(
    #     "Select the Coated Time:",
    #     options=df["Time"].unique(),
    #     default=df["Time"].unique()
    # )

    df_selection = df.query(
        "Date_Coat == @date_coat"# & Time == @coated_time"
    )
    df_selection["Date_Coat"] = df_selection["Date_Coat"].dt.date

    # Line Chart with Plotly
    st.subheader("Line Chart of each Parameter📈")
    grouped_df = df_selection.groupby("Date_Coat")
    opm_press_line_plotly = go.Figure()
    for date_coat, group in grouped_df:
        x_values = (group.index - group.index[0]).values
        opm_press_line_plotly.add_trace(go.Scatter(x=x_values, y=group["OPM_light_quantity"],
                                                   mode="lines",
                                                   name=f"OPM_light_quantity - Date_Coat: {date_coat}",
                                                   hoverinfo="y+text",
                                                   text=group["Layer_No"].astype(str),
                                                   textposition="top center"))
        opm_press_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Pressure"],
                                                   mode="lines",
                                                   name=f"Pressure - Date_Coat: {date_coat}",
                                                   hoverinfo="y+text",
                                                   text=group["Layer_No"].astype(str),
                                                   textposition="top center",
                                                   yaxis="y2"))
    opm_press_line_plotly.update_layout(title="OPM_light_quantity and Pressure",
                                        yaxis_title="OPM_light_quantity",
                                        yaxis2=dict(title="Pressure", overlaying="y", side="right"),
                                        width=1000, height=600,
                                        showlegend=True)
    st.plotly_chart(opm_press_line_plotly)

    # Line Plot of Source_current and Rate_A_sec
    grouped_df = df_selection.groupby("Date_Coat")
    sc_rate_line_plotly = go.Figure()
    for date_coat, group in grouped_df:
        x_values = (group.index - group.index[0]).values
        sc_rate_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Source_current"],
                                                   mode="lines",
                                                   name=f"Source_current - Date_Coat: {date_coat}",
                                                   hoverinfo="y+text",
                                                   text=group["Layer_No"].astype(str),
                                                   textposition="top center"))
        sc_rate_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Rate_A_sec"],
                                                   mode="lines",
                                                   name=f"Rate_A_sec - Date_Coat: {date_coat}",
                                                   hoverinfo="y+text",
                                                   text=group["Layer_No"].astype(str),
                                                   textposition="top center",
                                                   yaxis="y2"))
    sc_rate_line_plotly.update_layout(title="Source_current and Rate_A_sec",
                                        yaxis_title="Source_current",
                                        yaxis2=dict(title="Rate_A_sec", overlaying="y", side="right"),
                                        width=1000, height=600,
                                        showlegend=True)
    st.plotly_chart(sc_rate_line_plotly)

    # Line Plot of Pressure and Flow
    grouped_df = df_selection.groupby("Date_Coat")
    press_flow_line_plotly = go.Figure()
    for date_coat, group in grouped_df:
        x_values = (group.index - group.index[0]).values
        press_flow_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Pressure"],
                                                   mode="lines",
                                                   name=f"Pressure - Date_Coat: {date_coat}",
                                                   hoverinfo="y+text",
                                                   text=group["Layer_No"].astype(str),
                                                   textposition="top center"))
        press_flow_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Flow"],
                                                   mode="lines",
                                                   name=f"Flow - Date_Coat: {date_coat}",
                                                   hoverinfo="y+text",
                                                   text=group["Layer_No"].astype(str),
                                                   textposition="top center",
                                                   yaxis="y2"))
    press_flow_line_plotly.update_layout(title="Pressure and Flow",
                                        yaxis_title="Pressure",
                                        yaxis2=dict(title="Flow", overlaying="y", side="right"),
                                        width=1000, height=600,
                                        showlegend=True)
    st.plotly_chart(press_flow_line_plotly)

    # Sepate Graph
    fig_time_sec = go.Figure()
    for date_coat, group in grouped_df:
        x_values = (group.index - group.index[0]).values
        fig_time_sec.add_trace(go.Scatter(x=x_values, y=group["Time_sec"],
                                         mode="lines",
                                         name=f"Date_Coat: {date_coat}",
                                         text=group["Layer_No"].astype(str),
                                         textposition="top center",
                                         hoverinfo="y+text"))

    fig_time_sec.update_layout(title="Time_sec Plot",
                               xaxis_title="Nested X-Axis",
                               yaxis_title="Time_sec",
                               width=700, height=500,
                               showlegend=True)

    fig_AccVol = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_AccVol.add_trace(go.Scatter(x=x_values, y=group["AccVol"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_AccVol.update_layout(title="AccVol Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="AccVol",
                      width=700, height=500,
                      showlegend=True)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_time_sec, use_container_width=True)
    right_column.plotly_chart(fig_AccVol, use_container_width=True)

    fig_AccCur = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_AccCur.add_trace(go.Scatter(x=x_values, y=group["AccCur"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_AccCur.update_layout(title="AccCur Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="AccCur",
                      width=1000, height=500,
                      showlegend=True)

    fig_SupVol = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_SupVol.add_trace(go.Scatter(x=x_values, y=group["SupVol"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_SupVol.update_layout(title="SupVol Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="SupVol",
                      width=1000, height=500,
                      showlegend=True)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_AccCur, use_container_width=True)
    right_column.plotly_chart(fig_SupVol, use_container_width=True)

    fig_BiasCur = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_BiasCur.add_trace(go.Scatter(x=x_values, y=group["BiasCur"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_BiasCur.update_layout(title="BiasCur Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="BiasCur",
                      width=1000, height=500,
                      showlegend=True)

    fig_RF_Forword = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_RF_Forword.add_trace(go.Scatter(x=x_values, y=group["RF_Forword"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_RF_Forword.update_layout(title="RF_Forword Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="RF_Forword",
                      width=1000, height=500,
                      showlegend=True)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_BiasCur, use_container_width=True)
    right_column.plotly_chart(fig_RF_Forword, use_container_width=True)

    fig_RF_Refrect = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_RF_Refrect.add_trace(go.Scatter(x=x_values, y=group["RF_Refrect"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_RF_Refrect.update_layout(title="RF_Refrect Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="RF_Refrect",
                      width=1000, height=500,
                      showlegend=True)

    fig_O2Flow = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_O2Flow.add_trace(go.Scatter(x=x_values, y=group["O2Flow"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_O2Flow.update_layout(title="O2Flow Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="O2Flow",
                      width=1000, height=500,
                      showlegend=True)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_RF_Refrect, use_container_width=True)
    right_column.plotly_chart(fig_O2Flow, use_container_width=True)

    fig_ArFlow = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_ArFlow.add_trace(go.Scatter(x=x_values, y=group["ArFlow"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_ArFlow.update_layout(title="ArFlow Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="ArFlow",
                      width=1000, height=500,
                      showlegend=True)

    fig_NtFlow = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_NtFlow.add_trace(go.Scatter(x=x_values, y=group["NtFlow"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_NtFlow.update_layout(title="NtFlow Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="NtFlow",
                      width=1000, height=500,
                      showlegend=True)

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_ArFlow, use_container_width=True)
    right_column.plotly_chart(fig_NtFlow, use_container_width=True)

    fig_APC_Pressure = go.Figure()
    for date_coat, group in grouped_df:
        group.index = group.index - group.index[0]
        x_values = group.index
        fig_APC_Pressure.add_trace(go.Scatter(x=x_values, y=group["APC_Pressure"],
                                 mode="lines",
                                 name=f"Date_Coat: {date_coat}"))
    fig_APC_Pressure.update_layout(title="APC_Pressure Plot",
                      xaxis_title="Nested X-Axis",
                      yaxis_title="APC_Pressure",
                      width=700, height=500,
                      showlegend=True)
    st.plotly_chart(fig_APC_Pressure)

else:
    st.warning("Please upload an Excel file.")
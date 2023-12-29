import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly

# https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Automate Data Analysis for Coating Machine",
                   page_icon="📈",
                   layout="wide"
)

machine_options = ["Shrincon Old Version", "Shrincon New Version", "Optorun CT25",
                   "Optorun CT26", "Inline", "Inline (Single Coat)", "Showa", "AFC: CT17"]
selected_machine = st.selectbox("Select Machine", machine_options)

                                        # Shrincon
if selected_machine in ["Shrincon Old Version", "Shrincon New Version"]:
    uploaded_file = st.file_uploader("Upload an Exel File", type=["xlsx"])
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

        st.warning("Analysis for other machines is not implemented yet.")

else:
    st.warning("Analysis for the selected machine is not implemented yet.")

                                        # Optorun CT25
if selected_machine in ["Optorun CT25"]:
    uploaded_file = st.file_uploader("Upload an Exel File", type=["xlsx"])
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

        df_selection = df.query(
            "Date_Coat == @date_coat"# & Time == @coated_time"
        )
        df_selection["Date_Coat"] = df_selection["Date_Coat"].dt.date

        # Line Chart with Plotly
        st.subheader("Line Chart of each Parameter📈")
        grouped_df = df_selection.groupby("Date_Coat")
        press_APC_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = (group.index - group.index[0]).values
            press_APC_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Pressure"],
                                                       mode="lines",
                                                       name=f"APC_Flow_sscm - Date_Coat: {date_coat}",
                                                       hoverinfo="y+text",
                                                       text=group["Layer_No"].astype(str),
                                                       textposition="top center"))
            press_APC_line_plotly.add_trace(go.Scatter(x=x_values, y=group["APC_Flow_sscm"],
                                                       mode="lines",
                                                       name=f"APC_Flow_sscm - Date_Coat: {date_coat}",
                                                       hoverinfo="y+text",
                                                       text=group["Layer_No"].astype(str),
                                                       textposition="top center",
                                                       yaxis="y2"))
        press_APC_line_plotly.update_layout(title="Pressure and APC_Flow_sscm",
                                            yaxis_title="Pressure",
                                            yaxis2=dict(title="APC_Flow_sscm", overlaying="y", side="right"),
                                            width=1000, height=600,
                                            showlegend=True)
        st.plotly_chart(press_APC_line_plotly)

        # Line Plot of Source_current and Rate_A_sec
        grouped_df = df_selection.groupby("Date_Coat")
        eb_rate_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = (group.index - group.index[0]).values
            eb_rate_line_plotly.add_trace(go.Scatter(x=x_values, y=group["EB_Emission_mA"],
                                                       mode="lines",
                                                       name=f"EB_Emission_mA - Date_Coat: {date_coat}",
                                                       hoverinfo="y+text",
                                                       text=group["Layer_No"].astype(str),
                                                       textposition="top center"))
            eb_rate_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Rate_A_sec"],
                                                       mode="lines",
                                                       name=f"Rate_A_sec - Date_Coat: {date_coat}",
                                                       hoverinfo="y+text",
                                                       text=group["Layer_No"].astype(str),
                                                       textposition="top center",
                                                       yaxis="y2"))
        eb_rate_line_plotly.update_layout(title="EB_Emission_mA and Rate_A_sec",
                                            yaxis_title="EB_Emission_mA",
                                            yaxis2=dict(title="Rate_A_sec", overlaying="y", side="right"),
                                            width=1000, height=600,
                                            showlegend=True)
        st.plotly_chart(eb_rate_line_plotly)

        # Line Plot of Pressure and Flow
        grouped_df = df_selection.groupby("Date_Coat")
        tn_light_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = (group.index - group.index[0]).values
            tn_light_line_plotly.add_trace(go.Scatter(x=x_values, y=group["TN_KA"],
                                                       mode="lines",
                                                       name=f"TN_KA - Date_Coat: {date_coat}",
                                                       hoverinfo="y+text",
                                                       text=group["Layer_No"].astype(str),
                                                       textposition="top center"))
            tn_light_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Light_Value_R"],
                                                       mode="lines",
                                                       name=f"Light_Value_R - Date_Coat: {date_coat}",
                                                       hoverinfo="y+text",
                                                       text=group["Layer_No"].astype(str),
                                                       textposition="top center",
                                                       yaxis="y2"))
        tn_light_line_plotly.update_layout(title="TN_KA and Light_Value_R",
                                            yaxis_title="TN_KA",
                                            yaxis2=dict(title="Light_Value_R", overlaying="y", side="right"),
                                            width=1000, height=600,
                                            showlegend=True)
        st.plotly_chart(tn_light_line_plotly)

        st.warning("Analysis for other machines is not implemented yet.")

else:
    st.warning("Analysis for the selected machine is not implemented yet.")

                                        # Optorun CT26

                                        # Inline
if selected_machine in ["Inline"]:
    uploaded_file = st.file_uploader("Upload an Exel File", type=["xlsx"])
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

        df_selection = df.query(
            "Date_Coat == @date_coat"# & Time == @coated_time"
        )
        df_selection["Date_Coat"] = pd.to_datetime(df_selection["Date_Coat"])
        df_selection["Date_Coat"] = df_selection["Date_Coat"].dt.date

        # Line Chart with Plotly
        st.subheader("Line Chart of each Parameter📈")
        grouped_df = df_selection.groupby("Date_Coat")
        opm_press_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = (group.index - group.index[0]).values
            opm_press_line_plotly.add_trace(go.Scatter(x=x_values, y=group["OPM_Light_Quantity"],
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

        # Line Plot of Source_Current and Rate_A_sec
        grouped_df = df_selection.groupby("Date_Coat")
        sc_rate_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = (group.index - group.index[0]).values
            sc_rate_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Source_Current"],
                                                       mode="lines",
                                                       name=f"Source_Current - Date_Coat: {date_coat}",
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
        sc_rate_line_plotly.update_layout(title="Source_Current and Rate_A_sec",
                                            yaxis_title="Source_Current",
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

        st.warning("Analysis for other machines is not implemented yet.")

else:
    st.warning("Analysis for the selected machine is not implemented yet.")

                                        # Inline (Single Coat)
if selected_machine in ["Inline (Single Coat)"]:
    uploaded_file = st.file_uploader("Upload an Exel File", type=["xlsx"])
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

        df_selection = df.query(
            "Date_Coat == @date_coat"# & Time == @coated_time"
        )
        df_selection["Date_Coat"] = pd.to_datetime(df_selection["Date_Coat"])
        df_selection["Date_Coat"] = df_selection["Date_Coat"].dt.date

        # Line Chart with Plotly
        st.subheader("Line Chart of each Parameter📈")
        grouped_df = df_selection.groupby("Date_Coat")
        opm_press_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = group.index
            opm_press_line_plotly.add_trace(go.Scatter(x=x_values, y=group["OPM_Light_Quantity"],
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

        # Line Plot of Source_Current and Rate_A_sec
        grouped_df = df_selection.groupby("Date_Coat")
        sc_rate_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = group.index
            sc_rate_line_plotly.add_trace(go.Scatter(x=x_values, y=group["Source_Current"],
                                                       mode="lines",
                                                       name=f"Source_Current - Date_Coat: {date_coat}",
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
        sc_rate_line_plotly.update_layout(title="Source_Current and Rate_A_sec",
                                            yaxis_title="Source_Current",
                                            yaxis2=dict(title="Rate_A_sec", overlaying="y", side="right"),
                                            width=1000, height=600,
                                            showlegend=True)
        st.plotly_chart(sc_rate_line_plotly)

        # Line Plot of Pressure and Flow
        grouped_df = df_selection.groupby("Date_Coat")
        press_flow_line_plotly = go.Figure()
        for date_coat, group in grouped_df:
            x_values = group.index
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
        
        st.warning("Analysis for other machines is not implemented yet.")

else:
    st.warning("Analysis for the selected machine is not implemented yet.")

                                        # Showa
    

                                        # AFC CT17    
if selected_machine in ["AFC: CT17"]:
    uploaded_file = st.file_uploader("Upload an Exel File", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(
            io = uploaded_file,
            engine='openpyxl',
            sheet_name=None,
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

        df_selection = df.query(
            "Date_Coat == @date_coat"
        )
        df_selection["Date_Coat"] = df_selection["Date_Coat"].dt.date

        # Line Chart with Plotly
        st.subheader("Line Chart of each Parameter📈")
        # Sepate Graph
        grouped_df = df_selection.groupby("Date_Coat")
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

        fig_pressure = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_pressure.add_trace(go.Scatter(x=x_values, y=group["Press"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_pressure.update_layout(title="Pressure Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="Pressure",
                          width=700, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_time_sec, use_container_width=True)
        right_column.plotly_chart(fig_pressure, use_container_width=True)

        fig_tg1_elec_pow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_elec_pow.add_trace(go.Scatter(x=x_values, y=group["TG1 electric power"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_elec_pow.update_layout(title="TG1 electric power Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 electric power",
                          width=1000, height=500,
                          showlegend=True)

        fig_tg1_cur = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_cur.add_trace(go.Scatter(x=x_values, y=group["TG1 current"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_cur.update_layout(title="TG1 current Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 current",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg1_elec_pow, use_container_width=True)
        right_column.plotly_chart(fig_tg1_cur, use_container_width=True)

        fig_tg1_vol = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_vol.add_trace(go.Scatter(x=x_values, y=group["TG1 voltage"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_vol.update_layout(title="TG1 voltage Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 voltage",
                          width=1000, height=500,
                          showlegend=True)

        fig_tg2_elec_pow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_elec_pow.add_trace(go.Scatter(x=x_values, y=group["TG2 electric power"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_elec_pow.update_layout(title="TG2 electric power Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 electric power",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg1_vol, use_container_width=True)
        right_column.plotly_chart(fig_tg2_elec_pow, use_container_width=True)

        fig_tg2_curr = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_curr.add_trace(go.Scatter(x=x_values, y=group["TG2 current"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_curr.update_layout(title="TG2 current Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 current",
                          width=1000, height=500,
                          showlegend=True)

        fig_tg2_vol = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_vol.add_trace(go.Scatter(x=x_values, y=group["TG2 voltage"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_vol.update_layout(title="TG2 voltage Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 voltage",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg2_curr, use_container_width=True)
        right_column.plotly_chart(fig_tg2_vol, use_container_width=True)

        fig_rs_inci_elec_pow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_rs_inci_elec_pow.add_trace(go.Scatter(x=x_values, y=group["RS Incidence electric power"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_rs_inci_elec_pow.update_layout(title="RS Incidence electric power Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="RS Incidence electric power",
                          width=1000, height=500,
                          showlegend=True)

        fig_rs_reflec_elec_pow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_rs_reflec_elec_pow.add_trace(go.Scatter(x=x_values, y=group["RS Reflection electric power"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_rs_reflec_elec_pow.update_layout(title="RS Reflection electric power Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="RS Reflection electric power",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_rs_inci_elec_pow, use_container_width=True)
        right_column.plotly_chart(fig_rs_reflec_elec_pow, use_container_width=True)

        fig_tg1_ar_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_ar_flow.add_trace(go.Scatter(x=x_values, y=group["TG1 Ar flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_ar_flow.update_layout(title="TG1 Ar flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 Ar flow",
                          width=700, height=500,
                          showlegend=True)
        
        fig_tg1_o2_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_o2_flow.add_trace(go.Scatter(x=x_values, y=group["TG1 O2 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_o2_flow.update_layout(title="TG1 O2 flow",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 O2 flow",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg1_ar_flow, use_container_width=True)
        right_column.plotly_chart(fig_tg1_o2_flow, use_container_width=True)

        fig_tg1_aux1_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_aux1_flow.add_trace(go.Scatter(x=x_values, y=group["TG1 Aux1 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_aux1_flow.update_layout(title="TG1 Aux1 flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 Aux1 flow",
                          width=700, height=500,
                          showlegend=True)
        
        fig_tg1_aux2_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg1_aux2_flow.add_trace(go.Scatter(x=x_values, y=group["TG1 Aux2 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg1_aux2_flow.update_layout(title="TG1 Aux2 flow",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG1 Aux2 flow",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg1_aux1_flow, use_container_width=True)
        right_column.plotly_chart(fig_tg1_aux2_flow, use_container_width=True)

        fig_tg2_ar_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_ar_flow.add_trace(go.Scatter(x=x_values, y=group["TG2 Ar flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_ar_flow.update_layout(title="TG2 Ar flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 Ar flow",
                          width=700, height=500,
                          showlegend=True)
        
        fig_tg2_o2_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_o2_flow.add_trace(go.Scatter(x=x_values, y=group["TG2 O2 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_o2_flow.update_layout(title="TG2 O2 flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 O2 flow",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg2_ar_flow, use_container_width=True)
        right_column.plotly_chart(fig_tg2_o2_flow, use_container_width=True)

        fig_tg2_aux1_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_aux1_flow.add_trace(go.Scatter(x=x_values, y=group["TG2 Aux1 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_aux1_flow.update_layout(title="TG2 Aux1 flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 Aux1 flow",
                          width=700, height=500,
                          showlegend=True)
        
        fig_tg2_aux2_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg2_aux2_flow.add_trace(go.Scatter(x=x_values, y=group["TG2 Aux2 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg2_aux2_flow.update_layout(title="TG2 Aux2 flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG2 Aux2 flow",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_tg2_aux1_flow, use_container_width=True)
        right_column.plotly_chart(fig_tg2_aux2_flow, use_container_width=True)

        fig_rs_o2_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_rs_o2_flow.add_trace(go.Scatter(x=x_values, y=group["RS O2 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_rs_o2_flow.update_layout(title="RS O2 flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="RS O2 flow",
                          width=700, height=500,
                          showlegend=True)
        
        fig_rs_ar_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_rs_ar_flow.add_trace(go.Scatter(x=x_values, y=group["RS Ar flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_rs_ar_flow.update_layout(title="RS AR flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="RS AR flow",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_rs_o2_flow, use_container_width=True)
        right_column.plotly_chart(fig_rs_ar_flow, use_container_width=True)

        fig_rs_aux_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_rs_aux_flow.add_trace(go.Scatter(x=x_values, y=group["RS Aux flow flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_rs_aux_flow.update_layout(title="RS Aux flow flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="RS Aux flow flow",
                          width=700, height=500,
                          showlegend=True)
        
        fig_tg_o2_flow = go.Figure()
        for date_coat, group in grouped_df:
            group.index = group.index - group.index[0]
            x_values = group.index
            fig_tg_o2_flow.add_trace(go.Scatter(x=x_values, y=group["TG O2 flow"],
                                     mode="lines",
                                     name=f"Date_Coat: {date_coat}",
                                     text=group["Layer_No"].astype(str),
                                     textposition="top center",
                                     hoverinfo="y+text"))
        fig_tg_o2_flow.update_layout(title="TG O2 flow Plot",
                          xaxis_title="Nested X-Axis",
                          yaxis_title="TG O2 flow",
                          width=1000, height=500,
                          showlegend=True)

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_rs_aux_flow, use_container_width=True)
        right_column.plotly_chart(fig_tg_o2_flow, use_container_width=True)

        st.warning("Analysis for other machines is not implemented yet.")

else:
    st.warning("Analysis for the selected machine is not implemented yet.")
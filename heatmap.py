import streamlit as st
import pandas as pd

col1, col2 = st.columns([1,3])

with col1:
    results_filtered = pd.read_csv("heatmap.csv", index_col=False)
    results_filtered['date'] = pd.to_datetime(results_filtered['datetime']).dt.date
    st.dataframe(results_filtered)

with col2:
    st.vega_lite_chart(results_filtered,{"labels":False, "width":500, "height":250,
                                            "mark": {"type":"rect"},
                                            "autosize": {"type":"fit", "contains":"padding"},
                                            "config": {"axis": {"grid":True,"gridwidth":10,"gridColor":"#000"}},
                                            "encoding": {
                                                "y": {
                                                    "title": '',
                                                    "field":"datetime",
                                                    "type":"ordinal",
                                                    "timeUnit":"week",
                                                    "axis": {"tickBand":"extent","labelOpacity":0}
                                                },
                                                "x": {
                                                    "title": '',
                                                    "field":"datetime",
                                                    "type":"ordinal",
                                                    "timeUnit":"day",
                                                    "axis": {"tickBand":"extent","grid":True}
                                                },
                                                "color": {
                                                    "field":"score",
                                                    "type":"quantitative",
                                                    "scale": {"scheme":"greens"}
                                                },
                                                "tooltip": [
                                                    {"field":"date", "type":"temporal"},
                                                    {"field":"score", "type":"quantitative"}
                                                ]
                                            }
                                        })
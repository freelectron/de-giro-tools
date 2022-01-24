import os

import pendulum
import plotly.graph_objects as go

from de_giro_client_nl.data_getters.daily_portfolio_status import DailyPortfolioResults
from de_giro_client_nl.client.session import DeGiroSession
from de_giro_client_nl.translators import EURO_VALUE_COLUMN_NAME, PRODUCT_NAME_COLUMN_NAME


dg_session = DeGiroSession(
    de_giro_account_id=os.getenv("de_giro_account_id")
)

dg_session.connect(
    username=os.getenv('de_giro_username'),
    password=os.getenv('de_giro_password'),
)

date_start = pendulum.local(2021, 11, 1).date()
# Table data for today is not updated [2022-01-24]
date_end = pendulum.today().date() - pendulum.Duration(days=1)
period = pendulum.Period(date_start, date_end, pendulum.Duration(days=1))

df_portfolio_results = DailyPortfolioResults(dg_session).get_dataframe(period)

# Subdivide into traces
FILTER_BY_COLUMN_NAME: str = PRODUCT_NAME_COLUMN_NAME
COLUMN_NAME_TO_TRACE: str = EURO_VALUE_COLUMN_NAME

traces = dict()
product_name_list = ['AEGON', 'CRESUD S.A.C.I.F. Y A.',
                     'D/B/A SIBANYE-STILLWATER LIMITE...', 'GAZPROM PAO',
                     'HEALTHPEAK PROPERTIES INC', 'ING GROEP N.V.',
                     'ISHARES STOXX EUROPE 600 OIL & ...', 'ROYAL DUTCH SHELLA',
                     'SHIFT TECHNOLOGIES INC', 'WDP', 'WELLS FARGO & COMPANY',
                     'WISDOMTREE COMMODITY SECURITIES...']

for product_name in product_name_list:
    series = df_portfolio_results[df_portfolio_results[FILTER_BY_COLUMN_NAME] == product_name][COLUMN_NAME_TO_TRACE]
    series = DailyPortfolioResults.get_percentage_difference(series)
    trace_y = series.values
    trace_x = series.index
    trace_product = go.Scatter(x=trace_x, y=trace_y, name=product_name, showlegend=True)

    traces[product_name] = trace_product

fig = go.Figure()

fig.add_traces(list(traces.values()))

fig.update_layout(
    title=f"Portfolio's `{COLUMN_NAME_TO_TRACE}` cumulative percentage ",
    legend_title=FILTER_BY_COLUMN_NAME,
    autosize=False,
    width=1400,
    height=800,
    font=dict(size=18)
)
fig.show()

print()

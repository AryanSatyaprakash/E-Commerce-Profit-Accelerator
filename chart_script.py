import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Load the data
data = {
    "months": ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06", "2017-07", "2017-08", "2017-09", "2017-10", "2017-11", "2017-12", "2018-01", "2018-02", "2018-03", "2018-04", "2018-05", "2018-06", "2018-07", "2018-08", "2018-09", "2018-10", "2018-11", "2018-12"],
    "revenue": [285000, 320000, 410000, 450000, 520000, 480000, 550000, 580000, 620000, 720000, 850000, 920000, 680000, 720000, 810000, 850000, 920000, 880000, 950000, 980000, 1020000, 1150000, 1280000, 1320000],
    "orders": [1200, 1350, 1580, 1720, 1950, 1810, 2050, 2180, 2350, 2680, 3100, 3400, 2500, 2650, 2980, 3120, 3380, 3200, 3450, 3520, 3680, 4100, 4500, 4650],
    "customers": [980, 1100, 1290, 1410, 1580, 1470, 1680, 1750, 1890, 2150, 2480, 2720, 2000, 2120, 2380, 2490, 2700, 2560, 2750, 2810, 2940, 3280, 3600, 3720]
}

df = pd.DataFrame(data)

# Calculate 3-month moving averages for trend lines
df['revenue_ma'] = df['revenue'].rolling(window=3, center=True).mean()
df['orders_ma'] = df['orders'].rolling(window=3, center=True).mean()
df['customers_ma'] = df['customers'].rolling(window=3, center=True).mean()

# Brand colors in order
colors = ['#1FB8CD', '#DB4545', '#2E8B57']

# Create subplots with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add revenue line on primary y-axis
fig.add_trace(
    go.Scatter(
        x=df['months'], 
        y=df['revenue']/1000,  # Convert to thousands for better display
        mode='lines+markers',
        name='Revenue',
        line=dict(color=colors[0], width=3),
        marker=dict(size=6),
        cliponaxis=False,
        hovertemplate='<b>Revenue</b><br>Month: %{x}<br>Revenue: $%{y:.0f}k<extra></extra>'
    ),
    secondary_y=False
)

# Add revenue trend line
fig.add_trace(
    go.Scatter(
        x=df['months'], 
        y=df['revenue_ma']/1000,
        mode='lines',
        name='Rev Trend',
        line=dict(color=colors[0], width=2, dash='dash'),
        showlegend=False,
        cliponaxis=False,
        hovertemplate='<b>Revenue Trend</b><br>Month: %{x}<br>Avg: $%{y:.0f}k<extra></extra>'
    ),
    secondary_y=False
)

# Add orders line on secondary y-axis
fig.add_trace(
    go.Scatter(
        x=df['months'], 
        y=df['orders'],
        mode='lines+markers',
        name='Orders',
        line=dict(color=colors[1], width=3),
        marker=dict(size=6),
        cliponaxis=False,
        hovertemplate='<b>Orders</b><br>Month: %{x}<br>Orders: %{y:.0f}<extra></extra>'
    ),
    secondary_y=True
)

# Add customers line on secondary y-axis
fig.add_trace(
    go.Scatter(
        x=df['months'], 
        y=df['customers'],
        mode='lines+markers',
        name='Customers',
        line=dict(color=colors[2], width=3),
        marker=dict(size=6),
        cliponaxis=False,
        hovertemplate='<b>Customers</b><br>Month: %{x}<br>Customers: %{y:.0f}<extra></extra>'
    ),
    secondary_y=True
)

# Update layout
fig.update_layout(
    title='E-Commerce Business Performance',
    xaxis_title='Month',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Set y-axes titles
fig.update_yaxes(title_text="Revenue ($k)", secondary_y=False)
fig.update_yaxes(title_text="Orders & Cust", secondary_y=True)

# Update x-axis
fig.update_xaxes(tickangle=45)

# Format primary y-axis (revenue) with currency style
fig.update_yaxes(tickformat="$,.0f", secondary_y=False)

# Format secondary y-axis (orders/customers) 
fig.update_yaxes(tickformat=",.0f", secondary_y=True)

# Save the chart
fig.write_image('ecommerce_dashboard.png')
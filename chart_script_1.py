import plotly.graph_objects as go
import plotly.io as pio

# Data
categories = ["Health & Beauty", "Sports & Leisure", "Electronics", "Home & Garden", "Fashion", "Auto", "Books", "Food & Beverages"]
revenue = [3750000, 3150000, 2840000, 2680000, 2420000, 1950000, 1580000, 1320000]
avg_order_value = [168.50, 142.30, 198.75, 156.80, 135.20, 178.90, 89.50, 78.40]
satisfaction_rating = [4.2, 4.1, 4.0, 4.3, 3.9, 4.0, 4.4, 4.1]
market_share = [22.3, 18.7, 16.9, 15.9, 14.4, 11.6, 9.4, 7.8]

# Sort by revenue
sorted_data = sorted(zip(categories, revenue, avg_order_value, satisfaction_rating, market_share), 
                    key=lambda x: x[1], reverse=True)

sorted_categories, sorted_revenue, sorted_aov, sorted_satisfaction, sorted_market_share = zip(*sorted_data)

# Abbreviate category names to fit 15 char limit
abbreviated_categories = []
for cat in sorted_categories:
    if cat == "Health & Beauty":
        abbreviated_categories.append("Health & Beauty")
    elif cat == "Sports & Leisure":
        abbreviated_categories.append("Sports & Leis.")
    elif cat == "Home & Garden":
        abbreviated_categories.append("Home & Garden")
    elif cat == "Food & Beverages":
        abbreviated_categories.append("Food & Beverag.")
    else:
        abbreviated_categories.append(cat[:15])

# Format revenue in millions
revenue_formatted = [r/1000000 for r in sorted_revenue]

# Define performance tiers and colors
high_performers = ['#1FB8CD', '#1FB8CD', '#1FB8CD']  # Top 3
mid_performers = ['#2E8B57', '#2E8B57', '#2E8B57']   # Middle 3
low_performers = ['#DB4545', '#DB4545']              # Bottom 2

colors = high_performers + mid_performers + low_performers

# Create hover text
hover_text = []
for i in range(len(sorted_categories)):
    hover_text.append(
        f"Category: {sorted_categories[i]}<br>" +
        f"Revenue: ${sorted_revenue[i]/1000000:.1f}M<br>" +
        f"AOV: ${sorted_aov[i]:.0f}<br>" +
        f"Satisfaction: {sorted_satisfaction[i]}/5<br>" +
        f"Market Share: {sorted_market_share[i]:.1f}%"
    )

# Create figure
fig = go.Figure()

# Add revenue bars
fig.add_trace(go.Bar(
    y=abbreviated_categories,
    x=revenue_formatted,
    orientation='h',
    marker=dict(color=colors),
    name='Revenue',
    text=[f"{ms:.1f}%" for ms in sorted_market_share],
    textposition='inside',
    textfont=dict(color='white', size=11),
    hovertext=hover_text,
    hoverinfo='text',
    cliponaxis=False
))

# Add AOV as scatter points
fig.add_trace(go.Scatter(
    y=abbreviated_categories,
    x=[aov/10 for aov in sorted_aov],  # Scale AOV to fit with revenue scale
    mode='markers+text',
    marker=dict(
        symbol='diamond',
        size=12,
        color='white',
        line=dict(color='black', width=2)
    ),
    text=[f"AOV:${aov:.0f}" for aov in sorted_aov],
    textposition='middle right',
    textfont=dict(color='black', size=10),
    name='AOV (Scaled)',
    hoverinfo='skip',
    cliponaxis=False
))

# Add satisfaction ratings as text
for i, (cat, sat) in enumerate(zip(abbreviated_categories, sorted_satisfaction)):
    fig.add_trace(go.Scatter(
        y=[cat],
        x=[revenue_formatted[i] + 0.1],
        mode='text',
        text=[f"★{sat}"],
        textfont=dict(color='gold', size=12),
        showlegend=False,
        hoverinfo='skip',
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title="Category Performance: Revenue, AOV & Rating",
    xaxis_title="Revenue (M)",
    yaxis_title="Category",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes
fig.update_xaxes(tickformat='.1f', ticksuffix='M')
fig.update_yaxes(autorange="reversed")

# Save the chart
fig.write_image("category_performance_analysis.png")
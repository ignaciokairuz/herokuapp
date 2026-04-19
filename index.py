import os
import io
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, Response, render_template_string
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Import our scraper
import scraper

app = Flask(__name__)

# Initialize Background Scheduler
scheduler = BackgroundScheduler()
# Run scraper every 5 minutes
scheduler.add_job(func=scraper.scrape_coto, trigger="interval", minutes=5)
# Start the scheduler
scheduler.start()

def process_data(x, y, op, allow_none=False):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    # Mathematical transformation from original code
    y_new = (y * x / op) - 1

    # Handling values < 0 based on original code
    if allow_none:
        # Instead of None, we can use np.nan so matplotlib skips drawing these segments
        y_new[y_new < 0] = np.nan
    else:
        y_new[y_new < 0] = 0

    return x, y_new

def add_glow_effect(ax, x, y, color, label):
    # Smooth the curve
    # Filter out NaNs for smoothing
    valid = ~np.isnan(y)
    x_valid = x[valid]
    y_valid = y[valid]

    if len(x_valid) > 3:
        x_smooth = np.linspace(x_valid.min(), x_valid.max(), 300)
        spl = make_interp_spline(x_valid, y_valid, k=3)
        y_smooth = spl(x_smooth)

        # Prevent smoothing artifacts going below 0 if original didn't
        if not np.any(y_valid < 0):
            y_smooth = np.clip(y_smooth, 0, None)
    else:
        x_smooth, y_smooth = x_valid, y_valid

    # Draw glow
    n_lines = 10
    diff_linewidth = 1.05
    alpha_value = 0.03
    for n in range(1, n_lines + 1):
        ax.plot(x_smooth, y_smooth,
                linewidth=2 + (diff_linewidth * n),
                alpha=alpha_value,
                color=color)

    # Draw the primary solid line
    line, = ax.plot(x_smooth, y_smooth, linewidth=2, color=color, label=label)

    # Fill under curve
    ax.fill_between(x_smooth, y_smooth, color=color, alpha=0.1)

    # Highlight max point
    if len(y_valid) > 0:
        max_idx = np.argmax(y_smooth)
        ax.scatter(x_smooth[max_idx], y_smooth[max_idx], color='white', s=50, zorder=5)
        ax.annotate(f'Peak\n{y_smooth[max_idx]:.2f}',
                    xy=(x_smooth[max_idx], y_smooth[max_idx]),
                    xytext=(0, 15), textcoords='offset points',
                    ha='center', color='white', fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="none", alpha=0.5))

@app.route('/')
def index():
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Dark modern background
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')

    # Grid styling
    ax.grid(color='#21262d', linestyle='--', linewidth=0.5, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color('#30363d')

    # Line 1 Data
    x1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    y1 = [4992000,2518000,1776000,1337000,1115000,966000,860000,780000,718000,669000,628000,595000,0,0,520000]
    op1 = 4992000
    x1_p, y1_p = process_data(x1, y1, op1)

    # Line 2 Data
    x2 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    y2 = [1815000,1071000,745000,567000,460000,378000,344000,303000,271000,246000,225000,207000,195000,184000,174000,169000,163000,156000]
    op2 = 1815000
    x2_p, y2_p = process_data(x2, y2, op2, allow_none=True)

    # Line 3 Data
    x3 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    y3 = [3710000,0,0,0,0,745000,0,0,0,0,0,465000,0,0,0,395000]
    op3 = 3710000
    x3_p, y3_p = process_data(x3, y3, op3)

    # Plot with neon colors
    add_glow_effect(ax, x1_p, y1_p, color='#00ff41', label="Cyber Node Alpha")
    add_glow_effect(ax, x2_p, y2_p, color='#fe019a', label="Neon Flux Beta")
    add_glow_effect(ax, x3_p, y3_p, color='#00ffff', label="Quantum Sync Gamma")

    # Titles and Labels
    ax.set_xlabel('Temporal Sequence (t)', color='#8b949e', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amplitude Variance (Δ)', color='#8b949e', fontsize=12, fontweight='bold')
    ax.set_title('Advanced Multiline Temporal Graph', color='white', fontsize=16, fontweight='bold', pad=20)

    # Legend styling
    ax.legend(facecolor='#0d1117', edgecolor='#30363d', labelcolor='white')

    # Convert the figure to a PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    image_data = buf.read()

    # Close figure safely to free memory
    plt.close(fig)

    import base64
    b64_image = base64.b64encode(image_data).decode('utf-8')
    static_img_html = f'<img src="data:image/png;base64,{b64_image}" alt="Static Chart" style="max-width:100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">'

    # ---------------------------------------------------------
    # PART 2: Interactive Plotly Chart from DB
    # ---------------------------------------------------------
    try:
        # Initialize DB in case it doesn't exist yet before query
        scraper.init_db()
        conn = sqlite3.connect(scraper.DB_NAME)
        df = pd.read_sql_query("SELECT * FROM prices", conn)
        conn.close()

        if df.empty:
            plotly_html = "<i>No pricing data yet... Please wait a moment.</i>"
        else:
            # Create interactive plotly chart
            fig_plotly = px.line(
                df, x="timestamp", y="discount_price", color="product_name",
                markers=True,
                title="Live Coto Digital Headphone Prices (Updated every 5 mins)",
                labels={"timestamp": "Time", "discount_price": "Price (ARS)", "product_name": "Product"},
                template="plotly_dark"
            )
            # Add some styling
            fig_plotly.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
            )
            plotly_html = pio.to_html(fig_plotly, full_html=False, include_plotlyjs='cdn')
    except Exception as e:
        plotly_html = f"Error loading chart: {e}"

    # Return combined HTML page
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Dashboard</title>
        <style>
            body {{
                background-color: #0d1117;
                color: #c9d1d9;
                font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
                margin: 0; padding: 2rem;
                display: flex; flex-direction: column; align-items: center;
            }}
            h1 {{
                color: #58a6ff;
            }}
            .container {{
                max-width: 1200px; width: 100%;
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 2rem;
                margin-bottom: 2rem;
            }}
            .chart-box {{
                width: 100%;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Multi-Data Dashboard</h1>

        <div class="container">
            <h2>Live Coto Digital Prices (Interactive)</h2>
            <p>Tracking headphone prices automatically every 5 minutes.</p>
            <div class="chart-box">
                {plotly_html}
            </div>
        </div>

        <div class="container">
            <h2>Legacy System: Theoretical Math Output (Static Image)</h2>
            <div style="text-align: center;">
                {static_img_html}
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=int(os.getenv("PORT", 5000)))

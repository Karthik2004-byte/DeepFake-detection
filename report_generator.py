import datetime
import os
import matplotlib
matplotlib.use("Agg")  # Prevent GUI backend errors
import matplotlib.pyplot as plt
from fpdf import FPDF


# --- Custom PDF Class with Top-Left Header & Footer ---
class TruthNetPDF(FPDF):
    def header(self):
        # Professional header (top-left)
        self.set_font("Helvetica", 'B', 13)
        self.set_text_color(37, 99, 235)  # Blue header text
        self.cell(0, 10, "TruthNet : AI-Powered Deepfake Detection", ln=False, align="L")
        self.ln(10)
        self.set_draw_color(200, 200, 200)
        self.line(10, 20, 200, 20)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", 'I', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10,
                  f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  Page {self.page_no()}",
                  align="C")


# --- Generate Pie Chart Only ---
def generate_graphs(confidence_over_frames, base_filename):
    graph_dir = "static/reports"
    os.makedirs(graph_dir, exist_ok=True)

    avg_conf = sum(confidence_over_frames) / len(confidence_over_frames)
    labels = ["Deepfake", "Real"]
    sizes = [avg_conf, 1 - avg_conf]
    colors = ['#ef4444', '#10b981']  # Red = Deepfake, Green = Real

    pie_chart = os.path.join(graph_dir, f"{base_filename}_pie.png")
    plt.figure(figsize=(4, 4))
    plt.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=90,
        colors=colors, textprops={'fontsize': 10}
    )
    plt.title("Prediction Probability", fontsize=12)
    plt.tight_layout()
    plt.savefig(pie_chart, dpi=150)
    plt.close()

    return pie_chart


# --- Generate PDF Report (Single Page) ---
def generate_pdf_report(username, video_name, result, confidence, confidence_over_frames):
    base_filename = os.path.splitext(video_name)[0]
    report_dir = "static/reports"
    os.makedirs(report_dir, exist_ok=True)

    pie_chart = generate_graphs(confidence_over_frames, base_filename)

    pdf_path = os.path.join(report_dir, f"{base_filename}_report.pdf")
    pdf = TruthNetPDF()
    pdf.add_page()

    # ---- Report Title ----
    pdf.set_font("Helvetica", 'B', 17)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 10, "Deepfake Detection Analysis Report", ln=True, align="C")
    pdf.ln(6)

    # ---- Report Info ----
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Generated for: {username}", ln=True)
    pdf.cell(0, 6, f"Video: {video_name}", ln=True)
    pdf.cell(0, 6, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(8)

    # ---- Detection Results ----
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 8, "Detection Results:", ln=True)
    pdf.set_font("Helvetica", '', 11)

    # ✅ Styled Prediction (Blue for Real, Red for Deepfake)
    if result.lower() == "real":
        pdf.set_text_color(16, 185, 129)  # Green for Real
    else:
        pdf.set_text_color(239, 68, 68)   # Red for Deepfake
    pdf.cell(0, 6, f"Prediction: {result}", ln=True)

    # ✅ Confidence as percentage
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 6, f"Confidence Score: {confidence * 100:.2f}%", ln=True)
    pdf.ln(8)

    # ---- Observations ----
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Observations:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 6,
        "This report provides an AI-based analysis of the submitted video using a hybrid CNN-LSTM model. "
        "The model evaluates spatial and temporal features to determine manipulation likelihood. "
        "In borderline or partially altered cases, manual verification is advised. "
        "This document is intended solely for informational and research use."
    )
    pdf.ln(10)

    # ---- Pie Chart ----
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Prediction Probability Chart:", ln=True)
    pdf.image(pie_chart, x=70, w=70)

    pdf.output(pdf_path)
    return pdf_path

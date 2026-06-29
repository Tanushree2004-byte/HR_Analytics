"""Report generation service — PDF, CSV, Excel."""
from __future__ import annotations

from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.backend.services.data_service import DataService


class ReportService:
    @staticmethod
    def generate_pdf() -> BytesIO:
        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=0.5 * inch)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("Title", parent=styles["Heading1"], textColor=colors.HexColor("#4F4F4F"), spaceAfter=12)
        body = styles["Normal"]

        kpis = DataService.get_kpis()
        insights = DataService.get_insights().get("insights", [])[:8]
        metrics = DataService.get_model_metrics()

        elements = [
            Paragraph("HR Intelligence Platform — Analytics Report", title_style),
            Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}", body),
            Spacer(1, 20),
            Paragraph("Key Performance Indicators", styles["Heading2"]),
        ]

        kpi_data = [["Metric", "Value"]]
        for k, v in kpis.items():
            label = k.replace("Employees", " Employees").replace("Rate", " Rate").replace("average", "Average ")
            kpi_data.append([label, str(v)])

        kpi_table = Table(kpi_data, colWidths=[3 * inch, 2 * inch])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D4AF37")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F6F3")]),
        ]))
        elements.append(kpi_table)
        elements.append(Spacer(1, 20))

        if metrics.get("best_model"):
            elements.append(Paragraph(f"Best ML Model: {metrics['best_model']} (ROC-AUC: {metrics.get('best_roc_auc', 'N/A')})", body))
            elements.append(Spacer(1, 12))

        elements.append(Paragraph("Business Insights", styles["Heading2"]))
        for item in insights:
            elements.append(Paragraph(f"<b>{item['title']}</b>: {item['insight']}", body))
            elements.append(Spacer(1, 8))

        doc.build(elements)
        buf.seek(0)
        return buf

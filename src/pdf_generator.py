#!/usr/bin/env python3

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import plotly.graph_objects as go
import plotly.io as pio
import tempfile
import base64

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for PDF generation"""
        # Custom title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#000428'),
            alignment=TA_CENTER,
            borderWidth=2,
            borderColor=HexColor('#00d4ff'),
            borderRadius=10
        ))
        
        # Custom heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#1e3c72'),
            borderWidth=1,
            borderColor=HexColor('#00d4ff'),
            borderRadius=5
        ))
        
        # Custom subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubheading',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor=HexColor('#2a5298')
        ))
        
        # Custom body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=black,
            leading=14
        ))
    
    def create_analytics_pdf(self, analytics_data, filename=None):
        """Generate PDF for Analytics Report"""
        if filename is None:
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        
        # Title Page
        story.append(Paragraph("📊 Cuspera Analytics Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Report Metadata
        metadata = [
            ['Report Type', 'Interactive Analytics'],
            ['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Company', analytics_data.get('company_name', 'N/A')],
            ['Industry', analytics_data.get('industry', 'N/A')],
            ['Target Software', analytics_data.get('target_software', 'N/A')]
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 20))
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("🎯 Executive Summary", self.styles['CustomHeading']))
        
        summary_text = f"""
        This comprehensive analytics report provides detailed insights for {analytics_data.get('company_name', 'Your Company')} 
        in the {analytics_data.get('industry', 'Technology')} industry. The analysis focuses on implementing 
        {analytics_data.get('target_software', '6sense Revenue AI')} with projected improvements in key performance metrics.
        """
        
        story.append(Paragraph(summary_text, self.styles['CustomBody']))
        story.append(Spacer(1, 12))
        
        # Key Metrics
        story.append(Paragraph("📈 Key Performance Metrics", self.styles['CustomHeading']))
        
        metrics_data = [
            ['Metric', 'Current', 'Projected', 'Improvement'],
            ['ROI', f"{analytics_data.get('current_roi', 2.0):.1f}x", f"{analytics_data.get('projected_roi', 3.5):.1f}x", f"+{analytics_data.get('projected_roi', 3.5)/analytics_data.get('current_roi', 2.0)*100-100:.0f}%"],
            ['Monthly Leads', f"{analytics_data.get('monthly_leads', 100)}", f"{analytics_data.get('projected_leads', 210)}", f"+{analytics_data.get('projected_leads', 210)/analytics_data.get('monthly_leads', 100)*100-100:.0f}%"],
            ['Conversion Rate', f"{analytics_data.get('conversion_rate', 5.0):.1f}%", f"{analytics_data.get('projected_conversion', 7.0):.1f}%", f"+{analytics_data.get('projected_conversion', 7.0)/analytics_data.get('conversion_rate', 5.0)*100-100:.0f}%"],
            ['Payback Period', f"{analytics_data.get('timeline', 3)} months", f"{analytics_data.get('payback_months', 2.1):.1f} months", f"-{analytics_data.get('timeline', 3)-analytics_data.get('payback_months', 2.1):.1f} months"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 20))
        
        # Financial Impact
        story.append(Paragraph("💰 Financial Impact Analysis", self.styles['CustomHeading']))
        
        current_revenue = analytics_data.get('monthly_leads', 100) * analytics_data.get('avg_deal_size', 10000) * (analytics_data.get('conversion_rate', 5.0)/100)
        projected_revenue = analytics_data.get('projected_leads', 210) * analytics_data.get('avg_deal_size', 10000) * (analytics_data.get('projected_conversion', 7.0)/100)
        monthly_increase = projected_revenue - current_revenue
        
        financial_data = [
            ['Financial Metric', 'Amount'],
            ['Current Monthly Revenue', f"${current_revenue:,.0f}"],
            ['Projected Monthly Revenue', f"${projected_revenue:,.0f}"],
            ['Monthly Increase', f"${monthly_increase:,.0f}"],
            ['Annual Impact', f"${monthly_increase*12:,.0f}"]
        ]
        
        financial_table = Table(financial_data, colWidths=[3*inch, 3*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(financial_table)
        story.append(Spacer(1, 20))
        
        # RAG Insights
        if analytics_data.get('rag_insights'):
            story.append(Paragraph("🧠 AI-Powered Insights", self.styles['CustomHeading']))
            story.append(Paragraph(analytics_data['rag_insights'], self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Implementation Strategy
        story.append(Paragraph("🚀 Implementation Strategy", self.styles['CustomHeading']))
        
        strategy_text = f"""
        <b>Software:</b> {analytics_data.get('target_software', 'N/A')}<br/>
        <b>Timeline:</b> {analytics_data.get('timeline', 3)} months<br/>
        <b>Complexity:</b> {analytics_data.get('complexity', 'Medium')}<br/>
        <b>Budget:</b> {analytics_data.get('budget', 'N/A')}<br/>
        <b>Expected ROI:</b> {analytics_data.get('projected_roi', 3.5):.1f}x
        """
        
        story.append(Paragraph(strategy_text, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def create_roi_pdf(self, roi_data, filename=None):
        """Generate PDF for ROI Calculator Report"""
        if filename is None:
            filename = f"roi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        
        # Title Page
        story.append(Paragraph("💰 ROI Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Company Information
        story.append(Paragraph("🏢 Company Profile", self.styles['CustomHeading']))
        
        company_data = [
            ['Company Name', roi_data.get('company_name', 'N/A')],
            ['Industry', roi_data.get('industry', 'N/A')],
            ['Company Size', roi_data.get('company_size', 'N/A')],
            ['Annual Revenue', f"${roi_data.get('annual_revenue', 0):,.0f}"],
            ['Target Software', roi_data.get('target_software', 'N/A')]
        ]
        
        company_table = Table(company_data, colWidths=[2.5*inch, 3.5*inch])
        company_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(company_table)
        story.append(Spacer(1, 20))
        
        # ROI Calculations
        story.append(Paragraph("📊 ROI Analysis", self.styles['CustomHeading']))
        
        roi_calculations = [
            ['Metric', 'Value', 'Calculation'],
            ['Current Monthly Revenue', f"${roi_data.get('current_monthly_revenue', 0):,.0f}", f"{roi_data.get('monthly_leads', 0)} × ${roi_data.get('avg_deal_size', 0):,.0f} × {roi_data.get('conversion_rate', 0):.1f}%"],
            ['Projected Monthly Revenue', f"${roi_data.get('projected_monthly_revenue', 0):,.0f}", f"{roi_data.get('projected_leads', 0)} × ${roi_data.get('avg_deal_size', 0):,.0f} × {roi_data.get('projected_conversion', 0):.1f}%"],
            ['Monthly Increase', f"${roi_data.get('monthly_increase', 0):,.0f}", "Projected - Current"],
            ['Annual Impact', f"${roi_data.get('annual_impact', 0):,.0f}", "Monthly × 12"],
            ['Implementation Cost', f"${roi_data.get('implementation_cost', 0):,.0f}", "Based on budget range"],
            ['Payback Period', f"{roi_data.get('payback_months', 0):.1f} months", "Cost ÷ Monthly Increase"],
            ['Annual ROI', f"{roi_data.get('annual_roi', 0):.1f}x", "Annual Impact ÷ Cost"]
        ]
        
        roi_table = Table(roi_calculations, colWidths=[2.5*inch, 2*inch, 3*inch])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(roi_table)
        story.append(Spacer(1, 20))
        
        # RAG Insights
        if roi_data.get('rag_insights'):
            story.append(Paragraph("🧠 AI-Powered ROI Insights", self.styles['CustomHeading']))
            story.append(Paragraph(roi_data['rag_insights'], self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Recommendations
        story.append(Paragraph("💡 Recommendations", self.styles['CustomHeading']))
        
        recommendations = [
            "✅ Proceed with implementation based on positive ROI projections",
            "✅ Focus on quick wins to demonstrate early value",
            "✅ Establish clear KPIs for performance tracking",
            "✅ Plan for continuous optimization and improvement"
        ]
        
        for rec in recommendations:
            story.append(Paragraph(rec, self.styles['CustomBody']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def create_comprehensive_report_pdf(self, report_data, filename=None):
        """Generate PDF for Comprehensive Report"""
        if filename is None:
            filename = f"comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        story = []
        
        # Title Page
        story.append(Paragraph("📋 Comprehensive Intelligence Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Report Information
        story.append(Paragraph("📊 Report Information", self.styles['CustomHeading']))
        
        report_info = [
            ['Report Type', report_data.get('type', 'N/A')],
            ['Target Software', report_data.get('software', 'N/A')],
            ['Industry', report_data.get('industry', 'N/A')],
            ['Company Focus', report_data.get('company', 'N/A')],
            ['Period', f"{report_data.get('date_range', [datetime.now(), datetime.now()])[0]} to {report_data.get('date_range', [datetime.now(), datetime.now()])[1]}"],
            ['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        ]
        
        info_table = Table(report_info, colWidths=[2.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1e3c72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("🎯 Executive Summary", self.styles['CustomHeading']))
        
        summary_text = f"""
        This comprehensive intelligence report provides in-depth analysis of {report_data.get('software', 'N/A')} 
        for the {report_data.get('industry', 'N/A')} industry. The analysis includes implementation strategies, 
        ROI projections, best practices, and technical considerations specifically tailored for 
        {report_data.get('company', 'your organization')}.
        """
        
        story.append(Paragraph(summary_text, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Main RAG Report
        if report_data.get('main_report'):
            story.append(Paragraph("🧠 AI-Generated Analysis", self.styles['CustomHeading']))
            story.append(Paragraph(report_data['main_report'], self.styles['CustomBody']))
            story.append(Spacer(1, 20))
        
        # Additional Insights
        if report_data.get('additional_insights'):
            story.append(Paragraph("🔍 Deep Dive Analysis", self.styles['CustomHeading']))
            
            for i, insight in enumerate(report_data['additional_insights'][:4]):
                story.append(Paragraph(f"🔍 Insight {i+1}", self.styles['CustomSubheading']))
                story.append(Paragraph(insight, self.styles['CustomBody']))
                story.append(Spacer(1, 12))
        
        # Implementation Timeline
        story.append(Paragraph("📅 Implementation Roadmap", self.styles['CustomHeading']))
        
        phases = [
            {
                'phase': 'Phase 1: Planning & Setup',
                'duration': 'Weeks 1-2',
                'activities': ['Stakeholder alignment', 'Technical assessment', 'Resource allocation']
            },
            {
                'phase': 'Phase 2: Implementation',
                'duration': 'Weeks 3-6',
                'activities': ['System integration', 'Team training', 'Process mapping']
            },
            {
                'phase': 'Phase 3: Optimization',
                'duration': 'Weeks 7-12+',
                'activities': ['Performance monitoring', 'Continuous improvement', 'Advanced features']
            }
        ]
        
        for phase in phases:
            story.append(Paragraph(phase['phase'], self.styles['CustomSubheading']))
            story.append(Paragraph(f"<b>Duration:</b> {phase['duration']}", self.styles['CustomBody']))
            story.append(Paragraph("<b>Key Activities:</b>", self.styles['CustomBody']))
            for activity in phase['activities']:
                story.append(Paragraph(f"• {activity}", self.styles['CustomBody']))
            story.append(Spacer(1, 12))
        
        # Success Metrics
        story.append(Paragraph("📊 Success Metrics & KPIs", self.styles['CustomHeading']))
        
        kpis = [
            ['KPI', 'Target', 'Measurement'],
            ['Lead Quality Score', '85%', 'AI scoring algorithm'],
            ['Implementation Velocity', '2.3x faster', 'Time to deployment'],
            ['ROI Achievement', '3.5x average', 'Revenue vs. investment'],
            ['User Adoption', '92%', 'Platform usage metrics'],
            ['Process Efficiency', '+45%', 'Workflow optimization']
        ]
        
        kpi_table = Table(kpis, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#ff6b6b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#00d4ff'))
        ]))
        
        story.append(kpi_table)
        story.append(Spacer(1, 20))
        
        # Action Items
        story.append(Paragraph("🚀 Recommended Action Items", self.styles['CustomHeading']))
        
        actions = [
            {'priority': '🔴 Critical', 'action': 'Executive Sponsorship', 'timeline': 'Week 1', 'owner': 'Project Sponsor'},
            {'priority': '🟡 High', 'action': 'Technical Assessment', 'timeline': 'Week 2', 'owner': 'IT Team'},
            {'priority': '🟢 Medium', 'action': 'Team Training', 'timeline': 'Week 3-4', 'owner': 'HR/Training'},
            {'priority': '🔵 Low', 'action': 'Performance Monitoring', 'timeline': 'Ongoing', 'owner': 'Operations'}
        ]
        
        for action in actions:
            story.append(Paragraph(f"{action['priority']} {action['action']}", self.styles['CustomSubheading']))
            story.append(Paragraph(f"<b>Timeline:</b> {action['timeline']} | <b>Owner:</b> {action['owner']}", self.styles['CustomBody']))
            story.append(Spacer(1, 8))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    def save_pdf_to_temp(self, pdf_content, filename):
        """Save PDF content to temporary file and return path"""
        temp_dir = tempfile.gettempdir()
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        
        return filepath

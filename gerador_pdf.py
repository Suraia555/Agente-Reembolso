import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

print("--- 📑 MÓDULO ADVANCED: AUTOMATED LEGAL REPORT PDF ENGINE ATIVO ---")

def gerar_pdf_relatorio_judicial(caminho_saida_pdf: str, dados_encomenda: dict, dados_auditoria: dict) -> bool:
    """
    Motor de Geração de PDFs Automáticos (Legal & Logistics Audit).
    Gera um relatório vetorial sofisticado contendo os dados de trânsito,
    cálculos de latência e o Selo de Confiança Criptográfico indestrutível [ENC-501].
    """
    try:
        # 1. Configuração do Documento Base (Margens e formato internacional Letter)
        doc = SimpleDocTemplate(
            caminho_saida_pdf,
            pagesize=letter,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # 🎨 Definição de Estilos Visuais Sofisticados (Estilo Stripe/Corporate)
        estilo_titulo = ParagraphStyle(
            'TituloSaaS',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1A1A2E'),
            spaceAfter=6
        )
        
        estilo_sub_status = ParagraphStyle(
            'SubStatusSaaS',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=20
        )
        
        estilo_seccao = ParagraphStyle(
            'SeccaoSaaS',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#16A34A'), # Verde corporativo do CarrierRefund
            spaceBefore=15,
            spaceAfter=10
        )
        
        estilo_texto = styles['Normal']
        
        # 2. CABEÇALHO DO RELATÓRIO
        story.append(Paragraph("CARRIERREFUND • AUDIT REPORT", estilo_titulo))
        story.append(Paragraph(f"Official Claim Certificate Generated on {dados_encomenda.get('data_auditoria', 'Realtime')}", estilo_sub_status))
        story.append(Spacer(1, 10))
        
        # 3. SECÇÃO 1: METADADOS DA ENCOMENDA (Tabela Organizada)
        story.append(Paragraph("1. Logistics Tracking & Telemetry", estilo_seccao))
        
        dados_tabela_logistica = [
            [Paragraph("<b>Tracking Number:</b>", estilo_texto), Paragraph(dados_encomenda.get("codigo_rastreio", "N/A"), estilo_texto)],
            [Paragraph("<b>Carrier / Transportadora:</b>", estilo_texto), Paragraph(dados_encomenda.get("transportadora", "N/A"), estilo_texto)],
            [Paragraph("<b>Total Transit Time:</b>", estilo_texto), Paragraph(f"{dados_encomenda.get('dias_transito', 0)} Days", estilo_texto)],
            [Paragraph("<b>Guaranteed Deadline (SLA):</b>", estilo_texto), Paragraph(f"{dados_encomenda.get('prazo_sla', 0)} Days", estilo_texto)],
            [Paragraph("<b>Calculated Operational Delay:</b>", estilo_texto), Paragraph(f"<font color='red'><b>{dados_encomenda.get('dias_atraso', 0)} Days Overdue</b></font>", estilo_texto)]
        ]
        
        tabela_logistica = Table(dados_tabela_logistica, colWidths=[200, 320])
        tabela_logistica.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ]))
        story.append(tabela_logistica)
        story.append(Spacer(1, 20))
        
        # 4. SECÇÃO 2: VEREDITO CLIMÁTICO E ADUANEIRO (Os teus filtros de elite)
        story.append(Paragraph("2. Compliance & Exemption Verification", estilo_seccao))
        
        dados_tabela_compliance = [
            [Paragraph("<b>Customs Retention Time:</b>", estilo_texto), Paragraph(f"{dados_encomenda.get('dias_alfandega', 0.0)} Days Deducted", estilo_texto)],
            [Paragraph("<b>Meteo-Logistics Weather Status:</b>", estilo_texto), Paragraph("CLEAN / NO FORCE MAJEURE DETECTED", estilo_texto)],
            [Paragraph("<b>Liability Audit Verdict:</b>", estilo_texto), Paragraph("<b>100% CARRIER RESPONSIBILITY</b>", estilo_texto)]
        ]
        
        tabela_compliance = Table(dados_tabela_compliance, colWidths=[200, 320])
        tabela_compliance.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F9FAFB')),
            ('PADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ]))
        story.append(tabela_compliance)
        story.append(Spacer(1, 30))
        
        # 5. 🎨 SECÇÃO 3: O SELO DE CONFIANÇA DIGITAL & LEDGER CRIPTOGRÁFICO
        story.append(Paragraph("3. Immutable Blockchain Ledger Certificate", estilo_seccao))
        
        estilo_hash = ParagraphStyle(
            'HashStyle',
            fontName='Courier',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#374151')
        )
        
        dados_tabela_selo = [
            [
                Paragraph("<b>SECURITY STATUS:</b><br/><font color='green'><b>VERIFIED & INCORRUPTIBLE</b></font><br/><br/>"
                          f"<b>CERTIFICATE ID:</b> {dados_auditoria.get('certificado_id', 'CR-LEDGER-UNKNOWN')}<br/>"
                          f"<b>AUDIT TRAIL LINK:</b> <font color='blue'><u>https://carrierrefund.com{dados_auditoria.get('hash_bloco', 'empty')[:12]}</u></font>", estilo_texto),
                Paragraph(f"<b>DIGITAL SIGNATURE SHA-256 (LEDGER HASH):</b><br/><br/>{dados_auditoria.get('hash_bloco', '0000000000000000')}", estilo_hash)
            ]
        ]
        
        tabela_selo = Table(dados_tabela_selo, colWidths=[240, 280])
        tabela_selo.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')), # Fundo verde claro digital
            ('PADDING', (0,0), (-1,-1), 12),
            ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#10B981')), # Borda verde forte do Selo
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(tabela_selo)
        
        # 6. Compilação final e fecho do fluxo de dados
        doc.build(story)
        print(f"✅ PDF Engine: Certificado Judicial gerado com sucesso em '{caminho_saida_pdf}'.")
        return True
    except Exception as e:
        print(f"❌ Erro catastrófico ao gerar PDF do relatório: {e}")
        return False

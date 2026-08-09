from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line
from database import get_connection


def generate():

    conn = get_connection()
    cursor = conn.cursor()
    # -----------------------
    # Dashboard Statistics
    # -----------------------

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='Positive'")
    positive = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='Negative'")
    negative = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM feedback WHERE sentiment='Neutral'")
    neutral = cursor.fetchone()[0]

    cursor.execute("""
    SELECT *
    FROM feedback
    ORDER BY submission_id DESC,
    CASE category
        WHEN 'Course' THEN 1
        WHEN 'Faculty' THEN 2
        WHEN 'Facility' THEN 3
    END
    """)

    rows = cursor.fetchall()

    conn.close()

    pdf = SimpleDocTemplate("FeedbackReport.pdf")

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    subtitle_style = styles["Heading2"]
    subtitle_style.alignment = TA_CENTER

    elements = []

    # ==========================
    # Project Logo
    # ==========================

    logo = Image(
        "static/images/logo.png",
        width=80,
        height=80
    )

    logo.hAlign = "CENTER"

    elements.append(logo)

    elements.append(Spacer(1, 10))

    from datetime import datetime

    today = datetime.now().strftime("%d %B %Y, %I:%M %p")

    score = round(
        ((positive * 100) + (neutral * 50)) / total
    ) if total else 0

    # -----------------------
    # Report Heading
    # -----------------------

    elements.append(
        Paragraph(
            "<font color='#0d6efd'><b>SMART FEEDBACK &amp; SUGGESTION PORTAL</b></font>",
            title_style
        )
    )

    d = Drawing(500, 1)

    d.add(Line(0, 0, 500, 0))

    elements.append(d)

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        "AI Powered Student Feedback Analytics Report",
        subtitle_style
    ))

    elements.append(Spacer(1,6))

    elements.append(Paragraph(
        f"<b>Report Generated:</b> {today}",
        styles["Normal"]
    ))

    elements.append(Spacer(1,6))

    elements.append(Paragraph(
        "<b>DASHBOARD SUMMARY</b>",
        styles["Heading2"]
    ))

    elements.append(Paragraph(
        f"Total Feedback : {total}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Positive Feedback : {positive}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Negative Feedback : {negative}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Neutral Feedback : {neutral}",
        styles["Normal"]
    ))

    elements.append(Paragraph(
        f"Overall Satisfaction Score : {score}/100",
        styles["Normal"]
    ))

    elements.append(Spacer(1,18))

    # -----------------------
    # AI Summary
    # -----------------------

    elements.append(Paragraph(
        "<b>AI SUMMARY</b>",
        styles["Heading2"]
    ))

    if score >= 80:

        summary = "Overall student satisfaction is excellent."

    elif score >= 60:

        summary = "Student satisfaction is good with minor improvements needed."

    elif score >= 40:

        summary = "Student satisfaction is moderate. Improvement is recommended."

    else:

        summary = "Student satisfaction is low. Immediate action is required."

    elements.append(
        Paragraph(summary, styles["Normal"])
    )

    elements.append(Spacer(1,6))

    # -----------------------
    # AI Recommendations
    # -----------------------

    elements.append(Paragraph(
        "<b>AI RECOMMENDATIONS</b>",
        styles["Heading2"]
    ))

    recommendations = []

    if negative > positive:

        recommendations.append(
            "• High negative feedback detected. Investigate student concerns."
        )

    if positive >= negative:

        recommendations.append(
            "• Maintain current academic quality and continue collecting feedback."
        )

    if neutral > 0:

        recommendations.append(
            "• Encourage students to provide more detailed feedback."
        )

    recommendations.append(
        "• Review course quality, faculty performance, and campus facilities regularly."
    )

    for item in recommendations:

        elements.append(
            Paragraph(item, styles["Normal"])
        )

    elements.append(Spacer(1,18))

    from reportlab.platypus import PageBreak

    elements.append(PageBreak())

    from reportlab.lib.styles import ParagraphStyle

    report_title = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading2"],
        alignment=1,
        textColor=colors.HexColor("#0d6efd"),
        spaceAfter=18
    )

    elements.append(
        Paragraph(
            "<b>COMPLETE FEEDBACK REPORT</b>",
            report_title
        )
    )

    elements.append(Spacer(1, 15))

    # ----------------------------
    # Group rows by Submission ID
    # ----------------------------

    submissions = {}

    for row in rows:

        sid = row["submission_id"]

        if sid not in submissions:

            submissions[sid] = {
                "student": row["student_name"],
                "date": row["date"].strftime("%Y-%m-%d") if row["date"] else "",
                "overall": row["overall_suggestion"],
                "items": []
            }

        submissions[sid]["items"].append(row)

    # ----------------------------
    # Print Report
    # ----------------------------

    for sid, data in submissions.items():

        submission_style = ParagraphStyle(
            "SubmissionStyle",
            parent=styles["Heading1"],
            alignment=1,
            textColor=colors.HexColor("#0d6efd"),
            spaceAfter=10
        )

        line = Drawing(450,1)
        line.add(Line(0,0,450,0))
        elements.append(line)

        elements.append(Spacer(1,10))

        submission_style = ParagraphStyle(
            "SubmissionStyle",
            parent=styles["Heading1"],
            alignment=1,
            textColor=colors.HexColor("#0d6efd"),
            spaceAfter=10
        )

        elements.append(
            Paragraph(
                f"<b>Submission #{sid}</b>",
                submission_style
            )
        )

        from datetime import datetime

        try:
            formatted_date = datetime.strptime(
                data["date"],
                "%Y-%m-%d"
            ).strftime("%d %B %Y")
        except:
            formatted_date = data["date"]

        elements.append(
            Paragraph(
                f"<b>Student :</b> {data['student']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Date :</b> {formatted_date}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1,8))


        elements.append(Spacer(1,10))

        table_data = [

            ["Category", "Sentiment", "AI Suggestion"]

        ]

        for item in data["items"]:

            if item["category"] == "Course":
                category = "Course"

            elif item["category"] == "Faculty":
                category = "Faculty"

            else:
                category = "Facility"

            if item["sentiment"] == "Positive":
                sentiment = "Positive"

            elif item["sentiment"] == "Negative":
                sentiment = "Negative"

            else:
                sentiment = "Neutral"

            table_data.append([

                category,

                sentiment,

                Paragraph(
                    item["suggestion"],
                    styles["BodyText"]
                )

            ])

        table = Table(

            table_data,

            colWidths=[130,100,210]

        )

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0d6efd")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("BOTTOMPADDING",(0,0),(-1,0),12),

            ("TOPPADDING",(0,0),(-1,0),12),

        ]))

        elements.append(table)

        elements.append(Spacer(1,6))

        elements.append(

            Paragraph(

                "<b>Feedback Details</b>",

                styles["Heading3"]

            )

        )

        elements.append(Spacer(1,5))

        for item in data["items"]:

            if item["category"] == "Course":
                category = "Course"

            elif item["category"] == "Faculty":
                category = "Faculty"

            else:
                category = "Facility"

            elements.append(
                Paragraph(
                    f"<b>{category}</b>",
                    styles["Heading3"]
                )
            )

            elements.append(
                Paragraph(
                    item["feedback"].replace("\n", "<br/>"),
                    styles["BodyText"]
                )
            )

            elements.append(Spacer(1,8))

        if data["overall"]:

            elements.append(Spacer(1,8))

            suggestion_table = Table([

                ["Student Suggestion"],

                [Paragraph(data["overall"], styles["BodyText"])]

            ], colWidths=[440])

            suggestion_table.setStyle(TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0d6efd")),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("BOTTOMPADDING",(0,0),(-1,-1),8),

                ("TOPPADDING",(0,0),(-1,-1),8),

            ]))

            elements.append(suggestion_table)

        elements.append(Spacer(1,6))

        elements.append(Spacer(1,10))

        line = Drawing(450,1)

        line.add(

            Line(

                0,

                0,

                450,

                0

            )

        )

        elements.append(line)

        elements.append(Spacer(1,8))

        elements.append(Spacer(1,8))

    elements.append(Spacer(1,20))

    elements.append(Spacer(1,20))

    line = Drawing(450,1)
    line.add(Line(0,0,450,0))
    elements.append(line)

    elements.append(Spacer(1,12))

    elements.append(
        Paragraph(
            "<para align='center'><b>Generated by</b></para>",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "<para align='center'><font color='#0d6efd'><b>SMART FEEDBACK &amp; SUGGESTION PORTAL</b></font></para>",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1,8))

    elements.append(
        Paragraph(
            "<para align='center'><b>Developed By</b></para>",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "<para align='center'>Avijit Roy</para>",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,10))

    elements.append(
        Paragraph(
            "<para align='center'><font color='grey'>This report was automatically generated by the Smart Feedback &amp; Suggestion Portal.</font></para>",
            styles["Italic"]
        )
    )

    pdf.build(elements)

def generate_login_history():

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # Statistics
    # ==========================

    cursor.execute("SELECT COUNT(*) FROM login_history")
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM login_history
    WHERE status='Online'
    """)
    online = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM login_history
    WHERE status='Logged Out'
    """)
    logged_out = cursor.fetchone()[0]

    cursor.execute("""
    SELECT *
    FROM login_history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    pdf = SimpleDocTemplate("LoginHistoryReport.pdf")

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    subtitle_style = styles["Heading2"]
    subtitle_style.alignment = TA_CENTER

    elements = []

    # ==========================
    # Project Logo
    # ==========================

    logo = Image(
        "static/images/logo.png",
        width=80,
        height=80
    )

    logo.hAlign = "CENTER"

    elements.append(logo)

    elements.append(Spacer(1, 10))

    today = get_ist_time().strftime("%d %B %Y %I:%M %p")

    # ==========================
    # Heading
    # ==========================

    elements.append(
        Paragraph(
            "<font color='#0d6efd'><b>SMART FEEDBACK &amp; SUGGESTION PORTAL</b></font>",
            title_style
        )
    )

    d = Drawing(500, 1)

    d.add(Line(0, 0, 500, 0))

    elements.append(d)

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Student Login History Report",
            subtitle_style
        )
    )

    elements.append(Spacer(1,6))

    elements.append(
        Paragraph(
            f"<b>Generated On:</b> {today}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,8))

    # ==========================
    # Summary
    # ==========================

    elements.append(
        Paragraph(
            "<b>LOGIN SUMMARY</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Login Records : {total}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Currently Online : {online}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Logged Out : {logged_out}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1,18))

    # ==========================
    # Table
    # ==========================

    data = [[

        "ID",

        "Student",

        "Email",

        "Login",

        "Logout",

        "Status"

    ]]

    for i, row in enumerate(rows, start=1):

        logout = row["logout_time"]

        if logout is None:

            logout = "Still Online"

        data.append([

            i,

            row["student_name"],

            row["email"],

            row["login_time"],

            logout,

            row["status"]

        ])

    table = Table(

        data,

        colWidths=[30,80,150,110,110,70]

    )

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("FONTSIZE",(0,0),(-1,-1),8),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE")

    ]))

    elements.append(table)

    elements.append(Spacer(1,20))

    elements.append(
        Paragraph(
            "<b>Generated by Smart Feedback & Suggestion Portal</b>",
            styles["Heading3"]
        )
    )

    elements.append(
        Paragraph(
            "Developed By: Avijit Roy",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1,10)
    )

    elements.append(
        Paragraph(
            "<font color='grey'>This report was automatically generated by the Smart Feedback & Suggestion Portal.</font>",
            styles["Italic"]
        )
    )

    pdf.build(elements)
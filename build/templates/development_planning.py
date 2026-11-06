from .base import *


class GanttChart(PptxSpec):
    @property
    def rel(self):
        return "development-planning/gantt-chart/gantt-chart.pptx"

    example = {
        "text": {
            "title": "Coupon feature for FreshDrop, 5 Jan – 16 Feb 2026",
            "start_date": "5 January 2026",
            "milestones": "26 Jan: design approved. 9 Feb: QA complete. 16 Feb: launch to all users",
            "dependencies": "Screens wait for the design; QA waits for the API and screens. The QA chain (days 21–35) sets the launch date",
            "risks": "Payment provider certification may take 5 days; a 3-day buffer sits inside the QA task",
        },
        "charts": {"gantt": {
            "categories": ["1. Design coupon flow · Anna", "2. Build API · Ivan", "3. Build app screens · Olga (after 1)",
                           "4. QA and fixes · Ivan (after 2, 3)", "5. Staged rollout · Lena (after 4)", "◆ Milestone: launch"],
            "series": [{"name": "Start, day from kickoff", "values": [0, 7, 10, 21, 35, 42]},
                       {"name": "Duration, days", "values": [10, 14, 10, 14, 7, 0]},
                       {"name": "Milestone", "values": [0, 0, 0, 0, 0, 0.5]}],
        }},
    }

    def draw(self, prs, slide):
        header(slide, "GANTT CHART", "{{title: project and planning horizon}}")
        tasks = [("{{task: task name, owner and dependencies}}", 0, 0, 0)]
        data = CategoryChartData()
        data.categories = [t[0] for t in tasks]
        data.add_series("Start, day from kickoff", [t[1] for t in tasks])
        data.add_series("Duration, days", [t[2] for t in tasks])
        data.add_series("Milestone", [t[3] for t in tasks])
        frame = slide.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(5.5), data)
        label(slide.shapes, 0.5, 6.85, 8.5, 0.4,
              "Scale — days from kickoff. Start: {{start_date: project start date}}", size=11, color=MUTED)
        frame.name = "gantt"
        chart = frame.chart
        ids = {}
        for el in chart._chartSpace.xpath(".//c:axId | .//c:crossAx"):
            el.set("val", str(ids.setdefault(el.get("val"), 500000 + len(ids))))
        chart.has_legend = False
        chart.font.name, chart.font.size = FONT, Pt(11)
        chart.font.color.rgb = INK
        offset, duration, milestone = chart.plots[0].series
        milestone.format.fill.solid()
        milestone.format.fill.fore_color.rgb = INK
        offset.format.fill.background()
        offset.format.line.fill.background()
        duration.format.fill.solid()
        duration.format.fill.fore_color.rgb = ACCENT
        chart.plots[0].gap_width = 60
        cat = chart.category_axis
        cat.reverse_order = True
        cat.format.line.color.rgb = LINE
        cat.has_major_gridlines = False
        val = chart.value_axis
        val.minimum_scale = 0
        val.major_unit = 7
        val.has_major_gridlines = True
        val.major_gridlines.format.line.color.rgb = LINE
        val.tick_labels.number_format = "0"
        val.tick_labels.number_format_is_linked = False
        val.format.line.fill.background()

        x, w = 9.25, 3.6
        panels = [
            ("Milestones", "{{milestones: key dates, one per line}}", 1.3, 1.75),
            ("Dependencies", "{{dependencies: tasks that wait for others, critical chain}}", 3.15, 2.0),
            ("Schedule risks", "{{risks: what could shift the plan, and the buffer}}", 5.25, 1.95),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.35, w, ph - 0.35), token, size=11)

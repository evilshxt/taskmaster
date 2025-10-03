"""Dashboard widget for TaskMaster Pro.

This module contains the dashboard widget that displays task statistics and productivity metrics.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QPen, QBrush
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis

from ...models.task import Status, Priority

class DashboardWidget(QWidget):
    """Dashboard widget showing task statistics and productivity metrics."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the dashboard UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Stats cards row
        stats_layout = QHBoxLayout()
        self.total_tasks_card = self.create_stat_card("Total Tasks", "0", "#4CAF50")
        self.completed_card = self.create_stat_card("Completed", "0", "#2196F3")
        self.in_progress_card = self.create_stat_card("In Progress", "0", "#FFC107")
        self.overdue_card = self.create_stat_card("Overdue", "0", "#F44336")
        
        stats_layout.addWidget(self.total_tasks_card)
        stats_layout.addWidget(self.completed_card)
        stats_layout.addWidget(self.in_progress_card)
        stats_layout.addWidget(self.overdue_card)
        
        # Charts row
        charts_layout = QHBoxLayout()
        
        # Priority chart
        priority_chart = self.create_priority_chart()
        priority_chart.setMinimumHeight(300)
        
        # Status chart
        status_chart = self.create_status_chart()
        status_chart.setMinimumHeight(300)
        
        charts_layout.addWidget(priority_chart, 1)
        charts_layout.addWidget(status_chart, 1)
        
        # Add to main layout
        layout.addLayout(stats_layout)
        layout.addLayout(charts_layout, 1)
        
    def create_stat_card(self, title, value, color):
        """Create a stat card widget."""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }}
            QLabel#value {{ 
                font-size: 24px; 
                font-weight: bold;
                color: {color};
            }}
            QLabel#title {{ 
                color: #666;
                font-size: 14px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        title_label = QLabel(title)
        title_label.setObjectName("title")
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        layout.addStretch()
        
        return card
        
    def create_priority_chart(self):
        """Create a pie chart showing task distribution by priority."""
        series = QPieSeries()
        series.append("High", 0)
        series.append("Medium", 0)
        series.append("Low", 0)
        
        # Set colors
        slices = series.slices()
        slices[0].setColor("#F44336")  # Red for high
        slices[1].setColor("#FFC107")  # Yellow for medium
        slices[2].setColor("#8BC34A")  # Green for low
        
        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Tasks by Priority")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background: transparent;")
        
        return chart_view
        
    def create_status_chart(self):
        """Create a bar chart showing task distribution by status."""
        # Create bars
        bar_set = QBarSet("Tasks")
        bar_set << 0 << 0 << 0  # Placeholder values for Not Started, In Progress, Completed
        
        # Set colors
        bar_set.setColor("#2196F3")  # Blue for bars
        
        # Create series and add bars
        series = QBarSeries()
        series.append(bar_set)
        
        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Tasks by Status")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Customize axis
        categories = ["Not Started", "In Progress", "Completed"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 10)  # Will be updated with actual data
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        chart.legend().setVisible(False)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setStyleSheet("background: transparent;")
        
        return chart_view
        
    def update_stats(self, tasks):
        """Update dashboard statistics with the given tasks."""
        if not tasks:
            return
            
        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == Status.COMPLETED)
        in_progress = sum(1 for t in tasks if t.status == Status.IN_PROGRESS)
        overdue = sum(1 for t in tasks if t.due_date and t.due_date < datetime.now() and t.status != Status.COMPLETED)
        
        # Update stat cards
        self.total_tasks_card.findChild(QLabel, "value").setText(str(total))
        self.completed_card.findChild(QLabel, "value").setText(str(completed))
        self.in_progress_card.findChild(QLabel, "value").setText(str(in_progress))
        self.overdue_card.findChild(QLabel, "value").setText(str(overdue))
        
        # Update priority chart
        priority_chart = self.findChild(QChartView).chart()
        if priority_chart and priority_chart.series():
            series = priority_chart.series()[0]
            high = sum(1 for t in tasks if t.priority == Priority.HIGH)
            medium = sum(1 for t in tasks if t.priority == Priority.MEDIUM)
            low = sum(1 for t in tasks if t.priority == Priority.LOW)
            
            for i, count in enumerate([high, medium, low]):
                series.slices()[i].setValue(count)
        
        # Update status chart
        status_chart = self.findChildren(QChartView)[1].chart()
        if status_chart and status_chart.series():
            series = status_chart.series()[0]
            bar_set = series.barSets()[0]
            
            not_started = sum(1 for t in tasks if t.status == Status.NOT_STARTED)
            in_progress = sum(1 for t in tasks if t.status == Status.IN_PROGRESS)
            completed = sum(1 for t in tasks if t.status == Status.COMPLETED)
            
            bar_set.replace(0, not_started)
            bar_set.replace(1, in_progress)
            bar_set.replace(2, completed)
            
            # Update Y-axis range
            max_value = max(not_started, in_progress, completed, 1)  # At least 1 to avoid division by zero
            status_chart.axisY().setRange(0, max_value * 1.2)  # Add 20% padding

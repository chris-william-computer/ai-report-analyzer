from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database.connection import Base

class Report(Base):
    """
    Database model representing a processed report with metadata and analytical results.

    This model defines the structure for storing information about uploaded reports that
    have been processed by the system. It captures essential metadata such as filename,
    upload timestamp, and row count, along with analytical results including a textual
    summary and an insight score. The Report model serves as the parent entity for
    associated metrics and provides a central record for tracking report processing
    status and results within the application's data pipeline.

    Example:
        # Creating a new report record
        report = Report(
            filename="sales_data_2024.csv",
            total_rows=1500,
            summary_text="Monthly sales analysis showing 15% growth",
            insight_score=8.7
        )
        
        # Querying existing reports
        recent_reports = session.query(Report).order_by(Report.upload_date.desc()).limit(10)
    """

    __tablename__ = "reports"
    """
    Database table name for storing report records.
    
    This specifies the physical table name in the database where Report instances are stored.
    The table contains columns for ID, filename, upload date, row count, summary text,
    and insight scores for processed reports.
    """

    id = Column(Integer, primary_key=True, index=True)
    """
    Unique identifier for the report record.
    
    This auto-incrementing integer serves as the primary key for the reports table,
    providing a unique identifier for each report record. The index property enables
    fast lookups and joins based on the ID field. This column is automatically
    managed by the database and should not be set manually when creating new records.
    """

    filename = Column(String, index=True)
    """
    Original filename of the uploaded report document.
    
    This string field stores the original name of the file that was uploaded and
    processed to create this report record. The indexed property allows for efficient
    searching and filtering by filename. This field is useful for identifying and
    referencing specific report files in the user interface and for audit purposes.
    """

    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    """
    Timestamp indicating when the report was uploaded and initially processed.
    
    This datetime field automatically captures the precise moment when the report
    was first created in the system. The timezone-aware setting ensures accurate
    time representation across different geographical locations. The server_default
    with func.now() ensures the timestamp is set by the database server rather than
    the application, providing more reliable and consistent timing information.
    """

    total_rows = Column(Integer)
    """
    Total number of data rows contained in the processed report.
    
    This integer field stores the count of rows in the original dataset that was
    analyzed to create this report. It provides valuable metadata about the size
    and scope of the processed data, which can be useful for performance monitoring,
    data validation, and user experience considerations when displaying results.
    """

    summary_text = Column(Text)
    """
    Analytical summary generated from the report data.
    
    This text field contains a human-readable summary of the insights extracted
    from the report data. The summary typically includes key findings, trends,
    anomalies, or other relevant information discovered during the analysis process.
    The Text type allows for longer content compared to String, accommodating detailed
    analytical summaries without length restrictions.
    """

    insight_score = Column(Float)
    """
    Numerical score representing the quality or significance of insights found in the report.
    
    This floating-point field contains a calculated score that quantifies the value
    or importance of the insights extracted from the report. Higher scores typically
    indicate more significant findings, stronger patterns, or more actionable intelligence
    discovered in the data. This score can be used for prioritization, sorting, or
    filtering reports based on their analytical value.
    """

class Metric(Base):
    """
    Database model representing individual metrics extracted from processed reports.

    This model defines the structure for storing quantitative measurements and key
    performance indicators that are extracted from reports during the analysis process.
    Each metric is associated with a specific report and contains a name-value pair
    representing a particular measurement. The Metric model enables detailed analysis
    of specific data points and supports reporting dashboards, trend analysis, and
    comparative studies across different reports.

    Example:
        # Creating metrics associated with a report
        revenue_metric = Metric(
            report_id=1,
            metric_name="total_revenue",
            metric_value=125000.50
        )
        
        conversion_metric = Metric(
            report_id=1,
            metric_name="conversion_rate",
            metric_value=2.35
        )
        
        # Querying metrics for a specific report
        report_metrics = session.query(Metric).filter(Metric.report_id == 1).all()
    """
    __tablename__ = "metrics"
    """
    Database table name for storing metric records.
    
    This specifies the physical table name in the database where Metric instances are stored.
    The table contains columns for ID, report reference, metric name, and metric value.
    """

    id = Column(Integer, primary_key=True, index=True)
    """
    Unique identifier for the metric record.
    
    This auto-incrementing integer serves as the primary key for the metrics table,
    providing a unique identifier for each metric record. The index property enables
    fast lookups and joins based on the ID field. This column is automatically
    managed by the database and should not be set manually when creating new records.
    """

    report_id = Column(Integer, index=True)
    """
    Foreign key reference to the associated report record.
    
    This integer field links the metric to its parent report by storing the ID of
    the corresponding Report record. The indexed property enables efficient queries
    to find all metrics associated with a particular report. While this doesn't
    enforce foreign key constraints at the SQLAlchemy level, it establishes the
    logical relationship between metrics and reports for data organization.
    """

    metric_name = Column(String)
    """
    Name or identifier of the measured metric.
    
    This string field contains the descriptive name of the metric being tracked,
    such as "revenue", "conversion_rate", "user_count", or "average_session_duration".
    The name provides semantic meaning to the metric value and allows for consistent
    identification of similar measurements across different reports. This field is
    crucial for metric categorization and analysis.
    """

    metric_value = Column(Float)
    """
    Numerical value of the measured metric.
    
    This floating-point field stores the actual quantitative value of the metric.
    It can represent various types of measurements including counts, percentages,
    monetary amounts, ratios, or other numerical data extracted from reports.
    The float type accommodates both integer and decimal values, providing precision
    for financial calculations, percentages, and other detailed measurements.
    """
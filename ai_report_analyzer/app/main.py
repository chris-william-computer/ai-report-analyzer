from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db, Base, engine
from app.database.models import Report, Metric
from app.ingestion.loader import load_csv_from_bytes, validate_dataframe
from app.processing.aggregator import aggregate_data, prepare_context_for_ai
from app.ai_integration.gemini_client import generate_insights
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload")
async def upload_report(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload and process a CSV report file, generating AI-powered insights.

    This endpoint accepts CSV file uploads and processes them through a complete
    data pipeline including validation, statistical analysis, and AI-powered
    insight generation. The function orchestrates the entire workflow from file
    ingestion to database persistence, creating a comprehensive report record
    with analytical results. It handles both the core data processing and the
    storage of results in the application database.

    The processing pipeline includes data loading and validation, statistical
    aggregation, AI context preparation, insight generation using Google's
    Gemini model, and database persistence of results. Error handling ensures
    that any issues during the processing pipeline are caught and reported
    appropriately, while successful processing results in a persistent report
    record that can be retrieved later.

    Args:
        file (UploadFile): CSV file uploaded by the client. The file must contain
                valid CSV-formatted data with appropriate headers and
                structure. The file size should be within reasonable
                limits to prevent memory issues during processing.

        db (Session): SQLAlchemy database session dependency injected by FastAPI.
                Provides access to the database for persisting report and
                metric records. The session is managed by the dependency
                injection system and automatically closed after the request.

    Returns:
        dict: Success response containing:
            - "status": Always "success" for successful processing
            - "report_id": Unique identifier of the created report in the database
            - "insights": AI-generated insights as a string (JSON format if parsing succeeds)

    Raises:
        HTTPException: With status code 500 if any error occurs during the
                processing pipeline, including file reading, data validation,
                AI processing failures, or database operations. The exception
                details contain the underlying error message for debugging.

    Example:
        # Using curl to upload a CSV file
        curl -X POST -F "file=@report.csv" http://localhost:8000/upload
        
        # Expected response on success:
        {
            "status": "success",
            "report_id": 123,
            "insights": "{\\"insight_1\\": \\"Revenue increased 15%...\\", ...}"
        }
    """
    try:
        contents = await file.read()
        df = load_csv_from_bytes(contents)
        validate_dataframe(df)
        
        stats = aggregate_data(df)
        context = prepare_context_for_ai(df, stats)
        ai_response = generate_insights(context)
        
        try:
            insights_json = json.loads(ai_response)
            summary_text = str(insights_json)
            score = insights_json.get("overall_score", 0.0)
        except:
            summary_text = ai_response
            score = 50.0
            
        new_report = Report(
            filename=file.filename,
            total_rows=len(df),
            summary_text=summary_text,
            insight_score=score
        )
        
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        
        return {"status": "success", "report_id": new_report.id, "insights": summary_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports")
async def get_reports(db: Session = Depends(get_db)):
    """
    Retrieve all processed reports from the database.

    This endpoint fetches all report records that have been successfully processed
    and stored in the database through previous upload operations. It provides a
    comprehensive view of all available reports with their metadata and analytical
    results. The function serves as a retrieval mechanism for accessing historical
    analysis results and reviewing previously processed data.

    The endpoint returns complete report objects including filenames, upload dates,
    row counts, summary texts, and insight scores. This information enables clients
    to browse, filter, and analyze the collection of processed reports. The operation
    performs a simple SELECT query on the reports table and returns all matching
    records without additional filtering or pagination.

    Args:
        db (Session): SQLAlchemy database session dependency injected by FastAPI.
                Provides access to the database for querying report records.
                The session is managed by the dependency injection system and
                automatically closed after the request completes.

    Returns:
        list: List of Report objects containing all processed reports in the database.
                Each Report object includes properties such as id, filename, upload_date,
                total_rows, summary_text, and insight_score. The returned list contains
                complete report data suitable for display in user interfaces or further
                processing by client applications.

    Example:
        # Request to get all reports
        GET http://localhost:8000/reports
        
        # Expected response:
        [
            {
                "id": 1,
                "filename": "sales_report.csv",
                "upload_date": "2024-01-15T10:30:00Z",
                "total_rows": 1500,
                "summary_text": "{\\"insight_1\\": \\"Sales up 15%...\\", ...}",
                "insight_score": 92.5
            },
            {
                "id": 2,
                "filename": "inventory_data.csv", 
                "upload_date": "2024-01-16T09:15:00Z",
                "total_rows": 850,
                "summary_text": "{\\"insight_1\\": \\"Inventory levels stable...\\", ...}",
                "insight_score": 78.0
            }
        ]
    """
    reports = db.query(Report).all()
    return reports
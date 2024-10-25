# Image Scaling Service

A microservice-based solution for scaling images using async processing with FastAPI and Redis queue.

## Architecture

The service consists of two main components:
- API Service (FastAPI)
- Processor Service (Async worker)

And uses the following infrastructure:
- Redis (Queue and temporary storage)
- PostgreSQL (Metadata storage)

### System Design
```
Client -> API Service -> Redis Queue -> Processor Service
                     -> PostgreSQL
```

## Features

- Upload images for scaling
- Async processing with task status tracking
- Configurable scaling options
  - Target width/height
  - Preserve aspect ratio
- Support for common image formats (JPEG, PNG, WebP)
- Task status monitoring
- Result retrieval

## Installation

### Requirements

- Python 3.11+
- Docker and Docker Compose
- Poetry (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd image-scaling-service
```

2. Install dependencies:
```bash
poetry install
```

3. Run with Docker Compose:
```bash
docker-compose up --build
```

## Usage

### API Endpoints

#### Create Scaling Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg" \
     -F "width=800" \
     -F "height=600" \
     -F "preserve_ratio=true"
```

Response:
```json
{
    "id": "task-uuid",
    "status": "pending",
    "created_at": "2024-01-01T12:00:00"
}
```

#### Get Task Status
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}"
```

Response:
```json
{
    "id": "task-uuid",
    "status": "completed",
    "created_at": "2024-01-01T12:00:00",
    "completed_at": "2024-01-01T12:00:05"
}
```

#### Get Result
```bash
curl -X GET "http://localhost:8000/api/v1/results/{task_id}"
```

Response:
```json
{
    "status": "completed",
    "data": "<processed-image-data>"
}
```

## Project Structure

```
image_scaling_service/
├── src/
│   ├── api/               # API service
│   │   ├── models/        # Data models
│   │   ├── views/         # FastAPI routes
│   │   ├── controllers/   # Business logic
│   │   └── repositories/  # Data access
│   │
│   ├── processor/         # Processing service
│   │   ├── models/       
│   │   └── services/     
│   │
│   └── common/           # Shared code
│       ├── config/      
│       └── utils/       
├── docker/              # Docker configs
└── tests/              # Test files
```

## Configuration

Environment variables:
```env
REDIS_URL=redis://redis:6379
POSTGRES_DSN=postgresql://user:password@postgres:5432/scaling_db
```

## Development

1. Create poetry environment:
```bash
poetry shell
```

2. Run services locally:
```bash
# API Service
uvicorn src.api.main:app --reload

# Processor Service
python -m src.processor.main
```

## API Documentation

Once running, access the OpenAPI documentation at:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Technical Details

### Image Processing
- Uses Pillow for image manipulation
- Supports aspect ratio preservation
- Handles multiple image formats

### Task Queue
- Redis-based queue for async processing
- Task status tracking
- Temporary result storage

### Error Handling
- Input validation
- Processing error tracking
- Task status monitoring

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
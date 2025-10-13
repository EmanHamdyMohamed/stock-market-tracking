# stock-market-backend

A FastAPI project generated with MCP (Model Context Protocol).

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **CORS Support**: Configured for cross-origin requests
- **Health Check**: Built-in health monitoring endpoint
- **Modular Structure**: Organized codebase with routers, models, schemas, and services
- **Environment Configuration**: Ready for environment-specific settings

## Project Structure

```
stock-market-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main FastAPI application
│   ├── routers/             # API route handlers
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── middleware/          # Custom middleware
│   ├── utils/               # Utility functions
│   └── core/                # Core configuration
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment (Optional)

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Available Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Development

### Adding New Routes

1. Create a new router in `app/routers/`
2. Import and include it in `app/main.py`

### Adding Models

1. Define your Pydantic models in `app/schemas/`
2. Add database models in `app/models/` (if using a database)

### Adding Services

1. Create business logic in `app/services/`
2. Import and use in your routers

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pydantic Settings**: Settings management

## License

This project is open source and available under the MIT License.

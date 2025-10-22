# Stock Market Tracking Application

A full-stack web application for tracking stock market data with user authentication, watchlist management, and real-time stock information.

## 🚀 Features

### Backend (FastAPI)
- **RESTful API** with FastAPI framework
- **JWT Authentication** with secure token management
- **MongoDB Integration** using MongoEngine ODM
- **CORS Configuration** for cross-origin requests
- **User Management** with registration, login, and profile management
- **Stock Management** with CRUD operations
- **Watchlist Functionality** for tracking favorite stocks
- **Predefined Companies** with popular stock symbols
- **Environment-based Configuration** with Pydantic settings

### Frontend (Next.js)
- **Modern React 19** with TypeScript
- **Next.js 15** with App Router
- **Tailwind CSS** for styling
- **Responsive Design** for mobile and desktop
- **User Authentication** with context management
- **Stock Search** with autocomplete
- **Interactive Watchlist** with add/remove functionality
- **Dashboard** with user profile management
- **Real-time Updates** and error handling

## 🏗️ Architecture

```
stock-market-tracking/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/           # Core configuration and utilities
│   │   ├── models/         # MongoDB models
│   │   ├── routers/        # API route handlers
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── middleware/     # Custom middleware
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container configuration
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app router pages
│   │   ├── components/    # React components
│   │   ├── contexts/      # React contexts
│   │   ├── hooks/         # Custom React hooks
│   │   └── lib/           # Utility functions
│   └── package.json       # Node.js dependencies
└── README.md              # This file
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** 0.104.1 - Modern Python web framework
- **MongoDB** - NoSQL database
- **MongoEngine** 0.28.2 - MongoDB ODM
- **Pydantic** 2.5.0 - Data validation
- **JWT** - Authentication tokens
- **Uvicorn** - ASGI server

### Frontend
- **Next.js** 15.5.6 - React framework
- **React** 19.1.0 - UI library
- **TypeScript** 5.x - Type safety
- **Tailwind CSS** 4.x - Styling
- **ESLint** 9.x - Code linting

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- MongoDB (local or cloud)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env.local
   # Edit .env.local with your configuration
   ```

5. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   ```
   http://localhost:3000
   ```

## 🔧 Configuration

### Backend Environment Variables

Copy `env.example` to `.env.local` file in the backend directory:



### Frontend Environment Variables

Copy `env.example` to `.env.local` file in the frontend directory:


## 📚 API Documentation

Once the backend is running, you can access:

- **Interactive API Docs:** http://localhost:8000/docs
- **OpenAPI Schema:** http://localhost:8000/openapi.json


## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm run lint
npm run build
```

## 🐳 Docker Support

### Backend Docker
```bash
cd backend
docker build -t stock-market-backend .
docker run -p 8000:8000 stock-market-backend
```

### Full Stack with Docker Compose
```bash
docker-compose up --build
```

## 📱 Features Overview

### User Authentication
- Secure user registration and login
- JWT token-based authentication
- Protected routes and API endpoints
- User profile management

### Stock Management
- Browse predefined company list
- Search and filter stocks
- Add/remove stocks from watchlist
- View stock statistics and metrics

### Watchlist Features
- Personal stock watchlist
- Real-time stock data (when integrated with external APIs)
- Interactive stock cards with remove functionality
- Watchlist statistics and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/stock-market-tracking/issues) page
2. Review the API documentation at `/docs`
3. Check the console for error messages
4. Ensure all environment variables are properly configured



---

**Happy Trading! 📈**
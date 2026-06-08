# Personal Intelligence OS

Personal Intelligence OS is a comprehensive, AI-powered system designed to manage, analyze, and optimize your professional and learning journey. By leveraging advanced LLMs and a Graph Database architecture, this platform ingests your data (Resumes, GitHub, LinkedIn, LeetCode) and provides actionable insights to accelerate your career growth.

## 🌟 Key Features

- **Data Ingestion Pipeline**: Automatically parse and structure data from multiple sources (GitHub, LinkedIn, Resumes, Certifications).
- **Intelligent Analytics**: Real-time readiness scoring, skill gap analysis, and market trend tracking.
- **AI-Powered Agents**: A suite of LLM-backed specialized agents including:
  - Career Agent
  - Interview Simulator Agent
  - Job Market Agent
  - Learning & Project Agents
- **Knowledge Graph**: Stores complex relationships between skills, projects, and career trajectories using Neo4j.
- **RAG Pipeline**: Advanced Retrieval-Augmented Generation for deep contextual recommendations and personalized learning paths.
- **Modern UI**: A responsive, interactive React-based frontend dashboard for a seamless user experience.

## 🏗️ Architecture

The system is broken down into two main components:

- **Backend (Python)**: Handles data ingestion, analytics, RAG pipelines, LLM integration, graph queries, and scheduling. Built with modularity and extensibility in mind.
- **Frontend (React/Vite)**: A sleek, modern dashboard for interacting with your AI Copilot, viewing analytics, tracking market trends, and managing your learning roadmap.

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose (Recommended)
- Node.js (v18+)
- Python 3.10+
- A valid LLM API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bharathsingh9/Personal_-intelligence_os.git
   cd Personal_-intelligence_os
   ```

2. **Environment Setup:**
   Create a `.env` file in the root directory. Add your necessary API keys and database configurations:
   ```env
   # LLM Configuration
   API_KEY=your_llm_api_key_here

   # Database Configuration (Neo4j)
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=password
   ```

### Running the Application

#### Option A: Using Docker (Recommended)
You can spin up the entire stack, including the databases, backend, and frontend using Docker Compose:
```bash
docker-compose up --build
```

#### Option B: Local Development
If you prefer running the services locally without Docker:

**1. Start the Backend:**
```bash
# Create and activate a virtual environment
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Run the server
uvicorn main:app --reload
```

**2. Start the Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 🧠 Copilot & AI Capabilities

The core of the system is driven by LLM integration. Instead of a simple chatbot, Personal Intelligence OS uses a multi-agent architecture where distinct LLM agents collaborate to:
- Generate comprehensive learning roadmaps.
- Suggest projects tailored specifically to your missing skills.
- Simulate technical interviews based on your profile and current job market trends.

## 📄 License

This project is licensed under the MIT License.

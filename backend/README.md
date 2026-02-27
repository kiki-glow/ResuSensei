# ResuSensei - AI-Powered Resume Analyzer

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-brightgreen)](https://www.mongodb.com/)

**ResuSensei** is an advanced AI-powered resume analysis platform that provides comprehensive ATS (Applicant Tracking System) optimization, role-specific recommendations, and detailed scoring across multiple dimensions.

## 🌟 Features

### Core Features
- **ATS Compatibility Analysis** - Ensures your resume passes Applicant Tracking Systems
- **Role-Specific Optimization** - Tailored analysis for 10+ professional roles including:
  - Frontend/Backend/Full Stack Developer
  - Data Analyst/Data Scientist
  - DevOps Engineer
  - Product Manager
  - UI/UX Designer
  - Virtual Assistant
  - Cybersecurity Analyst
  
- **Multi-Format Support** - PDF, DOCX, and RTF files
- **Comprehensive Scoring** - 6 key metrics:
  - ATS Compatibility (25%)
  - Content Quality (25%)
  - Keyword Optimization (20%)
  - Structure (15%)
  - Achievements (10%)
  - Formatting (5%)

### Advanced Features
- **Keyword Matching** - Compare resume against role-specific essential and preferred keywords
- **Actionable Recommendations** - Prioritized, specific suggestions for improvement
- **Quick Tips** - Instant, actionable advice based on analysis
- **Missing Section Detection** - Identifies gaps in resume structure
- **Quantification Analysis** - Checks for metrics, percentages, and measurable achievements
- **Action Verb Analysis** - Evaluates use of strong, role-appropriate action verbs
- **Analysis History** - Track improvements over time

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [File Structure](#file-structure)
- [Supported Roles](#supported-roles)
- [Scoring Methodology](#scoring-methodology)
- [Examples](#examples)
- [Contributing](#contributing)

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- MongoDB 6.0 or higher
- Pandoc (for RTF support)

### Step 1: Clone the Repository

```bash
git clone https://github.com/kiki-glow/ResuSensei.git
cd ResuSensei
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Pandoc (for RTF support)

**Ubuntu/Debian:**
```bash
sudo apt-get install pandoc
```

**macOS:**
```bash
brew install pandoc
```

**Windows:**
Download from [pandoc.org](https://pandoc.org/installing.html)

### Step 5: Set Up MongoDB

Make sure MongoDB is running:
```bash
# Ubuntu
sudo systemctl start mongod

# macOS
brew services start mongodb-community

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## ⚙️ Configuration

### Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings:
```env
MONGO_URI=mongodb://localhost:27017/
DB_NAME=ResuSenseiDB
OPENAI_API_KEY=your_key_here  # Optional
```

### Directory Structure

The application will automatically create necessary directories:
- `uploads/` - Temporary storage for uploaded files
- `models/` - For ML model files (future feature)
- `logs/` - Application logs

## 🏃 Running the Application

### Development Mode

```bash
python main.py
```

or

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker (Optional)

```bash
docker build -t resusensei .
docker run -p 8000:8000 -e MONGO_URI=mongodb://host.docker.internal:27017/ resusensei
```

The API will be available at: `http://localhost:8000`

Interactive API Documentation: `http://localhost:8000/docs`

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "running",
  "version": "2.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 2. Get Available Roles
```http
GET /api/roles
```

**Response:**
```json
{
  "available_roles": [
    {
      "key": "frontend_developer",
      "name": "Frontend Developer",
      "essential_keywords_count": 18,
      "preferred_keywords_count": 15
    },
    ...
  ],
  "total_roles": 10
}
```

#### 3. Analyze Resume
```http
POST /api/analyze
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): Resume file (PDF, DOCX, or RTF)
- `target_role` (optional): Target role key for role-specific analysis

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf" \
  -F "target_role=frontend_developer"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/api/analyze"
files = {"file": open("resume.pdf", "rb")}
data = {"target_role": "frontend_developer"}

response = requests.post(url, files=files, data=data)
print(response.json())
```

**Response:**
```json
{
  "resume_id": "507f1f77bcf86cd799439011",
  "filename": "john_doe_resume.pdf",
  "target_role": "frontend_developer",
  "overall_score": 78,
  "grade": "C",
  "score_breakdown": {
    "ats_compatibility": 85,
    "content_quality": 75,
    "keyword_optimization": 72,
    "structure": 80,
    "achievements": 65,
    "formatting": 90
  },
  "recommendations": [
    {
      "priority": "critical",
      "category": "Keyword Optimization",
      "title": "Add Essential Frontend Developer Keywords",
      "description": "Your resume is missing critical keywords...",
      "impact": "High - Essential for passing ATS keyword filters",
      "keywords": ["React", "TypeScript", "Redux"]
    }
  ],
  "quick_tips": [
    "🎯 Use standard section headers like 'Work Experience'...",
    "🔑 Review the job description and include relevant keywords..."
  ],
  "role_analysis": {
    "role_name": "Frontend Developer",
    "essential_keywords": {
      "present": ["JavaScript", "HTML", "CSS"],
      "missing": ["React", "TypeScript"],
      "match_percentage": 67.5
    },
    "overall_match": 68.3
  },
  "analyzed_at": "2024-01-15T10:30:00"
}
```

#### 4. Get Analysis by ID
```http
GET /api/analysis/{resume_id}
```

**Response:** Same as analyze endpoint response

#### 5. Get Analysis History
```http
GET /api/history?limit=10&skip=0
```

**Response:**
```json
{
  "analyses": [...],
  "count": 10,
  "skip": 0,
  "limit": 10
}
```

#### 6. Get Statistics
```http
GET /api/stats
```

**Response:**
```json
{
  "total_analyses": 150,
  "average_scores": {
    "avg_overall_score": 74.5,
    "avg_ats_score": 78.2,
    "avg_content_score": 71.8
  },
  "role_distribution": [
    {"_id": "frontend_developer", "count": 45},
    {"_id": "data_analyst", "count": 32}
  ]
}
```

## 📁 File Structure

```
resume_analyzer/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── README.md                        # This file
│
├── config/
│   └── settings.py                  # Application configuration & role keywords
│
├── app/
│   ├── services/
│   │   ├── text_extraction.py       # File text extraction service
│   │   ├── scoring_service.py       # Resume scoring logic
│   │   └── recommendation_engine.py # Recommendation generation
│   │
│   └── utils/
│       └── text_analysis.py         # Text analysis utilities
│
├── uploads/                         # Temporary file storage
├── models/                          # ML models (future)
└── logs/                           # Application logs
```

## 🎯 Supported Roles

Currently supports 10 professional roles with optimized keyword databases:

1. **Frontend Developer** - React, Vue, Angular, TypeScript, etc.
2. **Backend Developer** - Python, Java, Node.js, APIs, databases
3. **Full Stack Developer** - Combined frontend/backend skills
4. **Data Analyst** - SQL, Excel, Tableau, Python, statistics
5. **Data Scientist** - ML, Python, TensorFlow, PyTorch
6. **DevOps Engineer** - Docker, Kubernetes, CI/CD, AWS
7. **Product Manager** - Product strategy, roadmaps, Agile
8. **UI/UX Designer** - Figma, Adobe XD, user research
9. **Virtual Assistant** - Admin support, scheduling, CRM
10. **Cybersecurity Analyst** - Security, SIEM, penetration testing

Each role has:
- 15-20 essential keywords
- 15+ preferred keywords
- Role-specific action verbs
- Relevant certifications

## 📊 Scoring Methodology

### Overall Score Calculation

The overall score (0-100) is calculated using weighted components:

```
Overall Score = (ATS × 0.25) + (Content × 0.25) + (Keywords × 0.20) + 
                (Structure × 0.15) + (Achievements × 0.10) + (Formatting × 0.05)
```

### Individual Scores

**1. ATS Compatibility (25%)**
- Contact information presence
- Standard section headers
- File format compatibility
- Special character usage
- Bullet point formatting

**2. Content Quality (25%)**
- Word count (optimal: 400-800 words)
- Action verb usage
- Readability score
- Professional language

**3. Keyword Optimization (20%)**
- Essential keywords match (70% weight)
- Preferred keywords match (30% weight)
- Industry-specific terminology

**4. Structure (15%)**
- Required sections (Experience, Education)
- Recommended sections (Skills, Summary)
- Logical organization

**5. Achievements (10%)**
- Quantifiable metrics
- Percentages and numbers
- Impact statements
- Years of experience

**6. Formatting (5%)**
- Consistent spacing
- Proper capitalization
- Bullet point usage
- Professional appearance

### Grading Scale

- **A (90-100)**: Excellent - ATS-optimized, strong content
- **B (80-89)**: Good - Minor improvements needed
- **C (70-79)**: Fair - Several areas need work
- **D (60-69)**: Poor - Significant improvements required
- **F (0-59)**: Needs major revision

## 💡 Examples

### Example 1: Analyze Frontend Developer Resume

```python
import requests

# Upload and analyze
with open('frontend_resume.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files={'file': f},
        data={'target_role': 'frontend_developer'}
    )

result = response.json()
print(f"Overall Score: {result['overall_score']}/100")
print(f"Grade: {result['grade']}")
print(f"\nTop Recommendations:")
for rec in result['recommendations'][:3]:
    print(f"- [{rec['priority']}] {rec['title']}")
```

### Example 2: Get Role-Specific Keywords

```python
import requests

response = requests.get('http://localhost:8000/api/roles')
roles = response.json()['available_roles']

# Find data analyst role
data_analyst = next(r for r in roles if r['key'] == 'data_analyst')
print(f"Role: {data_analyst['name']}")
print(f"Essential Keywords: {data_analyst['essential_keywords_count']}")
```

### Example 3: Track Improvement Over Time

```python
import requests

# Get history
response = requests.get('http://localhost:8000/api/history?limit=5')
history = response.json()['analyses']

# Compare scores
for analysis in history:
    print(f"{analysis['filename']}: {analysis['overall_score']}/100")
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Machine Learning model for score prediction
- [ ] Cover letter analysis
- [ ] LinkedIn profile optimization
- [ ] Resume template recommendations
- [ ] Multi-language support
- [ ] PDF generation with suggestions
- [ ] Integration with job boards
- [ ] Browser extension
- [ ] Mobile app

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues, questions, or contributions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/resusensei/issues)
- Email: support@resusensei.com
- Documentation: [docs.resusensei.com](https://docs.resusensei.com)

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- MongoDB for the database
- pdfplumber for PDF text extraction
- python-docx for DOCX processing

---

**Made with ❤️ by the ResuSensei Team**
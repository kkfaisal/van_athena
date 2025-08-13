# What is van_athena? 

## Overview

**van_athena** is an AI-powered natural language to SQL query system specifically designed for Amazon Athena. It enables users to ask questions in plain English and automatically generates, validates, and executes SQL queries against Amazon Athena databases.

## Core Purpose

This application democratizes data access by allowing non-technical users to query data lakes and databases using natural language instead of writing complex SQL queries. It bridges the gap between business questions and data insights.

## Key Features

### 🤖 Natural Language to SQL
- Ask questions like "Show me sales data for last month"
- AI generates Athena-compatible SQL automatically
- Supports complex queries with joins, aggregations, and filters

### 🔍 Query Execution & Validation
- Executes queries directly on Amazon Athena
- Validates SQL syntax before execution
- Returns results as interactive tables and charts

### 📊 Data Visualization
- Automatic chart generation from query results
- Interactive tables with sorting and filtering
- Export capabilities for further analysis

### 🧠 AI Training System
- Learn from database schema and documentation
- Continuous improvement through user feedback
- Vector-based semantic search for better accuracy

### 🔐 Authentication & Security
- Simple email/password authentication
- Session management for secure access
- User-specific configurations

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                           Web Interface                         │
│                         (Flask + Auth)                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                        Vanna.AI Framework                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   DeepSeek V3   │  │  Vector Store   │  │  Query Engine   │ │
│  │      LLM        │  │   (pgvector)    │  │   (Custom)      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                       Amazon Athena                            │
│                    (Query Execution)                           │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Core Components
- **Python 3.12** - Runtime environment
- **Flask** - Web framework for UI
- **Vanna.AI** - Natural language to SQL framework
- **DeepSeek V3** - Large Language Model for SQL generation
- **PostgreSQL + pgvector** - Vector database for embeddings
- **boto3** - AWS SDK for Athena integration

### Dependencies
- `torch` - Deep learning framework
- `sentence-transformers` - Text embeddings
- `pandas` - Data manipulation
- `psycopg2-binary` - PostgreSQL driver

## File Structure & Responsibilities

### Core Application Files

#### `app.py` - Main Application
```python
# Main Flask web application
# - Integrates Vanna.AI with custom Athena support
# - Handles web UI and user interactions
# - Manages authentication and sessions
# - Provides endpoints for queries and visualizations
```

#### `athena_utils.py` - Athena Integration
```python
# Amazon Athena query execution utilities
# - execute_athen_query(): Runs SQL on Athena
# - athena_result_to_df(): Converts results to DataFrame
# - run_athena_query(): Main query interface
# - validate_athena_query(): SQL validation using EXPLAIN
```

#### `auth_ui.py` - Authentication
```python
# Simple authentication system
# - Login/logout functionality
# - Session management with cookies
# - Custom login forms
# - User validation
```

#### `train.py` - AI Training
```python
# Train the AI model with database knowledge
# - Load database schema from information_schema
# - Train on table/column metadata
# - Process documentation files
# - Build vector embeddings for semantic search
```

### Configuration Files

#### `docker-compose.yml` - Container Orchestration
```yaml
# Defines two services:
# 1. vanna-app: Main Flask application
# 2. postgres-vector: PostgreSQL with vector extensions
```

#### `Dockerfile` - Application Container
```dockerfile
# Python 3.12 slim image
# Installs dependencies and sets up Flask app
# Exposes port 5000 for web interface
```

#### `requirements.txt` - Python Dependencies
```
# All required Python packages
# Including Vanna.AI, Flask, boto3, torch, etc.
```

#### `init.sql` - Database Setup
```sql
# Creates vector database user and database
# Enables pgvector extension
# Sets up permissions for vector operations
```

## Workflow

### 1. Setup Phase
```bash
# Start containers
docker-compose up --build

# Train the AI (inside container)
docker exec -it vannaai-vanna-app-1 bash
python train.py

# Restart app to load training data
docker-compose restart vanna-app
```

### 2. Query Phase
1. User logs into web interface at `localhost:5000`
2. User types natural language question
3. AI generates Athena-compatible SQL
4. System validates SQL syntax
5. Query executes on Amazon Athena
6. Results displayed as tables/charts

### 3. Learning Phase
- Users can add question/SQL pairs
- System learns from corrections
- Vector embeddings improve accuracy
- Documentation updates enhance understanding

## Configuration Requirements

### AWS Configuration
```python
# In athena_utils.py
boto3.setup_default_session(profile_name='<your_aws_profile>')
athena_cl = boto3.client('athena', region_name='us-east-1')

# Database and S3 settings
db = 'cafu_transformed'  # Your Athena database
s3_outpt = 's3://<bucket>/query_results/'  # Output location
```

### Database Connection
```python
# Vector database connection string
vector_connection_string = "postgresql://vector_user:vector_pass@postgres-vector:5432/vector_db"
```

### Authentication
```python
# In app.py - update credentials
auth=SimplePassword(users=[{"email": "admin@example.com", "password": "*********"}])
```

## Use Cases

### Business Analysts
- "Show me total revenue by month for 2024"
- "Which products have the highest profit margins?"
- "Compare sales performance across regions"

### Data Scientists
- "Find customers with highest lifetime value"
- "Show correlation between marketing spend and conversions"
- "Identify trending product categories"

### Executives
- "What are our top KPIs for this quarter?"
- "Show me a dashboard of key business metrics"
- "Compare performance vs last year"

## Benefits

### For Organizations
- **Democratizes Data Access** - Non-technical users can query databases
- **Reduces IT Burden** - Self-service analytics reduces support tickets
- **Faster Insights** - Quick answers to business questions
- **Cost Effective** - Uses existing Athena infrastructure

### For Users
- **No SQL Knowledge Required** - Natural language interface
- **Interactive Results** - Charts and tables automatically generated
- **Learning System** - Gets better with use
- **Secure Access** - Authentication and session management

## Customization Options

### LLM Provider
Currently uses DeepSeek V3, but can be configured for:
- OpenAI GPT models
- Anthropic Claude
- Local LLMs
- Other OpenAI-compatible APIs

### Vector Store
Currently uses PostgreSQL + pgvector, alternatives:
- Chroma
- Pinecone
- Weaviate
- Qdrant

### Authentication
Simple password auth can be replaced with:
- OAuth (Google, Microsoft, etc.)
- SAML/SSO
- Active Directory
- Custom authentication systems

## Getting Started

1. **Clone the repository**
2. **Configure AWS credentials** and update `athena_utils.py`
3. **Set database details** in `init.sql`
4. **Update connection strings** in `train.py` and `app.py`
5. **Add documentation** in `train_doc_1.txt`
6. **Build and run** with `docker-compose up --build`
7. **Train the model** with `python train.py`
8. **Access UI** at `localhost:5000`

This system transforms how organizations interact with their data, making complex database queries as simple as asking a question in plain English.
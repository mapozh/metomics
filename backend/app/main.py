import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import metadata_routes, chatbot_routes
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Configure logging

# Load environment variables from .env file
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")
print(f"Database URL: {SQLALCHEMY_DATABASE_URL}") 

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI app
app = FastAPI(
    title="RNA-seq Metadata Management API",
    description="Manages RDF data for RNA-seq experiments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow requests from your frontend's origin
origins = [
    os.getenv("FRONTEND_URL", "http://localhost:5000"),
]

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Update this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password context (keep only one implementation)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Include routes
app.include_router(metadata_routes.router)
app.include_router(chatbot_routes.router)

# Root Endpoint
@app.get("/")
def root():
    """
    Root endpoint for API.
    """
    return {"message": "Welcome to RNA-seq Metadata API"}

# SQLAlchemy models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    initial = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    gender = Column(String)
    position = Column(String)
    lab_name = Column(String)
    location = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tokens")

    User.tokens = relationship("Token", back_populates="user")

# Create Pydantic models to validate input data
class RegisterUser(BaseModel):
    initial: str = Field(..., min_length=1, max_length=5)
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    position: str = Field(..., min_length=2)
    lab_name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=8, regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$")
    confirm_password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Your API registration endpoint
@app.post("/register", status_code=201)
async def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for email: {user.email}")
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.warning(f"Duplicate registration attempt: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        if user.password != user.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        hashed_password = pwd_context.hash(user.password)
        
        db_user = User(
            initial=user.initial,
            first_name=user.first_name,
            last_name=user.last_name,
            position=user.position,
            lab_name=user.lab_name,
            email=user.email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        db.add(db_user)
        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error occurred")
            
        logger.info(f"User registered successfully: {user.email}")
        return {"message": "User registered successfully!"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to hash the password using bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to generate a random token
def generate_random_token(length: int = 15) -> str:
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        logger.info(f"Validating token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials.")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired.")
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError as e:
        logger.error(f"Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
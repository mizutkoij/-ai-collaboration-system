# REST API Example

## Request
"Build a RESTful API for an e-commerce platform with product catalog, user management, and order processing"

## AI Conversation Flow

### ChatGPT o3 (Design Phase)
1. **API Architecture**: Microservices with API Gateway
2. **Database Design**: Product, User, Order, Payment tables
3. **Security**: OAuth2 + JWT tokens
4. **Documentation**: OpenAPI/Swagger specs

### Claude Code (Implementation)
1. **FastAPI Setup**: Project structure and configuration
2. **Models**: SQLAlchemy ORM models
3. **Endpoints**: CRUD operations for all resources
4. **Security**: Authentication middleware
5. **Testing**: Comprehensive test suite
6. **Documentation**: Auto-generated API docs

## Generated Files
```
ecommerce_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── product.py       # Product model
│   │   └── order.py         # Order model
│   ├── api/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── products.py      # Product endpoints
│   │   ├── users.py         # User endpoints
│   │   └── orders.py        # Order endpoints
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── security.py      # Security utilities
│   │   └── database.py      # Database connection
│   └── tests/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Features Generated
- ✅ User registration and authentication
- ✅ Product catalog with search and filtering
- ✅ Shopping cart functionality
- ✅ Order processing workflow
- ✅ Payment integration structure
- ✅ Admin panel endpoints
- ✅ Rate limiting and security
- ✅ Automated testing (90%+ coverage)
- ✅ API documentation
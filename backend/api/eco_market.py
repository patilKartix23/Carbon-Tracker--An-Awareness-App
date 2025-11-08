"""
EcoMarket API Routes - FastAPI Implementation
Sustainable shopping with real eco-friendly products
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional, List
import json
from pathlib import Path
from datetime import datetime
import uuid

router = APIRouter()

# Load products from JSON file
def load_products_from_json():
    """Load eco-friendly products from JSON file"""
    try:
        json_path = Path(__file__).parent.parent / 'data' / 'eco_products.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            products = data.get('products', [])
            print(f"[EcoMarket] Loaded {len(products)} products from database")
            return products
    except Exception as e:
        print(f"Error loading products from JSON: {e}")
        return []

# Initialize products
PRODUCTS = load_products_from_json()
CARTS = {}

@router.get("/products")
async def get_products(
    q: Optional[str] = None,
    category: Optional[str] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    ecoFeatures: Optional[str] = None,
    minRating: Optional[float] = None,
    inStock: Optional[bool] = None,
    sortBy: Optional[str] = "relevance",
    page: int = 1,
    limit: int = 12
):
    """Get products with search and filters"""
    try:
        filtered_products = PRODUCTS.copy()
        
        # Filter by category
        if category:
            filtered_products = [p for p in filtered_products if p.get("category") == category]
        
        # Filter by price range
        if minPrice is not None or maxPrice is not None:
            min_p = minPrice or 0
            max_p = maxPrice or float('inf')
            filtered_products = [p for p in filtered_products if min_p <= p.get("price", 0) <= max_p]
        
        # Filter by eco features
        if ecoFeatures:
            features = ecoFeatures.split(',')
            filtered_products = [
                p for p in filtered_products 
                if any(ef.get("type") in features for ef in p.get("ecoFeatures", []))
            ]
        
        # Filter by rating
        if minRating:
            filtered_products = [p for p in filtered_products if p.get("rating", 0) >= minRating]
        
        # Filter by stock
        if inStock:
            filtered_products = [p for p in filtered_products if p.get("inStock", False)]
        
        # Search by query
        if q:
            query_lower = q.lower()
            filtered_products = [
                p for p in filtered_products
                if query_lower in p.get("name", "").lower() or 
                   query_lower in p.get("description", "").lower() or
                   query_lower in p.get("brand", "").lower() or
                   any(query_lower in tag for tag in p.get("tags", []))
            ]
        
        # Sort products
        if sortBy == "price-low":
            filtered_products.sort(key=lambda x: x.get("price", 0))
        elif sortBy == "price-high":
            filtered_products.sort(key=lambda x: x.get("price", 0), reverse=True)
        elif sortBy == "rating":
            filtered_products.sort(key=lambda x: x.get("rating", 0), reverse=True)
        elif sortBy == "eco-score":
            filtered_products.sort(key=lambda x: x.get("ecoScore", 0), reverse=True)
        
        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_products = filtered_products[start_idx:end_idx]
        
        return {
            "success": True,
            "data": {
                "products": paginated_products,
                "totalCount": len(filtered_products),
                "page": page,
                "limit": limit,
                "hasNext": end_idx < len(filtered_products),
                "hasPrev": page > 1
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get single product details"""
    product = next((p for p in PRODUCTS if p.get("id") == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "success": True,
        "data": product
    }

@router.get("/categories")
async def get_categories():
    """Get product categories with counts"""
    categories = {}
    for product in PRODUCTS:
        category = product.get('category')
        if category and category not in categories:
            categories[category] = {
                'name': category,
                'count': 0,
                'subcategories': set()
            }
        if category:
            categories[category]['count'] += 1
            if product.get('subCategory'):
                categories[category]['subcategories'].add(product['subCategory'])
    
    # Convert sets to lists
    for category in categories.values():
        category['subcategories'] = list(category['subcategories'])
    
    return {
        "success": True,
        "data": list(categories.values())
    }

@router.get("/recommendations")
async def get_recommendations(
    type: str = "eco-friendly",
    limit: int = 6
):
    """Get personalized product recommendations"""
    products = PRODUCTS.copy()
    
    if type == "eco-friendly":
        products.sort(key=lambda x: x.get('ecoScore', 0), reverse=True)
    elif type == "popular":
        products = [p for p in products if p.get('isBestSeller')]
    elif type == "new":
        products = [p for p in products if p.get('isNewArrival')]
    
    return {
        "success": True,
        "data": products[:limit]
    }

@router.get("/cart")
async def get_cart(x_user_id: str = Header(default="anonymous")):
    """Get user's cart"""
    cart = CARTS.get(x_user_id, {
        "id": str(uuid.uuid4()),
        "items": [],
        "totalItems": 0,
        "subtotal": 0,
        "ecoImpactSummary": {
            "totalCarbonSaved": 0,
            "plasticAvoided": 0,
            "treesPlanted": 0,
            "waterSaved": 0,
            "wasteReduced": 0
        }
    })
    
    return {
        "success": True,
        "data": cart
    }

@router.post("/cart/add")
async def add_to_cart(
    request_data: dict,
    x_user_id: str = Header(default="anonymous")
):
    """Add item to cart"""
    product_id = request_data.get('productId')
    quantity = request_data.get('quantity', 1)
    
    if not product_id:
        raise HTTPException(status_code=400, detail="Product ID is required")
    
    product = next((p for p in PRODUCTS if p.get("id") == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if x_user_id not in CARTS:
        CARTS[x_user_id] = {
            "id": str(uuid.uuid4()),
            "items": [],
            "totalItems": 0,
            "subtotal": 0,
            "updatedAt": datetime.now().isoformat()
        }
    
    cart = CARTS[x_user_id]
    
    # Check if item already exists
    existing_item = next((item for item in cart["items"] if item["product"]["id"] == product_id), None)
    
    if existing_item:
        existing_item["quantity"] += quantity
    else:
        cart["items"].append({
            "id": str(uuid.uuid4()),
            "product": product,
            "quantity": quantity,
            "addedAt": datetime.now().isoformat()
        })
    
    # Update totals
    cart["totalItems"] = sum(item["quantity"] for item in cart["items"])
    cart["subtotal"] = sum(item["product"]["price"] * item["quantity"] for item in cart["items"])
    
    # Calculate eco impact
    total_carbon_saved = sum(
        (5.0 - item["product"].get("carbonFootprint", 0)) * item["quantity"] 
        for item in cart["items"]
    )
    
    cart["ecoImpactSummary"] = {
        "totalCarbonSaved": max(0, total_carbon_saved),
        "plasticAvoided": sum(item["quantity"] * 50 for item in cart["items"]),
        "treesPlanted": int(cart["totalItems"] / 10),
        "waterSaved": sum(item["quantity"] * 100 for item in cart["items"]),
        "wasteReduced": sum(item["quantity"] * 0.5 for item in cart["items"])
    }
    
    cart["updatedAt"] = datetime.now().isoformat()
    
    return {
        "success": True,
        "data": cart,
        "message": "Product added to cart successfully"
    }

@router.get("/educational/content")
async def get_educational_content():
    """Get educational content for homepage"""
    # Sample data - can be expanded
    return {
        "success": True,
        "data": {
            "facts": [],
            "tips": [],
            "challenges": [],
            "featured": {
                "fact": None,
                "tip": None,
                "challenge": None
            }
        }
    }

"""
Eco-Shopping API Routes
Comprehensive e-commerce functionality with sustainability focus
"""
from flask import Blueprint, request, jsonify
import json
from datetime import datetime, timedelta
import uuid
import numpy as np

eco_shopping_bp = Blueprint('eco_shopping', __name__)

# Sample data for demonstration
SAMPLE_PRODUCTS = [
    {
        "id": "eco-001",
        "name": "Organic Cotton T-Shirt",
        "description": "100% GOTS certified organic cotton t-shirt made with natural dyes and fair trade practices.",
        "price": 899,
        "originalPrice": 1299,
        "discount": 31,
        "category": "clothing",
        "subCategory": "t-shirts",
        "images": [
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
            "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400"
        ],
        "rating": 4.7,
        "reviewCount": 234,
        "inStock": True,
        "stockCount": 150,
        "ecoScore": 92,
        "ecoFeatures": [
            {
                "type": "organic",
                "description": "Made from 100% GOTS certified organic cotton",
                "icon": "🌱",
                "impactDescription": "Reduces pesticide use by 90% compared to conventional cotton"
            },
            {
                "type": "fair-trade",
                "description": "Fair trade certified ensuring ethical labor practices",
                "icon": "🤝",
                "impactDescription": "Supports fair wages and working conditions for farmers"
            }
        ],
        "materials": ["100% Organic Cotton"],
        "certifications": [
            {
                "name": "GOTS Certified",
                "description": "Global Organic Textile Standard",
                "logo": "gots-logo.png",
                "verifiedBy": "Control Union"
            }
        ],
        "carbonFootprint": 2.1,
        "recyclability": 85,
        "packaging": {
            "type": "plastic-free",
            "description": "Packaged in compostable mailers made from plant starch",
            "recyclable": True,
            "compostable": True
        },
        "vendor": {
            "id": "vendor-001",
            "name": "EcoThreads India",
            "description": "Sustainable fashion brand focused on organic and ethical clothing",
            "rating": 4.8,
            "sustainabilityScore": 95
        },
        "tags": ["organic", "sustainable", "fair-trade", "cotton"],
        "isEcoChoice": True
    },
    {
        "id": "eco-002",
        "name": "Bamboo Fiber Reusable Water Bottle",
        "description": "Leak-proof bamboo fiber water bottle with natural antimicrobial properties. BPA-free and dishwasher safe.",
        "price": 649,
        "category": "kitchenware",
        "subCategory": "bottles",
        "images": [
            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
            "https://images.unsplash.com/photo-1594735797061-4042d2b3db52?w=400"
        ],
        "rating": 4.5,
        "reviewCount": 189,
        "inStock": True,
        "stockCount": 89,
        "ecoScore": 88,
        "ecoFeatures": [
            {
                "type": "renewable",
                "description": "Made from fast-growing bamboo fiber",
                "icon": "🎋",
                "impactDescription": "Bamboo grows 10x faster than trees and absorbs more CO2"
            },
            {
                "type": "plastic-free",
                "description": "Zero plastic components",
                "icon": "🚫",
                "impactDescription": "Eliminates 156 plastic bottles per year per user"
            }
        ],
        "materials": ["Bamboo Fiber", "Natural Silicone Seal"],
        "carbonFootprint": 1.2,
        "recyclability": 90,
        "vendor": {
            "id": "vendor-002",
            "name": "GreenLife Products",
            "rating": 4.6,
            "sustainabilityScore": 89
        },
        "tags": ["bamboo", "reusable", "plastic-free", "eco-friendly"],
        "isBestSeller": True
    },
    {
        "id": "eco-003",
        "name": "Solar-Powered LED Garden Lights (Set of 4)",
        "description": "Weather-resistant solar garden lights with auto on/off sensor. Charges during day, provides warm lighting for 8+ hours.",
        "price": 1299,
        "category": "home-garden",
        "subCategory": "lighting",
        "images": [
            "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
            "https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?w=400"
        ],
        "rating": 4.6,
        "reviewCount": 156,
        "inStock": True,
        "stockCount": 67,
        "ecoScore": 94,
        "ecoFeatures": [
            {
                "type": "solar-powered",
                "description": "100% solar-powered with high-efficiency panels",
                "icon": "☀️",
                "impactDescription": "Saves 12 kWh of grid electricity per year"
            },
            {
                "type": "renewable",
                "description": "Uses renewable solar energy",
                "icon": "♻️",
                "impactDescription": "Reduces carbon footprint by 8.4 kg CO2 annually"
            }
        ],
        "materials": ["Recycled Aluminum", "Tempered Glass", "High-efficiency Solar Panel"],
        "carbonFootprint": 0.8,
        "recyclability": 95,
        "vendor": {
            "id": "vendor-003",
            "name": "SolarGreen Tech",
            "rating": 4.7,
            "sustainabilityScore": 92
        },
        "tags": ["solar", "LED", "garden", "renewable-energy"],
        "isNewArrival": True
    },
    {
        "id": "eco-004",
        "name": "Biodegradable Phone Case",
        "description": "Compostable phone case made from wheat straw and plant-based materials. Full protection with eco-responsibility.",
        "price": 799,
        "category": "accessories",
        "subCategory": "phone-cases",
        "images": [
            "https://images.unsplash.com/photo-1556656793-08538906a9f8?w=400"
        ],
        "rating": 4.4,
        "reviewCount": 98,
        "inStock": True,
        "stockCount": 234,
        "ecoScore": 91,
        "ecoFeatures": [
            {
                "type": "biodegradable",
                "description": "100% compostable within 6 months",
                "icon": "🌍",
                "impactDescription": "Decomposes naturally without harmful chemicals"
            },
            {
                "type": "plastic-free",
                "description": "Made from agricultural waste",
                "icon": "🌾",
                "impactDescription": "Utilizes wheat straw that would otherwise be burned"
            }
        ],
        "materials": ["Wheat Straw", "Plant-based Polymers"],
        "carbonFootprint": 0.3,
        "recyclability": 100,
        "vendor": {
            "id": "vendor-004",
            "name": "BioCases India",
            "rating": 4.5,
            "sustainabilityScore": 88
        },
        "tags": ["biodegradable", "phone-case", "wheat-straw", "compostable"]
    },
    {
        "id": "eco-005",
        "name": "Recycled Paper Plantable Notebooks (Pack of 3)",
        "description": "Eco-friendly notebooks made from recycled paper with seeds embedded in pages. Plant pages after use to grow herbs!",
        "price": 449,
        "category": "books-media",
        "subCategory": "stationery",
        "images": [
            "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400"
        ],
        "rating": 4.8,
        "reviewCount": 312,
        "inStock": True,
        "stockCount": 178,
        "ecoScore": 96,
        "ecoFeatures": [
            {
                "type": "recycled",
                "description": "Made from 100% recycled paper",
                "icon": "📄",
                "impactDescription": "Saves 3 trees and 50% water compared to virgin paper"
            },
            {
                "type": "biodegradable",
                "description": "Pages can be planted to grow herbs",
                "icon": "🌱",
                "impactDescription": "Creates new plant life after product lifecycle"
            }
        ],
        "materials": ["100% Recycled Paper", "Organic Seeds", "Natural Binding"],
        "carbonFootprint": 0.5,
        "recyclability": 100,
        "vendor": {
            "id": "vendor-005",
            "name": "Seed Paper Co.",
            "rating": 4.9,
            "sustainabilityScore": 97
        },
        "tags": ["recycled", "plantable", "paper", "notebooks", "seeds"]
    }
]

SAMPLE_ECO_FACTS = [
    {
        "id": "fact-001",
        "title": "Plastic Takes 450 Years to Decompose",
        "content": "A single plastic bottle takes approximately 450 years to completely decompose in a landfill. By choosing reusable alternatives, you can prevent hundreds of plastic bottles from entering the waste stream.",
        "category": "pollution",
        "impact": "High",
        "actionTip": "Switch to a reusable water bottle and save 156 plastic bottles per year!",
        "sources": ["EPA", "National Geographic"],
        "difficulty": "easy"
    },
    {
        "id": "fact-002",
        "title": "Organic Cotton Uses 91% Less Water",
        "content": "Organic cotton farming uses 91% less water than conventional cotton farming. It also eliminates the use of toxic pesticides that harm soil and water systems.",
        "category": "sustainability",
        "impact": "High",
        "actionTip": "Choose organic cotton clothing to reduce your water footprint and support healthier farming practices.",
        "sources": ["Textile Exchange", "WWF"],
        "difficulty": "easy"
    },
    {
        "id": "fact-003",
        "title": "Solar Energy Can Power Your Home for 25+ Years",
        "content": "Solar panels have a lifespan of 25-30 years and can reduce household electricity bills by 70-90%. They pay for themselves within 6-8 years through energy savings.",
        "category": "energy",
        "impact": "Very High",
        "actionTip": "Start small with solar-powered gadgets and garden lights before considering rooftop solar.",
        "sources": ["IRENA", "Solar Power World"],
        "difficulty": "medium"
    }
]

SAMPLE_ECO_TIPS = [
    {
        "id": "tip-001",
        "title": "DIY Natural All-Purpose Cleaner",
        "description": "Make an effective, non-toxic cleaner using ingredients you already have at home.",
        "category": "cleaning",
        "difficulty": "easy",
        "estimatedTime": "5 minutes",
        "carbonImpact": 2.3,
        "cost": "free",
        "steps": [
            "Mix 1 cup white vinegar with 1 cup water",
            "Add 10-15 drops of essential oil (optional)",
            "Pour into a spray bottle",
            "Shake well before each use",
            "Clean surfaces as needed"
        ],
        "benefits": [
            "Eliminates toxic chemicals from your home",
            "Saves money on cleaning products",
            "Reduces plastic packaging waste",
            "Safe for children and pets"
        ],
        "relatedProducts": ["eco-002"],
        "likes": 1247,
        "implementedCount": 892,
        "tags": ["DIY", "cleaning", "non-toxic", "budget-friendly"]
    },
    {
        "id": "tip-002",
        "title": "Create a Zero-Waste Kitchen",
        "description": "Transform your kitchen into a zero-waste zone with simple swaps and habits.",
        "category": "kitchen",
        "difficulty": "medium",
        "estimatedTime": "1 week to implement",
        "carbonImpact": 15.7,
        "cost": "low",
        "steps": [
            "Replace paper towels with washable cloth rags",
            "Use glass containers instead of plastic bags",
            "Compost food scraps",
            "Buy in bulk to reduce packaging",
            "Choose reusable water bottles and coffee cups"
        ],
        "benefits": [
            "Reduces household waste by 60%",
            "Saves money on disposable items",
            "Healthier food storage options",
            "Supports sustainable shopping habits"
        ],
        "relatedProducts": ["eco-002", "eco-005"],
        "likes": 2156,
        "implementedCount": 1423,
        "tags": ["zero-waste", "kitchen", "sustainable-living"]
    }
]

SAMPLE_CHALLENGES = [
    {
        "id": "challenge-001",
        "title": "30-Day Plastic-Free Challenge",
        "description": "Eliminate single-use plastics from your daily routine for 30 days and discover sustainable alternatives.",
        "type": "monthly",
        "category": "waste-reduction",
        "duration": 30,
        "difficulty": "medium",
        "points": 500,
        "participants": 2847,
        "completionRate": 73,
        "carbonImpact": 12.5,
        "isActive": True,
        "featured": True,
        "tasks": [
            {
                "id": "task-001",
                "title": "Replace plastic water bottles",
                "description": "Switch to a reusable water bottle for the entire challenge",
                "type": "purchase",
                "points": 50,
                "required": True,
                "verificationMethod": "purchase"
            },
            {
                "id": "task-002",
                "title": "Use reusable shopping bags",
                "description": "Bring your own bags for all shopping trips",
                "type": "action",
                "points": 30,
                "required": True,
                "verificationMethod": "self-report"
            },
            {
                "id": "task-003",
                "title": "Document your journey",
                "description": "Share photos of your plastic-free swaps",
                "type": "share",
                "points": 25,
                "required": False,
                "verificationMethod": "photo"
            }
        ],
        "rewards": [
            {
                "type": "points",
                "value": 500,
                "description": "Eco Champion Points",
                "conditions": "Complete all required tasks"
            },
            {
                "type": "badge",
                "value": "Plastic-Free Warrior",
                "description": "Special badge for challenge completion",
                "conditions": "Complete challenge with 80%+ task completion"
            },
            {
                "type": "discount",
                "value": "15%",
                "description": "Discount on next eco-friendly purchase",
                "conditions": "Valid for 30 days after challenge completion"
            }
        ]
    }
]

class EcoShoppingService:
    def __init__(self):
        self.products = SAMPLE_PRODUCTS.copy()
        self.eco_facts = SAMPLE_ECO_FACTS.copy()
        self.eco_tips = SAMPLE_ECO_TIPS.copy()
        self.challenges = SAMPLE_CHALLENGES.copy()
        self.carts = {}
        self.orders = {}
        self.wishlists = {}

    def search_products(self, query="", category=None, filters=None, sort_by="relevance", page=1, limit=12):
        """Search and filter products"""
        filtered_products = self.products.copy()
        
        # Filter by category
        if category:
            filtered_products = [p for p in filtered_products if p["category"] == category]
        
        # Apply filters
        if filters:
            if filters.get("priceRange"):
                min_price = filters["priceRange"].get("min", 0)
                max_price = filters["priceRange"].get("max", float('inf'))
                filtered_products = [p for p in filtered_products if min_price <= p["price"] <= max_price]
            
            if filters.get("ecoFeatures"):
                eco_features = filters["ecoFeatures"]
                filtered_products = [
                    p for p in filtered_products 
                    if any(ef["type"] in eco_features for ef in p["ecoFeatures"])
                ]
            
            if filters.get("rating"):
                min_rating = filters["rating"]
                filtered_products = [p for p in filtered_products if p["rating"] >= min_rating]
            
            if filters.get("inStock"):
                filtered_products = [p for p in filtered_products if p["inStock"]]
        
        # Search by query
        if query:
            query_lower = query.lower()
            filtered_products = [
                p for p in filtered_products
                if query_lower in p["name"].lower() or 
                   query_lower in p["description"].lower() or
                   any(query_lower in tag for tag in p["tags"])
            ]
        
        # Sort products
        if sort_by == "price-low":
            filtered_products.sort(key=lambda x: x["price"])
        elif sort_by == "price-high":
            filtered_products.sort(key=lambda x: x["price"], reverse=True)
        elif sort_by == "rating":
            filtered_products.sort(key=lambda x: x["rating"], reverse=True)
        elif sort_by == "eco-score":
            filtered_products.sort(key=lambda x: x["ecoScore"], reverse=True)
        
        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_products = filtered_products[start_idx:end_idx]
        
        return {
            "products": paginated_products,
            "totalCount": len(filtered_products),
            "page": page,
            "limit": limit,
            "hasNext": end_idx < len(filtered_products),
            "hasPrev": page > 1
        }
    
    def get_product_by_id(self, product_id):
        """Get product details by ID"""
        return next((p for p in self.products if p["id"] == product_id), None)
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        """Add product to cart"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        
        if user_id not in self.carts:
            self.carts[user_id] = {
                "id": str(uuid.uuid4()),
                "items": [],
                "totalItems": 0,
                "subtotal": 0,
                "updatedAt": datetime.now().isoformat()
            }
        
        cart = self.carts[user_id]
        
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
        
        self._update_cart_totals(cart)
        return cart
    
    def _update_cart_totals(self, cart):
        """Update cart totals and eco impact"""
        cart["totalItems"] = sum(item["quantity"] for item in cart["items"])
        cart["subtotal"] = sum(item["product"]["price"] * item["quantity"] for item in cart["items"])
        
        # Calculate eco impact
        total_carbon_saved = sum(
            (5.0 - item["product"]["carbonFootprint"]) * item["quantity"] 
            for item in cart["items"]
        )
        
        cart["ecoImpactSummary"] = {
            "totalCarbonSaved": max(0, total_carbon_saved),
            "plasticAvoided": sum(item["quantity"] * 50 for item in cart["items"]),  # Estimated grams
            "treesPlanted": int(cart["totalItems"] / 10),  # 1 tree per 10 items
            "waterSaved": sum(item["quantity"] * 100 for item in cart["items"]),  # Estimated liters
            "wasteReduced": sum(item["quantity"] * 0.5 for item in cart["items"])  # Estimated kg
        }
        
        cart["updatedAt"] = datetime.now().isoformat()

eco_service = EcoShoppingService()

@eco_shopping_bp.route('/products', methods=['GET'])
def get_products():
    """Get products with search and filters"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 12))
        sort_by = request.args.get('sortBy', 'relevance')
        
        # Parse filters
        filters = {}
        if request.args.get('minPrice') or request.args.get('maxPrice'):
            filters['priceRange'] = {
                'min': float(request.args.get('minPrice', 0)),
                'max': float(request.args.get('maxPrice', 999999))
            }
        
        if request.args.get('ecoFeatures'):
            filters['ecoFeatures'] = request.args.get('ecoFeatures').split(',')
        
        if request.args.get('minRating'):
            filters['rating'] = float(request.args.get('minRating'))
        
        if request.args.get('inStock'):
            filters['inStock'] = request.args.get('inStock').lower() == 'true'
        
        result = eco_service.search_products(
            query=query,
            category=category,
            filters=filters,
            sort_by=sort_by,
            page=page,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product details"""
    try:
        product = eco_service.get_product_by_id(product_id)
        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': product
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get product categories with counts"""
    try:
        categories = {}
        for product in eco_service.products:
            category = product['category']
            if category not in categories:
                categories[category] = {
                    'name': category,
                    'count': 0,
                    'subcategories': set()
                }
            categories[category]['count'] += 1
            if product.get('subCategory'):
                categories[category]['subcategories'].add(product['subCategory'])
        
        # Convert sets to lists
        for category in categories.values():
            category['subcategories'] = list(category['subcategories'])
        
        return jsonify({
            'success': True,
            'data': list(categories.values())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/cart', methods=['GET'])
def get_cart():
    """Get user's cart"""
    try:
        user_id = request.headers.get('X-User-ID', 'anonymous')
        cart = eco_service.carts.get(user_id, {
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
        
        return jsonify({
            'success': True,
            'data': cart
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    try:
        user_id = request.headers.get('X-User-ID', 'anonymous')
        data = request.get_json()
        
        product_id = data.get('productId')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({
                'success': False,
                'error': 'Product ID is required'
            }), 400
        
        cart = eco_service.add_to_cart(user_id, product_id, quantity)
        if not cart:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': cart,
            'message': 'Product added to cart successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/educational/facts', methods=['GET'])
def get_eco_facts():
    """Get daily eco facts"""
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 10))
        
        facts = eco_service.eco_facts.copy()
        if category:
            facts = [f for f in facts if f['category'] == category]
        
        # Add daily fact
        today = datetime.now().day
        daily_fact_index = today % len(facts)
        daily_fact = facts[daily_fact_index] if facts else None
        
        return jsonify({
            'success': True,
            'data': {
                'facts': facts[:limit],
                'dailyFact': daily_fact,
                'totalCount': len(facts)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/educational/tips', methods=['GET'])
def get_eco_tips():
    """Get eco tips"""
    try:
        category = request.args.get('category')
        difficulty = request.args.get('difficulty')
        limit = int(request.args.get('limit', 10))
        
        tips = eco_service.eco_tips.copy()
        if category:
            tips = [t for t in tips if t['category'] == category]
        if difficulty:
            tips = [t for t in tips if t['difficulty'] == difficulty]
        
        # Sort by popularity (likes + implemented count)
        tips.sort(key=lambda x: x['likes'] + x['implementedCount'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'tips': tips[:limit],
                'totalCount': len(tips)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/educational/challenges', methods=['GET'])
def get_eco_challenges():
    """Get eco challenges"""
    try:
        challenge_type = request.args.get('type')
        active_only = request.args.get('active', 'true').lower() == 'true'
        
        challenges = eco_service.challenges.copy()
        if challenge_type:
            challenges = [c for c in challenges if c['type'] == challenge_type]
        if active_only:
            challenges = [c for c in challenges if c['isActive']]
        
        # Sort by featured first, then by participants
        challenges.sort(key=lambda x: (x.get('featured', False), x['participants']), reverse=True)
        
        return jsonify({
            'success': True,
            'data': {
                'challenges': challenges,
                'totalCount': len(challenges)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/educational/content', methods=['GET'])
def get_educational_content():
    """Get all educational content for homepage"""
    try:
        # Get featured content
        today = datetime.now().day
        
        daily_fact = eco_service.eco_facts[today % len(eco_service.eco_facts)]
        featured_tip = eco_service.eco_tips[0]  # Most popular
        featured_challenge = next((c for c in eco_service.challenges if c.get('featured')), eco_service.challenges[0])
        
        return jsonify({
            'success': True,
            'data': {
                'facts': eco_service.eco_facts[:3],
                'tips': eco_service.eco_tips[:3],
                'challenges': [c for c in eco_service.challenges if c['isActive']][:3],
                'featured': {
                    'fact': daily_fact,
                    'tip': featured_tip,
                    'challenge': featured_challenge
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@eco_shopping_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get personalized product recommendations"""
    try:
        user_id = request.headers.get('X-User-ID', 'anonymous')
        recommendation_type = request.args.get('type', 'eco-friendly')
        limit = int(request.args.get('limit', 6))
        
        products = eco_service.products.copy()
        
        if recommendation_type == 'eco-friendly':
            # Recommend products with highest eco score
            products.sort(key=lambda x: x['ecoScore'], reverse=True)
        elif recommendation_type == 'popular':
            # Recommend best sellers
            products = [p for p in products if p.get('isBestSeller')]
        elif recommendation_type == 'new':
            # Recommend new arrivals
            products = [p for p in products if p.get('isNewArrival')]
        
        return jsonify({
            'success': True,
            'data': products[:limit]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

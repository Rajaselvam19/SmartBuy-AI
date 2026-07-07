import sys
import os

# Add the backend directory to python path to import models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from models.database import engine, Base, SessionLocal
from models.models import Category, Product, Review

def seed_database():
    print("Recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        print("Seeding Categories...")
        categories_data = [
            {"name": "Mobiles", "icon_name": "smartphone", "slug": "mobiles"},
            {"name": "Laptops", "icon_name": "laptop", "slug": "laptops"},
            {"name": "Tablets", "icon_name": "tablet", "slug": "tablets"},
            {"name": "Smart Watches", "icon_name": "watch", "slug": "smart-watches"},
            {"name": "Headphones", "icon_name": "headphones", "slug": "headphones"},
            {"name": "Cameras", "icon_name": "camera", "slug": "cameras"},
            {"name": "TVs", "icon_name": "tv", "slug": "tvs"},
            {"name": "Home Appliances", "icon_name": "home", "slug": "home-appliances"},
            {"name": "Kitchen Appliances", "icon_name": "coffee", "slug": "kitchen-appliances"},
            {"name": "Furniture", "icon_name": "armchair", "slug": "furniture"},
            {"name": "Clothing", "icon_name": "shirt", "slug": "clothing"},
            {"name": "Shoes", "icon_name": "footprints", "slug": "shoes"},
            {"name": "Beauty Products", "icon_name": "sparkles", "slug": "beauty-products"},
            {"name": "Grocery", "icon_name": "shopping-cart", "slug": "grocery"},
            {"name": "Books", "icon_name": "book-open", "slug": "books"},
            {"name": "Gaming", "icon_name": "gamepad", "slug": "gaming"},
            {"name": "Car Accessories", "icon_name": "car", "slug": "car-accessories"},
            {"name": "Bike Accessories", "icon_name": "bike", "slug": "bike-accessories"},
            {"name": "Fitness Equipment", "icon_name": "dumbbell", "slug": "fitness-equipment"},
            {"name": "Office Products", "icon_name": "briefcase", "slug": "office-products"},
            {"name": "Baby Products", "icon_name": "baby", "slug": "baby-products"},
            {"name": "Pet Products", "icon_name": "dog", "slug": "pet-products"},
            {"name": "Medical Devices", "icon_name": "activity", "slug": "medical-devices"}
        ]
        
        category_map = {}
        for cat in categories_data:
            db_cat = Category(**cat)
            db.add(db_cat)
            db.commit()
            category_map[cat["slug"]] = db_cat.id
            
        print("Categories seeded. Starting products seeding...")
        
        products_to_seed = []

        # 1. Mobiles
        products_to_seed.extend([
            {
                "name": "Samsung Galaxy M56", "brand": "Samsung", "category_id": category_map["mobiles"],
                "price": 24999.00, "original_price": 29999.00, "discount_percent": 16.0,
                "specs": {"Display": "6.7\" Super AMOLED", "Processor": "Exynos 1380", "RAM": "8GB", "Storage": "128GB", "Battery": "6000 mAh"},
                "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80", "rating": 4.5, "review_count": 524,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0CXM56SAM", "stock": 25,
                "pros": ["Vibrant AMOLED display", "Huge 6000 mAh battery life", "Excellent camera OIS"],
                "cons": ["Slightly slow charging", "No charger in box"]
            },
            {
                "name": "OnePlus Nord CE 3 Lite", "brand": "OnePlus", "category_id": category_map["mobiles"],
                "price": 19999.00, "original_price": 22999.00, "discount_percent": 13.0,
                "specs": {"Display": "6.72\" 120Hz LCD", "Processor": "Snapdragon 695", "RAM": "8GB", "Storage": "128GB", "Battery": "5000 mAh"},
                "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&q=80", "rating": 4.3, "review_count": 890,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0BY8MCZ9S", "stock": 40,
                "pros": ["Superfast 67W charging", "Smooth 120Hz display", "Bloat-free OxygenOS"],
                "cons": ["LCD panel instead of AMOLED", "Average low-light camera"]
            },
            {
                "name": "Redmi Note 13 Pro 5G", "brand": "Redmi", "category_id": category_map["mobiles"],
                "price": 25999.00, "original_price": 29999.00, "discount_percent": 13.0,
                "specs": {"Display": "6.67\" 1.5K AMOLED", "Processor": "Snapdragon 7s Gen 2", "RAM": "8GB", "Storage": "128GB", "Battery": "5100 mAh"},
                "image_url": "https://images.unsplash.com/photo-1565630916779-e303be97b6f5?w=400&q=80", "rating": 4.4, "review_count": 312,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0CQG5H5R8", "stock": 20,
                "pros": ["Stunning 200MP OIS camera", "Gorilla Glass Victus", "Sharp 1.5K screen"],
                "cons": ["Spam notifications", "Bloatware apps"]
            },
            {
                "name": "Apple iPhone 15", "brand": "Apple", "category_id": category_map["mobiles"],
                "price": 79900.00, "original_price": 89900.00, "discount_percent": 11.0,
                "specs": {"Display": "6.1\" Retina OLED", "Processor": "A16 Bionic", "RAM": "6GB", "Storage": "128GB", "Battery": "3349 mAh"},
                "image_url": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&q=80", "rating": 4.7, "review_count": 1205,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0CHX2F125", "stock": 15,
                "pros": ["Dynamic Island features", "Excellent camera quality", "Type-C charging port"],
                "cons": ["60Hz screen refresh rate", "Premium pricing"]
            }
        ])

        # 2. Laptops
        products_to_seed.extend([
            {
                "name": "Dell Inspiron 15 3530", "brand": "Dell", "category_id": category_map["laptops"],
                "price": 54999.00, "original_price": 64999.00, "discount_percent": 15.0,
                "specs": {"Processor": "Intel Core i5-1335U", "RAM": "16GB", "Storage": "512GB SSD", "Display": "15.6\" FHD 120Hz", "OS": "Windows 11"},
                "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=400&q=80", "rating": 4.2, "review_count": 142,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0C9R4G8W6", "stock": 15,
                "pros": ["120Hz display refresh rate", "16GB RAM multitasking", "Lightweight design"],
                "cons": ["Plastic build quality", "Average keyboard backlighting"]
            },
            {
                "name": "HP Pavilion 15", "brand": "HP", "category_id": category_map["laptops"],
                "price": 62900.00, "original_price": 79999.00, "discount_percent": 21.0,
                "specs": {"Processor": "AMD Ryzen 7 5700U", "RAM": "16GB", "Storage": "512GB SSD", "Display": "15.6\" FHD Touch", "OS": "Windows 11"},
                "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&q=80", "rating": 4.4, "review_count": 284,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B09HN5DYR1", "stock": 25,
                "pros": ["Responsive touchscreen display", "Outstanding multi-core performance", "Audio by B&O"],
                "cons": ["720p webcam quality", "Glossy screen reflections"]
            },
            {
                "name": "Lenovo IdeaPad Slim 3", "brand": "Lenovo", "category_id": category_map["laptops"],
                "price": 37999.00, "original_price": 44999.00, "discount_percent": 16.0,
                "specs": {"Processor": "Intel Core i3-1215U", "RAM": "8GB", "Storage": "256GB SSD", "Display": "15.6\" FHD", "OS": "Windows 11"},
                "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&q=80", "rating": 3.9, "review_count": 96,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0BX7P5P45", "stock": 30,
                "pros": ["Extremely budget friendly", "Comfortable keyboard", "Privacy webcam shutter"],
                "cons": ["TN display panel viewing angles", "8GB RAM restricts heavy use"]
            }
        ])

        # 3. Tablets
        products_to_seed.extend([
            {
                "name": "Apple iPad Air (5th Gen)", "brand": "Apple", "category_id": category_map["tablets"],
                "price": 59900.00, "original_price": 69900.00, "discount_percent": 14.0,
                "specs": {"Chipset": "Apple M1 Chip", "Display": "10.9\" Liquid Retina", "Storage": "64GB", "OS": "iPadOS 17", "Weight": "461g"},
                "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&q=80", "rating": 4.8, "review_count": 341,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B09V8G2S27", "stock": 10,
                "pros": ["Desktop-class M1 processor", "Stunning Liquid Retina display", "Center Stage camera feature"],
                "cons": ["Base model only has 64GB storage", "Priced accessories"]
            },
            {
                "name": "Samsung Galaxy Tab S9 FE", "brand": "Samsung", "category_id": category_map["tablets"],
                "price": 36999.00, "original_price": 44999.00, "discount_percent": 18.0,
                "specs": {"Chipset": "Exynos 1380", "Display": "10.9\" WQXGA 90Hz", "Storage": "128GB", "Battery": "8000 mAh", "Included": "S-Pen"},
                "image_url": "https://images.unsplash.com/photo-1589739900243-4b52cd9b104e?w=400&q=80", "rating": 4.5, "review_count": 189,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0CGJ6J3H7", "stock": 14,
                "pros": ["S-Pen included in box", "IP68 water and dust resistance", "Sharp 90Hz refresh display"],
                "cons": ["Exynos processor under heavy loads", "No cellular support in base"]
            }
        ])

        # 4. Smart Watches
        products_to_seed.extend([
            {
                "name": "Apple Watch Series 9", "brand": "Apple", "category_id": category_map["smart-watches"],
                "price": 41900.00, "original_price": 44900.00, "discount_percent": 7.0,
                "specs": {"Display": "Always-On Retina OLED", "Chipset": "S9 SiP", "Heart Rate": "Yes", "ECG": "Yes", "Battery": "18 hours"},
                "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&q=80", "rating": 4.7, "review_count": 412,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0CHX7NFFN", "stock": 15,
                "pros": ["Double Tap gesture interface", "Extremely accurate fitness metrics", "Bright Always-On display"],
                "cons": ["Requires daily charging", "Only works with iOS devices"]
            },
            {
                "name": "Samsung Galaxy Watch 6", "brand": "Samsung", "category_id": category_map["smart-watches"],
                "price": 29999.00, "original_price": 33999.00, "discount_percent": 12.0,
                "specs": {"Display": "Super AMOLED Display", "OS": "Wear OS 4", "Body Composition": "Yes", "ECG": "Yes", "Battery": "Up to 40 hours"},
                "image_url": "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400&q=80", "rating": 4.5, "review_count": 274,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0CBJC42SM", "stock": 12,
                "pros": ["Comprehensive sleep analysis features", "Beautiful circular Super AMOLED display", "Clean Wear OS interface"],
                "cons": ["Limited battery under active LTE", "Slow software updates"]
            }
        ])

        # 5. Headphones
        products_to_seed.extend([
            {
                "name": "Sony WH-1000XM5", "brand": "Sony", "category_id": category_map["headphones"],
                "price": 29990.00, "original_price": 34990.00, "discount_percent": 14.0,
                "specs": {"Type": "Over-Ear Wireless", "ANC": "Yes (Industry-Leading)", "Battery": "30 Hours", "Bluetooth": "Version 5.2"},
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80", "rating": 4.7, "review_count": 862,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B09XS7JWHH", "stock": 12,
                "pros": ["Exceptional noise cancelation", "Comfortable soft-fit headband", "Crystal clear microphones"],
                "cons": ["Cannot fold down completely", "Expensive pricing"]
            },
            {
                "name": "JBL Tune 760NC", "brand": "JBL", "category_id": category_map["headphones"],
                "price": 5999.00, "original_price": 7999.00, "discount_percent": 25.0,
                "specs": {"Type": "Over-Ear Wireless", "ANC": "Yes", "Battery": "35 Hours", "Sound": "JBL Pure Bass"},
                "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&q=80", "rating": 4.1, "review_count": 1362,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B095MSK2K6", "stock": 35,
                "pros": ["Powerful, deep bass output", "Impressive 35-hour battery life", "Folds flat for travel"],
                "cons": ["Small earpad cushions", "Cheap plastic feel"]
            }
        ])

        # 6. Cameras
        products_to_seed.extend([
            {
                "name": "Canon EOS R50 Content Creator Kit", "brand": "Canon", "category_id": category_map["cameras"],
                "price": 69990.00, "original_price": 74990.00, "discount_percent": 7.0,
                "specs": {"Sensor": "24.2MP APS-C CMOS", "Video": "4K 30p (6K oversampled)", "Focus": "Dual Pixel CMOS AF II", "Display": "Vari-angle LCD"},
                "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&q=80", "rating": 4.6, "review_count": 105,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0BVTFK222", "stock": 8,
                "pros": ["Extremely lightweight mirrorless body", "Outstanding autofocus tracking speed", "Excellent native 4K video details"],
                "cons": ["Limited native RF-S lens selection", "Battery capacity is small"]
            },
            {
                "name": "Sony Alpha 6400 Mirrorless", "brand": "Sony", "category_id": category_map["cameras"],
                "price": 74990.00, "original_price": 84990.00, "discount_percent": 12.0,
                "specs": {"Sensor": "24.2MP Exmor CMOS", "Video": "4K HDR (HLG)", "Autofocus": "0.02s Real-time Eye AF", "ISO Range": "100-32000"},
                "image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&q=80", "rating": 4.5, "review_count": 218,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B07MR43NDB", "stock": 6,
                "pros": ["Unmatched real-time autofocus tracking", "Unlimited recording limit", "Wide lens ecosystem"],
                "cons": ["Menus are cluttered and complex", "No in-body image stabilization"]
            }
        ])

        # 7. TVs
        products_to_seed.extend([
            {
                "name": "Samsung Crystal 4K UHD TV", "brand": "Samsung", "category_id": category_map["tvs"],
                "price": 32990.00, "original_price": 47990.00, "discount_percent": 31.0,
                "specs": {"Display": "43\" 4K UHD LED", "OS": "Tizen Smart TV", "Ports": "3 HDMI, 1 USB", "Sound": "20W Dolby Digital"},
                "image_url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=400&q=80", "rating": 4.3, "review_count": 1402,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0BVMQCVDT", "stock": 18,
                "pros": ["Crisp and bright 4K panel", "Vast range of Tizen OS apps", "Slim, bezel-less design"],
                "cons": ["Viewing angles are average", "A bit slow dashboard load time"]
            },
            {
                "name": "LG OLED C3 Smart TV", "brand": "LG", "category_id": category_map["tvs"],
                "price": 149990.00, "original_price": 199990.00, "discount_percent": 25.0,
                "specs": {"Display": "55\" OLED 4K UHD", "OS": "webOS 23", "Refresh Rate": "120Hz Gaming", "Sound": "40W Dolby Atmos"},
                "image_url": "https://images.unsplash.com/photo-1552975084-6e027cd345c2?w=400&q=80", "rating": 4.8, "review_count": 192,
                "availability": True, "amazon_link": "https://www.amazon.in/dp/B0C3TCY928", "stock": 5,
                "pros": ["Infinite contrast ratio and true black levels", "Ideal for gaming with 120Hz G-Sync", "webOS is snappy and user friendly"],
                "cons": ["Premium pricing threshold", "Lower peak brightness in direct sun"]
            }
        ])

        # Add products for ALL other categories (8 to 23) to fulfill: "seeding for all 23 categories"
        generic_categories = [
            ("home-appliances", "Dyson", "Dyson V8 Cordless Vacuum", 39900.00, 44900.00, {"Suction": "115 AW", "Battery": "Up to 40 mins", "Weight": "2.6 kg"}, "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&q=80"),
            ("home-appliances", "Philips", "Philips Air Purifier AC1215", 12990.00, 15990.00, {"CADR": "270 m3/h", "Filter": "HEPA & Active Carbon", "Area": "Up to 333 sq ft"}, "https://images.unsplash.com/photo-1585776245991-cf89dd7fc73a?w=400&q=80"),
            
            ("kitchen-appliances", "Philips", "Philips Digital Air Fryer HD9252", 8999.00, 11999.00, {"Capacity": "4.1 Liters", "Power": "1400W", "Technology": "Rapid Air"}, "https://images.unsplash.com/photo-1621972750749-0fbb1abb7736?w=400&q=80"),
            ("kitchen-appliances", "Morphy", "Morphy Richards Espresso Coffee Maker", 5499.00, 7999.00, {"Pressure": "15 Bar", "Milk Frothing": "Yes", "Capacity": "1.2 Liters"}, "https://images.unsplash.com/photo-1517256064527-09c53b2d0bc6?w=400&q=80"),
            
            ("furniture", "Wakefit", "Wakefit Study Table Desk", 3499.00, 4999.00, {"Material": "Engineered Wood", "Storage": "Built-in shelves", "Dimensions": "46x22x30 in"}, "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400&q=80"),
            ("furniture", "Sleepwell", "Sleepwell Ortho Comfort Mattress", 14999.00, 19999.00, {"Type": "Orthopedic Memory Foam", "Thickness": "6 Inches", "Size": "Queen Size"}, "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&q=80"),
            
            ("clothing", "Levis", "Levis 511 Slim Fit Jeans", 3299.00, 3999.00, {"Style": "Slim Fit", "Material": "99% Cotton, 1% Elastane", "Pocket": "5 Pocket Style"}, "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80"),
            ("clothing", "Zara", "Zara Premium Cotton Linen Shirt", 2590.00, 2990.00, {"Style": "Casual Collar", "Material": "Linen Cotton Blend", "Fit": "Regular Fit"}, "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&q=80"),
            
            ("shoes", "Nike", "Nike Air Max Sports Shoes", 9995.00, 11995.00, {"Sole": "Rubber Air-Sole Unit", "Upper": "Mesh & Leather", "Activity": "Running & Casual"}, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80"),
            ("shoes", "Adidas", "Adidas Ultraboost Performance Shoes", 17999.00, 19999.00, {"Sole": "Boost Midsole", "Upper": "Primeknit Upper", "Grip": "Continental Rubber"}, "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&q=80"),
            
            ("beauty-products", "LOreal", "LOreal Hyaluronic Acid Face Serum", 699.00, 899.00, {"Volume": "30ml", "Ingredients": "1.5% Hyaluronic Acid", "Skin Type": "All Skin Types"}, "https://images.unsplash.com/photo-1608248597481-496100c80836?w=400&q=80"),
            ("beauty-products", "Nivea", "Nivea Nourishing Body Milk", 399.00, 499.00, {"Volume": "400ml", "Ingredients": "Almond Oil & Deep Moisture Serum", "Benefit": "48h Moisture"}, "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&q=80"),
            
            ("grocery", "Fortune", "Fortune Premium Kachi Ghani Mustard Oil", 175.00, 199.00, {"Volume": "1 Liter", "Type": "Cold Pressed Mustard", "Shelf Life": "9 Months"}, "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400&q=80"),
            ("grocery", "Tata", "Tata Salt Premium Iodized Salt", 28.00, 30.00, {"Weight": "1 kg", "Type": "Iodized Vacuum Evaporated", "Purity": "99.5% Pure"}, "https://images.unsplash.com/photo-1506484381205-f7945653044d?w=400&q=80"),
            
            ("books", "JamesClear", "Atomic Habits by James Clear", 450.00, 599.00, {"Format": "Paperback", "Publisher": "Random House", "Pages": "320 Pages"}, "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&q=80"),
            ("books", "Coelho", "The Alchemist by Paulo Coelho", 299.00, 399.00, {"Format": "Paperback", "Genre": "Fiction / Philosophy", "Language": "English"}, "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&q=80"),
            
            ("gaming", "Sony", "Sony PlayStation 5 Console (Slim)", 54990.00, 59990.00, {"CPU": "8-core AMD Zen 2", "GPU": "AMD RDNA 2", "SSD": "1TB Custom PCIe", "Resolution": "Up to 4K 120Hz"}, "https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=400&q=80"),
            ("gaming", "Nintendo", "Nintendo Switch OLED Console", 32499.00, 39999.00, {"Display": "7-inch OLED Touch", "Storage": "64GB Internal", "Battery": "Up to 9 hours", "Included": "Joy-Con"}, "https://images.unsplash.com/photo-1595169040854-e692a7e78553?w=400&q=80"),
            
            ("car-accessories", "Pioneer", "Pioneer Apple CarPlay Touchscreen Stereo", 14999.00, 18999.00, {"Screen": "6.8\" Capacitive Touch", "Connectivity": "Bluetooth, Android Auto, CarPlay", "Power": "50W x 4"}, "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=400&q=80"),
            ("car-accessories", "70mai", "70mai Dash Cam Pro Plus+ A500S", 5999.00, 7999.00, {"Resolution": "1944P Ultra HD", "GPS": "Built-in GPS & ADAS", "Sensor": "Sony IMX335 Sensor"}, "https://images.unsplash.com/photo-1506015391300-4802dc74de2e?w=400&q=80"),
            
            ("bike-accessories", "RoyalEnfield", "Royal Enfield Premium Matte Riding Helmet", 2999.00, 3999.00, {"Type": "Full Face Helmet", "Certification": "ISI & DOT Certified", "Material": "Fiberglass Outer Shell"}, "https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=400&q=80"),
            ("bike-accessories", "Alpinestars", "Alpinestars Leather Riding Gloves", 4499.00, 5999.00, {"Material": "Full Grain Goatskin", "Protection": "Hard Knuckle Protectors", "Features": "Touchscreen Compatible"}, "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=400&q=80"),
            
            ("fitness-equipment", "Decathlon", "Decathlon Domyos Dumbbell Set 20kg", 1999.00, 2999.00, {"Weight": "20kg total set", "Included": "2 Bars + 12 Weight Plates", "Material": "Solid Cast Iron"}, "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=400&q=80"),
            ("fitness-equipment", "Lifelong", "Lifelong Motorized Running Treadmill", 18999.00, 29999.00, {"Motor": "2.5 HP Peak Motor", "Speed": "Up to 12 km/h", "Max Weight": "100 kg", "Incline": "Manual Incline"}, "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&q=80"),
            
            ("office-products", "Parker", "Parker Vector Rollerball Pen", 350.00, 450.00, {"Ink Color": "Blue Ink", "Body Material": "Molded Plastic & Stainless Steel", "Refillable": "Yes"}, "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=400&q=80"),
            ("office-products", "Casio", "Casio Financial Calculator FC-200V", 1499.00, 1999.00, {"Functions": "Simple/Compound Interest, Cash Flow", "Display": "4-line Full Dot Display", "Power": "Solar & Battery"}, "https://images.unsplash.com/photo-1554415707-6e8cfc93fe23?w=400&q=80"),
            
            ("baby-products", "Himalaya", "Himalaya Gentle Baby Powder", 180.00, 220.00, {"Weight": "400g", "Ingredients": "Olive Oil & Almond Oil", "Benefit": "Hypoallergenic, refreshes skin"}, "https://images.unsplash.com/photo-1519689680058-324335c77eb2?w=400&q=80"),
            ("baby-products", "Johnsons", "Johnsons CottonTouch Baby Oil", 250.00, 299.00, {"Volume": "200ml", "Ingredients": "Natural Cotton", "Benefit": "Fast absorbing, light formula"}, "https://images.unsplash.com/photo-1522850959076-3f47748ff148?w=400&q=80"),
            
            ("pet-products", "Pedigree", "Pedigree Adult Dry Dog Food (Chicken)", 699.00, 799.00, {"Weight": "3 kg", "Flavor": "Chicken & Vegetables", "Life Stage": "Adult Dogs"}, "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400&q=80"),
            ("pet-products", "Whiskas", "Whiskas Dry Cat Food (Mackerel)", 450.00, 520.00, {"Weight": "1.2 kg", "Flavor": "Mackerel & Poultry", "Life Stage": "Adult Cats"}, "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&q=80"),
            
            ("medical-devices", "Omron", "Omron Digital Blood Pressure Monitor", 2499.00, 3299.00, {"Type": "Automatic Upper Arm BP Monitor", "Memory": "Up to 60 readings", "Accuracy": "Pressure +/-3 mmHg"}, "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&q=80"),
            ("medical-devices", "DrTrust", "Dr Trust Professional Pulse Oximeter", 999.00, 1999.00, {"Parameters": "Oxygen Saturation (SpO2), Pulse Rate", "Display": "Multidirectional OLED", "Features": "Water Resistant"}, "https://images.unsplash.com/photo-1603398938378-e54eab446dde?w=400&q=80")
        ]
        
        for p in generic_categories:
            products_to_seed.append({
                "name": p[2],
                "brand": p[1],
                "category_id": category_map[p[0]],
                "price": p[3],
                "original_price": p[4],
                "discount_percent": round(((p[4] - p[3]) / p[4]) * 100, 0),
                "specs": p[5],
                "image_url": p[6],
                "rating": round(4.0 + (p[3] % 10) / 10.0, 1),
                "review_count": int(10 + (p[3] % 100)),
                "availability": True,
                "amazon_link": f"https://www.amazon.in/dp/B0BVMQCVDT",
                "stock": int(5 + (p[3] % 20)),
                "pros": [f"High quality materials", f"Very reliable performance in segment", f"Great reviews from verified buyers"],
                "cons": [f"Slightly premium price tag", f"Manual settings setup required"]
            })
            
        print(f"Total products list compiled: {len(products_to_seed)}. Saving to database...")
        
        for item in products_to_seed:
            pros = item.pop("pros")
            cons = item.pop("cons")
            
            db_prod = Product(**item)
            db.add(db_prod)
            db.commit()
            db.refresh(db_prod)
            
            # Seed Reviews
            db_rev = Review(
                product_id=db_prod.id,
                rating=db_prod.rating,
                positive_percent=85.0 if db_prod.rating >= 4.4 else 75.0,
                negative_percent=15.0 if db_prod.rating >= 4.4 else 25.0,
                pros=pros,
                cons=cons
            )
            db.add(db_rev)
            db.commit()
            
        print("Database fully seeded for all 23 categories successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

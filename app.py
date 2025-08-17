import streamlit as st
import pandas as pd
import random
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# إعدادات الصفحة
st.set_page_config(
    page_title="العقارات الذهبية - البوت الذكي المتطور",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة الدارك مود
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# CSS متطور مع دارك مود
def load_css():
    if st.session_state.dark_mode:
        # الدارك مود
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
            color: white;
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .chat-message-user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 20px;
            margin: 10px 0;
            text-align: right;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .chat-message-bot {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 15px 20px;
            border-radius: 20px;
            margin: 10px 0;
            max-width: 80%;
            margin-right: auto;
            backdrop-filter: blur(10px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .stats-card {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        .property-card {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # اللايت مود
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .chat-message-user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 20px;
            margin: 10px 0;
            text-align: right;
            max-width: 80%;
            margin-left: auto;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        .chat-message-bot {
            background: white;
            border: 1px solid #e0e0e0;
            color: #333;
            padding: 15px 20px;
            border-radius: 20px;
            margin: 10px 0;
            max-width: 80%;
            margin-right: auto;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stats-card {
            background: white;
            color: #333;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border: 1px solid #e0e0e0;
        }
        
        .property-card {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            color: #333;
        }
        </style>
        """, unsafe_allow_html=True)

# تطبيق الـ CSS
load_css()

# أزرار التحكم العلوية
col_theme, col_lang, col_help = st.columns([1, 1, 8])

with col_theme:
    if st.button("🌙" if not st.session_state.dark_mode else "☀", help="تبديل الوضع الليلي/النهاري"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with col_lang:
    if st.button("🌐 EN", help="تغيير اللغة"):
        st.info("قريباً: دعم اللغة الإنجليزية!")

# بيانات العقارات المحسنة
@st.cache_data
def load_properties():
    properties = [
        {
            "id": 1,
            "type": "شقة",
            "price": 850000,
            "area": 120,
            "rooms": 3,
            "bathrooms": 2,
            "location": "القاهرة الجديدة",
            "district": "التجمع الخامس",
            "description": "شقة فاخرة بتشطيب سوبر لوكس مع جاردن خاصة",
            "features": ["جاردن خاصة", "جراج مغطى", "أمن 24 ساعة", "مصعد", "إنترنت فايبر"],
            "image": "🏢",
            "lat": 30.0594885,
            "lon": 31.4236813,
            "year_built": 2020,
            "floor": 3,
            "furnished": True,
            "price_per_meter": 7083
        },
        {
            "id": 2,
            "type": "فيلا",
            "price": 2500000,
            "area": 300,
            "rooms": 5,
            "bathrooms": 4,
            "location": "الشيخ زايد",
            "district": "الحي السادس عشر",
            "description": "فيلا مستقلة مع حديقة واسعة ومسبح خاص",
            "features": ["مسبح خاص", "حديقة 200م²", "جراج لسيارتين", "روف", "غرفة خدم"],
            "image": "🏘",
            "lat": 30.0776185,
            "lon": 30.9982239,
            "year_built": 2019,
            "floor": 0,
            "furnished": False,
            "price_per_meter": 8333
        },
        {
            "id": 3,
            "type": "شقة",
            "price": 650000,
            "area": 100,
            "rooms": 2,
            "bathrooms": 2,
            "location": "المعادي",
            "district": "المعادي الجديدة",
            "description": "شقة مودرن مطلة على النيل مباشرة",
            "features": ["إطلالة مباشرة على النيل", "تكييف مركزي", "مصعد حديث", "بلكونة واسعة"],
            "image": "🏙",
            "lat": 29.9602203,
            "lon": 31.2569438,
            "year_built": 2018,
            "floor": 7,
            "furnished": True,
            "price_per_meter": 6500
        },
        {
            "id": 4,
            "type": "محل",
            "price": 1200000,
            "area": 80,
            "rooms": 1,
            "bathrooms": 1,
            "location": "وسط البلد",
            "district": "العتبة",
            "description": "محل تجاري في أكثر المناطق حيوية",
            "features": ["موقع تجاري ممتاز", "واجهة زجاجية كبيرة", "قريب من المترو"],
            "image": "🏪",
            "lat": 30.0444196,
            "lon": 31.2357116,
            "year_built": 2015,
            "floor": 0,
            "furnished": False,
            "price_per_meter": 15000
        },
        {
            "id": 5,
            "type": "شقة",
            "price": 950000,
            "area": 140,
            "rooms": 3,
            "bathrooms": 2,
            "location": "مدينة نصر",
            "district": "الحي العاشر",
            "description": "شقة واسعة ومضيئة مع بلكونة كبيرة",
            "features": ["بلكونة واسعة", "قريبة من مترو الأنفاق", "تشطيب حديث"],
            "image": "🏘",
            "lat": 30.0616863,
            "lon": 31.3260018,
            "year_built": 2021,
            "floor": 5,
            "furnished": False,
            "price_per_meter": 6786
        },
        {
            "id": 6,
            "type": "فيلا",
            "price": 3200000,
            "area": 400,
            "rooms": 6,
            "bathrooms": 5,
            "location": "أكتوبر الجديدة",
            "district": "الحي الثالث",
            "description": "فيلا فخمة مع تشطيب إيطالي فاخر",
            "features": ["تشطيب إيطالي فاخر", "مسبح أوليمبي", "حديقة استوائية", "جاكوزي"],
            "image": "🏖",
            "lat": 29.9602203,
            "lon": 30.9020376,
            "year_built": 2022,
            "floor": 0,
            "furnished": True,
            "price_per_meter": 8000
        }
    ]
    return pd.DataFrame(properties)

# تهيئة البيانات
if 'properties_df' not in st.session_state:
    st.session_state.properties_df = load_properties()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'analytics_data' not in st.session_state:
    st.session_state.analytics_data = {
        'searches': 0,
        'messages': 0,
        'bookings': 0,
        'popular_areas': {},
        'popular_types': {}
    }

# دوال مساعدة
def format_price(price):
    if price >= 1000000:
        return f"{price/1000000:.1f} مليون جنيه"
    else:
        return f"{price:,} جنيه"

def create_whatsapp_link(message_type="general", property_id=None):
    base_number = "201234567890"
    messages = {
        "general": "مرحباً، أريد الاستفسار عن خدماتكم العقارية",
        "booking": f"مرحباً، أريد حجز موعد لمعاينة العقار رقم {property_id}" if property_id else "مرحباً، أريد حجز موعد معاينة",
        "search": "مرحباً، أريد البحث عن عقار مناسب",
        "financing": "مرحباً، أريد الاستفسار عن خيارات التمويل"
    }
    message = messages.get(message_type, messages["general"])
    return f"https://wa.me/{base_number}?text={message}"

def search_properties(budget_min=0, budget_max=10000000, property_type=None, location=None, min_rooms=0, furnished=None):
    df = st.session_state.properties_df
    df = df[(df['price'] >= budget_min) & (df['price'] <= budget_max)]
    
    if property_type and property_type != "الكل":
        df = df[df['type'] == property_type]
    
    if location and location != "الكل":
        df = df[df['location'].str.contains(location, case=False, na=False)]
    
    if min_rooms > 0:
        df = df[df['rooms'] >= min_rooms]
        
    if furnished is not None:
        df = df[df['furnished'] == furnished]
    
    st.session_state.analytics_data['searches'] += 1
    return df

def get_smart_response(user_message, properties_df):
    user_message = user_message.lower().strip()
    
    # ردود ذكية محسنة
    if any(word in user_message for word in ['فيلا', 'فيلات']):
        villas = properties_df[properties_df['type'] == 'فيلا']
        if not villas.empty:
            avg_price = villas['price'].mean()
            return f"""🏘 لدينا {len(villas)} فيلات رائعة!

💰 متوسط الأسعار: {avg_price:,.0f} جنيه
📐 المساحات: من {villas['area'].min()} إلى {villas['area'].max()} م²

🏆 أفضل عروضنا:
• {villas.iloc[0]['location']}: {format_price(villas.iloc[0]['price'])}
• {villas.iloc[1]['location']}: {format_price(villas.iloc[1]['price'])}

استخدم أدوات البحث للمزيد! 🔍"""

    elif any(word in user_message for word in ['شقة', 'شقق']):
        apartments = properties_df[properties_df['type'] == 'شقة']
        return f"""🏢 عندنا {len(apartments)} شقق متميزة!

💰 الأسعار تبدأ من {format_price(apartments['price'].min())}
📍 في أفضل المناطق: {', '.join(apartments['location'].unique()[:3])}

✨ مميزات خاصة:
• شقق مفروشة وغير مفروشة
• إطلالات متنوعة (نيل، حدائق، مدينة)  
• تشطيبات عالية الجودة

جرب البحث بالميزانية المناسبة! 💡"""

    # ردود أساسية
    responses = {
        "مرحبا": f"""🌟 أهلاً وسهلاً بك في العقارات الذهبية!

أنا مساعدك الذكي المتطور، يمكنني مساعدتك في:
🏠 البحث عن العقارات ({len(properties_df)} عقار متاح)
📊 تحليل الأسعار والمقارنات  
📍 معلومات المناطق المختلفة
📅 حجز مواعيد المعاينة
💰 استشارات التمويل والتقسيط

كيف يمكنني خدمتك اليوم؟ ✨""",

        "شكرا": """العفو وبالتوفيق! 😊
سعدنا بخدمتك، لا تتردد في التواصل معنا أي وقت!
فريقنا متاح 24/7 📞""",
        
        "باي": """مع السلامة! 👋
شكراً لزيارتك العقارات الذهبية
العقارات الذهبية - خيارك الأول دائماً! 💎"""
    }
    
    for key, response in responses.items():
        if key in user_message:
            return response
    
    return f"""🤖 يمكنني مساعدتك بشكل أفضل!

جرب هذه الاقتراحات:
💭 "أريد شقة في المعادي"
💭 "فيلات في الشيخ زايد"
💭 "ميزانيتي 800 ألف"

أو استخدم الكلمات المفتاحية:
🔑 أسعار | مواعيد | مناطق | تمويل

حالياً لدينا {len(properties_df)} عقار في {len(properties_df['location'].unique())} منطقة! 🏠"""

# واجهة المستخدم الرئيسية
st.markdown("""
<div class="main-header">
    <h1>🏠 العقارات الذهبية</h1>
    <h3>البوت العقاري الذكي المتطور</h3>
    <p>مساعدك الشخصي المتطور للعثور على العقار المثالي</p>
</div>
""", unsafe_allow_html=True)

# شريط جانبي محسن
with st.sidebar:
    st.markdown("### 🎛 لوحة التحكم المتقدمة")
    
    # تبويبات
    tab1, tab2, tab3 = st.tabs(["🔍 البحث", "📊 الإحصائيات", "⚙ الإعدادات"])
    
    with tab1:
        st.markdown("#### فلاتر البحث المتقدم")
        
        budget_range = st.slider(
            "💰 الميزانية (جنيه)",
            min_value=500000,
            max_value=4000000,
            value=(500000, 4000000),
            step=50000
        )
        
        property_type = st.selectbox(
            "🏠 نوع العقار",
            options=["الكل", "شقة", "فيلا", "محل"]
        )
        
        location = st.selectbox(
            "📍 المنطقة",
            options=["الكل"] + list(st.session_state.properties_df['location'].unique())
        )
        
        min_rooms = st.number_input(
            "🛏 الحد الأدنى للغرف",
            min_value=0,
            max_value=10,
            value=0
        )
        
        furnished_filter = st.radio(
            "🪑 الأثاث",
            options=[None, True, False],
            format_func=lambda x: "الكل" if x is None else ("مفروش" if x else "غير مفروش"),
            index=0
        )
        
        if st.button("🔍 بحث متقدم", type="primary"):
            filtered_properties = search_properties(
                budget_min=budget_range[0],
                budget_max=budget_range[1],
                property_type=property_type,
                location=location,
                min_rooms=min_rooms,
                furnished=furnished_filter
            )
            st.session_state.filtered_properties = filtered_properties
            st.success(f"✅ تم العثور على {len(filtered_properties)} عقار!")
    
    with tab2:
        st.markdown("#### 📈 إحصائيات سريعة")
        df = st.session_state.properties_df
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏠 العقارات", len(df))
            st.metric("💰 متوسط السعر", f"{df['price'].mean():,.0f}")
        with col2:
            st.metric("📍 المناطق", len(df['location'].unique()))
            st.metric("🔍 البحثات", st.session_state.analytics_data['searches'])
        
        # أشهر المناطق
        st.markdown("📊 أشهر المناطق:")
        location_counts = df['location'].value_counts()
        for loc, count in location_counts.items():
            st.write(f"• {loc}: {count} عقار")
    
    with tab3:
        st.markdown("#### ⚙ إعدادات التطبيق")
        
        if st.button("🌙 تبديل الوضع" + (" النهاري" if st.session_state.dark_mode else " الليلي")):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        show_charts = st.checkbox("📊 عرض الرسوم البيانية", value=True)
        show_map = st.checkbox("🗺 عرض الخرائط", value=True)
        show_analytics = st.checkbox("📈 عرض الإحصائيات", value=True)
        
        st.markdown("---")
        st.markdown("#### 📞 معلومات التواصل")
        st.info("""
        📱 واتساب: 01234567890  
        📧 البريد: info@goldenestate.com  
        📍 العنوان: شارع النيل، القاهرة
        """)

# المحتوى الرئيسي
main_col1, main_col2 = st.columns([2, 1])

with main_col1:
    # واجهة المحادثة المحسنة
    st.markdown("### 💬 المحادثة الذكية")
    
    # عرض المحادثات
    chat_container = st.container(height=400)
    
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message-user">
                        <strong>👤 أنت:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message-bot">
                        <strong>🤖 المساعد الذكي:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
    
    # مربع الرسائل
    user_input = st.text_input(
        "💬 اكتب رسالتك هنا...",
        placeholder="مثال: أبحث عن فيلا في الشيخ زايد بميزانية 3 مليون جنيه",
        key="user_input"
    )
    
    col_send, col_clear, col_whatsapp = st.columns([2, 1, 2])
    
    with col_send:
        if st.button("📤 إرسال", type="primary") and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            response = get_smart_response(user_input, st.session_state.properties_df)
            st.session_state.chat_history.append({"role": "bot", "content": response})
            st.session_state.analytics_data['messages'] += 1
            st.rerun()
    
    with col_clear:
        if st.button("🗑 مسح"):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_whatsapp:
        whatsapp_url = create_whatsapp_link("general")
        st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:5px;cursor:pointer;">📱 واتساب</button></a>', unsafe_allow_html=True)

with main_col2:
    # إحصائيات متطورة
    if 'show_analytics' in locals() and show_analytics:
        st.markdown("### 📊 لوحة الإحصائيات")
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{st.session_state.analytics_data['searches']}</h3>
                <p>عملية بحث</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>{st.session_state.analytics_data['messages']}</h3>
                <p>رسالة محادثة</p>
            </div>
            """, unsafe_allow_html=True)

# رسائل البداية السريعة
if not st.session_state.chat_history:
    st.markdown("### 🚀 رسائل سريعة")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_messages = [
        ("👋 مرحبا", "مرحبا"),
        ("🏠 أريد شقة", "أريد شقة"),
        ("💰 الأسعار", "اسعار"),
        ("📅 حجز موعد", "حجز موعد")
    ]
    
    for i, (text, msg) in enumerate(quick_messages):
        col = [col1, col2, col3, col4][i]
        with col:
            if st.button(text, key=f"quick_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": msg})
                response = get_smart_response(msg, st.session_state.properties_df)
                st.session_state.chat_history.append({"role": "bot", "content": response})
                st.session_state.analytics_data['messages'] += 1
                st.rerun()

# عرض نتائج البحث
if 'filtered_properties' in st.session_state and not st.session_state.filtered_properties.empty:
    st.markdown("---")
    st.markdown("### 🏘 نتائج البحث")
    
    results_df = st.s

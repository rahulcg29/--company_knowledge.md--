import streamlit as st
import time
import json

# Configure the app
st.set_page_config(
    page_title="CR IT Infopark - REXA",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cache company knowledge
@st.cache_data
def load_company_knowledge():
    """Load company knowledge with caching"""
    return """
    CR IT Infopark - Leading IT Solutions Provider
    
    🏢 ABOUT US:
    - Established IT company providing cutting-edge solutions
    - Specializing in web development, mobile apps, and cloud services
    - Committed to innovation and customer satisfaction
    
    💼 SERVICES:
    - Custom Web Development (React, Angular, Node.js)
    - Mobile App Development (iOS & Android)
    - Cloud Solutions (AWS, Azure, Google Cloud)
    - AI/ML Development and Consulting
    - E-commerce Solutions
    - Digital Marketing Services
    
    🚀 CAREERS:
    Available Positions:
    - Full Stack Developer (React/Node.js)
    - Mobile App Developer (React Native/Flutter)
    - UI/UX Designer
    - DevOps Engineer
    - Project Manager
    - Quality Assurance Engineer
    
    📋 BENEFITS:
    - Competitive salary packages
    - Flexible working hours
    - Remote work options
    - Health insurance
    - Professional development opportunities
    - Modern work environment
    
    📞 CONTACT:
    - Email: careers@critinfopark.com
    - Phone: +91-XXX-XXX-XXXX
    - Website: www.critinfopark.com
    - Location: Infopark, Kochi, Kerala
    
    🏆 VALUES:
    - Innovation and Excellence
    - Customer-Centric Approach
    - Team Collaboration
    - Continuous Learning
    """

# Fast response system using pre-defined answers
@st.cache_data
def get_quick_responses():
    """Pre-defined responses for maximum speed"""
    return {
        # About company
        "about":"""CR IT info is a leading company in coimbatore \n\n
                CR Info park was founded in the year of 2003.\n\n
                we service across different technologies through different region .\n\n
                We mainly focused in the field of AIML /PYTHON /JAVA .\n\n
                we have a successfully doned the projects for more than 500+ clients.serving to the nation through information and technology.\n\n
                CR Info Park is a leading information technology company dedicated to delivering innovative digital solutions that drive business transformation.\n\n
                we have established ourselves as a trusted partner for organizations seeking to leverage technology for competitive advantage and operational excellence.\n\n""",
        
        "services": """We offer: Custom Web Development (React, Node.js)\n\n
                       Mobile Apps (iOS/Android)\n\n 
                       Cloud Solutions (AWS, Azure)\n\n
                       AI/ML Development\n\n
                       E-commerce Solutions\n\n
                       Digital Marketing Services.""",
        
        "company": """Founded as a technology-first company\n\n
                      CR IT Infopark focuses on cutting-edge solutions for businesses.\n\n
                      We combine innovation with reliability to deliver exceptional results.""",
        
        # Jobs and careers
        "jobs": """Current openings: Full Stack Developer\n\n
                   *Mobile App Developer\n\n
                   *UI/UX Designer, DevOps Engineer\n\n
                   *Project Manager, QA Engineer\n\n
                   *All positions offer competitive packages and growth opportunities.""",
        
        "career": """Join our dynamic team! We offer competitive salaries, flexible hours, remote work options, health insurance, and professional development.\n\n 
                     Email: careers@critinfopark.com""",
        
        "apply": """***To apply***
                    Send your resume to careers@critinfopark.com \n\n
                    With the position title in the subject line.\n\n
                    Include a cover letter highlighting your relevant experience.""",
        
        "benefits": "Employee benefits include: Competitive salary, flexible working hours, remote work options, comprehensive health insurance, professional development budget, and modern office environment.",
        
        # Contact and location  
        "contact": "📞 Phone: +91-6382074060\n\n📧 Email: careers@critinfopark.com\n\n🌐 Website: www.critinfopark.com\n\n📍 Location: Infopark, Kochi, chennai",
        
        "location": "We're located at Infopark, Kochi, Kerala - India's premier IT hub. Our modern office provides an excellent work environment for our team.",
        
        # Skills and requirements
        "skills": "We look for skills in: React/Angular, Node.js, Python, Mobile development (React Native/Flutter), Cloud platforms (AWS/Azure), DevOps tools, and strong problem-solving abilities.",
        
        "requirements": "Generally we require: Relevant degree in CS/IT, 2+ years experience (varies by role), strong technical skills, good communication, and passion for technology innovation.",
    }

def find_best_response(query):
    """Ultra-fast response matching using keywords"""
    query_lower = query.lower()
    responses = get_quick_responses()
    
    # Keyword mapping for intelligent matching
    keyword_map = {
        "about": ["about", "company", "what", "who", "cr", "infopark"],
        "services": ["service", "offer", "do", "provide", "solutions", "development"],
        "jobs": ["job", "position", "opening", "vacancy", "role", "hiring"],
        "career": ["career", "work", "join", "opportunity", "growth"],
        "apply": ["apply", "application", "how to", "process", "submit", "resume"],
        "benefits": ["benefit", "package", "salary", "insurance", "flexible", "perks"],
        "contact": ["contact", "phone", "email", "reach", "call", "address"],
        "location": ["location", "where", "office", "address", "kochi", "kerala"],
        "skills": ["skill", "technology", "tech", "programming", "language"],
        "requirements": ["requirement", "qualification", "experience", "degree"],
    }
    
    # Find best match based on keyword frequency
    best_match = "about"  # default
    max_score = 0
    
    for response_key, keywords in keyword_map.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        if score > max_score:
            max_score = score
            best_match = response_key
    
    return responses.get(best_match, responses["about"])

def generate_lightning_response(prompt):
    """Generate ultra-fast response using pre-defined answers"""
    start_time = time.time()
    
    # Quick validation
    if len(prompt.strip()) == 0:
        return "Please ask me something about CR IT Infopark!"
    
    if len(prompt) > 200:
        return "Please ask a shorter, more specific question for faster response."
    
    # Check if it's company-related
    company_keywords = ["cr", "it", "infopark", "company", "job", "career", "service", "about", "work", "apply"]
    is_company_query = any(keyword in prompt.lower() for keyword in company_keywords)
    
    if not is_company_query and len(prompt.split()) > 3:
        return "I can only answer questions about CR IT Infopark. Please ask about our services, careers, or company information."
    
    # Generate response
    response = find_best_response(prompt)
    
    elapsed = time.time() - start_time
    
    # Add timing for very fast responses
    if elapsed < 0.1:
        response += f"\n\n⚡ _Lightning response: {elapsed*1000:.0f}ms_"
    
    return response

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Lightning-fast prompts
INSTANT_PROMPTS = {
    "🏢 About Us": "Tell me about CR IT Infopark",
    "💼 Job Openings": "What jobs are available?", 
    "🚀 How to Apply": "How do I apply for a job?",
    "📧 Contact Info": "How can I contact you?",
    "🎯 Services": "What services do you offer?"
}

# Main UI
st.title("⚡ REXA - Lightning Fast Assistant")
st.caption("Instant answers about CR IT Infopark (No API required!)")

# Performance indicator
st.success("🟢 Ultra-fast local responses ready!")

# Lightning Quick Actions
st.subheader("⚡ Instant Answers")
cols = st.columns(len(INSTANT_PROMPTS))

for i, (emoji_label, prompt) in enumerate(INSTANT_PROMPTS.items()):
    with cols[i]:
        if st.button(emoji_label, use_container_width=True, key=f"quick_{i}"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate instant response
            response = generate_lightning_response(prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# Chat display (show last 6 messages for performance)
if st.session_state.messages:
    st.subheader("💬 Chat History")
    for message in st.session_state.messages[-6:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Lightning-fast chat input
if prompt := st.chat_input("⚡ Ask me anything about CR IT Infopark...", max_chars=200):
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate instant response
    with st.chat_message("assistant"):
        start = time.time()
        response = generate_lightning_response(prompt)
        elapsed = time.time() - start
        
        st.markdown(response)
        
        # Show performance metric
        if elapsed < 0.01:
            st.success(f"⚡ Instant response: {elapsed*1000:.1f}ms")

    st.session_state.messages.append({"role": "assistant", "content": response})

# Information panels
col1, col2 = st.columns(2)

with col1:
    with st.expander("⚡ Why So Fast?"):
        st.info("""
        **No API Calls Required!**
        - Pre-computed responses
        - Local keyword matching  
        - Cached company knowledge
        - Optimized algorithms
        
        **Response Time: <10ms**
        """)

with col2:
    with st.expander("📋 Available Topics"):
        st.info("""
        **I can help with:**
        - Company information
        - Job openings & careers
        - Application process
        - Services offered
        - Contact details
        - Benefits & culture
        """)

# Quick utilities
col3, col4 = st.columns(2)

with col3:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

with col4:
    if st.button("📋 Show All Services"):
        knowledge = load_company_knowledge()
        st.session_state.messages.append({"role": "user", "content": "Show me all services"})
        st.session_state.messages.append({"role": "assistant", "content": knowledge})
        st.rerun()

# Performance stats
if st.session_state.messages:
    st.sidebar.metric("Total Messages", len(st.session_state.messages))
    st.sidebar.metric("Response Type", "⚡ Instant Local")
    st.sidebar.success("No internet required!")

# Custom CSS for maximum speed
st.markdown("""
<style>
    .stChatMessage {
        animation: none !important;
        transition: none !important;
    }
    .stButton > button {
        transition: all 0.05s ease !important;
    }
    .main .block-container {
        padding-top: 2rem !important;
        max-width: 900px !important;
    }
    .stSuccess, .stInfo {
        animation: none !important;
    }
</style>
""", unsafe_allow_html=True)
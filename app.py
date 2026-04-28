import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -------------------------------------------------------------
# Configuration and Setup
# -------------------------------------------------------------
st.set_page_config(
    page_title="Career Intelligence Pro", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# Database (Careers, Courses, etc.)
# -------------------------------------------------------------
CAREERS_DB = {
    "Software Developer": {
        "domain": "Technology", 
        "skills": ["Python", "Java", "SQL", "Git", "Problem Solving", "React", "Cloud"], 
        "description": "Architects, tests, and maintains scalable software applications.", 
        "salary": "$105,000", "min_salary": 70000, "max_salary": 160000,
        "environments": ["Remote", "Hybrid", "On-site"],
        "traits": ["Analytical", "Collaborative", "Problem-Solver"],
        "demand_index": 95, "future_scope": "Excellent"
    },
    "Data Scientist": {
        "domain": "Technology", 
        "skills": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization"], 
        "description": "Transforms complex data into actionable business and product insights.", 
        "salary": "$120,000", "min_salary": 85000, "max_salary": 180000,
        "environments": ["Remote", "Hybrid"],
        "traits": ["Analytical", "Curious", "Detail-Oriented"],
        "demand_index": 98, "future_scope": "Excellent"
    },
    "Medical Doctor": {
        "domain": "Healthcare", 
        "skills": ["Empathy", "Anatomy", "Diagnostics", "Communication", "Patient Care"], 
        "description": "Diagnoses, treats, and prevents medical conditions in patients.", 
        "salary": "$200,000+", "min_salary": 150000, "max_salary": 300000,
        "environments": ["On-site"],
        "traits": ["Empathetic", "Resilient", "Detail-Oriented"],
        "demand_index": 99, "future_scope": "Excellent"
    },
    "Educator": {
        "domain": "Education", 
        "skills": ["Communication", "Patience", "Subject Knowledge", "Mentoring"], 
        "description": "Focuses on curriculum delivery, mentoring, and student development.", 
        "salary": "$60,000", "min_salary": 45000, "max_salary": 90000,
        "environments": ["On-site", "Hybrid"],
        "traits": ["Empathetic", "Communicator", "Patient"],
        "demand_index": 85, "future_scope": "Stable"
    },
    "Business Analyst": {
        "domain": "Business", 
        "skills": ["Data Analysis", "Communication", "Excel", "SQL", "Agile"], 
        "description": "Evaluates organizational operations and designs systems for efficiency.", 
        "salary": "$85,000", "min_salary": 65000, "max_salary": 120000,
        "environments": ["Hybrid", "On-site", "Remote"],
        "traits": ["Analytical", "Strategic", "Collaborative"],
        "demand_index": 88, "future_scope": "Good"
    },
    "UI/UX Designer": {
        "domain": "Design", 
        "skills": ["Figma", "Creativity", "Typography", "User Research", "Wireframing"], 
        "description": "Crafts intuitive, user-centric visual experiences for digital platforms.", 
        "salary": "$75,000", "min_salary": 55000, "max_salary": 110000,
        "environments": ["Remote", "Hybrid"],
        "traits": ["Creative", "Detail-Oriented", "Empathetic"],
        "demand_index": 80, "future_scope": "Good"
    },
    "Product Manager": {
        "domain": "Business", 
        "skills": ["Leadership", "Agile", "Strategy", "Communication", "Data Analysis"], 
        "description": "Guides the lifecycle of a product from conception through launch to market.", 
        "salary": "$110,000", "min_salary": 80000, "max_salary": 160000,
        "environments": ["Hybrid", "Remote", "On-site"],
        "traits": ["Strategic", "Collaborative", "Communicator"],
        "demand_index": 92, "future_scope": "Excellent"
    },
    "Mechanical Engineer": {
        "domain": "Engineering", 
        "skills": ["AutoCAD", "Mathematics", "Problem Solving", "Physics"], 
        "description": "Designs and tests mechanical and thermal sensors and devices.", 
        "salary": "$90,000", "min_salary": 70000, "max_salary": 130000,
        "environments": ["On-site", "Hybrid"],
        "traits": ["Analytical", "Detail-Oriented", "Practical"],
        "demand_index": 82, "future_scope": "Stable"
    },
    "Financial Analyst": {
        "domain": "Business", 
        "skills": ["Excel", "Financial Modeling", "Accounting", "Risk Management"], 
        "description": "Directs investments and analyzes market data for portfolios and growth.", 
        "salary": "$95,000", "min_salary": 65000, "max_salary": 150000,
        "environments": ["Hybrid", "On-site"],
        "traits": ["Analytical", "Detail-Oriented", "Independent"],
        "demand_index": 86, "future_scope": "Very Good"
    },
    "Registered Nurse": {
        "domain": "Healthcare", 
        "skills": ["Patient Care", "Empathy", "CPR", "Time Management"], 
        "description": "Delivers vital, frontline medical care and support in critical settings.", 
        "salary": "$80,000", "min_salary": 65000, "max_salary": 115000,
        "environments": ["On-site"],
        "traits": ["Empathetic", "Detail-Oriented", "Resilient"],
        "demand_index": 97, "future_scope": "Excellent"
    }
}

# Unique set derivations
ALL_SKILLS = sorted(list(set([skill for career in CAREERS_DB.values() for skill in career["skills"]])))
DOMAINS = ["Any Domain"] + sorted(list(set([c["domain"] for c in CAREERS_DB.values()])))
TRAITS = ["Analytical", "Collaborative", "Independent", "Problem-Solver", "Curious", 
          "Detail-Oriented", "Empathetic", "Resilient", "Communicator", "Creative", 
          "Patient", "Strategic", "Adaptable", "Practical"]

def get_course_path(skill):
    return [
        f"📖 **Foundation:** Intro to {skill} (Coursera)",
        f"🛠️ **Application:** Intermediate {skill} Bootcamps (edX)",
        f"🚀 **Mastery:** Advanced {skill} Portfolios (GitHub / Project-based)"
    ]

# -------------------------------------------------------------
# Helper: Analytical Engine
# -------------------------------------------------------------
def analyze_fit(skills, domain, interests, traits, environment, salary):
    recs = []
    u_skills = set(skills)
    u_traits = set(traits)
    
    for title, data in CAREERS_DB.items():
        if domain != "Any Domain" and data["domain"] != domain: continue
            
        r_skills = set(data["skills"])
        r_traits = set(data["traits"])
        
        # Weighted Dimensions
        p_skill = int((len(u_skills.intersection(r_skills)) / len(r_skills)) * 100) if r_skills else 0
        p_trait = int((len(u_traits.intersection(r_traits)) / len(r_traits)) * 100) if r_traits and u_traits else 50
        p_env = 100 if environment == "Flexible (Any)" or environment in data["environments"] else 40
        p_sal = 100 if salary <= data["min_salary"] else max(20, int(100 - ((salary - data["min_salary"]) / (data["max_salary"] - data["min_salary"]) * 60))) if salary <= data["max_salary"] else 20
            
        # Core Formula
        total = (p_skill * 0.45) + (p_trait * 0.25) + (p_env * 0.15) + (p_sal * 0.15)
        
        # Industry Interest Booster
        if data["domain"] in interests: total += 5
        total = min(int(total), 100)
        
        recs.append({
            "Title": title, "Domain": data["domain"], "Desc": data["description"],
            "Salary": data["salary"], "Future": data["future_scope"],
            "Dim_Skill": p_skill, "Dim_Trait": p_trait, "Dim_Env": p_env, "Dim_Sal": p_sal,
            "Score": total, "Demand": data["demand_index"], "Traits": data["traits"],
            "Missing": list(r_skills - u_skills)
        })
        
    return sorted(recs, key=lambda x: x["Score"], reverse=True)

# -------------------------------------------------------------
# Clean UI: Sidebar
# -------------------------------------------------------------
with st.sidebar:
    st.title("🎯 Career Configurator")
    st.caption("Tell us about yourself to tailor the engine.")
    
    st.subheader("1. Profile Overview")
    user_name = st.text_input("Full Name", placeholder="Alex Doe")
    user_exp = st.number_input("Years of Experience", 0, 40, 0)
    
    st.subheader("2. Knowledge Base")
    user_skills = st.multiselect("Technical Skills", ALL_SKILLS, placeholder="Choose capabilities...")
    user_interests = st.multiselect("Industry Interests", DOMAINS[1:], placeholder="What excites you?")
    
    st.subheader("3. Work DNA & Culture")
    user_traits = st.multiselect("Core Personality Traits", TRAITS, max_selections=4, placeholder="Select up to 4")
    user_environment = st.radio("Target Environment", ["Flexible (Any)", "Remote", "Hybrid", "On-site"], horizontal=True)
    user_salary = st.slider("Absolute Minimum Compensation ($)", 40000, 200000, 60000, step=5000)
    user_domain = st.selectbox("Strict Industry Filter", DOMAINS)

# -------------------------------------------------------------
# Clean UI: Main Content
# -------------------------------------------------------------
st.title("Career Intelligence Ecosystem 💼")

if not user_name or not user_skills:
    # Empty State
    with st.container(border=True):
        st.info("👈 **Awaiting Data Input:** Please complete the setup in the sidebar to generate your personalized career matrix.")
else:
    # Analytics State
    results = analyze_fit(user_skills, user_domain, user_interests, user_traits, user_environment, user_salary)
    
    if not results:
        st.error("No matches found based on your strictest filters. Try relaxing the 'Industry Filter'.")
    else:
        # Welcome Hero
        col_greet, col_stat = st.columns([2, 1])
        col_greet.success(f"**Analysis Generated for {user_name}** • Engine consumed {len(user_skills)} skills & {len(user_traits)} traits.")
        col_stat.metric("Top Fit Match", f"{results[0]['Score']}%", "Optimal")
        
        # Main Navigation
        tabs = st.tabs(["🏆 Recommended Careers", "🕸️ Capability Radar", "🗺️ Upskill Maps", "📈 Global Insights"])
        
        # --- TAB 1: RECOMMENDATIONS ---
        with tabs[0]:
            st.markdown("#### Primary Alignments")
            for i, c in enumerate(results[:3]):
                with st.container(border=True):
                    row1, row2 = st.columns([3, 1])
                    
                    with row1:
                        st.subheader(f"{i+1}. {c['Title']}")
                        st.caption(f"**{c['Domain']}** • {c['Desc']}")
                        st.markdown("**Culture Match:** " + ' · '.join([f"`{t}`" for t in c['Traits']]))
                        st.markdown(f"**Compensation:** {c['Salary']} (Average)  |  **Future Outlook:** {c['Future']}")
                        
                        if c["Missing"]:
                            st.warning(f"**Gaps:** {', '.join(c['Missing'])}")
                        else:
                            st.success("✨ **Gaps:** None. 100% Technical Match.")
                            
                    with row2:
                        st.metric("Compatibility", f"{c['Score']}%")
                        st.progress(c['Score']/100)
        
        # --- TAB 2: VISUAL RADAR ---
        with tabs[1]:
            st.markdown("#### Multi-Dimensional Signature")
            
            fig = go.Figure()
            colors = ["#3b82f6", "#10b981", "#8b5cf6"]
            
            for i, c in enumerate(results[:2]): # Plot top 2
                fig.add_trace(go.Scatterpolar(
                    r=[c["Dim_Skill"], c["Dim_Trait"], c["Dim_Env"], c["Dim_Sal"]],
                    theta=['Technical Skills', 'Personality', 'Environment Form', 'Salary Match'],
                    fill='toself', name=f"#{i+1} {c['Title']}",
                    line_color=colors[i], opacity=0.8
                ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True, margin=dict(l=40, r=40, t=40, b=40),
                paper_bgcolor="rgba(0,0,0,0)" # transparent
            )
            st.plotly_chart(fig, use_container_width=True)

        # --- TAB 3: UPSKILL MAPS ---
        with tabs[2]:
            st.markdown("#### Targeted Learning Journeys")
            top_needs = results[0]
            
            if not top_needs["Missing"]:
                st.success(f"**Validation:** You hold all required technical skills for '#1 {top_needs['Title']}'. Focus on soft-skills and networking!")
            else:
                st.info(f"Closing the gap for #1 **{top_needs['Title']}**:")
                
                for skill in top_needs["Missing"]:
                    with st.expander(f"Acquire: {skill}", expanded=True):
                        paths = get_course_path(skill)
                        for p in paths:
                            st.write(p)
                            
        # --- TAB 4: INSIGHTS ---
        with tabs[3]:
            st.markdown("#### Macro Trends Context")
            
            df = pd.DataFrame(results[:5])
            col_chart, col_data = st.columns([2, 1])
            
            with col_chart:
                fig2 = px.bar(
                    df, x='Title', y='Demand', color='Score', 
                    color_continuous_scale="Blues",
                    labels={'Demand': 'Market Demand (1-100)', 'Title': ''}
                )
                fig2.update_layout(margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, use_container_width=True)
                
            with col_data:
                st.write("**Top 5 Averages**")
                st.metric("Avg Compatibility", f"{df['Score'].mean():.1f}%")
                st.metric("Avg Tech Mastery", f"{df['Dim_Skill'].mean():.1f}%")
                st.metric("Avg Demand Index", f"{df['Demand'].mean():.0f}/100")
                
                # Download Button safely integrated here
                csv_data = df[['Title', 'Domain', 'Score', 'Salary', 'Future']].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Export Analysis CSV",
                    data=csv_data,
                    file_name="career_matrix.csv",
                    mime="text/csv",
                    use_container_width=True
                )
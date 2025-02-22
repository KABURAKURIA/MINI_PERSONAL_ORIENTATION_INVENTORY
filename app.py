import streamlit as st
import altair as alt
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---------- Inject Custom CSS for a Faded Existential Background and Glassy Widgets ----------
st.markdown(
    """
    <style>
    /* Faded existential background inspired by Dr. Seuss architectural style */
    body {
        background: linear-gradient(rgba(20,20,20,0.6), rgba(20,20,20,0.6)),
                    url('https://www.toptal.com/designers/subtlepatterns/patterns/diagmonds.png');
        background-size: cover;
        background-attachment: fixed;
        color: #fff;
        font-family: 'Roboto', sans-serif;
    }
    /* Standard glassy container (frosted look with contrast in opacity) */
    .glassy-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(255, 255, 255, 0.2);
    }
    /* Full-width glassy container for charts */
    .full-width-glassy {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(255, 255, 255, 0.2);
    }
    /* Headings and text styling with glow and metallic feel */
    h1, h2, h3, p, label {
        color: #fff;
        text-shadow: 0 0 5px rgba(0,0,0,0.7);
    }
    h1 {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    h1:after {
        content: '';
        display: block;
        margin: 0.5rem auto;
        width: 200px;
        height: 3px;
        background: linear-gradient(45deg, #fff, #ccc);
        box-shadow: 0 0 8px #ccc;
    }
    /* Input and slider styling */
    .stTextInput>div>input, .stSlider>div>div>div {
        background: rgba(0,0,0,0.7) !important;
        color: #fff !important;
        border: 1px solid #555 !important;
        border-radius: 4px;
    }
    .stTextInput>div>input::placeholder {
        color: #aaa !important;
    }
    /* Button styling with metallic glow */
    .stButton button, .metallic-button {
        background: #fff;
        color: #000;
        border: 2px solid #fff;
        border-radius: 4px;
        font-size: 1.1rem;
        cursor: pointer;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        background-image: linear-gradient(45deg, #ccc, #888, #ccc);
        background-blend-mode: multiply;
    }
    .stButton button:hover, .metallic-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.8);
    }
    /* Footer styling */
    footer {
        width: 100%;
        background: #000;
        color: #fff;
        padding: 1.5rem;
        text-align: center;
        border-top: 2px solid #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Wrap Title, Description, and Form in a Glassy Widget ----------
st.markdown("<div class='glassy-container'>", unsafe_allow_html=True)
st.title("Mini Orientation Inventory")
st.markdown(
    "#### Discover your self-actualizing potential with this Mini Orientation Inventory. "
    "This assessment is designed for college-age and adult individuals to help reveal attitudes "
    "and values that indicate positive mental health."
)

# ---------- Define Sample Assessment Questions ----------
questions = [
    {"trait": "Time Competence", "question": "I am focused on and engaged with the present moment."},
    {"trait": "Inner-Directed", "question": "I trust my inner guidance when making decisions."},
    {"trait": "Self-Actualizing Value", "question": "I strive to realize my full potential."},
    {"trait": "Existentiality", "question": "I respond authentically to life’s challenges."},
    {"trait": "Feeling Reactivity", "question": "I am sensitive to my own emotions."},
    {"trait": "Spontaneity", "question": "I act spontaneously and express my true self."},
]

# ---------- Define Therapeutic Recommendations for Each Scale ----------
recommendations = {
    "Time Competence": {
        1: "Practice mindfulness meditation to become more present.",
        2: "Incorporate breathing exercises into your daily routine.",
        3: "Maintain daily mindfulness practices for balance.",
        4: "Try advanced mindfulness techniques such as body scan meditation.",
        5: "Your time competence is excellent; consider sharing your practices with peers."
    },
    "Inner-Directed": {
        1: "Reflect on your personal values to strengthen your inner guidance.",
        2: "Keep a journal to connect with your inner voice.",
        3: "Maintain a balanced trust in your intuition.",
        4: "Enhance decision-making skills with structured self-reflection.",
        5: "Your inner-directedness is strong; consider mentoring others."
    },
    "Self-Actualizing Value": {
        1: "Explore personal development workshops to unlock your potential.",
        2: "Set modest goals and track your progress.",
        3: "Balance ambition with realistic planning.",
        4: "Engage in advanced personal growth activities.",
        5: "Your pursuit of self-actualization is inspiring; share your journey with others."
    },
    "Existentiality": {
        1: "Reflect on how you react to life’s challenges.",
        2: "Consider counseling or group discussions to explore existential concerns.",
        3: "Maintain a balanced approach to existential issues.",
        4: "Engage in philosophical readings and discussions.",
        5: "Your existential awareness is profound; consider guiding others."
    },
    "Feeling Reactivity": {
        1: "Practice emotional regulation techniques like deep breathing.",
        2: "Engage in mindfulness to better understand your emotions.",
        3: "Balance sensitivity with calmness through daily meditation.",
        4: "Participate in emotional intelligence training workshops.",
        5: "Your emotional sensitivity is an asset; share your insights with others."
    },
    "Spontaneity": {
        1: "Challenge yourself to act more freely in low-risk situations.",
        2: "Engage in activities that encourage spontaneous expression.",
        3: "Balance planning with spur-of-the-moment actions.",
        4: "Explore creative outlets to express your spontaneity.",
        5: "Your spontaneity is vibrant; consider creative leadership roles."
    }
}

# ---------- Create the Assessment Form ----------
with st.form(key="assessment_form"):
    st.markdown("<div class='glassy-container'>", unsafe_allow_html=True)
    name = st.text_input("Enter your full name")
    st.markdown("##### Rate the following statements on a scale from 1 (Not at all) to 5 (Very Much):")
    user_responses = {}
    for q in questions:
        user_responses[q["trait"]] = st.slider(q["question"], 1, 5, 3, key=q["trait"])
    submitted = st.form_submit_button("Submit Assessment")
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)  # End of Title/Description/Form Container

# ---------- Process and Display Results ----------
if submitted and name:
    st.success(f"Thank you, {name}! Your results are ready.")
    
    # Orientation Profile section
    st.markdown("<div class='glassy-container'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <h2 style="text-align:center;">{name}'s Orientation Profile</h2>
        <ul>
            {"".join([f"<li><strong>{trait}:</strong> {score}/5</li>" for trait, score in user_responses.items()])}
        </ul>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Therapeutic Recommendations section
    st.markdown("<div class='glassy-container'>", unsafe_allow_html=True)
    rec_html = "<h3 style='text-align:center;'>Therapeutic Recommendations</h3><ul>"
    for trait, score in user_responses.items():
        rec_html += f"<li><strong>{trait}:</strong> {recommendations[trait][score]}</li>"
    rec_html += "</ul>"
    st.markdown(rec_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Multicolored Bar Chart of Scores in a full-width glassy container
    st.markdown("<div class='full-width-glassy'>", unsafe_allow_html=True)
    df = pd.DataFrame({
        "Trait": list(user_responses.keys()),
        "Score": list(user_responses.values())
    })
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Trait:N", sort=None, title="Trait"),
        y=alt.Y("Score:Q", title="Score"),
        color=alt.Color("Score:Q", scale=alt.Scale(scheme="category10"))
    ).properties(width=700, height=400)
    st.altair_chart(chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- PDF Report Generation Function using FPDF (without chart image) ----------
    def generate_pdf_report(name, responses, recs, generated_on):
        pdf = FPDF()
        pdf.add_page()
        # Optional: Set a decorative background in the PDF (requires pdf_background.png)
        try:
            pdf.image("pdf_background.png", x=0, y=0, w=pdf.w, h=pdf.h)
        except Exception:
            pass
        # Draw a decorative border
        pdf.set_draw_color(180, 180, 180)
        pdf.rect(5, 5, pdf.w - 10, pdf.h - 10)
        
        # Header with black background and white text
        pdf.set_fill_color(0, 0, 0)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 15, f"{name}'s Orientation Report", ln=True, align="C", fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Generated on: {generated_on}", ln=True, align="C")
        pdf.ln(5)
        # Orientation Profile
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Orientation Profile:", ln=True)
        pdf.set_font("Arial", "", 12)
        for trait, score in responses.items():
            pdf.cell(0, 10, f"{trait}: {score}/5", ln=True)
        pdf.ln(5)
        # Therapeutic Recommendations
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Therapeutic Recommendations:", ln=True)
        pdf.set_font("Arial", "", 12)
        for trait, score in responses.items():
            pdf.multi_cell(0, 10, f"{trait}: {recs[trait][score]}")
        # Footer
        pdf.set_y(-20)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, "Developed by Kabura Kuria - Contact: +254 707 865 934", 0, 0, "C")
        pdf.ln(5)
        pdf.cell(0, 10, "© 2025", 0, 0, "C")
        return pdf.output(dest="S").encode("latin1")
    
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf_bytes = generate_pdf_report(name, user_responses, recommendations, generated_on)
    
    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=f"{name}_Assessment_{int(datetime.now().timestamp())}.pdf",
        mime="application/pdf"
    )

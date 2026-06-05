import streamlit as st
from PIL import Image
import google.generativeai as genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Architectural Prompt Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS — MINIMAL ORANGE / WHITE THEME
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

:root {
    --orange:       #E85D04;
    --orange-light: #FFF0E8;
    --orange-mid:   #FFDCCA;
    --white:        #FFFFFF;
    --off-white:    #FAFAF9;
    --border:       #E8E3DE;
    --text:         #1A1A1A;
    --text-soft:    #6B6560;
    --text-muted:   #A8A09A;
    --radius:       6px;
}

html, body, .stApp {
    background-color: var(--white) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }

.block-container {
    max-width: 1320px !important;
    padding: 2rem 2.5rem 4rem !important;
}

/* ----- Top bar ----- */
.topbar {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    border-bottom: 2px solid var(--orange);
    padding-bottom: 1rem;
    margin-bottom: 2.5rem;
}
.topbar-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}
.topbar-sub {
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 400;
}

/* ----- Section labels ----- */
.sec {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--orange);
    display: block;
    margin-bottom: 0.75rem;
}

/* ----- Rule line ----- */
.rule {
    height: 1px;
    background: var(--border);
    margin: 1.6rem 0;
}

/* ----- API key box ----- */

.api-status-ok {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.5rem;
    font-size: 11px;
    color: #2D7A3A;
}
.api-status-empty {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.5rem;
    font-size: 11px;
    color: var(--text-muted);
}

/* ----- Inputs ----- */
.stSelectbox label,
.stTextArea label,
.stTextInput label,
.stCheckbox label,
.stFileUploader label {
    font-size: 11px !important;
    font-weight: 500 !important;
    color: var(--text-soft) !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

.stSelectbox > div > div {
    background: var(--off-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,93,4,0.1) !important;
}

.stTextArea textarea {
    background: var(--off-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,93,4,0.1) !important;
    outline: none !important;
}

.stTextInput input {
    background: var(--off-white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-size: 13px !important;
}
.stTextInput input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px rgba(232,93,4,0.1) !important;
    outline: none !important;
}

.stCheckbox span {
    font-size: 13px !important;
    color: var(--text) !important;
    font-weight: 400 !important;
    text-transform: none !important;
    letter-spacing: normal !important;
}
.stCheckbox > div > label {
    text-transform: none !important;
    font-size: 13px !important;
    letter-spacing: normal !important;
}

.stFileUploader > div {
    background: var(--orange-light) !important;
    border: 1px dashed var(--orange-mid) !important;
    border-radius: var(--radius) !important;
}
.stFileUploader > div:hover {
    border-color: var(--orange) !important;
}
.stFileUploader p, .stFileUploader span {
    color: var(--text-soft) !important;
    font-size: 14px !important;
}

/* ----- Buttons ----- */
.stButton > button {
    width: 100% !important;
    background: var(--orange) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.25rem !important;
    transition: background 0.15s !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: #C94E00 !important;
}
.stButton > button:disabled {
    background: var(--border) !important;
    color: var(--text-muted) !important;
}

.stDownloadButton > button {
    width: 100% !important;
    background: transparent !important;
    color: var(--orange) !important;
    border: 1px solid var(--orange) !important;
    border-radius: var(--radius) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1.25rem !important;
    transition: background 0.15s !important;
    margin-top: 0.4rem !important;
}
.stDownloadButton > button:hover {
    background: var(--orange-light) !important;
}

/* ----- Image ----- */
.stImage img {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
}

/* ----- Output textarea ----- */
.stTextArea textarea[readonly] {
    background: var(--off-white) !important;
    color: var(--text-soft) !important;
    font-family: 'Courier New', monospace !important;
    font-size: 12px !important;
    line-height: 1.65 !important;
    border-color: var(--border) !important;
}

/* ----- Scrollbar ----- */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

[data-testid="column"] { padding: 0 0.6rem !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }

</style>
""", unsafe_allow_html=True)

# =========================================================
# TOPBAR
# =========================================================

st.markdown("""
<div class="topbar">
    <span class="topbar-title">Architectural Prompt Generator</span>
    <span class="topbar-sub">Image-specific prompts for architectural AI rendering</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LAYOUT
# =========================================================

col_left, col_right = st.columns([1, 1], gap="large")

# =========================================================
# LEFT — CONTROLS
# =========================================================

with col_left:

    # ----- 00 — API Key (inline) -----
    st.markdown('<span class="sec">00 — API Configuration</span>', unsafe_allow_html=True)
    st.markdown('<div class="api-box">', unsafe_allow_html=True)
    GEMINI_API_KEY = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter API key",
        help="Get your key at https://aistudio.google.com/app/apikey",
        label_visibility="collapsed"
    )
    if GEMINI_API_KEY:
        st.markdown("""
        <div class="api-status-ok">
            <span>●</span> <span>Key entered — ready to generate</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="api-status-empty">
            <span>○</span> <span>Enter your Gemini API key above &nbsp;·&nbsp; <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#E85D04; text-decoration:none;">Get one free ↗</a></span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # ----- 01 — Reference Image -----
    st.markdown('<span class="sec">01 — Reference Image</span>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">02 — Render Objective</span>', unsafe_allow_html=True)
    render_goal = st.selectbox(
        "Objective",
        [
            "Ultra Realistic Enhancement",
            "Generate Different Perspective",
            "Texture / Material Modification",
            "Luxury Upgrade",
            "Corporate Styling",
            "Minimal Styling",
            "Scandinavian Styling",
            "Industrial Styling",
            "Lighting Enhancement"
        ],
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">03 — Camera Settings</span>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        camera_type = st.selectbox("Camera Body", ["Sony A7R IV", "Canon EOS R5", "RED Komodo", "Nikon Z8"])
    with c2:
        lens_type = st.selectbox("Lens", ["16mm Ultra Wide", "24mm Architectural", "35mm Natural Perspective", "50mm Cinematic"])

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">04 — Perspective</span>', unsafe_allow_html=True)
    enable_perspective = st.checkbox("Enable Different Perspective Generation")
    perspective_instruction = ""
    custom_perspective = ""
    if enable_perspective:
        perspective_instruction = st.selectbox(
            "New Camera View",
            [
                "View From Left Corner", "View From Right Corner",
                "Wide Angle Entire Room", "Closer Human Eye Perspective",
                "View Facing Main Wall", "View Towards Seating Area",
                "View Towards Window", "Top Corner Perspective",
                "Low Angle Cinematic View", "Eye-Level Architectural Shot"
            ]
        )
        custom_perspective = st.text_input("Additional Perspective Instructions", placeholder="Example: Camera moved 2 meters backward")

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">05 — Lighting</span>', unsafe_allow_html=True)
    lighting_style = st.selectbox(
        "Lighting Style",
        ["Natural Daylight", "Warm Ambient", "Golden Hour", "Soft Luxury", "Cinematic", "Studio Lighting", "Evening Mood"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">06 — Texture / Material</span>', unsafe_allow_html=True)
    enable_texture_change = st.checkbox("Enable Texture / Material Changes")
    texture_instruction = ""
    if enable_texture_change:
        texture_instruction = st.text_area(
            "Texture Instructions",
            placeholder=(
                "Examples:\n"
                "- Replace flooring with Italian marble\n"
                "- Replace wall texture with oak veneer\n"
                "- Change sofa fabric to grey suede\n"
                "- Keep ceiling unchanged"
            ),
            height=130
        )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">07 — Preservation Rules</span>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        preserve_geometry  = st.checkbox("Preserve Exact Geometry",    value=True)
        preserve_layout    = st.checkbox("Preserve Furniture Layout",   value=True)
        preserve_materials = st.checkbox("Preserve Existing Materials", value=True)
    with p2:
        preserve_lighting       = st.checkbox("Preserve Existing Lighting", value=True)
        preserve_scene_identity = st.checkbox("Preserve Scene Identity",    value=True)

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">08 — Realism Quality</span>', unsafe_allow_html=True)
    realism_quality = st.selectbox(
        "Quality",
        ["Ultra Photorealistic", "Architectural Magazine Quality", "Luxury Interior Photography", "Competition Render Quality", "DSLR Realism"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    st.markdown('<span class="sec">09 — Hallucination Prevention</span>', unsafe_allow_html=True)
    custom_negative = st.text_area(
        "Additional Restrictions",
        placeholder=(
            "Examples:\n"
            "- Do not add extra furniture\n"
            "- Do not redesign ceiling\n"
            "- Do not add windows"
        ),
        height=110
    )

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

    # Determine button state and label
    if not uploaded_file and not GEMINI_API_KEY:
        btn_label = "Upload Image & Enter API Key"
        btn_disabled = True
    elif not uploaded_file:
        btn_label = "Upload an Image to Continue"
        btn_disabled = True
    elif not GEMINI_API_KEY:
        btn_label = "Enter API Key Above to Continue"
        btn_disabled = True
    else:
        btn_label = "Generate Prompt"
        btn_disabled = False

    generate_btn = st.button(btn_label, disabled=btn_disabled)

# =========================================================
# RIGHT — OUTPUT
# =========================================================

with col_right:

    st.markdown('<span class="sec">Prompt Output</span>', unsafe_allow_html=True)

    if not uploaded_file:
        st.markdown("""
        <div style="
            border: 1px dashed #E8E3DE;
            border-radius: 6px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: #A8A09A;
            font-size: 13px;
            line-height: 2;
            background: #FAFAF9;
        ">
            Upload a reference image<br>and configure the left panel.
        </div>
        """, unsafe_allow_html=True)

    elif not GEMINI_API_KEY:
        st.markdown("""
        <div style="
            border: 1px dashed #FFDCCA;
            border-radius: 6px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: #A8A09A;
            font-size: 13px;
            line-height: 2;
            background: #FFF0E8;
        ">
            Image uploaded.<br>
            Enter your <strong style="color:#E85D04;">Gemini API key</strong> in section 00 on the left.
        </div>
        """, unsafe_allow_html=True)

    elif generate_btn:

        genai.configure(api_key=GEMINI_API_KEY)
        vision_model = genai.GenerativeModel("gemini-2.5-flash")

        with st.spinner("Analyzing image..."):
            analysis_prompt = """
            Analyze this architectural/interior image carefully.

            STRICT RULES:
            - Be factual only
            - Do not hallucinate
            - Only describe visible elements
            - Do not assume hidden geometry

            Identify:
            - Room type
            - Architectural style
            - Furniture
            - Flooring
            - Wall materials
            - Ceiling design
            - Lighting setup
            - Camera perspective
            - Spatial layout
            - Material palette

            Keep response concise and structured.
            """
            response = vision_model.generate_content([analysis_prompt, image])
            scene_analysis = response.text

        perspective_block = ""
        if enable_perspective:
            perspective_block = f"""

---------------------------------------------------
PERSPECTIVE VIEW SYNTHESIS
---------------------------------------------------

Generate a new camera viewpoint of the SAME
existing physical space.

STRICT VIEW SYNTHESIS RULES:
- Preserve exact room geometry
- Preserve exact architecture
- Preserve exact furniture
- Preserve exact materials
- Preserve exact lighting fixtures
- Preserve exact object placement
- Preserve exact spatial proportions
- Preserve wall positions
- Preserve ceiling design
- Preserve flooring pattern

DO NOT:
- Add new furniture
- Remove furniture
- Change room dimensions
- Hallucinate hidden spaces
- Redesign architecture
- Modify textures unless instructed
- Change lighting layout
- Invent unseen areas
- Create conceptual reinterpretation

ONLY:
- Change camera viewpoint realistically
- Simulate physically possible camera movement
- Maintain same room identity

NEW CAMERA VIEW:
{perspective_instruction}

ADDITIONAL CAMERA INSTRUCTIONS:
{custom_perspective}

CAMERA BEHAVIOR:
- Physically accurate perspective
- DSLR architectural photography
- Realistic depth perception
- Consistent vanishing points
- Natural field of view
"""

        texture_block = ""
        if enable_texture_change:
            texture_block = f"""

---------------------------------------------------
TEXTURE / MATERIAL MODIFICATION
---------------------------------------------------

{texture_instruction}

STRICT MATERIAL RULES:
- Modify ONLY specified materials
- Preserve all other materials
- Maintain realistic texture scale
- Maintain realistic reflections
- Maintain physically accurate materials
- Preserve original architecture
"""

        negative_prompt = f"""

---------------------------------------------------
STRICT NEGATIVE PROMPT
---------------------------------------------------

Do not redesign the room.
Do not add decorative objects.
Do not add windows.
Do not change wall placement.
Do not change furniture count.
Do not alter material layout.
Do not create imaginary space.
Do not modify architecture.
Do not generate hidden rooms.
Do not stylize artistically.
Do not reinterpret design.
Maintain exact scene identity.

{custom_negative}
"""

        final_prompt = f"""
STRICT IMAGE-TO-IMAGE ARCHITECTURAL RENDERING PROMPT

===================================================
EXISTING IMAGE ANALYSIS
===================================================

{scene_analysis}

===================================================
RENDER OBJECTIVE
===================================================

{render_goal}

===================================================
CAMERA SETTINGS
===================================================

Camera:
{camera_type}

Lens:
{lens_type}

===================================================
LIGHTING SETTINGS
===================================================

Lighting Style:
{lighting_style}

===================================================
STRICT PRESERVATION RULES
===================================================

- Preserve Exact Geometry:
{preserve_geometry}

- Preserve Furniture Layout:
{preserve_layout}

- Preserve Existing Materials:
{preserve_materials}

- Preserve Existing Lighting:
{preserve_lighting}

- Preserve Scene Identity:
{preserve_scene_identity}

===================================================
REALISM TARGET
===================================================

{realism_quality}

- Ultra realistic
- DSLR-quality photography
- Architectural visualization quality
- Physically accurate lighting
- Realistic shadows
- Realistic reflections
- High dynamic range realism
- Realistic depth perception
- Cinematic architectural photography
- Ray-traced lighting behavior

{perspective_block}

{texture_block}

{negative_prompt}

===================================================
CRITICAL INSTRUCTIONS
===================================================

- Maintain architectural accuracy
- Maintain realistic proportions
- Preserve room dimensions
- Preserve scene continuity
- Preserve object consistency
- Preserve realistic material behavior
- Preserve realistic lighting physics
- Only apply explicitly requested modifications
"""

        st.text_area("Output", final_prompt, height=820, label_visibility="collapsed")

        # Copy button + Gemini link row
        import json
        escaped_prompt = json.dumps(final_prompt)
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-top:0.6rem; margin-bottom:0.2rem;">
            <button onclick="
                navigator.clipboard.writeText({escaped_prompt}).then(() => {{
                    this.textContent = '✓ Copied';
                    this.style.background = '#2D7A3A';
                    setTimeout(() => {{
                        this.textContent = 'Copy Prompt';
                        this.style.background = '#E85D04';
                    }}, 2000);
                }});
            " style="
                background: #E85D04;
                color: #fff;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                padding: 0.6rem 1.1rem;
                cursor: pointer;
                transition: background 0.15s;
                font-family: 'Inter', sans-serif;
            ">Copy Prompt</button>
            <a href="https://gemini.google.com" target="_blank" style="
                display: inline-flex;
                align-items: center;
                gap: 6px;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #E85D04;
                text-decoration: none;
                border: 1px solid #FFDCCA;
                border-radius: 6px;
                padding: 0.55rem 1rem;
                background: #FFF0E8;
                transition: background 0.15s;
            ">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z" fill="#E85D04"/>
                </svg>
                Open Google Gemini ↗
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "Download Prompt as .txt",
            final_prompt,
            file_name="architectural_prompt.txt"
        )

        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        word_count  = len(final_prompt.split())
        char_count  = len(final_prompt)
        block_count = 2 + (1 if enable_perspective else 0) + (1 if enable_texture_change else 0)

        for col, label, val in zip(
            [m1, m2, m3],
            ["Words", "Characters", "Active Blocks"],
            [word_count, char_count, block_count]
        ):
            with col:
                st.markdown(f"""
                <div style="text-align:center; padding:1rem 0.5rem;
                            border:1px solid #E8E3DE; border-radius:6px; background:#FAFAF9;">
                    <div style="font-size:1.5rem; font-weight:600; color:#E85D04; line-height:1;">{val}</div>
                    <div style="font-size:10px; letter-spacing:0.1em; text-transform:uppercase;
                                color:#A8A09A; margin-top:4px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="
            border: 1px dashed #E8E3DE;
            border-radius: 6px;
            padding: 3.5rem 2rem;
            text-align: center;
            color: #A8A09A;
            font-size: 13px;
            line-height: 2;
            background: #FAFAF9;
        ">
            Parameters configured.<br>
            Press <strong style="color:#E85D04;">Generate Prompt</strong> to continue.
        </div>
        """, unsafe_allow_html=True)

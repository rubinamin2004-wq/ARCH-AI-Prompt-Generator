import streamlit as st
from PIL import Image
import google.generativeai as genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Architectural Prompt Generator",
    layout="wide"
)

st.title("Architectural AI Prompt Generator")
st.write(
    "Generate strict image-specific prompts for architectural AI rendering."
)

# =========================================================
# API KEY
# =========================================================
# PASTE YOUR GEMINI API KEY HERE

GEMINI_API_KEY = "AIzaSyAmjoOIA00AXCKfAg19M4lK29D-Pnw1kZw"

# =========================================================
# IMAGE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Interior / Exterior Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns([1, 1])

    with col1:

        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

    # =====================================================
    # MAIN OBJECTIVE
    # =====================================================

    st.subheader("1. Render Objective")

    render_goal = st.selectbox(
        "Select Objective",
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
        ]
    )

    # =====================================================
    # CAMERA SETTINGS
    # =====================================================

    st.subheader("2. Camera Settings")

    camera_type = st.selectbox(
        "Camera",
        [
            "Sony A7R IV",
            "Canon EOS R5",
            "RED Komodo",
            "Nikon Z8"
        ]
    )

    lens_type = st.selectbox(
        "Lens",
        [
            "16mm Ultra Wide",
            "24mm Architectural",
            "35mm Natural Perspective",
            "50mm Cinematic"
        ]
    )

    # =====================================================
    # PERSPECTIVE CONTROL
    # =====================================================

    st.subheader("3. Perspective View Synthesis")

    enable_perspective = st.checkbox(
        "Enable Different Perspective Generation"
    )

    perspective_instruction = ""

    if enable_perspective:

        perspective_instruction = st.selectbox(
            "Select New Camera View",
            [
                "View From Left Corner",
                "View From Right Corner",
                "Wide Angle Entire Room",
                "Closer Human Eye Perspective",
                "View Facing Main Wall",
                "View Towards Seating Area",
                "View Towards Window",
                "Top Corner Perspective",
                "Low Angle Cinematic View",
                "Eye-Level Architectural Shot"
            ]
        )

        custom_perspective = st.text_input(
            "Additional Perspective Instructions",
            placeholder="Example: Camera moved 2 meters backward"
        )

    else:

        custom_perspective = ""

    # =====================================================
    # LIGHTING
    # =====================================================

    st.subheader("4. Lighting")

    lighting_style = st.selectbox(
        "Lighting Style",
        [
            "Natural Daylight",
            "Warm Ambient",
            "Golden Hour",
            "Soft Luxury",
            "Cinematic",
            "Studio Lighting",
            "Evening Mood"
        ]
    )

    # =====================================================
    # TEXTURE / MATERIAL CONTROL
    # =====================================================

    st.subheader("5. Texture / Material Modification")

    enable_texture_change = st.checkbox(
        "Enable Texture / Material Changes"
    )

    texture_instruction = ""

    if enable_texture_change:

        texture_instruction = st.text_area(
            "Texture Instructions",
            placeholder="""
Examples:

- Replace flooring with Italian marble
- Replace wall texture with oak veneer
- Change sofa fabric to grey suede
- Replace countertop with black granite
- Keep ceiling unchanged
"""
        )

    # =====================================================
    # STRICT PRESERVATION
    # =====================================================

    st.subheader("6. Strict Preservation Rules")

    preserve_geometry = st.checkbox(
        "Preserve Exact Geometry",
        value=True
    )

    preserve_layout = st.checkbox(
        "Preserve Furniture Layout",
        value=True
    )

    preserve_materials = st.checkbox(
        "Preserve Existing Materials",
        value=True
    )

    preserve_lighting = st.checkbox(
        "Preserve Existing Lighting",
        value=True
    )

    preserve_scene_identity = st.checkbox(
        "Preserve Scene Identity",
        value=True
    )

    # =====================================================
    # REALISM SETTINGS
    # =====================================================

    st.subheader("7. Realism Settings")

    realism_quality = st.selectbox(
        "Realism Quality",
        [
            "Ultra Photorealistic",
            "Architectural Magazine Quality",
            "Luxury Interior Photography",
            "Competition Render Quality",
            "DSLR Realism"
        ]
    )

    # =====================================================
    # NEGATIVE PROMPT
    # =====================================================

    st.subheader("8. Hallucination Prevention")

    custom_negative = st.text_area(
        "Additional Restrictions",
        placeholder="""
Examples:

- Do not add extra furniture
- Do not redesign ceiling
- Do not add windows
- Do not modify architecture
"""
    )

    # =====================================================
    # GENERATE PROMPT
    # =====================================================

    if st.button("Generate Prompt"):

        # ================================================
        # API ONLY CALLED HERE
        # ================================================

        genai.configure(api_key=GEMINI_API_KEY)

        vision_model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        with st.spinner("Analyzing Image..."):

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

            response = vision_model.generate_content(
                [
                    analysis_prompt,
                    image
                ]
            )

            scene_analysis = response.text

        # =================================================
        # PERSPECTIVE BLOCK
        # =================================================

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

        # =================================================
        # TEXTURE BLOCK
        # =================================================

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

        # =================================================
        # NEGATIVE PROMPT
        # =================================================

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

        # =================================================
        # FINAL PROMPT
        # =================================================

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

        with col2:

            st.subheader("Generated Prompt")

            st.text_area(
                "Prompt",
                final_prompt,
                height=850
            )

            st.download_button(
                "Download Prompt",
                final_prompt,
                file_name="architectural_prompt.txt"
            )
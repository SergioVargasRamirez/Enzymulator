import streamlit as st


def tab_controls(label):
    st.subheader(f"{label} Controls")

    col1, col2, col3 = st.columns(3)

    # Defaults (used only for first render)
    defaults = {
        "temperature": 37,
        "pH": 7.0,
        "enzyme_count": 10,
        "substrate_count": 100,
        "inhibitor": 0
    }

    # ---------------------------------------------------
    # Sliders
    # ---------------------------------------------------
    with col1:
        temperature = st.slider(
            "Temp (°C)",
            0, 100,
            value=defaults["temperature"],
            key=f"temperature_{label}"
        )

        pH = st.slider(
            "pH",
            0.0, 14.0,
            value=defaults["pH"],
            key=f"pH_{label}"
        )

    with col2:
        enzyme_count = st.slider(
            "Enzymes",
            1, 50,
            value=defaults["enzyme_count"],
            key=f"enzyme_{label}"
        )

        substrate_count = st.slider(
            "Substrates",
            10, 500,
            value=defaults["substrate_count"],
            key=f"substrate_{label}"
        )

    inhibitor = 0
    if label != "No Inhibitor":
        with col3:
            inhibitor = st.slider(
                "Inhibitor",
                0, 100,
                value=defaults["inhibitor"],
                key=f"inhibitor_{label}"
            )

    # ---------------------------------------------------
    # Buttons
    # ---------------------------------------------------
    start_key = f"start_{label}"

    if start_key not in st.session_state:
        st.session_state[start_key] = False

    if st.button("Start", key=f"start_btn_{label}"):
        st.session_state[start_key] = True

    clean_pressed = st.button("Clean Screen", key=f"clean_{label}")

    return {
        "temperature": temperature,
        "pH": pH,
        "enzyme_count": enzyme_count,
        "substrate_count": substrate_count,
        "inhibitor": inhibitor,
        "start": st.session_state[start_key],
        "clean": clean_pressed,
    }


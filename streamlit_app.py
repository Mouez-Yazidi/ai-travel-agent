"""
AI Travel Agent — Streamlit App
Run with:
    streamlit run streamlit_app.py
"""

import streamlit as st


# --------------------------------------------------
# AGENT EXECUTION
# --------------------------------------------------

def run_agent(city: str):
    """Run the LangGraph travel agent."""
    from graph import app
    return app.invoke({"city": city})


# --------------------------------------------------
# CLEAN MODEL OUTPUT (REMOVE THINKING / REASONING)
# --------------------------------------------------

def clean_agent_output(result: dict) -> dict:
    """
    Remove any internal reasoning fields returned by the model.
    Only keep fields required by the UI.
    """

    return {
        "attractions": result.get("attractions", []),
        "weather": result.get("weather", ""),
        "itinerary": result.get("itinerary", "")
    }


# --------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------

def main():

    st.set_page_config(
        page_title="AI Travel Agent",
        page_icon="✈️",
        layout="centered"
    )

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    st.title("✈️ AI Travel Agent")

    st.caption(
        "Discover attractions, check the weather, and generate a smart "
        "1-day itinerary for any city using an AI agent."
    )

    st.divider()

    # --------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------

    with st.sidebar:

        st.header("About")

        st.write(
            "This application uses a **LangGraph AI agent** that:"
        )

        st.markdown(
            """
- 🧠 Suggests attractions using an LLM  
- 🌤️ Retrieves live weather data  
- 📅 Generates a full 1-day itinerary
"""
        )

        st.divider()

        st.subheader("Quick cities")

        if st.button("🇹🇳 Tunis", use_container_width=True):
            st.session_state.city = "Tunis"

        if st.button("🇫🇷 Paris", use_container_width=True):
            st.session_state.city = "Paris"

        if st.button("🇯🇵 Tokyo", use_container_width=True):
            st.session_state.city = "Tokyo"

        if st.button("🇺🇸 New York", use_container_width=True):
            st.session_state.city = "New York"

    # --------------------------------------------------
    # CITY INPUT
    # --------------------------------------------------

    if "city" not in st.session_state:
        st.session_state.city = "Tunis"

    city = st.text_input(
        "Enter a city",
        value=st.session_state.city,
        placeholder="Example: Rome, Dubai, Barcelona"
    ).strip()

    st.session_state.city = city

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        generate = st.button(
            "🚀 Generate Travel Plan",
            use_container_width=True
        )

    if not generate:
        st.info("Enter a city and click **Generate Travel Plan**.")
        return

    # --------------------------------------------------
    # RUN AGENT
    # --------------------------------------------------

    with st.spinner("🔎 AI is preparing your travel plan..."):

        try:

            raw_result = run_agent(city)

            result = clean_agent_output(raw_result)

        except ValueError as e:

            st.error(str(e))
            st.caption("Make sure your API keys are configured in `.env`.")
            return

        except Exception as e:

            st.error(f"Unexpected error: {e}")
            return

    st.divider()

    st.header(f"🗺️ Travel Plan for {city}")

    # --------------------------------------------------
    # ATTRACTIONS
    # --------------------------------------------------

    attractions = result["attractions"]

    if attractions:

        st.subheader("📍 Top Attractions")

        for i, place in enumerate(attractions, 1):
            st.write(f"**{i}.** {place}")

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    weather = result["weather"]

    if weather:

        st.subheader("🌤️ Weather Overview")

        st.success(weather)

    # --------------------------------------------------
    # ITINERARY
    # --------------------------------------------------

    itinerary = result["itinerary"]

    if itinerary:

        st.subheader("📅 Suggested 1-Day Itinerary")

        with st.expander("View itinerary", expanded=True):
            st.write(itinerary)

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.divider()

    st.caption(
        "Built with **LangGraph + Streamlit + OpenWeather API**"
    )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    main()
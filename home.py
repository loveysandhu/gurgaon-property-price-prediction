import streamlit as st

st.set_page_config(
    page_title="Gurgaon Property Intelligence",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Gurgaon Property Intelligence")

st.markdown("""
### Find the Right Property with Confidence

Whether you're looking to estimate a property's value, explore the Gurgaon real estate market,
or discover similar properties, this platform brings everything together in one place.
""")

st.divider()

st.header("What would you like to do today?")

col1, col2, col3 = st.columns(3)

with col1:
    st.container(border=True)

    st.subheader("💰 Predict Property Price")

    st.write("""
Enter the property details to get an estimated market price along with an expected price range.
""")

with col2:
    st.container(border=True)

    st.subheader("📊 Explore Market Trends")

    st.write("""
View different charts and visualizations to better understand Gurgaon property prices and market patterns.
""")

with col3:
    st.container(border=True)

    st.subheader("🏡 Find Similar Properties")

    st.write("""
Search properties based on your preferred location, budget and BHK, then discover similar options nearby.
""")

st.divider()

st.header("How it works")

st.markdown("""
- **Price Predictor** → Estimate the value of a property.

- **Analysis** → Explore market trends through interactive charts.

- **Recommendation** → Find properties that match your preferences and discover similar alternatives.
""")

st.divider()

st.info("""
👈 Use the navigation menu on the left to switch between different modules.
""")

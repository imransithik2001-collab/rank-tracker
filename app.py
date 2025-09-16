import streamlit as st
import pandas as pd
from serpapi import GoogleSearch
from time import sleep

# ----------------------------
# Function to fetch rankings
# ----------------------------
def get_google_rank(keyword, domain, api_key, country="in", lang="en"):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": api_key,
        "gl": country,  # Country code
        "hl": lang,     # Language
        "num": 100,     # Top 100 results
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])

        for idx, result in enumerate(organic_results, start=1):
            link = result.get("link", "")
            if domain in link:
                return idx
        return "Not in top 100"
    except Exception as e:
        return f"Error: {e}"


# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Google Rank Tracker", page_icon="📊", layout="wide")
st.title("📊 Google SERP Rank Tracker (via SerpAPI)")

st.markdown("""
Enter your **SerpAPI key**, keywords to track, and the domain you want to monitor.
The app will check Google rankings (top 100 results) and display your keyword positions.
""")

# API Key Input
api_key = st.text_input("🔑 Enter your SerpAPI API Key:", type="password")

# Domain Input
domain = st.text_input("🌐 Enter the target domain:", placeholder="example.com")

# Keywords Input
keywords_input = st.text_area(
    "📝 Enter keywords (comma or newline separated):",
    placeholder="keyword 1\nkeyword 2\nkeyword 3"
)
keywords = [kw.strip() for kw in keywords_input.replace(",", "\n").split("\n") if kw.strip()]

# Run tracker
if st.button("🚀 Check Rankings"):
    if not api_key or not domain or not keywords:
        st.warning("⚠️ Please provide API key, domain, and at least one keyword.")
    else:
        results = []
        progress = st.progress(0)

        for i, keyword in enumerate(keywords):
            position = get_google_rank(keyword, domain, api_key)
            results.append({"Keyword": keyword, "Rank Position": position})
            sleep(1)  # Prevent hitting SerpAPI limits
            progress.progress((i + 1) / len(keywords))

        df = pd.DataFrame(results)
        st.success("✅ Ranking check complete!")
        st.dataframe(df, use_container_width=True)

        # Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "rankings.csv", "text/csv")

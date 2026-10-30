import streamlit as st
import pandas as pd

st.set_page_config(page_title="English Grammar Assistant", page_icon="📚")

st.title("📚 English Grammar Assistant")
st.write("Check your grammar, learn from mistakes and practice!")

data = pd.read_csv("grammar_data.csv")

# Memory
if "mistakes" not in st.session_state:
    st.session_state.mistakes = {}
if "checked" not in st.session_state:
    st.session_state.checked = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0

# Practice questions
practice = {
    "Subject-Verb Agreement": [
        ("She ___ to school every day.", ["go", "goes", "going"], "goes"),
        ("He ___ cricket every day.", ["play", "plays", "playing"], "plays"),
        ("She ___ a book.", ["have", "has", "having"], "has"),
        ("They ___ football.", ["play", "plays", "playing"], "play"),
        ("He ___ chocolate.", ["like", "likes", "liking"], "likes")
    ],

    "Tense": [
        ("I ___ to school yesterday.", ["go", "went", "going"], "went"),
        ("She ___ there yesterday.", ["go", "went", "goes"], "went"),
        ("He ___ last week.", ["go", "went", "goes"], "went"),
        ("They ___ the movie yesterday.", ["watch", "watched", "watching"], "watched"),
        ("I ___ my homework last night.", ["finish", "finished", "finishing"], "finished")
    ],

    "Articles": [
        ("I have ___ apple.", ["a", "an", "the"], "an"),
        ("He is ___ student.", ["a", "an", "the"], "a"),
        ("She is ___ teacher.", ["a", "an", "the"], "a"),
        ("I saw ___ elephant.", ["a", "an", "the"], "an"),
        ("He bought ___ book.", ["a", "an", "the"], "a")
    ],

    "Common Word Mistake": [
        ("He ___ like tea.", ["don't", "doesn't", "didn't"], "doesn't"),
        ("She ___ play tennis.", ["don't", "doesn't", "didn't"], "doesn't"),
        ("They ___ a car.", ["have", "has", "having"], "have"),
        ("I ___ a pen.", ["has", "have", "having"], "have"),
        ("We ___ two books.", ["has", "have", "having"], "have")
    ]
}

tab1, tab2, tab3 = st.tabs(
    ["🔍 Grammar Checker", "📝 Practice", "📊 My Report"]
)

# ---------------- GRAMMAR CHECKER ----------------

with tab1:

    st.subheader("Check Your Sentence")

    sentence = st.text_input(
        "Enter a sentence:",
        placeholder="Example: She go to school every day."
    )

    if st.button("Check Grammar"):

        if sentence.strip() == "":
            st.warning("Please enter a sentence.")

        else:
            st.session_state.checked += 1

            clean = sentence.lower().strip().rstrip(".!?")
            clean = " ".join(clean.split())

            data["Clean"] = data["Wrong Sentence"].str.lower().str.strip().str.rstrip(".!?")

            result = data[data["Clean"] == clean]

            if len(result) > 0:

                row = result.iloc[0]

                st.error("❌ Grammar mistake found!")
                st.write("**Correct sentence:**", row["Correct Sentence"])
                st.info("Mistake: " + row["Mistake Type"])
                st.write("Explanation:", row["Explanation"])

                mistake = row["Mistake Type"]

                st.session_state.mistakes[mistake] = \
                    st.session_state.mistakes.get(mistake, 0) + 1

            else:
                st.success("✅ No mistake found in our dataset!")
                st.session_state.correct += 1

# ---------------- PRACTICE ----------------

with tab2:

    st.subheader("📝 Personalized Practice")

    if not st.session_state.mistakes:

        st.info("Check some sentences first to unlock practice.")

    else:

        st.write("### Your Weak Areas")

        for topic, count in st.session_state.mistakes.items():
            st.write("• " + topic + " — " + str(count) + " mistake(s)")

        topics = list(st.session_state.mistakes.keys())

        topic = st.selectbox(
            "Choose a topic to practice:",
            topics
        )

        questions = practice[topic]

        st.write("### Practice: " + topic)

        answers = []

        for i, q in enumerate(questions):

            st.write("**Q" + str(i + 1) + ". " + q[0] + "**")

            answer = st.radio(
                "Choose:",
                q[1],
                key="q" + str(i)
            )

            answers.append(answer)

        if st.button("Submit Practice"):

            score = 0

            for i in range(5):
                if answers[i] == questions[i][2]:
                    score += 1

            st.success(
                "🎯 Your Score: " + str(score) + " / 5"
            )

            if score == 5:
                st.balloons()
                st.write("🏆 Excellent! You mastered this topic!")
            elif score >= 3:
                st.write("👏 Good job! Keep practicing.")
            else:
                st.write("📚 Keep practicing this topic.")

# ---------------- REPORT ----------------

with tab3:

    st.subheader("📊 My Grammar Report")

    total = st.session_state.checked
    mistakes = sum(st.session_state.mistakes.values())

    if total == 0:

        st.info("Check some sentences to see your report.")

    else:

        score = int(
            st.session_state.correct / total * 100
        )

        st.metric("Grammar Score", str(score) + "%")
        st.metric("Sentences Checked", total)
        st.metric("Total Mistakes", mistakes)

        if mistakes > 0:

            st.write("### Mistake History")

            for topic, count in st.session_state.mistakes.items():
                st.write(
                    "• " + topic + ": " + str(count)
                )

    if st.button("🗑️ Reset Progress"):

        st.session_state.mistakes = {}
        st.session_state.checked = 0
        st.session_state.correct = 0

        st.rerun()

st.divider()

st.caption("English Grammar Assistant | Learn from your mistakes!")
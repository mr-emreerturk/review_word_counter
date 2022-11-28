import streamlit as st
import pandas as pd
from PIL import Image

### --- Define Functions
def flat(lis):
    flatList = []
    # Iterate with outer list
    for element in lis:
        if type(element) is list:
            # Check if type is list than iterate through the sublist
            for item in element:
                flatList.append(item)
        else:
            flatList.append(element)
    return flatList


def create_csv_most_common_words(number_of_words: int, data, column_name: str):
    mask_list = []
    mask_series = data[column_name].dropna().reset_index(drop=True)
    for x in range(0, len(mask_series)):
        mask = mask_series[x].split()
        mask_list.append(mask)

    list_of_words = flat(mask_list)

    from collections import Counter

    counter = Counter(list_of_words)
    result = counter.most_common(number_of_words)

    complete_list = pd.DataFrame(result)  # .to_csv("results_copymining")
    return complete_list


def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


### --- SET CONFIGURATION
st.set_page_config(
    page_title="Copymining Review Word Counter",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

### --- CREATE SIDEBAR
with st.sidebar:
    logo = "https://raw.githubusercontent.com/mr-emreerturk/review_word_counter/master/streamlit_app/emf_media_logo.png"
    st.image(logo, output_format="png")
    st.header("The App")
    st.markdown(
        """
    This app has one purpose: Count all reviews, and 
    return a list of the most used words for your copymining process
    """
    )
    st.header("How to use:")
    st.markdown(
        """
    1. Clean your import. Set the columnheader of the reviews to "review"
    2. Select the language of the reviews
    3. Drop the cleaned csv into the field
    4. Download the sorted list (also csv)
    5. Import the list to your Copy Mining sheet
    """
    )
    st.header("Tutorial")

st.title("Review Word Counter")
try:
    ### --- Step 1: upload file
    st.header("Step 1: Drop your file here:")
    uploaded_file = st.file_uploader(
        label="Drag and Drop your File here",
        accept_multiple_files=False,
        help="Upload your cleaned file here. Make sure adhere to cleaning standards in the tutorial.",
    )

    ### --- Step 2: Choose amount of words
    st.header("Step 2: Choose how many words you want?")
    number_of_words = st.slider(
        label="How many words do you want to count?",
        min_value=100,
        max_value=5000,
        step=100,
    )
    ### --- Step 3: Name of column
    st.header("Step 3: What is the name of the review column")
    column_name = st.text_input("What is the column name of the review column?")

    data = pd.read_csv(uploaded_file)
    most_common_words = create_csv_most_common_words(
        number_of_words, data=data, column_name=column_name
    )

    data_csv = convert_df(most_common_words)
    most_common_words = most_common_words.rename(
        {0: "word", 1: "# occurrance"}, axis="columns"
    )

    unimportant_words = [
        "et",
        "de",
        "le",
        "!",
        "est",
        "à",
        "les",
        "je",
        "la",
        "très",
        "pas",
        "pour",
        "un",
        "Je",
        "en",
        "que",
        "ne",
        "suis",
        "du",
        "plus",
        "qui",
        "une",
        "Le",
        "des",
        "sur",
        "mais",
        "ce",
        "au",
        "mes",
        "il",
        "avec",
        "a",
        "mon",
        "sont",
        "ce",
        "au",
        "mes",
        "il",
        "avec",
        "a",
        "mon",
        "sont",
        "the",
        "be",
        "to",
        "of",
        "and",
        "a",
        "in",
        "that",
        "have",
        "I",
        "it",
        "for",
        "not",
        "on",
        "with",
        "he",
        "as",
        "you",
        "do",
        "at",
        "this",
        "but",
        "his",
        "by",
        "from",
        "they",
        "we",
        "say",
        "her",
        "she",
        "or",
        "an",
        "will",
        "my",
        "one",
        "all",
        "would",
        "there",
        "their",
        "what",
        "so",
        "up",
        "out",
        "if",
        "about",
        "who",
        "get",
        "which",
        "go",
        "me",
        "when",
        "make",
        "can",
        "like",
        "time",
        "no",
        "just",
        "him",
        "know",
        "take",
        "into",
        "year",
        "your",
        "some",
        "could",
        "them",
        "see",
        "other",
        "than",
        "then",
        "now",
        "only",
        "come",
        "its",
        "over",
        "also",
        "back",
        "after",
        "use",
        "two",
        "how",
        "our",
        "way",
        "even",
        "want",
        "because",
        "any",
        "these",
        "give",
        "day",
        "most",
        "us",
    ]
    most_common_words = most_common_words[
        ~most_common_words.word.isin(unimportant_words)
    ].reset_index(drop=True)

    button = st.download_button(
        "Press to Download",
        data_csv,
        "review_word_count.csv",
        "text/csv",
        key="download-csv",
    )
    if button:
        st.balloons()

except ValueError:
    pass
except KeyError:
    st.warning(
        "Don't forget Step 2. Write the correct column header for the reviews in the input box.\n Check the name of your columns in your sheet.",
        icon="⚠️",
    )

st.header("Preview")
try:
    st.dataframe(most_common_words, use_container_width=True)
except NameError:
    st.info(
        "Please go through steps 1 - 3",
        icon="ℹ️",
    )

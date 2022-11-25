import streamlit as st
import pandas as pd

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


def create_csv_most_common_words(number_of_words, data):
    mask_list = []
    mask_series = data.review.dropna().reset_index(drop=True)
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
    page_title="Crypto Price & Dev App",
    page_icon="💰",
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
    col1, col2 = st.columns(2)
    with col1:
        number_of_words = st.slider(
            label="How many words do you want to count?",
            min_value=100,
            max_value=5000,
            step=100,
        )
    with col2:
        uploaded_file = st.file_uploader(
            label="Drag and Drop your File here",
            accept_multiple_files=False,
            help="Upload your cleaned file here. Make sure adhere to cleaning standards in the tutorial.",
        )

    data = pd.read_csv(uploaded_file)
    most_common_words = create_csv_most_common_words(number_of_words, data=data)
    st.write(most_common_words)

    data_csv = convert_df(most_common_words)
    st.download_button(
        "Press to Download", data_csv, "file.csv", "text/csv", key="download-csv"
    )
except ValueError:
    pass

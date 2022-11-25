import pandas as pd

def read_csv(file):
    data = pd.read_csv(f"{file}")
    return data

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

def create_csv_most_common_words(number_of_words, data = read_csv):
    mask_list = []
    mask_series = data.review.dropna().reset_index(drop=True)
    for x in range(0, len(mask_series)):
        mask = mask_series[x].split()
        mask_list.append(mask)

    list_of_words = flat(mask_list)

    from collections import Counter
    counter = Counter(list_of_words)
    result = counter.most_common(number_of_words)

    complete_list = pd.DataFrame(result).to_csv("results_copymining")
    return complete_list
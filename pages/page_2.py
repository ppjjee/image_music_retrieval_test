import streamlit as st
import os, glob, pathlib, pickle, random, commons, json
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter
# import tensorflow
# import sklearn
# import cv2
from PIL import Image
from tqdm import tqdm
# from tensorflow.python.client import device_lib
# from tensorflow.keras import applications
# from tensorflow.keras import layers
# from tensorflow.keras import losses
# from tensorflow.keras import optimizers
# from tensorflow.keras import metrics
# from tensorflow.keras import Model
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras import applications
# from tensorflow.keras.applications.efficientnet import EfficientNetB1, preprocess_input



def TagLoad(path):
    f = open(path)
    data = json.load(f)
    a = data['submits'][-1]['Change Tag1'] # 제일 마지막 저장된 Tag 정보 불러옴
    c_tag1 = list(a.split(" "))
    b = data['submits'][-1]['Change Tag2']
    c_tag2 = list(b.split(" "))
    c = data['submits'][-1]['Change Tag3']
    c_tag3 = list(c.split(" "))
    c_tags = []
    c_tags.append(c_tag1)
    c_tags.append(c_tag2)
    c_tags.append(c_tag3) # c_tags = [['calm'], ['advertising']]

    def flatten_list(_2d_list):
        flat_list = []
        # Iterate through the outer list
        for element in _2d_list:
            if type(element) is list:
                # If the element is of type list, iterate through the sublist
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        return flat_list

    f_tags = flatten_list(c_tags)     #f_tags = ['calm', 'advertising']
    print(f_tags, 'f_tags is')
    list_set = set(f_tags) # ['calm', 'advertising', 'calm] 일 경우, ['calm', 'advertising']
    final_tag = list(list_set)
    final_tag[:] = (value for value in final_tag if value != "-") # ['-']는 제외함
    return final_tag




input_file = '/nas2/epark/mtg-jamendo-dataset/data/autotagging_moodtheme.tsv'
tracks, tags, extra = commons.read_file(input_file)


find_tag_list = []
path = st.experimental_get_query_params()['path'][0]
print("path: " + path)
final_tag = TagLoad(path)

for i in final_tag:
    p = tags['mood/theme'][i]

    print("p is tags['mood/theme'][i]", p)

    q = list(p)
    find_tag_list.append(q)
    print('find_tag_list', find_tag_list)
    
if len(find_tag_list) == 3:
    a, b, c = find_tag_list
    elements_in_all = list(set.intersection(*map(set, [a, b, c])))
    elements_in_two = list(set.intersection(*map(set, [a, b])))
    elements_in_two_2nd = list(set.intersection(*map(set, [b, c])))
    elements_in_two_3rd = list(set.intersection(*map(set, [a, b])))
    elements_in_one = a
    
    if len(elements_in_all) !=0 and len(elements_in_all) >= 5:
        random_all = random.choices(elements_in_all, k=5)
    elif len(elements_in_all) == 0 and len(elements_in_two) != 0  and len(elements_in_two) >= 5:
        random_all = random.choices(elements_in_two, k=5)
    elif len(elements_in_all) ==0 and len(elements_in_two) ==0 and len(elements_in_two_2nd) >= 5:
        random_all = random.choices(elements_in_two_2nd, k=5)
    elif len(elements_in_all) ==0 and len(elements_in_two) ==0 and len(elements_in_two_2nd) ==0 and len(elements_in_two_3rd) >=5:
        random_all = random.choices(elements_in_two_3rd, k=5)
    else:
        random_all = random.choices(elements_in_one, k=5)

    
elif len(find_tag_list) == 2:
    a, b = find_tag_list
    elements_in_all = list(set.intersection(*map(set, [a, b])))
    elements_in_one = a
    elements_in_one_2nd = b
    
    if len(elements_in_all) !=0 and len(elements_in_all) >= 5:
        random_all = random.choices(elements_in_all, k=5)
    elif len(elements_in_all) == 0 and len(elements_in_one) >= 5:
        random_all = random.choices(elements_in_one, k=5)
    else: 
        random_all = random.choices(elements_in_one, k=5)

    
else:
    a = find_tag_list
    elements_in_all = a
    random_all = random.choices(elements_in_all, k=5)




music_tags = st.container()
with music_tags: # 자동으로 매칭된 오디오 리스트가 보이도록 변경 필요
    st.subheader("Now, we recommend a music list that matches the image!")
    st.text("🎧 Please enjoy the music and answer the questions below. 🎧")

    audio_file1 = open('/nas3/epark/workspace/retreival/music_data/mp3/' + str(random_all[0]) + '.mp3', 'rb')
    audio_bytes1 = audio_file1.read()
    st.audio(audio_bytes1, format='audio/ogg', start_time=0)

    audio_file2 = open('/nas3/epark/workspace/retreival/music_data/mp3/' + str(random_all[1]) + '.mp3', 'rb')
    audio_bytes2 = audio_file2.read()
    st.audio(audio_bytes2, format='audio/ogg', start_time=0)  

    audio_file3 = open('/nas3/epark/workspace/retreival/music_data/mp3/' + str(random_all[2]) + '.mp3', 'rb')
    audio_bytes3 = audio_file3.read()
    st.audio(audio_bytes3, format='audio/ogg', start_time=0)

    audio_file4 = open('/nas3/epark/workspace/retreival/music_data/mp3/' + str(random_all[3]) + '.mp3', 'rb')
    audio_bytes4 = audio_file4.read()
    st.audio(audio_bytes4, format='audio/ogg', start_time=0)

    audio_file5 = open('/nas3/epark/workspace/retreival/music_data/mp3/' + str(random_all[4]) + '.mp3', 'rb')
    audio_bytes5 = audio_file5.read()
    st.audio(audio_bytes5, format='audio/ogg', start_time=0)

    satis_result = st.slider('Do you satisfy with the recommended music?', min_value=0, max_value=100, value=50, step=1)


# save all submit
with st.form('Music_1'):
    submitted = st.form_submit_button('SUBMIT')
    print(submitted,"3")
    if submitted:
        result = {'Music Satisfaction': satis_result}
        with open(path, "r") as json_file:
            data = json.load(json_file)
        data['submits'][-1].update(result)

        with open(path, "w") as save_f:
            json.dump(data, save_f, ensure_ascii=False, indent=4)
            print("exists, after", data)
        st.info('**The submission is successfully uploaded.**')


    

# 클릭 하면 다음 페이지 넘어가도록 만들어야 함!


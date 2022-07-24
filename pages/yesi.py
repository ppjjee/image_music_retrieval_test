# load libraries
import streamlit as st
from st_clickable_images import clickable_images
import os, glob, pathlib, random, pickle, time, requests, json
import io
from io import StringIO, BytesIO
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import sklearn
import cv2
from PIL import Image
from tqdm import tqdm
import tensorflow 
from tensorflow.python.client import device_lib
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import optimizers
from tensorflow.keras import metrics
from tensorflow.keras import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras import applications
from tensorflow.keras.applications.efficientnet import EfficientNetB1, preprocess_input
import uuid

# set remove keras messages
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

# set GPU for keras version
os.environ['CUDA_VISIBLE_DEVICES']='7'
physical_devices = tensorflow.config.list_physical_devices('GPU')
# print('physical_device:', physical_devices)
try:
    tensorflow.config.experimental.set_visible_devices(physical_devices[0], 'GPU')
    tensorflow.config.experimental.set_memory_growth(physical_devices[0], True)
except RuntimeError as e:
    print(e)

def get_result_dir():
    path = os.getcwd() + "/results"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    print("created result dir: " + path)
    return path


st.cache(persist=True)
def main():
    # show frontend title 
    st.title('Image to Music Retrieval')
    st.text("✔️ Please select an image! We recommend music that matches the selected image.")
    st.text("✔️ After selecting an image, please wait for a while until the next process.")
    # show imgs to be selected    
    selection = st.container()
    with selection:
        model_load_state = st.info('👉 Loooooooooooooooooooaaaaaaaaaaaaaaaaaaaading... 👀')
        try:
            imgs = [
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/calm.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fun_summer_holiday.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fun.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fun_sport_children.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/fun_summer_holiday.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/funny.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/love.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/love_relaxing_sad.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/melodic_party.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/movie_background_film.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/nature.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/nature_calm_summer.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/nature_summer_film.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/relaxing.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/retro_love_melodic.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/romantic_inspiring_dream.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/sad.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/sad_calm.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/space.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/space_nature_calm.jpg?raw=true',
                    'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/space_sad_heavy.jpg?raw=true'
                    ]

            all_tags = []
            tag_list = []
            for i in imgs:
                a= i.split('/')[-1]
                b = a.split('?')[0]
                c = b.split('.')[0]
                tag_list.append(c)

            for j in tag_list:
                a = j.split('_')
                all_tags.append(a)
        
           # display images that can be clicked on using 'clickable_images' func
            clicked = clickable_images(paths=imgs, 
                                        titles=[f"Image {str(i)}" for i in range(1, len(imgs)+1)],
                                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                        img_style={"margin": "5px", "height": "200px"})  
            

            model_load_state.success('Show Up! Look Around Images!')
            selected_tags = all_tags[clicked]

            final_tag = []
            for tag in selected_tags:
                tup = (tag, 0)
                final_tag.append(tup)
            
            save_path = get_result_dir() + "/" + str(uuid.uuid4()) + ".json"
            print(save_path)
            
            if clicked >= 0:
                model_load_state.info(f"**Keywords of Image {str(int(clicked)+1)} Are Below.**")
                # show final tags of selected image
                show_tags = st.container()
                print(show_tags)
                with show_tags:
                    if len(final_tag) == 3:
                        with st.form('tags_3', clear_on_submit = True):
                            st.subheader(f"Keywords of Image {str(int(clicked)+1)}")
                            col1, col2, col3 = st.columns(3)
                            col1.metric('1st keyword', final_tag[0][0])
                            col2.metric('2nd keyword', final_tag[1][0])
                            col3.metric('3rd keyword', final_tag[2][0])
                            satis_result = st.slider(label='Do you satisfy with the extracted keywords?', min_value=0, max_value=100, value=50)
                            st.text("👉 If you like the auto-extracted keywords, click submit directly!")
                            
                            # revise the tags
                            st.text("👉 If you are not satisfied with the auto-extracted keywords,")
                            st.text("👉 please change the keyword from the options. You can select up to 3 keywords.")
                            
                            # select tag form
                            change = []
                            t1 = (f'{final_tag[0][0]}', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            t2 = (f'{final_tag[1][0]}', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            t3 = (f'{final_tag[2][0]}', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            tc1, tc2, tc3 = st.columns(3)
                            
                            with tc1:
                                change1 = st.selectbox("Select keyword", t1, key='tc1')
                            
                            with tc2:
                                change2 = st.selectbox("Select keyword", t2, key='tc2')
                            
                            with tc3:
                                change3 = st.selectbox("Select keyword", t3, key='tc3')
                        
                            
                            # save all submit
                            submitted = st.form_submit_button('SUBMIT')
                            print(submitted,"1")
                            if submitted:
                                model_load_state.info(f"**The Submission is Uploading.....**")
                                results_B = {'Image': f"{str(int(clicked)+1)}", 'Tag1': final_tag[0][0], 'Tag2': final_tag[1][0], 'Tag3': final_tag[2][0], 'Tags Satisfaction': satis_result, 'Change Tag1': change1, 'Change Tag2': change2, 'Change Tag3': change3}
                                if not os.path.exists(save_path):
                                    data = {}
                                    data['submits'] = []
                                    data['submits'].append(results_B)
                                    print("no exists", data)
                                    with open(save_path, 'w') as save_f:
                                        json.dump(data, save_f, ensure_ascii=False, indent=4) 
                                    model_load_state.info('**The submission is successfully uploaded.**')
                                
                                else:
                                    data = {}
                                    with open(save_path, "r") as json_file:
                                        data = json.load(json_file)
                                    data['submits'].append(results_B)
                                    print("exists, before", data)

                                    with open(save_path, "w") as save_f:
                                        json.dump(data, save_f, ensure_ascii=False, indent=4)
                                        print("exists, after", data)

                                    model_load_state.info('**The submission is successfully uploaded.**')
                                
                                st.experimental_set_query_params(path=save_path)
                            
                    elif len(final_tag) == 2:
                        with st.form('tags_2', clear_on_submit=True):
                            st.subheader(f"Keywords of Image {str(int(clicked)+1)} are below.")
                            col1, col2, col3 = st.columns(3)
                            col1.metric('1st keyword', final_tag[0][0])
                            col2.metric('2nd keyword', final_tag[1][0])
                            col3.metric('3rd keyword', '-')
                            satis_result = st.slider(label='Do you satisfy with the extracted keywords?', min_value=0, max_value=100, value=50)
                            st.text("👉 If you like the auto-extracted keywords, click submit directly!")
                           
                           # revise the tags
                            st.text("👉 If you are not satisfied with the auto-extracted keywords,")
                            st.text("👉 please change the keyword from the options. You can select up to 3 keywords.")
                            
                            # select tag form
                            change = []
                            t1 = (f'{final_tag[0][0]}', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            t2 = (f'{final_tag[1][0]}', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            t3 = ('-', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                 'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                 'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                 'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                 'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            tc1, tc2, tc3 = st.columns(3)
                           
                            with tc1:
                                change1 = st.selectbox("Select keyword", t1, key='tc1')
                            
                            with tc2:
                                change2 = st.selectbox("Select keyword", t2, key='tc2')
                            
                            with tc3:
                                change3 = st.selectbox("Select keyword", t3, key='tc3')


                            # save all submit
                            submitted = st.form_submit_button('SUBMIT')
                            print(submitted,"1")
                            if submitted:
                                model_load_state.info(f"**The Submission is Uploading.....**")
                                results_B = {'Image': f"{str(int(clicked)+1)}", 'Tag1': final_tag[0][0], 'Tag2': final_tag[1][0], 'Tag3': '-', 'Tags Satisfaction': satis_result, 'Change Tag1': change1, 'Change Tag2': change2, 'Change Tag3': change3}
                                if not os.path.exists(save_path):
                                    data = {}
                                    data['submits'] = []
                                    data['submits'].append(results_B)
                                    print("no exists", data)
                                    with open(save_path, 'w') as save_f:
                                        json.dump(data, save_f, ensure_ascii=False, indent=4)
                                    model_load_state.info('**The submission is successfully uploaded.**')
                                
                                else:
                                    data = {}
                                    with open(save_path, "r") as json_file:
                                        data = json.load(json_file)
                                    data['submits'].append(results_B)
                                    print("exists, before", data)

                                    with open(save_path, "w") as save_f:
                                        json.dump(data, save_f, ensure_ascii=False, indent=4)
                                        print("exists, after", data)
                                    model_load_state.info('**The submission is successfully uploaded.**')
                                

                    else:
                        with st.form('tags_1', clear_on_submit=True):
                            st.subheader(f"Keywords of Image {str(int(clicked)+1)} are below.")
                            col1, col2, col3 = st.columns(3)
                            print(final_tag[0][0])
                            col1.metric('1st keyword', final_tag[0][0])
                            col2.metric('2rd keyword', '-')
                            col3.metric('3rd keyword', '-')
                            satis_result = st.slider(label='Do you satisfy with the extracted keywords?', min_value=0, max_value=100, value=50)
                            st.text("👉 If you like the auto-extracted keywords, click submit directly!")
                            
                            # revise the tags
                            st.text("👉 If you are not satisfied with the auto-extracted keywords,")
                            st.text("👉 please change the keyword from the options. You can select up to 3 keywords.")
                            
                            # select tag form
                            change = []
                            t1 = (f'{final_tag[0][0]}', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                    'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                    'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                    'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                    'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            t2 = ('-', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                 'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                 'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                 'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                 'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            t3 = ('-', 'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 'children', 'christmas', 'commercial', 'cool', 'corporate',
                                 'dark', 'deep', 'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 'epic', 'fast', 'film', 'fun', 'funny', 'game',
                                 'groovy', 'happy', 'heavy', 'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 'melodic', 'motivational',
                                 'movie', 'nature', 'party', 'positive', 'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 'soundscape', 
                                 'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat', 'uplifting')
                            
                            tc1, tc2, tc3 = st.columns(3)
                            
                            with tc1:
                                change1 = st.selectbox("Select keyword", t1, key='tc1')
                            
                            with tc2:
                                change2 = st.selectbox("Select keyword", t2, key='tc2')
                            
                            with tc3:
                                change3 = st.selectbox("Select keyword", t3, key='tc3')

                            
                            # save all submit
                            submitted = st.form_submit_button('SUBMIT')
                            print(submitted,"1")
                            if submitted:
                                model_load_state.info(f"**The Submission is Uploading.....**")
                                results_B = {'Image': f"{str(int(clicked)+1)}", 'Tag1': final_tag[0][0], 'Tag2': '-', 'Tag3': '-', 'Tags Satisfaction': satis_result, 'Change Tag1': change1, 'Change Tag2': change2, 'Change Tag3': change3}
                                if not os.path.exists(save_path):
                                    data = {}
                                    data['submits'] = []
                                    data['submits'].append(results_B)
                                    print("no exists", data)
                                    with open(save_path, 'w') as save_f:
                                        json.dump(data, save_f, ensure_ascii=False, indent=4)
                                        print("exists, before", data)
                                    model_load_state.info('**The submission is successfully uploaded.**')
                                
                                else:
                                    data = {}
                                    with open(save_path, "r") as json_file:
                                        data = json.load(json_file)
                                    data['submits'].append(results_B)

                                    with open(save_path, "w") as save_f:
                                        json.dump(data, save_f, ensure_ascii=False, indent=4)
                                        print("exists, after", data)
                                    model_load_state.info('**The submission is successfully uploaded.**')
                                
                    

            else:
                model_load_state.info(f"**No Image Clicked. Click One, Please.**")
                
                
                
                


        except:
            message_container = st.empty() 
            message = message_container.write('👉 Please, wait. Loading... 👀')
            if message != '':
                time.sleep(23)
                message_container.empty()

            







if __name__ == '__main__':
    main()




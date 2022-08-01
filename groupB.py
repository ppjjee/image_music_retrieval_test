import streamlit as st
from st_clickable_images import clickable_images
import os, glob, pathlib, random, pickle, time, requests, json, commons
import io
from io import StringIO, BytesIO
from pathlib import Path
import pandas as pd
import numpy as np
from collections import Counter
import uuid
from itertools import chain
from sftp import SFTP

st.set_page_config(initial_sidebar_state="collapsed")

# set session_state for change pages
st.session_state.update(st.session_state)
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'Home'
    

# callback functions for change page
def CB_Home():
    st.session_state.active_page = 'Page_1'

def CB_Page1():
    st.session_state.active_page = 'Page_2'

def CB_Page2():
    st.session_state.active_page = 'Page_3'

def CB_Page3():
    st.session_state.active_page = 'Page_4'

def CB_Page4():
    st.session_state.active_page = 'Page_5'

def CB_Page5():
    st.session_state.active_page = 'Page_6'

def CB_Page6():
    st.session_state.active_page = 'Page_7'

def CB_Page7():
    st.session_state.active_page = 'Page_8'

def CB_Page8():
    st.session_state.active_page = 'Page_9'

def CB_Page9():
    st.session_state.active_page = 'Page_10'


sftp = SFTP(st.secrets["HOSTNAME"], st.secrets["USERNAME"], st.secrets["PASSWORD"])

def home():
    result_file_name = str(uuid.uuid4()) + ".json"
    save_path = get_result_dir() + "/" + result_file_name
    
    header = st.container()
    with header:
        title = st.title('We recommend music that matches the image.')
        
        sh1 = st.container()
        with sh1:
            subheader1 = st.subheader('Informed Consent 📝')
            st.text("This is an Yonsei University research project.")
            st.text("All data for research is collected anonymously for research purposes.")
            st.text("For questions, please contact park.je@yonsei.ac.kr.")
            st.text("If you are under 18 years old, you need consent from your parents to participate.")
            st.text("Those who participate in the experiment are deemed to have consented to proceed with the experiment.")
            st.write('-----')

        sh2 = st.container()
        with sh2:
            subheader2 = st.subheader('What you are going to do 🧪')
            st.text("In this experiment, we recommend musics that matches an image.") 
            st.text("We give you several kinds of image choices.")
            st.text("Select an image you like the most, then keywords will show up that match the selected image (up to 3).")
            st.text("If you are not satisfied with the keywords, you can change them from the selection.")
            st.text("When keyword selection is complete, we will automatically recommend musics that match the image.")
            st.write('-----')


        sh3 = st.container()
        with sh3:
            subheader3 = st.subheader('Warning 👀👂')
            st.text("If you SKIP A STEP, NO COMPENSATION will be provided.")
            st.text("If you DO NOT FOLLOW THE PROCESS, YOU MAY SEE AN ERROR MESSAGE AND YOUR PARTICIPATION IN THE EXPERIMENT MAY NOT BE COMPLETED.")
            st.write('-----')

        st.experimental_set_query_params(path=save_path)
        st.button('Agree, Start', on_click=CB_Home)
 
 ## ------------------ for Mood Image Retrieval ------------------------ 
def get_result_dir():
    path = os.getcwd() + "/results"
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    print("created result dir: " + path)
    return path

mood_imgs = [
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/mood/calm.jpg?raw=true',
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
theme_imgs = [
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/adventure_action.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/children.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/christmas.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/corporate.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/dark.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/fast.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/film.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/holiday_summer_travel.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/movie.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/nature.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/nature_dark.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/party.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/space.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/sport.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/sport_action_adventure.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/summer.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/summer_holiday_travel.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/summer_party.jpg?raw=true',
                'https://github.com/ppjjee/image_music_retrieval_test/blob/main/theme/trailer_film_background.jpg?raw=true'
            ]

def image_page(imgs, cb):
    # show frontend title 
    st.title('Image to Music Retrieval')
    st.text("✔️ Please select an image! We recommend music that matches the selected image.")
    st.text("✔️ After selecting an image, please wait for a while until the next process.")

    save_path = st.experimental_get_query_params()['path'][0]
    # show imgs to be selected    
    selection = st.container()
    with selection:
        model_load_state = st.info('👉 Loooooooooooooooooooaaaaaaaaaaaaaaaaaaaading... 👀')
        try:
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
            
                
            # if some image is clicked,
            if clicked >= 0:
                model_load_state.info(f"**Keywords of Image {str(int(clicked)+1)} Are Below.**")
                # show final tags of selected image
                show_tags = st.container()
                print(show_tags)
                with show_tags:
                    if len(final_tag) == 3:
                        st.write('-----')
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
               
    st.write('-----')
    st.text("🎧 Please enjoy the music and answer the questions below. 🎧")
    
    for i in range(5):
        createAudio(str(random_all[i]) + '.mp3')

    st.write('-----')

    ## save results
    with st.container():
        satis_result = st.slider('Do you satisfy with the recommended music?', min_value=0, max_value=100, value=50, step=1)
        st.write('-----')
        if st.checkbox("Do you want to move to the next page?", key='check4'):
            with open(save_path, "r") as json_file:
                results_B = {'Music Satisfaction': satis_result}
                data = json.load(json_file)
                data['submits'][-1].update(results_B)

            with open(save_path, "w") as save_f:
                json.dump(data, save_f, ensure_ascii=False, indent=4)    
                print("exists, after", data)
            
            st.experimental_set_query_params(path=save_path)
            st.button('NEXT', on_click=cb)


## ------------------ for Survey ------------------------ 
def survey_page():
    save_path = st.experimental_get_query_params()['path'][0]
    print("path 5: " + save_path)
    st.title('Image to Music Retrieval')
    st.subheader("please respond to the questionnaire consisting of 4 sections.")
    st.subheader("💪 You are almost there! 💪")

    survey = st.container()
    with survey:
        st.write('-----')
        st.text("############## First Section ##############")
        gender = st.radio(
            "What's your gender?",
            ('Male', 'Female', 'Non-binary/Third gender'))

        age = st.radio(
            "What's your age group?",
            ('10s', '20s', '30s', '40s', '50s', '60s', 'Above 60s'))

        education = st.radio(
            "What's the highest level of education that you have completed?",
            ('Less than high school', 'High school graduate', 'Some college', '2 year degree', '4 year degree', 'Professional degree', 'Doctorate'))
            # ('Primary/Elementary education not completed', 'Primary/Elementary education', 'Secondary education','Further education (Bachelor degree, diploma', 'Higher education (Masters, Doctorate)'))

        ethnicity = st.radio(
            "What's your Ethnicity (or Race)?",
            ('Prefer not to disclose', 'American Indigenous (Alaskan Native / Native American)', 'Asian', 'Black', 'Latinx / Hispanic', 'Middle Eastern / North African', 'Pacific Islander', 'White / Caucasian', 'Multi Race / Ethnicity'))
        st.write('-----')

        st.text("############## Second Section ##############")
        satisfaction1 = st.radio(
            "I'm very satisfied with this image-music retrievel system.",
            ('Very satisfied', 'Satisfied', 'Neutral', 'Unsatisfied', 'Very unsatisfied'))

        satisfaction2 = st.radio(
            "This image-music retrieval system meet my expectation.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        satisfaction3 = st.radio(
            "This image-music retrieval system work the way I want it to work.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        satisfaction4 = st.radio(
            "My experience with this image music retrieval system is very pleasing.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        satisfaction5 = st.radio(
            "This image music retrieval system does a satisfactory job of fulfilling my needs.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        st.write('-----')
        
        st.text("############## Third Section ##############")
        ItU1 = st.radio(
            "I intend to use this image-music retrieval system in the future.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        ItU2 = st.radio(
            "I plan to use this image-music retrieval system when it starts to service.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        ItU3 = st.radio(
            "I would recommend this image-music retrieval system to others.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        ItU4 = st.radio(
            "I intend to continue using this image music retrieval system rather than discontinue its use.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        st.write('-----')
        
        st.text("############## Fourth Section ##############")
        valence1 = st.radio(
            "After using this image music retrieval system, I feel that I have had a good experience.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        valence2 = st.radio(
            "I believe that this image music retrieval system provider tries to give me a good experience.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))

        valence3 = st.radio(
            "I believe that this image music retrieval system provider knows the type of experience its users want.",
            ('Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'))
        st.write('-----')


        ## save results
        if st.checkbox("Do you want to move to the next page?", key='fin'):
            results_B = {'gender': gender, 'age': age, 'education': education, 'ethnicity': ethnicity,
             'satisfaction1': satisfaction1, 
             'satisfaction2': satisfaction2, 
             'satisfaction3': satisfaction3, 
             'satisfaction4': satisfaction4, 
             'satisfaction5': satisfaction5, 
             'ItU1': ItU1, 
             'ItU2': ItU2, 
             'ItU3': ItU3,
             'ItU4': ItU4,
             'valence1': valence1,
             'valence2': valence2,
             'valence3': valence3,
             }
            with open(save_path, "r") as json_file:
                data = {}
                data = json.load(json_file)
            data['submits'].append(results_B)

            with open(save_path, "w") as save_f:
                json.dump(data, save_f, ensure_ascii=False, indent=4)
                print("exists, after", data)
            
            sftp.upload(save_path, sftp.dirRemoteSurveyResult + '/' + str(uuid.uuid4()) + ".json")
            st.button('END', on_click=CB_Page9)  
                                                



## ------------------ for Final ------------------------ 
def final_page():
    st.balloons()
    st.title("Thank you for your participation!")
           

                                                
# run the active page
if st.session_state.active_page == 'Home':
    home()
elif st.session_state.active_page == 'Page_1':
    image_page(mood_imgs, CB_Page1)
elif st.session_state.active_page == 'Page_2':
    music_page(CB_Page2)
elif st.session_state.active_page == 'Page_3':
    image_page(mood_imgs, CB_Page3)
elif st.session_state.active_page == 'Page_4':
    music_page(CB_Page4)
elif st.session_state.active_page == 'Page_5':
    image_page(theme_imgs, CB_Page5)
elif st.session_state.active_page == 'Page_6':
    music_page(CB_Page6)
elif st.session_state.active_page == 'Page_7':
    image_page(theme_imgs, CB_Page7)
elif st.session_state.active_page == 'Page_8':
    music_page(CB_Page8)
elif st.session_state.active_page == 'Page_9':
    survey_page()
elif st.session_state.active_page == 'Page_10':
    final_page()
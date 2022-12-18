import streamlit as st    
import pandas as pd 
import backend
import matplotlib.pyplot as plt
import seaborn as sns
import random


def _color_red_or_green(val):
    print(val)
    color = 'red' if val > 10 else 'green'
    return 'color: %s' % color
def main():
#     st.set_page_config(layout="wide")
    # st.config.show.disableWatchdogWarning = True
    
    # '''___________________ SIDEBAR ___________________'''
    st.sidebar.image('logo.png',width = 250)
    st.sidebar.title('Мониторинг оттока клиаентов | МАВИК')

    # '''___________________  MAIN  ___________________'''
    st.title('Мониторинг оттока клиаентов | МАВИК')
    st.write('Привет! Это команда МАВИК. Специально для организации Х мы разработали сервис для мониторига и детектирования оттока клиентов')
    

    
    # '''___________________  FILE_UPLOADER  ___________________'''
    file = st.file_uploader('Загрузите csv файл с данными о клиентах',type=['csv'])
    if file is not None: 
        st.write()
        
        df = backend.get_df(pd.read_csv(file))
        sample_size = st.sidebar.slider('sample_size',min_value=0,max_value=1100,step=100,value = 0)
        min_age = st.sidebar.slider('age',min_value=18,max_value=98,step=1,value = 18)
        max_age = st.sidebar.slider('age',min_value=19,max_value=100,step=1,value = 99)
        has_credit_card = st.sidebar.selectbox(label='Has Credit Card',options=['All'] + df.hascrcard.unique().tolist())
        if has_credit_card == 'All':
            has_credit_card = df.hascrcard.unique().tolist()
        else:
            has_credit_card = [has_credit_card]
        start_country = st.sidebar.multiselect(label='Geography',options=df.geography.unique().tolist(),default=df.geography.unique().tolist())
        start_gender = st.sidebar.multiselect(label='Gender',options=df.gender.unique().tolist(),default=df.gender.unique().tolist())
        all_criteria = {
            'age_range_' + str(min_age) + '_' + str(max_age) : '@min_age <= age <= @max_age',
            'credit_card_' + str(has_credit_card) : 'hascrcard in @has_credit_card',
            'start_country_' + str(start_country):  'geography in @start_country',
            'start_gender_' + str(start_gender):  'gender in @start_gender',
        }
        control_frame = pd.DataFrame(columns = ['criteria','target_rate','threshold'])
        num = 0
        for name,crit in all_criteria.items():
            crit_seed = name.encode('ascii')
            seed = sum([x for x in crit_seed])
            random.seed(seed)
            thr_by_seed = random.randint(10,25)
            part = df.query(crit)
            target_ratio = part.query('exited == 1').shape[0]/part.shape[0] 
            control_frame = pd.concat([control_frame,pd.DataFrame(data = [[name,target_ratio * 100,thr_by_seed]],columns = ['criteria','target_rate','threshold'])])
        control_frame = control_frame.set_index('criteria')
        st.write(control_frame)

        st.dataframe(control_frame.style.applymap(_color_red_or_green))
        df_ = df.copy()
        # df_ = df_[df_.process_flag_num == process_flag_num]
        if sample_size == 0:
            df_ = df_[(df_.geography.isin(start_country)) & (df_.gender.isin(start_gender))& (df_.hascrcard.isin(has_credit_card))& (df_.age > min_age)& (df_.age < max_age)]
        else:
            df_ = df_[(df_.geography.isin(start_country)) & (df_.gender.isin(start_gender))& (df_.hascrcard.isin(has_credit_card))& (df_.age > min_age)& (df_.age < max_age)].sample(sample_size,random_state = 42)
            
            
        if df_.shape[0] == 0:
            st.info('По текущим фильтрам ничего не найдено, сбросьте/измените фильтры или загрузите другой датасет')
        else:
            st.write(df_.describe())
            st.title('Лаборатория')
            st.write('Здесь вы сможите посмотреть зависимости между параметрами')
            axisX = st.selectbox(label='Выберите поле для оси Х',options=df.columns)
            axisY = st.selectbox(label='Выберите поле для оси Y',options=df.columns)
            try:
                fig,ax = plt.subplots()
                for_plot = df_[[axisX,axisY]].sort_values(by =axisY)
                plt.scatter(for_plot[axisX],for_plot[axisY])
                st.pyplot(fig)
            except:
                st.info('Что то пошло не так, попробуйте другие оси')
        
    else:
        st.info(
                
            f"""
                👆 Попробуйте загрузить [data.csv](https://drive.google.com/uc?export=download&id=1alUQ180VKTijKiKtvJmyTAkyqkYp-2eM)
                """
        )

    
if __name__ == '__main__':
    main()

import streamlit as st    
import pandas as pd 
import backend
import matplotlib.pyplot as plt
import seaborn as sns



def main():
#     st.set_page_config(layout="wide")
    # st.config.show.disableWatchdogWarning = True
    
    # '''___________________ SIDEBAR ___________________'''
    st.sidebar.image('logo.png',width = 250)
    st.sidebar.title('Мониторинг оттока клиентов | МАВИК')

    # '''___________________  MAIN  ___________________'''
    st.title('Мониторинг оттока клиентов | МАВИК')
    st.write('Привет! Это команда МАВИК. Специально для организации Х мы разработали сервис для мониторига и детектирования оттока клиентов')
    

    
    # '''___________________  FILE_UPLOADER  ___________________'''
    file = st.file_uploader('Загрузите csv файл с данными о клиентах',type=['csv'])
    if file is not None: 
        st.write()
        df = backend.get_df(pd.read_csv(file))
        min_age = st.sidebar.slider('age',min_value=18,max_value=98,step=1,value = 18)
        max_age = st.sidebar.slider('age',min_value=19,max_value=100,step=1,value = 99)
        has_credit_card = st.sidebar.selectbox(label='Has Credit Card',options=['All'] + df.hascrcard.unique().tolist())
        if has_credit_card == 'All':
            has_credit_card = df.hascrcard.unique().tolist()
        else:
            has_credit_card = [has_credit_card]
        start_country = st.sidebar.multiselect(label='Geography',options=df.geography.unique().tolist(),default=df.geography.unique().tolist())
        start_gender = st.sidebar.multiselect(label='Gender',options=df.gender.unique().tolist(),default=df.gender.unique().tolist())
#         start_balance = st.sidebar.multiselect(label='balance_cluster',options=df.balance_cluster.unique().tolist(),default=[df.balance_cluster.iloc[0]])
#         start_estimated_salary = st.sidebar.multiselect(label='estimated_salary_cluster',options=df.estimated_salary_cluster.unique().tolist(),default=[df.estimated_salary_cluster.iloc[0]])
#         start_salary_bucket = st.sidebar.multiselect(label='Geography',options=df.Geography.unique().tolist(),default=[df.Geography.iloc[0]])
#         start_product = st.sidebar.multiselect(label='Geography',options=df.Geography.unique().tolist(),default=[df.Geography.iloc[0]])
#         start_product = st.sidebar.multiselect(label='Geography',options=df.Geography.unique().tolist(),default=[df.Geography.iloc[0]])
        # day_time = st.sidebar.selectbox(label='day_time',options=df.day_time.unique())     
        # day_of_week = st.sidebar.selectbox(label='day_of_week',options=df.day_of_week.unique())

        df_ = df.copy()
        # df_ = df_[df_.process_flag_num == process_flag_num]
        df_ = df_[(df_.geography.isin(start_country)) & (df_.gender.isin(start_gender))& (df_.hascrcard.isin(has_credit_card))& (df_.age > min_age)& (df_.age < max_age)]
        
#                 df_ = df_[(df_.geography.isin(start_country)) & (df_.gender.isin(start_gender))& (df_.hascrcard.isin(has_credit_card))& (df_.age > min_age)& (df_.age < max_age) & (df_.balance_cluster.isin(start_balance)) & (df_.estimated_salary_cluster.isin(start_estimated_salary))]
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
        
#         metrics_by_user = backend.get_metrics_by_user(df_)
#         sankey_fig = backend.super_function(metrics_by_user, max_users)

#         st.plotly_chart(sankey_fig, use_container_width=True)

#         url_name = df.url_start.unique()[0:]
#         # st.sidebar.selectbox(label='url_name',options=df.url_start.unique())
#         # popular_paths = backend.find_popular_paths(backend.data_prep(df),url_name)
#         # st.write(popular_paths)

#         sank = backend.draw_sankey_popular(df,url_name)
#         st.write('Топовые пути')

#         st.plotly_chart(sank, use_container_width=True)


#         st.write('Метрики по страницам')

#         metrics_by_user = metrics_by_user.dropna(axis=1)
#         st.write(metrics_by_user.rename(columns={'diff_mean':'среднее время нахождения',
#                                                  'diff_max':'максимальное время нахождения',
#                                                  'diff_min':'минимальное время нахождения',
#                                                  'diff_sum':'суммарное время нахождения',
#                                                  'diff_std':'среднеее отклонение времени нахождения',
#                                                  'qty_rel_all':'сумма переходов',
#                                                  'is_reload':'процент перезагрузок',
#                                                  'process_order_mean':'средний шаг',
#                                                  'process_flag_num_max':'максимальный шаг перехода',
#                                                  'process_flag_num_min':'минимальный шаг перехода'}))

#         # url_name = st.sidebar.selectbox(label='popular_paths',options=['complete'])
    else:
        st.info(
                
            f"""
                👆 Попробуйте загрузить [data.csv](https://drive.google.com/uc?export=download&id=1alUQ180VKTijKiKtvJmyTAkyqkYp-2eM)
                """
        )

    
if __name__ == '__main__':
    main()

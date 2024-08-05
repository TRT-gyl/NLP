import streamlit as st

st.set_page_config(page_title="SummerTask",  page_icon=":dolphin:", layout="wide", initial_sidebar_state="expanded",
                       menu_items={'Get Help': 'https://docs.streamlit.io/',
                                   'About': "# 暑期任务"})
st.write("# Streamlit!")
st.sidebar.success("选择上方一个任务执行")

st.markdown(

    """
    Streamlit 是一个专为机器学习和数据科学项目而构建的开源应用框架。\n
    **👈 从侧边栏选择一个任务执行!**
    ### Bart大模型训练
    - 数据集---NLPCC2017将专注于语言计算，多语言访问，NLP数据科学/文本挖掘，机器学习的基础研究适用于NLP，适用于社交网络的NLP，信息检索，会话机器人/摘要/话语以及语言计算的应用。
    - 预训练模型[Bart](https://huggingface.co/facebook)
"""
)
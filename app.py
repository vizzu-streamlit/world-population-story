from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
import ssl
import streamlit as st 

ssl._create_default_https_context = ssl._create_unverified_context  

st.set_page_config(page_title="ipyvizzu-story in Streamlit", layout="centered")
#st.sidebar.title("Poll results - Presentation tools")
st.title("Data Scientists' Presentation Tools")
st.markdown(''' ### Hey there! Good to have you here! 😊
A few weeks ago, we asked data scientists in 5 LinkedIn groups about how they prepare content in Jupyter Notebooks to present the results of their analysis to business stakeholders. 
Here's a short data story we created from the combined results of these polls with [ipyvizzu-story](https://github.com/vizzuhq/ipyvizzu-story), a new, open-source data storytelling tool for data scientists. 🎬📈🚀

Feel free to fork and reuse the content by signing up for [Streamlit](https://streamlit.io/).

***Tip for mobile view:*** *Use the full-screen icon in the bottom right corner of the chart.*
''') 


def create_chart():
    # initialize chart
    data = Data()
    df = pd.read_csv("Data/Poll_results.csv")
    data.add_data_frame(df)
    #@title Create the story
    
    story = Story(data=data)
    story.set_size(700, 450)

    label_handler_method = "if(event.data.text.split(' ')[0] < 6) event.preventDefault()"

    story.add_event("plot-marker-label-draw", label_handler_method)

    slide1 = Slide(
        Step( 
            Style({
                "legend": {"label": {"fontSize": "1.1em"}, "width":"16em"},
                "plot": { 
                    "marker": { "label": { "fontSize": "1.1em"}}, 
                    #"paddingLeft": "10em",
                    "xAxis": {"title": { "color": "#00000000"}, "label": { "fontSize": "1.1em"}},
                    "yAxis": {"label": { "fontSize": "1.1em"}}},
                "logo": {"width": "6em"}
            }),
            Config.percentageBar({
                "x": "Group percentage [%]",
                "y": "Group number",
                "stackedBy": "Answer",
                "title": "How do you prepare content in Jupyter for presentation?"
            })
        )
    )
    story.add_slide(slide1)

    slide2 = Slide(
    Step(
        Style({ "plot": { "xAxis": { "label": { "color": "#00000000"}}}}),
        Config({ "align": "min", "split": True, "title": "Answers vary across groups"})
    )
    )
    story.add_slide(slide2)

    slide3 = Slide(
    Step(
        Style({ "plot": { "marker": { "label": { "fontSize": "0.916667em"}}}}),
        Config({ "x": {"set": ["Vote count","Answer"]}, "label": "Vote count", "title": "88% of votes came from two groups"}),
    )
)
    story.add_slide(slide3)

    slide4 = Slide()
    slide4.add_step(
        Step(
            Style({ "plot": { "yAxis": { "title": { "color": "#00000000"}}}}),
            Config({ "x": "Answer", "y": ["Group number","Vote count"], "split": False, "legend": "color"})
        )
    )

    slide4.add_step(
        Step(
            Style({ "plot": { "marker": { "label": { "fontSize": "1.1em"}}}}),
            Config({ "y": "Vote count", "title": "More than 1200 people voted"}),
        )
    )
    story.add_slide(slide4)

    slide5 = Slide()
    slide5.add_step(
        Step(
            Config({ "x": ["Total percentage [%]","Answer"], "y": None, "label":"Total percentage [%]"})
        )
    )

    slide5.add_step(
        Step(
        Style({ "plot": { "xAxis": {"label": {"color": "#00000000"}},
        "marker": { "label": { "fontSize": "1.6em"}}, 
        }}),            Config({ "coordSystem": "polar", "title":"Screenshots to PPT is the most popular option"})
        )
    )
    story.add_slide(slide5)
    
    # Switch on the tooltip that appears when the user hovers the mouse over a chart element.
    story.set_feature("tooltip", True)

    return story._repr_html_(),df


CHART,df = create_chart()
html(CHART, width=700, height=450)

st.markdown('''
            #### Create and publish similar data stories in Streamlit with [ipyvizzu-story](https://github.com/vizzuhq/ipyvizzu-story)
            * Group 1: Data Science community (moderated) [https://www.linkedin.com/groups/3063585/](https://www.linkedin.com/groups/3063585/)

            * Group 2: Data Scientist, Data Analyst and Data Engineer [https://www.linkedin.com/groups/6773411/](https://www.linkedin.com/groups/6773411/)

            * Group 3: Python Developers Community (moderated) [https://www.linkedin.com/groups/25827/](https://www.linkedin.com/groups/25827/)

            * Group 4: AI & ML  - Analytics , Data Science  .  SAP BI/ Analytics Cloud /Tableau /Power BI /Birst [https://www.linkedin.com/groups/1859449/](https://www.linkedin.com/groups/1859449/)

            * Group 5: Artificial Intelligence, Digital Transformation Data Science, Automation, Machine Learning Analytics [https://www.linkedin.com/groups/4376214/](https://www.linkedin.com/groups/4376214/)
            ''')    

st.balloons()
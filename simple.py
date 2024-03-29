from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
import ssl
import streamlit as st 

ssl._create_default_https_context = ssl._create_unverified_context  

st.set_page_config(page_title='World Population Story in Streamlit - Simple version', layout='centered')

# initialize chart
data = Data()
df = pd.read_csv('Data/worldpop.csv', dtype={'Year': str})
data.add_data_frame(df)
#@title Create the story

story = Story(data=data)
story.set_size(570, 400)

slide1 = Slide(
    Step(
        Data.filter("record.Period === 'Past' && record.Category === 'Population'"),       
        Config({
                'x': 'Year',
                'y': 'Medium',
                'label':'Medium',
                'title': 'The Population of the World 1950-2020'
            }),
        Style({
            "plot": { 'paddingLeft' : '8em',
                "yAxis": { 'title': {'color': '#FFFFFF00' },"label": { 'numberFormat' : 'prefixed','numberScale':'shortScaleSymbolUS'}},
                'marker' :{ 'label' :{ 'numberFormat' : 'prefixed','maxFractionDigits' : '1','numberScale':'shortScaleSymbolUS'}},
                "xAxis": { 'title': {'color': '#FFFFFF00' }, "label": {"angle": "2.5", 'numberFormat' : 'prefixed','numberScale':'shortScaleSymbolUS'}},
        }
    })
    )
)

story.add_slide(slide1)

slide2 = Slide(
    Step(
       Config({
                'y': ['Medium','Region'],
                'color': 'Region',
                'label': None,
                'title': 'The Population of Regions 1950-2020',
            }),
        Style({
            'plot' : {'marker' : { 'colorPalette' : '#FE7B00FF #FEBF25FF #55A4F3FF #91BF3BFF #E73849FF #948DEDFF'}},
            'legend' : {'width' : '12em'},
    })
))

story.add_slide(slide2)

slide3 = Slide()

slide3.add_step(
    Step(
        Data.filter("record.Category === 'Population'"),
        Config({'title': 'The Population of Regions 1950-2100'}),
        Style({'plot':{"xAxis": { "label": {"angle": "2.5",'fontSize':'90%'}}}})
))

slide3.add_step(
    Step(
        Config({'geometry': 'area'}),
    )
)

story.add_slide(slide3)

slide4 = Slide(
    Step(
        Config({'split': True}),
        Style({'plot': {'yAxis':{ 'label':{'color':'#00000000'}}}})
    ),
)

story.add_slide(slide4)

slide5 = Slide(
    Step(
        Config({
            'split': False, 
            'align':'stretch',
            'title': 'The Population of Regions 1950-2100 (%)'
        }),
        Style({'plot': {'yAxis':{ 'label':{'color':None}}}})
    ),
)

story.add_slide(slide5)

slide6 = Slide()

slide6.add_step(
    Step(
        Config({
            'align':'min'
        })
    ),
)

slide6.add_step(
    Step(
        Data.filter("record.Region == 'Africa' && record.Category == 'Population'"),
        Config({
		    'y': { "set":['Medium','Category'],"range": {"max": 6000000000} },
            'title': 'Medium Prediction for Africa'
        }),
    )
)

story.add_slide(slide6)

slide7 = Slide(
    Step(
        Config({
            'y': ['High','Region'],
            'title': 'High Prediction for Africa'
})))

story.add_slide(slide7)

slide8 = Slide(
    Step(
        Config({
            'y': ['Low','Region'],
            'title': 'Low Prediction for Africa'
})))

story.add_slide(slide8)

slide9 = Slide(
    Step(
        Config({
            'y': ['Medium','Region'],
            'title': 'Medium Prediction for Africa'
})))

story.add_slide(slide9)


slide10 = Slide()

slide10.add_step(
    Step(
        Config({
			'y':['Medium','Category'],
			'title': 'Adding Sources of Gain and Loss to the Mix '
        }),
    )
)

slide10.add_step(
    Step(
        Data.filter("record.Region == 'Africa' && (record.Category == 'Population' || record.Category == 'Migration+' || record.Category == 'Births')"),  
		Config({
			'color': 'Category'
		}),
        Style({ 'plot.marker.colorPalette': '#FF8080FF #808080FF #FE7B0020 #60A0FFFF #80A080FF' })
    )
)

slide10.add_step(
    Step(
		Data.filter("record.Region == 'Africa'")
    )
)
story.add_slide(slide10)

slide11 = Slide()

slide11.add_step(
    Step(
        Config({
            'geometry':'rectangle'
        })
    )
)

slide11.add_step(
    Step(
        Data.filter("record.Region === 'Africa' && record.Category !== 'Population' && record.Period === 'Future'"),  
        Config({
            'x': {'set':'Medium','range' : {'min': -6000000000 , 'max': 6000000000}},
            'y': {'set':'Category', 'range' : {'max' : 'auto'}},
            'title': 'Sources of Population Gain and Loss - Medium Scenario'
        })
    )
)

slide11.add_step(Step(Config({'label':'Medium'})))

story.add_slide(slide11)

slide12 = Slide(
    Step(
        Config({
            'x' : 'High',
            'label' : 'High',
            'title': 'Sources of Population Gain and Loss - High Scenario'
        })
))
story.add_slide(slide12)

slide13 = Slide(
    Step(
        Config({
            'x' : 'Low',
            'label' : 'Low',
            'title': 'Sources of Population Gain and Loss - Low Scenario'
        })
))
story.add_slide(slide13)

story.set_feature("tooltip", True)

html(story._repr_html_(), width=750, height=450)
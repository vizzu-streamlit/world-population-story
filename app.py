from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Data, Config, Style
from ipyvizzustory import Story, Slide, Step
import ssl
import streamlit as st 

ssl._create_default_https_context = ssl._create_unverified_context  

st.set_page_config(page_title='World Population Streamlit Story', layout='centered')
st.title('World Population Forecast - an interactive ipyvizzu-story in Streamlit')
st.markdown('''T.B.D''') 

width=750
height=450

# initialize chart
data = Data()
df = pd.read_csv('Data/worldpop.csv', dtype={'Year': str})
data.add_data_frame(df)
#@title Create the story

regions = df['Region'].unique()

sel_region = st.selectbox(
    'Select region',
    list(regions))

skip_intro = st.checkbox(
    'Skip intro slides', value=False
)

df_region = df[df['Region'] == sel_region]

pop_max = int(df_region[df_region['Category'] == 'Population'][['Medium [M]','High [M]','Low [M]']].max().T.max()*1.1)

df_future = df_region[df_region['Period'] == 'Future']

df_futureCategories = df_future[df_future['Category']!='Population'][['Category','Medium [M]','High [M]','Low [M]']];

df_future_sum = df_futureCategories.groupby('Category').sum().T

other_max = df_future_sum.max().max() * 1.1
other_min = df_future_sum.max().max() * -1.1 

region_palette = ['#FE7B00FF','#FEBF25FF','#55A4F3FF','#91BF3BFF','#E73849FF','#948DEDFF']
region_palette_str = ' '.join(region_palette)

region_color = region_palette[list(regions).index(sel_region)]

category_palette = ['#FF8080FF', '#808080FF', region_color.replace('FF','20'), '#60A0FFFF', '#80A080FF']
category_palette_str = ' '.join(category_palette)

# Define the style of the charts in the story
style = {
        'legend' : {'width' : '13em'},
        'plot': {
            'yAxis': {
                'label': {
                    'fontSize': '1em',
                    'numberFormat' : 'grouped',
                },
                'title': {'color': '#ffffff00'},
            },
            'marker' :{ 
                'label' :{ 'numberFormat' : 'grouped','maxFractionDigits' : '0'}
            },
            'xAxis': {
                'label': {
                    'angle': '2.5',
                    'fontSize': '1em',
                    'paddingRight': '0em',
                    'paddingTop': '1em',
                    'numberFormat' : 'grouped',
                },
                'title': {'color': '#ffffff00'},
            },
        },
    }

story = Story(data=data)
story.set_size(width, height)

# Add the first slide, containing a single animation step 
# that sets the initial chart.

if skip_intro == False:
    slide1 = Slide(
        Step(
            Data.filter("record.Period === 'Past' && record.Category === 'Population'"),
            Config(
                {
                    'x':'Year',
                    'y': 'Medium [M]',
                    'label': 'Medium [M]',
                    'title': 'The Population of the World 1950-2020',
                }
            ),
            Style(style)
        )
    )
    # Add the slide to the story
    story.add_slide(slide1)

    # Show components side-by-side
    slide2 = Slide(
        Step(
            Config(
                {
                    'y': ['Medium [M]','Region'],
                    'color': 'Region',
                    'label': None,
                    'title': 'The Population of Regions 1950-2020',
                }
            ),
            Style({ 'plot.marker.colorPalette': region_palette_str })
        )
    )
    story.add_slide(slide2)

    # Show components side-by-side
    slide3 = Slide()
    slide3.add_step(    
        Step(
            Data.filter("record.Category === 'Population'"),
            Config(
                {
                    'y': ['Medium [M]','Region'],
                    'color': 'Region',
            #     'lightness': 'Period',
            #     'x': ['Year','Period'],
                    'title': 'The Population of Regions 1950-2100',
                }
            )
    ))

    slide3.add_step(    
        Step(
            Config(
                {
                'geometry':'area'
                }
            )
    ))

    story.add_slide(slide3)

    slide4 = Slide(
        Step(
            Config(
                {
                    'split': True
                },
            ),
            Style({'plot' : {'yAxis' :{ 'label' :{ 'color' : '#99999900'}}}})
        )
    )
    story.add_slide(slide4)

    slide5 = Slide(
        Step(
            Config.percentageArea(
                {
                    'x':'Year',
                    'y':'Medium [M]',
                    'stackedBy':'Region',
                    'title': 'The Population of Regions 1950-2100 (%)'
                }
            ),
            Style({'plot' : {'yAxis' :{ 'label' :{ 'color' : '#999999FF'}}}})
        )
    )
    story.add_slide(slide5)

#style['plot.marker.colorPalette'] = region_palette_str

style['plot']['marker']['colorPalette'] = region_palette_str

slide6 = Slide()
slide6.add_step(    
    Step(
        Config.stackedArea(
            {
                'x':'Year',
                'y':'Medium [M]',
                'stackedBy':'Region',
            }
        ),
     Style(style) #,{'plot.marker.colorPalette': region_palette_str}
))

slide6.add_step(    
    Step(
        Data.filter(f'record.Category === "Population" && record.Region === "{sel_region}"'),
        Config({
                'title': 'The Population of '+sel_region+' 1950-2100',
                'channels':{'y':{
                    'range':{'max':pop_max}
                }}
        }),
    ))

story.add_slide(slide6)

slide7 = Slide(
    Step(
        Config(
            {
                'y':'High [M]',
                'title': 'High prediction for '+sel_region
            }
        )
    )
)
story.add_slide(slide7)

slide8 = Slide(
    Step(
        Config(
            {
                'y':'Low [M]',
                'title': 'Low prediction for '+sel_region
            }
        )
    )
)
story.add_slide(slide8)

slide9 = Slide(
    Step(
        Config(
            {
                'y':'Medium [M]',
                'title': 'Medium prediction for '+sel_region
            }
        )
    )
)
story.add_slide(slide9)

slide10 = Slide(
    Step(
        Data.filter(f'record.Region === "{sel_region}" && (record.Category === "Population" || record.Category === "Migration+" || record.Category === "Births")'),
        Config(
            {
                'y':['Medium [M]','Category'],
                'color': ['Category'],
                'title': 'Sources of growth: births and positive net migration'
            }),
        Style({ 'plot.marker.colorPalette': category_palette_str })
    )
)
story.add_slide(slide10)

slide11 = Slide(
    Step(
        Data.filter(f'record.Region === "{sel_region}"'),
        Config(
            {
                'title': 'Sources of loss: deaths and negative net migration'
            }
        )
    )
)
story.add_slide(slide11)

slide12 = Slide()

slide12.add_step(
    Step(
        Config(
            {
                'geometry':'rectangle',
            }
        )
    )
)

slide12.add_step(
    Step(
        Data.filter(f'record.Period === "Future" && record.Region === "{sel_region}"'),
        Config(
            {
                'title': 'Zoom to the future'
            }
        )
    )
)

slide12.add_step(
    Step(
        Data.filter(f'record.Period === "Future" && record.Region === "{sel_region}" && record.Category !== "Population"'),
        Config(
            {
                'channels':{
                    'x':{'set':['Medium [M]','Year'],'range':{'max':other_max,'min':other_min}},
                    'y':{'set': 'Category', 'range':{'max':'auto'}},
                },
                'title': 'Sum of births, deaths, and migration after 2020 - Medium prediction'
            },
        ),
        Style({'plot' : {'marker' :{ 'label' :{ 'maxFractionDigits' : '1'}}}})

    )
)

slide12.add_step(
    Step(
        Config(
            {
                'x':'Medium [M]',
                'label':'Medium [M]',
            }
        )
    )
)


story.add_slide(slide12)

slide13 = Slide(
    Step(
        Config(
            {
                'x':'High [M]',
                'label': 'High [M]',
                'title': 'Sum of births, deaths, and migration after 2020 - High prediction'
            }
        )
    )
)
story.add_slide(slide13)

slide14 = Slide(
    Step(
        Config(
            {
                'x':'Low [M]',
                'label': 'Low [M]',
                'title': 'Sum of births, deaths, and migration after 2020 - Low prediction'
            }
        )
    )
)
story.add_slide(slide14)

# Switch on the tooltip that appears when the user hovers the mouse over a chart element.
story.set_feature('tooltip', True)

html(story._repr_html_(), width=width, height=height)

st.download_button('Download HTML export', story.to_html(), file_name=f'world-population-story-{sel_region}.html', mime='text/html')

st.markdown('''T.B.D''')

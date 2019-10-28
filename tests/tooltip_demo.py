from justpy import *
#TODO: Pandas with drilldown option for highcharts
HIGHCHARTS = False

s1 = """
{
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Browser market shares in January, 2018'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: false
            },
            showInLegend: true
        }
    },
    series: [{
        name: 'Brands',
        colorByPoint: true,
        data: [{
            name: 'Chrome',
            y: 61.41,
            sliced: true,
            selected: true
        }, {
            name: 'Internet Explorer',
            y: 11.84
        }, {
            name: 'Firefox',
            y: 10.85
        }, {
            name: 'Edge',
            y: 4.67
        }, {
            name: 'Safari',
            y: 4.18
        }, {
            name: 'Other',
            y: 7.05
        }]
    }]
}
"""

s3 = """
{
 chart: {
        type: 'spline'
    },
    title: {
        text: ''
    },
    subtitle: {
        text: 'JustPy Tooltip Demo'
    },
    yAxis: {
        title: {
            text: 'Number of Employees'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },
    plotOptions: {
        series: {
            pointStart: 2010
        }
    },
    series: [{
        name: 'Installation',
        data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
    }, {
        name: 'Manufacturing',
        data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
    }, {
        name: 'Sales & Distribution',
        data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
    }, {
        name: 'Project Development',
        data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
    }, {
        name: 'Other',
        data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
    }],
    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }
}
"""


def tool_tip_demo(request):
    wp = WebPage()
    d = Div(classes='flex flex-wrap ', a=wp)
    charts = [s3, s3, s3]
    my_charts = []
    for chart in charts:
        my_chart = HighCharts(a=d, classes='m-2 p-2 border')
        my_charts.append(my_chart)
        my_chart.load_json(chart)

        # my_chart.on('tooltip', my_shared_tooltip)
    my_charts[0].options.tooltip.shared = False
    my_charts[1].options.tooltip.shared = True
    my_charts[2].options.tooltip.split = True
    my_charts[0].options.title.text = 'Simple Tooltip'
    my_charts[1].options.title.text = 'Shared Tooltip'
    my_charts[2].options.title.text = 'Split Tooltip'

    d = Div(classes='flex flex-wrap', a=wp)
    charts = [s3, s3, s3]
    my_charts = []
    for chart in charts:
        my_chart = HighCharts(a=d, classes='m-2 p-2 border')
        my_charts.append(my_chart)
        my_chart.load_json(chart)

        # my_chart.on('tooltip', my_shared_tooltip)
    my_charts[0].options.tooltip.shared = False
    my_charts[1].options.tooltip.shared = True
    my_charts[2].options.tooltip.split = True
    my_charts[0].options.title.text = 'Simple Tooltip - Formatter Example'
    my_charts[1].options.title.text = 'Shared Tooltip - Formatter Example'
    my_charts[2].options.title.text = 'Split Tooltip - Formatter Example'

    my_charts[2].options.chart.height = 700
    my_charts[2].options.chart.width = 900

    my_charts[0].on('tooltip', simple_tooltip)
    my_charts[1].on('tooltip', shared_tooltip)
    my_charts[2].on('tooltip', split_tooltip)

    return wp

async def simple_tooltip(self, msg):
    print(msg)
    # await asyncio.sleep(0.3) # Uncomment to simulate 200ms communication delay
    s1 = f'<span class="bg-white" style="color: {msg.color}">&#x25CF;</span>'
    div1 = f'<div>My formatter:</div>'
    div2 = f'<div>{s1}{msg.series_name}</div>'
    div3 = f'<div>Year: {msg.x}</div>'
    div4 = f'<div>Number of employees: {"{:,}".format(msg.y)}</div>'
    tooltip_div = f'<div class="text-red  text-lg"> {div1}{div2}{div3}{div4}</div>'
    # await websocket.send_json({'type': 'tooltip_update', 'data': tooltip_div, 'id': msg.id})
    return await self.tooltip_update(tooltip_div, get_websocket(msg))
    #return True # Not needed because the above returns True so page itlself won't update only tooltip


async def shared_tooltip(self, msg):
    # await asyncio.sleep(0.2)  # Uncomment to simulate 200ms communication delay
    tooltip_div = Div(classes="text-white bg-blue-800 text-xs", temp=True)
    for point in msg.points:
        point_div = Div(a=tooltip_div, temp=True)
        point_span = Span(text='&#x25CF;', classes='bg-white', style=f'color: {point.color}', a=point_div, temp=True)
        span1 = Span(text=f'{point.series_name}', a=point_div, temp=True)
        span2 = Span(text=f'Year: {point.x}', a=point_div, temp=True)
        span3 = Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div, temp=True)
    return await self.tooltip_update(tooltip_div.to_html(), get_websocket(msg))


async def split_tooltip(self, msg):
    # await asyncio.sleep(0.2)  # Uncomment to simulate 200ms communication delay
    tooltip_array = [msg.x]
    for point in msg.points:
        point_div = Div(temp=True)
        Span(text='&#x25CF;', classes='bg-white', style=f'color: {point.color}', a=point_div, temp=True)
        Span(text=f'{point.series_name}', a=point_div, temp=True)
        Span(text=f'Year: {point.x}', a=point_div, temp=True)
        Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div, temp=True)
        tooltip_array.append(point_div.to_html())
    return await self.tooltip_update(tooltip_array, get_websocket(msg))


justpy(tool_tip_demo)
from motion_detector import df # use dataframe from motion sensor
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df['Start_string'] = df['Start'].dt.strftime("%Y-%m-%d %H:%M:%S")
df['Finish_string'] = df['Finish'].dt.strftime("%Y-%m-%d %H:%M:%S")

column_data_source = ColumnDataSource(df)


fig = figure(x_axis_type="datetime", height=100, width=500, sizing_mode="scale_both", title="Motion Graph")
fig.yaxis.minor_tick_line_color = None
fig.ygrid[0].ticker.desired_num_ticks = 1

# hover tool to provide details when user d'move pointer over quandrant on time series graph of motion
hover = HoverTool(tooltips=[('Start: ', '@Start_string'), ('Finish: ', '@Finish_string')])
fig.add_tools(hover)


quadrant = fig.quad(left='Start', right='Finish', bottom=0, top=1, color="green", source=column_data_source)
# quadrant = fig.quad(left=df['Start'], right=df['Finish'], bottom=0, top=1, color="green")
# can't get hovertool to work - RuntimeError: Expected left and right to reference fields in the supplied data source.

output_file("Graph.html")

show(fig)